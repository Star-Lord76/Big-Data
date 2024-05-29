from selenium.webdriver.remote.webelement import WebElement
import pickle


def getHrefLinks(webElementsList: list[WebElement]) -> set[str]:
    """
    This Python function takes a list of WebElement objects and returns a set of href links extracted
    from each WebElement.

    :param webElementsList: A list of WebElement objects, which typically represent links on a web page
    :type webElementsList: list[WebElement]
    :return: A set of unique href links extracted from a list of WebElement objects.
    """
    returnSet = set()
    for webElement in webElementsList:
        returnSet.add(webElement.get_attribute("href"))
    return returnSet


def getQandA(multiLineString: str) -> list[str]:
    """
    The function `getQandA` takes a multi-line string as input and returns a list containing the 6th and
    13th lines of the input string.

    :param multiLineString: A multi-line string containing multiple lines of text
    :type multiLineString: str
    :return: The function `getQandA` takes a multi-line string as input and splits it into separate
    lines. It then returns a list containing the 6th and 13th lines of the input string.
    """
    splittedString = multiLineString.split("\n")
    return (splittedString[5], splittedString[12])


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
