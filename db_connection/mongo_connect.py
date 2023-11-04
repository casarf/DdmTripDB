# mongo_connect.py file inside the db_connection/ directory.

from pymongo import MongoClient

def create_connection(host='localhost', port=27017):
    """
    Creates a connection to the MongoDB database.

    :param host: The database host.
    :param port: The database port.
    :return: A MongoClient instance connected to the database.
    """
    # Create a MongoClient without authentication
    client = MongoClient(host, port)
    
    return client


# If desired, below could be an example to create a connection directly when the script is run.
# Be cautious with this approach, as it may create a connection whenever this script is imported.
# This is useful for testing the connectivity.
# if __name__ == "__main__":
#     connection = create_connection()
#     print("Connected to MongoDB at {} on port {}".format(connection.HOST, connection.PORT))