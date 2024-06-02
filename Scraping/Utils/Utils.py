import pickle
import re


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


def checkDateTimeFormat(date_time_string: str) -> bool:
    """
    The function `checkDateTimeFormat` checks if a given date and time string follows the format
    "dd.mm.yyyy hh:mm".

    :param date_time_string: The function `checkDateTimeFormat` is designed to check if a given
    `date_time_string` follows a specific format. The format pattern specified in the function is
    `dd.mm.yyyy hh:mm`, where:
    :return: The function `checkDateTimeFormat` is returning a boolean value. It returns `True` if the
    `date_time_string` matches the specified date and time format pattern, and `False` otherwise.
    """
    pattern = r"\b(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.\d{4} ([01][0-9]|2[0-3]):[0-5][0-9]\b"
    match = re.match(pattern, date_time_string)
    return match is not None


def stripAndJoin(lst: list[str]) -> str:
    """
    The function `stripAndJoin` takes a list of strings, removes leading and trailing whitespaces from
    each string, filters out empty strings, and then joins the cleaned strings with newline characters.

    :param lst: A list of strings that may contain leading or trailing whitespaces
    :type lst: list[str]
    :return: The function `stripAndJoin` takes a list of strings as input, strips any leading or
    trailing whitespace from each string, removes any empty strings, and then joins the remaining
    strings with a newline character ("\n"). The function returns a single string that is the result of
    joining the stripped strings with newline characters.
    """
    return "\n".join(s.strip() for s in lst if s != "")
