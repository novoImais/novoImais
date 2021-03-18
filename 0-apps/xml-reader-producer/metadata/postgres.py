import os
from psycopg2 import extensions, sql, connect
from dotenv import load_dotenv

load_dotenv()

# load variables
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_database = os.getenv("POSTGRES_DATABASE")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")


class Postgres:
    """Class that allows you to connect to the Postgres database.

    With this class you can:
        - Create the database in the instance of Postgres.
        - Create the table where processing logs will be saved (processed_files).
        - Inserts the metadata records from the files in the database

    """

    @staticmethod
    def create_database():
        """Create the database in the instance of Postgres.

        Using the information contained in the environment variables,
        the create or recreates the database method.

        """
        # get the isolation leve for autocommit
        autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT

        # set the isolation level for the connection's cursors
        # will raise ActiveSqlTransaction exception otherwise
        connection = connect(
            host=postgres_host,
            port=postgres_port,
            user=postgres_user,
            password=postgres_password,
        )
        connection.set_isolation_level(autocommit)

        # instantiate a cursor object from the connection
        cursor = connection.cursor()

        # use the sql module instead to avoid sql injection attacks
        cursor.execute(
            f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{postgres_database}' "
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(postgres_database))
            )

        # close the cursor to avoid memory leaks
        cursor.close()

        # close the connection to avoid memory leaks
        connection.close()

    @staticmethod
    def create_tables():
        """Create the table where processing logs will be saved (processed_files).

        Using the information of the environment variables to connect to the database,
        create or re-create the "processed_files" table

        """
        # open connection to database
        connection = connect(
            host=postgres_host,
            port=postgres_port,
            database=postgres_database,
            user=postgres_user,
            password=postgres_password,
        )
        cursor = connection.cursor()

        # drop table
        cursor.execute("""DROP TABLE IF EXISTS processed_files""")

        # create table
        cursor.execute(
            """
        CREATE TABLE public.processed_files
        (
                id SERIAL PRIMARY KEY, 
                process_name VARCHAR(100) NOT NULL,
                xml_type VARCHAR(100) NOT NULL,
                storage VARCHAR(100) NOT NULL,
                base_container VARCHAR(100),
                file_name VARCHAR(100) NOT NULL,
                file_size_bytes VARCHAR(100) NOT NULL,
                etag VARCHAR(100) NOT NULL,
                dt_current_timestamp TIMESTAMP NOT NULL
        )
        """
        )

        # commit transaction
        connection.commit()

        # close connection
        connection.close()

    @staticmethod
    def insert_rows_metadata_processed_files(rows):
        """Inserts the metadata records from the files in the database

        Using the information of the environment variables to connect to the database
        and the data sent by parameter, the method inserts the file metadata in the database

        ...

        Parameters
        -------
        rows: dict
            Records to be entered in the database.
        """
        # open connection
        connection = connect(
            host=postgres_host,
            port=postgres_port,
            database=postgres_database,
            user=postgres_user,
            password=postgres_password,
        )
        cursor = connection.cursor()

        # build insert query statement
        insert_query = """
                INSERT INTO public.processed_files (
                    process_name,
                    xml_type, 
                    storage,
                    base_container,
                    file_name,
                    file_size_bytes,
                    etag,
                    dt_current_timestamp
                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        # get object [dict] from objects
        # transform into tuple to a multiple insert process
        insert_data = [(tuple(rows.values()))]

        # invoke insert statement
        cursor.executemany(insert_query, insert_data)

        # commit transaction
        connection.commit()

        # close connection
        connection.close()
