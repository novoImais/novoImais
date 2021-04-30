import os
import json
from objects.imais_nfe_events import Events
from dotenv import load_dotenv
from datastores.kafka import delivery_reports, producer_settings
from confluent_kafka import Producer

load_dotenv()

# load variables
app_name = os.getenv("KAFKA_CLIENT_ID_JSON")
broker = os.getenv("KAFKA_BOOTSTRAP_SERVER")

# topics
topic_ide_json = os.getenv("KAFKA_TOPIC_IDE_JSON")
topic_emit_json = os.getenv("KAFKA_TOPIC_EMIT_JSON")
topic_dest_json = os.getenv("KAFKA_TOPIC_DEST_JSON")
topic_det_json = os.getenv("KAFKA_TOPIC_DET_JSON")
topic_total_json = os.getenv("KAFKA_TOPIC_TOTAL_JSON")
topic_pgto_json = os.getenv("KAFKA_TOPIC_PGTO_JSON")
topic_inf_adic_json = os.getenv("KAFKA_TOPIC_INF_ADIC_JSON")


def cfe_json_producer(xml):
    """Performs xml/event decomposition in Kafka topics.

    | The following topics are fed by this routine:
    | - Ide_Json: CF-e identification information group
    | - Emit_Json: CF-e issuer identification group
    | - Dest_Json: Identification group of the recipient of the CF-e
    | - Det_Json: Products and Services detailing group of CF-e
    | - Total_Json: CF-e Total Values Group
    | - Pgto_Json: CFe Payment Information Group
    | - Inf_Adic_Json: Additional Information Group

    | The routine happens in 3 steps:
    | - Creation of KafkaProducer
    | - XML decomposition
    | - Sending events to Kafka

    ...

    Parameters
    -------
    xml: str
        XML string to be decomposed

    """

    # init producer settings
    p = Producer(producer_settings.producer_settings_json(app_name, broker))

    # loop to insert data
    inserts = 0
    while inserts < 1:

        # get object [dict] from objects
        # calling different functions
        data_ide = Events(xml).get_ide()
        data_emit = Events(xml).get_emit()
        data_dest = Events(xml).get_dest()
        data_det = Events(xml).get_det()
        data_total = Events(xml).get_total()
        data_pgto = Events(xml).get_pgto()
        data_inf_adic = Events(xml).get_inf_adic()

        # try to ingest events
        try:
            # poll
            p.poll(0)

            # event = [ide]
            p.produce(
                topic=topic_ide_json,
                key=Events(xml).get_key(),
                value=json.dumps(data_ide).encode("utf-8"),
                callback=delivery_reports.on_delivery_json,
            )

            # event = [emit]
            p.produce(
                topic=topic_emit_json,
                key=Events(xml).get_key(),
                value=json.dumps(data_emit).encode("utf-8"),
                callback=delivery_reports.on_delivery_json,
            )

            # event = [dest]
            p.produce(
                topic=topic_dest_json,
                key=Events(xml).get_key(),
                value=json.dumps(data_dest).encode("utf-8"),
                callback=delivery_reports.on_delivery_json,
            )

            # event = [det]
            p.produce(
                topic=topic_det_json,
                key=Events(xml).get_key(),
                value=json.dumps(data_det).encode("utf-8"),
                callback=delivery_reports.on_delivery_json,
            )

            # event = [total]
            p.produce(
                topic=topic_total_json,
                key=Events(xml).get_key(),
                value=json.dumps(data_total).encode("utf-8"),
                callback=delivery_reports.on_delivery_json,
            )

            # event = [pgto]
            p.produce(
                topic=topic_pgto_json,
                key=Events(xml).get_key(),
                value=json.dumps(data_pgto).encode("utf-8"),
                callback=delivery_reports.on_delivery_json,
            )

            # event = [inf_adic]
            p.produce(
                topic=topic_inf_adic_json,
                key=Events(xml).get_key(),
                value=json.dumps(data_inf_adic).encode("utf-8"),
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
