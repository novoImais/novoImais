import os
import time
import logging
from dotenv import load_dotenv
from datetime import timezone, datetime
from cmreslogging.handlers import CMRESHandler
from azure.storage.blob import ContainerClient, BlobServiceClient, BlobClient
from objects.imais_cfe_events import Events
from datastores.kafka.json.cfe_json_producer import cfe_json_producer
from datastores.kafka.json.cfe_items_json_producer import cfe_items_json_producer
from metadata.postgres import Postgres

load_dotenv()

# load variables
http_base_container = os.getenv("HTTP_BASE_CONTAINER_IMAIS")
elastic_search_host = os.getenv("ELASTIC_SEARCH_HOST")
elastic_search_port = os.getenv("ELASTIC_SEARCH_PORT")
index_name = os.getenv("INDEX_NAME")
info = os.getenv("INFO")
logger_name = os.getenv("LOGGER_NAME")

# add elasticsearch logging capabilities
# parameters coming from env file
handler = CMRESHandler(
    hosts=[{"host": elastic_search_host, "port": elastic_search_port}],
    auth_type=CMRESHandler.AuthType.NO_AUTH,
    es_index_name=index_name,
)

# name of the logger
# level and handler
log = logging.getLogger(logger_name)
log.setLevel(logging.INFO)
log.addHandler(handler)


class BlobStorage(object):
    """A class that allows you to connect to Azure Blob Storage

    With this class it will be possible to identify the metadata of the files,
    copy the files between the containers, delete the files and process the files
    present in the container

    ...

    Parameters
    -------
    blob_storage_conn_str: str
        Connection string with Blob Storage.
    container_base: str
        Container where files will be read.
    container_processed: str
        Container where files will be sent after being processed.
    container_quarantined: str
        Container that stores quarantine files.
    """

    @staticmethod
    def utc_to_local(utc_dt):
        """Converts the utc time to the location

        ...

        Parameters
        -------
        utc_dt: datetime
            A datetime containing the value to be converted.

        Returns
        -------
        datetime
            A datetime containing the converted value.

        """
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def __init__(
        self,
        blob_storage_conn_str,
        container_base,
        container_processed,
        container_quarantined,
    ):
        """Creates a Blob Storage object

        ...

        Parameters
        -------
        blob_storage_conn_str: str
            Connection string with Blob Storage.
        container_base: str
            Container where files will be read.
        container_processed: str
            Container where files will be sent after being processed
            (Processed with sucess).
        container_quarantined: str
            Container that stores quarantine files (Processed with failure).

        """

        self.blob_storage_conn_str = blob_storage_conn_str
        self.container_base = container_base
        self.container_processed = container_processed
        self.container_quarantined = container_quarantined

        # init blob service & container connectivity
        # instantiate the blob storage class to perform operations on it
        self.blob_service_client = BlobServiceClient.from_connection_string(
            conn_str=self.blob_storage_conn_str
        )
        self.get_container_base_info = ContainerClient.from_connection_string(
            conn_str=self.blob_storage_conn_str, container_name=self.container_base
        )
        log.info(
            f"successfully established connection with container base: {self.container_base}"
        )
        print(
            f"successfully established connection with container base: {self.container_base}"
        )

        # get sku of the blob storage account
        account_info = self.get_container_base_info.get_account_information()
        log.info("storage sku: {}".format(account_info["sku_name"].lower()))

        # get stats of blob storage & container service info
        stats_blob_storage = self.blob_service_client.get_service_stats()
        log.info(
            "blob storage replication status: {}".format(
                stats_blob_storage["geo_replication"]["status"]
            )
        )
        log.info(
            "last blob storage sync replication time: {}".format(
                self.utc_to_local(
                    stats_blob_storage["geo_replication"]["last_sync_time"]
                )
            )
        )
        stats_container_base = self.get_container_base_info.get_container_properties()
        log.info(
            "last container modified time: {}".format(
                self.utc_to_local(stats_container_base.last_modified)
            )
        )

    def get_file_metadata_info(self):
        """Returns the metadata of files in a container.

        ...

        Returns
        -------
        dict_metadata: list
            A list that contains the metadata for all files in the container.

        """

        # list files inside of the container
        # listing based on alphabetical order [asc]
        blob_list = self.get_container_base_info.list_blobs()

        start_enum = time.time()
        amount_file = 0
        dict_metadata = []

        # list all files within the container folder
        for blob in blob_list:
            start_list_files = time.time()
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_base, blob=blob.name
            )
            properties = blob_client.get_blob_properties()

            # get timestamp
            current_timestamp = datetime.now()

            # files that are gonna be processed
            dict_values_dt = {
                "file_name": properties.name,
                "creation_time": BlobStorage.utc_to_local(properties.last_modified),
                "original_container": properties.container,
                "blob_type": properties.blob_type,
                "file_size_bytes": properties.size,
                "etag": properties.etag,
                "list_time": time.time() - start_list_files,
                "dt_current_timestamp": current_timestamp,
            }

            dict_metadata.append(dict_values_dt)
            amount_file += 1

        # print summarize info of listing process
        log.info(f"total amount of files inside of the container: {amount_file}")
        print(f"total amount of files inside of the container: {amount_file}")
        log.info(
            f"total time taken to list all files [secs]: {round(time.time() - start_enum,2)}"
        )
        print(
            f"total time taken to list all files [secs]: {round(time.time() - start_enum, 2)}"
        )

        return dict_metadata

    def copy_blob_files(self, file_name):
        """Copies the file from one container to the other.

        ...

        Parameters
        -------
        file_name: str
            File to be copied.

        """

        # set connectivity to blob storage
        blob_service_client = self.blob_service_client

        # get name of the file for copy activity
        log.info(f"initializing copy of the file: {file_name}")
        print(f"initializing copy of the file: {file_name}")

        # build command to copy file []
        # concat strings to build base http address
        # container and file name
        source_blob = http_base_container + file_name
        # print(source_blob)
        # print(copied_blob)
        log.info(f"http address of source file: {source_blob}")
        print(f"http address of source file: {source_blob}")
        copied_blob = blob_service_client.get_blob_client(
            self.container_processed, file_name
        )
        log.info(f"destination container of copied file: {self.container_processed}")
        print(f"destination container of copied file: {self.container_processed}")

        # copy started
        start = time.time()
        copied_blob.start_copy_from_url(source_blob)
        props = copied_blob.get_blob_properties()
        status = props.copy.status
        log.info(f"time taken to copy file [secs]: {round(time.time() - start, 2)}")
        print(f"time taken to copy file [secs]: {round(time.time() - start, 2)}")
        log.info("copy status: " + status)
        print("copy status: " + status)

        if status != "success":
            props = copied_blob.get_blob_properties()
            print(props.copy.status)
            copy_id = props.copy.id
            copied_blob.abort_copy(copy_id)
            props = copied_blob.get_blob_properties()
            print(props.copy.status)

    def delete_blob_files(self, file_name):
        """Deletes the file from a container.
        Used to clean the source location and reduce space usage

        ...

        Parameters
        -------
        file_name: str
            File to be deleted.

        """

        print(f"base location of deletion process: {self.container_base}")

        # instantiate a container client
        container_client = self.blob_service_client.get_container_client(
            self.container_base
        )
        log.info(f"base location of deletion process: {self.container_base}")
        print(f"base location of deletion process: {self.container_base}")

        # delete blob files
        log.info(f"initializing deletion of the file from base location: {file_name}")
        print(f"initializing deletion of the file from base location: {file_name}")

        start = time.time()
        container_client.delete_blobs(file_name)
        log.info(
            f"time taken to delete file from source in [secs]: {round(time.time() - start, 2)}"
        )
        print(
            f"time taken to delete file from source in [secs]: {round(time.time() - start, 2)}"
        )

    def process_blob_files(self):
        """Process files within a container.

        Processing takes place in 3 steps:

        - Treatment and data ingestion in Kafka topics (CFE data and your items).
        - Moves processed files to the successfully processed container.
        - Retrieve information to share with the metadata repository (Postgres).

        """

        dict_of_files_for_processing = self.get_file_metadata_info()
        count_xml_files = len(dict_of_files_for_processing)
        log.info(f"metadata of files: {dict_of_files_for_processing}")
        print(f"metadata of files: {dict_of_files_for_processing}")
        log.info(f"amount of files marked for processing: {count_xml_files}")
        print(f"amount of files marked for processing: {count_xml_files}")

        # init conditioner
        i = 0

        # loop to read all files within the received list
        # invoke function to go over xml files
        while i < count_xml_files:

            file_name = dict_of_files_for_processing[i]["file_name"]
            log.info(f"initializing processing of file: {file_name}")
            print(f"initializing processing of file: {file_name}")

            # read each file in a loop
            read_file_spec = BlobClient.from_connection_string(
                conn_str=self.blob_storage_conn_str,
                container_name=self.container_base,
                blob_name=file_name,
            )

            # download file over stream
            # read entire file - blocking stream until completion
            # decode individual file to utf-8 - type [str]
            download_blob_file_stream = read_file_spec.download_blob()
            read_entire_file = download_blob_file_stream.readall()
            file = read_entire_file.decode("utf-8")

            ######################
            # 1 - get event key
            ######################
            log.info(f"key of the event stream: {Events(file).get_key()}")
            print(f"key of the event stream: {Events(file).get_key()}")
            cfe_items_time = time.time()
            # print processed file
            # print(get_xml_files[i])
            log.info(f"name of the processed file: {file_name}")
            print(f"name of the processed file: {file_name}")

            ######################
            # 2 - cfe events
            ######################
            # ingest different nfe portions
            start = time.time()
            cfe_json_producer(file)
            log.info(
                f"time taken to produce cfe [secs]: {round(time.time() - start,2)}"
            )
            print(f"time taken to produce cfe [secs]: {round(time.time() - start,2)}")

            ######################
            # 3 - items events
            ######################
            # ingest items
            start = time.time()
            cfe_items_json_producer(file)
            log.info(
                f"time taken to produce items [secs]: {round(time.time() - start,2)}"
            )
            print(f"time taken to produce items [secs]: {round(time.time() - start,2)}")

            # total time of cfe and items processing
            log.info(
                f"time taken to produce cfe & items [secs]: {round(time.time() - cfe_items_time,2)}"
            )
            print(
                f"time taken to produce cfe & items [secs]: {round(time.time() - cfe_items_time,2)}"
            )

            ######################
            # 4 - copy & delete
            ######################
            # init copy & delete activity from source location
            self.copy_blob_files(file_name)
            self.delete_blob_files(file_name)

            ######################
            # 4 - metadata - cfe
            ######################
            # builds the correct dictionary to
            # write into the metadata store using postgres
            dict_metadata_cfe = {
                "process_name": "01379480000106",
                "xml_type": "cfe",
                "storage": "blob storage",
                "base_container": self.container_base,
                "file_name": dict_of_files_for_processing[i]["file_name"],
                "file_size_bytes": dict_of_files_for_processing[i]["file_size_bytes"],
                "etag": dict_of_files_for_processing[i]["etag"].replace('"', ""),
                "dt_current_timestamp": datetime.now(),
            }

            # inserting metadata [rows] on the control table
            log.info(f"storing metadata of the file: {file_name}")
            print(f"storing metadata of the file: {file_name}")
            start_metadata = time.time()
            Postgres().insert_rows_metadata_processed_files(rows=dict_metadata_cfe)
            log.info(
                f"time taken to store into the metadata store [secs]: {round(time.time() - start_metadata, 2)}"
            )
            print(
                f"time taken to store into the metadata store [secs]: {round(time.time() - start_metadata, 2)}"
            )

            # process files
            i += 1
        log.info(f"total amount of files processed: {i}")
        print(f"total amount of files processed: {i}")
