import os
import time
import logging
import xmltodict
import xml.etree.ElementTree as ET
from cmreslogging.handlers import CMRESHandler
from dotenv import load_dotenv
from azure.storage.blob import BlobClient, BlobServiceClient
from datastores.blob_storage.read_blob_files import BlobStorage

load_dotenv()

# load variables
blob_storage_connection_string = os.getenv("BLOB_STORAGE_CONNECTION_STRING")
http_base_container = os.getenv("HTTP_BASE_CONTAINER_IMAIS")
base_imais = os.getenv("CONTAINER_BASE_IMAIS")
processed_imais = os.getenv("CONTAINER_PROCESSED_IMAIS")
quarantined_imais = os.getenv("CONTAINER_QUARANTINED_IMAIS")
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


class StorageFileTypeValidator(object):
    """Class that validates the files present in the read container.

    | Validation takes place in 3 steps:
    | - The contents of the files present in the container are read.
    | - Identified the file type by the root node of the XML file.
    | - If the file is not of the CFE type, it will be sent to the "quarantine" container, where it will be analyzed later.

    """

    def run(self):
        """Performs the file validation process."""
        files_blob = BlobStorage(
            blob_storage_connection_string,
            base_imais,
            processed_imais,
            quarantined_imais,
        ).get_file_metadata_info()
        count_xml_files = len(files_blob)

        # init conditioner
        i = 0

        # loop to read all files within the received list
        # invoke function to go over xml files
        while i < count_xml_files:

            # get name of the file for processing
            file_name = files_blob[i]["file_name"]
            log.info(f"initializing file type validation: {file_name}")
            print(f"initializing file type validation: {file_name}")

            # read each file in a loop
            read_file_spec = BlobClient.from_connection_string(
                conn_str=blob_storage_connection_string,
                container_name=base_imais,
                blob_name=file_name,
            )

            # download file over stream
            # read entire file - blocking stream until completion
            # decode individual file to utf-8 - type [str]
            download_blob_file_stream = read_file_spec.download_blob()
            read_entire_file = download_blob_file_stream.readall()
            xml_file = read_entire_file.decode("utf-8")

            # parsing xml and creating object
            # finding root element
            # parsing string to xml
            tree = ET.ElementTree(ET.fromstring(xml_file))
            xml_data = tree.getroot()

            # converting to string using [utf-8]
            # converting string to dictionary
            # get cfe root element
            xml_to_str = ET.tostring(xml_data, encoding="utf-8", method="xml")
            data_dict = dict(xmltodict.parse(xml_to_str))

            # get the file type on the base containers
            # used to determine the type of the process
            get_file_type = list(data_dict.keys())[0]
            # print(get_file_type)
            log.info(f"file type: {get_file_type}")
            print(f"file type: {get_file_type}")

            ##################
            # model = CFe
            ##################

            if get_file_type != "CFe":

                # set connectivity to blob storage
                blob_service_client = BlobServiceClient.from_connection_string(
                    conn_str=blob_storage_connection_string
                )

                # get name of the file for copy activity
                log.info(f"initializing copy of the file: {file_name}")
                print(f"initializing copy of the file: {file_name}")

                # build command to copy file []
                # concat strings to build base http address
                # container and file name
                source_blob = http_base_container + file_name

                copied_blob = blob_service_client.get_blob_client(
                    quarantined_imais, file_name
                )
                log.info(f"destination container of copied file: {quarantined_imais}")
                print(f"destination container of copied file: {quarantined_imais}")

                ##############
                # copy started
                ##############
                start = time.time()
                copied_blob.start_copy_from_url(source_blob)
                props = copied_blob.get_blob_properties()
                status = props.copy.status
                log.info(
                    f"time taken to copy file [secs]: {round(time.time() - start, 2)}"
                )
                log.info("copy status: " + status)
                print(
                    f"time taken to copy file [secs]: {round(time.time() - start, 2)}"
                )
                print("copy status: " + status)

                if status != "success":
                    props = copied_blob.get_blob_properties()
                    print(props.copy.status)
                    copy_id = props.copy.id
                    copied_blob.abort_copy(copy_id)
                    props = copied_blob.get_blob_properties()
                    print(props.copy.status)

                ##############
                # delete started
                ##############
                # instantiate a container client
                container_client = blob_service_client.get_container_client(base_imais)
                log.info(f"base location of deletion process: {base_imais}")
                print(f"base location of deletion process: {base_imais}")

                # delete blob files
                log.info(
                    f"initializing deletion of the file from base location: {file_name}"
                )
                print(
                    f"initializing deletion of the file from base location: {file_name}"
                )
                start = time.time()
                container_client.delete_blobs(file_name)
                log.info(
                    f"time taken to delete file from source in [secs]: {round(time.time() - start, 2)}"
                )
                print(
                    f"time taken to delete file from source in [secs]: {round(time.time() - start, 2)}"
                )

            # finish entire process
            i += 1
