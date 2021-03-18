Connection with Azure Blob Storage
==================================

This is the module responsible for communicating with Azure Blobstorage
You can read the files in the containers and make the separation of valid files.
Valids will be suitable for processing and invalids will quarantine.

Reading the files
-----------------
.. automodule:: datastores.blob_storage.read_blob_files
   :members:

Validating the files
---------------------
.. automodule:: datastores.blob_storage.validate_file_type
   :members:
