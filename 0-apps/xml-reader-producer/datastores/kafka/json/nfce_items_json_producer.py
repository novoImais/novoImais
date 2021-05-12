import os
import json
from objects.imais_nfe_events import NFCeEvents
from dotenv import load_dotenv
from datastores.kafka import delivery_reports, producer_settings
from confluent_kafka import Producer

load_dotenv()

# load variables
app_name = os.getenv("KAFKA_CLIENT_ID_JSON")
broker = os.getenv("KAFKA_BOOTSTRAP_SERVER")

# topics
topic_items_json = os.getenv("KAFKA_TOPIC_NFCE_ITEMS_JSON")


def nfe_items_json_producer(xml):
    """Performs the sending of items (Tag Det) from xml to Kafka.

    | The following topics are fed by this routine:
    | - Items_Json: Product and Service Detailing Group of CF-e

    | The routine happens in 3 steps:
    | - Creation of KafkaProducer
    | - XML decomposition, searching for items in CF-e
    | - Sending events to Kafka

    ...

    Parameters
    -------
    xml: str
        XML string to be decomposed

    """

    # init producer settings
    p = Producer(producer_settings.producer_settings_json(app_name, broker))

    # get object [dict] from objects
    data_det = NFCeEvents(xml).get_nfe_det()

    # print(data_det)
    # print(len(data_det))

    # properly counting amount of items inside of the list
    # comparing between the type of return - [str] or [list]
    # str means that is 1 item where list means > 1
    items_count = 0
    for item in list(data_det):
        if isinstance(item, str):
            items_count = 1
            # print(items_count)
        else:
            items_count = len(data_det)
            # print(items_count)

    # one item only
    if items_count == 1:

        # try to ingest events
        try:
            # poll
            p.poll(0)

            # event = [ide]
            p.produce(
                topic=topic_items_json,
                key=NFCeEvents(xml).get_nfe_key(),
                value=json.dumps(data_det).encode("utf-8"),
                callback=delivery_reports.on_delivery_json,
            )

        # error = buffer
        except BufferError:
            print("buffer full")
            p.poll(0.1)

        # error = value
        except ValueError:
            print("invalid input")
            raise

        # error = shutdown
        except KeyboardInterrupt:
            raise

        # flush data
        p.flush()

    else:
        # loop to insert data
        # count items = [@nItem]
        inserts = 0
        while inserts < items_count:

            # print(inserts)
            # print(items_count)

            # try to ingest events
            try:
                # poll
                p.poll(0)

                # event = [ide]
                p.produce(
                    topic=topic_items_json,
                    key=NFCeEvents(xml).get_nfe_key(),
                    value=json.dumps(data_det[inserts]).encode("utf-8"),
                    callback=delivery_reports.on_delivery_json,
                )

            # error = buffer
            except BufferError:
                print("buffer full")
                p.poll(0.1)

            # error = value
            except ValueError:
                print("invalid input")
                raise

            # error = shutdown
            except KeyboardInterrupt:
                raise

            # increment values
            inserts += 1

        # flush data
        p.flush()
