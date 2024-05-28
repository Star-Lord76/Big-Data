from selenium.webdriver.remote.webelement import WebElement


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
