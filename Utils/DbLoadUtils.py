from pymongo import MongoClient, errors


def getMongoClient(mongoUri: str) -> MongoClient | None:
    """
    The function `getMongoClient` attempts to establish a connection to a MongoDB database using the
    provided URI and returns the MongoClient object if successful, or None if the connection fails.

    :param mongoUri: The `mongoUri` parameter in the `getMongoClient` function is expected to be a
    string that represents the connection URI for the MongoDB database. This URI typically includes
    information such as the host, port, database name, and authentication credentials required to
    establish a connection to the MongoDB server
    :type mongoUri: str
    :return: The function `getMongoClient` is returning an instance of `MongoClient` if the connection
    to MongoDB is successful. If there is a connection failure, it returns `None`.
    """
    try:
        client = MongoClient(mongoUri)
        print("Connection to MongoDB successful")
        return client
    except errors.ConnectionFailure as e:
        print(f"Connection failed: {e}")
        return None


def closeMongoClient(client: MongoClient) -> bool:
    try:
        client.close()
        return True
    except:
        return False
