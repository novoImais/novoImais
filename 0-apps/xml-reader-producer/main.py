# TODO logic to copy from one directory to another [azure logic apps]

# import libraries
import logging
import time
import os
from cmreslogging.handlers import CMRESHandler
from datastores.blob_storage.read_blob_files import BlobStorage
from datastores.blob_storage.validate_file_type import StorageFileTypeValidator
from dotenv import load_dotenv

# load env info
load_dotenv()

# load variables
blob_storage_connection_string = os.getenv("BLOB_STORAGE_CONNECTION_STRING")
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


# main
if __name__ == "__main__":

    # init ~ [cleaner]
    log.info("initializing cleaner process")
    print("initializing cleaner process")
    start = time.time()
    StorageFileTypeValidator().run()
    log.info(
        f"total time spend to move [non-validated] file types in [secs]: {round(time.time() - start, 2)}"
    )
    log.info(
        f"total time spend to move [non-validated] file types in [minutes]: {round(time.time() - start, 2)/60}"
    )
    log.info("finishing cleaner process")
    print(
        f"total time spend to move [non-validated] file types in [secs]: {round(time.time() - start, 2)}"
    )
    print(
        f"total time spend to move [non-validated] file types in [minutes]: {round(time.time() - start, 2) / 60}"
    )
    print("finishing cleaner process")
    # end ~ [cleaner]

    # init ~ [processing]
    log.info("initializing imais process")
    print("initializing imais process")
    start = time.time()
    BlobStorage(
        blob_storage_connection_string, base_imais, processed_imais, quarantined_imais
    ).process_blob_files()
    log.info(
        f"total time spend to produce event[s] in [secs]: {round(time.time() - start,2)}"
    )
    log.info(
        f"total time spend to produce event[s] in [minutes]: {round(time.time() - start, 2)/60}"
    )
    log.info("finishing imais process")
    print(
        f"total time spend to produce event[s] in [secs]: {round(time.time() - start,2)}"
    )
    print(
        f"total time spend to produce event[s] in [minutes]: {round(time.time() - start, 2)/60}"
    )
    print("finishing imais process")
    # end ~ [processing]


