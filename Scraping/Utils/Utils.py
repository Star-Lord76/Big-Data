import pickle


def createObjectPickleSnapshot(objectToSnapshot: any, path: str) -> bool:
    """
    The function `createObjectPickleSnapshot` takes an object and a file path as input, then saves a snapshot
    of the set to a pickle file at the specified path.

    :param setToSnapshot: The `objectToSnapshot` parameter is a set that you want to create a snapshot of.
    This function takes this set and saves it to a file using the Python `pickle` module. The `path`
    parameter specifies the file path where the snapshot will be saved
    :type setToSnapshot: set
    :param path: The `path` parameter in the `createObjectPickleSnapshot` function is a string that
    represents the file path where the snapshot of the set will be saved as a pickle file
    :type path: str
    :return: The function `createObjectPickleSnapshot` returns a boolean value. It returns `True` if the
    set `setToSnapshot` is successfully pickled and saved to the specified path, and it returns `False`
    if there is an exception raised during the process.
    """
    try:
        with open(path, 'wb') as f:
            pickle.dump(objectToSnapshot, f)
    except:
        return False
    return True


def loadObjectPickleSnapshot(path: str) -> any:
    """
    The function `loadObjectPickleSnapshot` loads a set object from a pickle file at the specified path.

    :param path: The `path` parameter in the `loadObjectPickleSnapshot` function is a string that
    represents the file path to the pickle file that contains the snapshot of a set object. This
    function reads the pickle file and returns the set object stored in it
    :type path: str
    :return: The function `loadSetPickleSnapshot` is returning an object that is loaded from a pickle
    file located at the specified `path`.
    """
    with open(path, 'rb') as f:
        pickleLinkObject = pickle.load(f)
    return pickleLinkObject
