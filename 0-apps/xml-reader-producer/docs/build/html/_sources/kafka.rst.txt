Connection with Kafka Broker
============================

This is the module responsible for communicating with kafka broker
Here are producer settings, the methods used for
Send CF-e data and its items to their respective topics and
Because Callback will be registered.


Creating Communication with Kafka
*********************************

Kafka Producer Settings
-----------------------
.. automodule:: datastores.kafka.producer_settings
   :members:

Registering Callbacks
---------------------
.. automodule:: datastores.kafka.delivery_reports
   :members:

Feeding Topics
**************

CF-E Topics
-----------
.. automodule:: datastores.kafka.json.cfe_json_producer
   :members:

Items topic
-----------
.. automodule:: datastores.kafka.json.cfe_items_json_producer
   :members: