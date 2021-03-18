def producer_settings_json(app_name, broker):
    """Returns the default settings for a Kafka Producer.

    ...

    Parameters
    -------
    app_name: str
        Name of the application that is sending the information to Kafka.
        This name will be used internally for logs and monitoring.
    broker: str
        Name of the Broker to be ingested by the producer.

    Returns
    -------
        settings : dict
            A dictionary with the settings to be used by the producer.

    """

    settings = {
        "client.id": app_name,
        "bootstrap.servers": broker,
        "batch.num.messages": 100000,
        "linger.ms": 1000,
        "acks": "all",
        "enable.idempotence": "true",
        "max.in.flight.requests.per.connection": 1,
        "retries": 100,
        "queue.buffering.max.ms": 100,
        "queue.buffering.max.messages": 1000,
    }

    return settings
