from metadata.postgres import Postgres


def create_database():
    """This method will create the database and the table where the logs will be registered"""
    # create initial structure
    print("creating postgres database")
    Postgres.create_database()
    # provision database and control table
    print("creating control metadata table")
    Postgres.create_tables()
