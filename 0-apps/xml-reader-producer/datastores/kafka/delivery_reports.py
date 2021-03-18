# import libraries
import logging
import os
from cmreslogging.handlers import CMRESHandler
from dotenv import load_dotenv

# get env
load_dotenv()

# load variables
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


# [json]
def on_delivery_json(err, msg):
    """Method used to log ingestion callbacks in Kafka

    ...

    Parameters
    -------
    err: str
        String with error information, if any.
    msg: obj
        Object with the information from where the message was saved.

    """
    if err is not None:
        print("message delivery failed: {}".format(err))
        log.info("message delivery failed: {}".format(err))
    else:
        print(
            "message successfully produced to {} [{}] at offset {}".format(
                msg.topic(), msg.partition(), msg.offset()
            )
        )
        log.info(
            "message successfully produced to {} [{}] at offset {}".format(
                msg.topic(), msg.partition(), msg.offset()
            )
        )
