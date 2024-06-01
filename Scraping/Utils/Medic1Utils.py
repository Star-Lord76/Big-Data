import re
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from tqdm.notebook import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


def divideInPosts(lst: list, startString: str) -> list:
    """
    The function `divide_list` takes a list of strings and divides it into sublists based on elements
    that start with startString .

    :param lst: It looks like the code snippet you provided is a function called `divide_list` that
    takes a list `lst` as input and divides it into sublists based on elements that start with startString . The
    function creates a new sublist every time it encounters an element that starts with startString 
    :return: The function `divide_list` takes a list as input and divides it into sublists based on
    elements that start with startString . The function returns a list of sublists where each sublist contains
    consecutive elements from the input list until an element starting with startString  is encountered.
    """
    divided_list = []
    temp_list = []
    for element in lst:
        if element.startswith(startString):
            if temp_list:
                divided_list.append(temp_list)
                temp_list = []
        else:
            temp_list.append(element)
    if temp_list:
        divided_list.append(temp_list)
    return divided_list


def isPostFromDoctor(post: list[str]) -> bool:
    return any(title in post[1].lower() for title in ["dr", "dott", "dottore", "dottoressa", "drs"])


def stripAndJoin(lst: list[str]) -> str:
    return "\n".join(s.strip() for s in lst if s != "")


def getAllHrefForArgument(driver: webdriver.Chrome, link: str, numeroPagine: int) -> set[str]:
    """
    This Python function retrieves all href links from a specified number of pages of a given website
    using a WebDriver.

    :param driver: The `driver` parameter is an instance of the `webdriver.Chrome` class, which is
    typically used in Selenium to automate web browsers for testing or web scraping purposes
    :type driver: webdriver.Chrome
    :param link: The `link` parameter in the `getAllHrefForArgument` function is a string that
    represents the URL of a webpage from which you want to extract href links
    :type link: str
    :param numeroPagine: The `numeroPagine` parameter in the `getAllHrefForArgument` function represents
    the total number of pages to iterate through when scraping href links from a website. This parameter
    determines how many pages the function will visit to collect the href links
    :type numeroPagine: int
    :return: A set of strings containing all the href links found on the specified number of pages
    starting from the given link.
    """
    linkSet = set()
    for currentIndex in tqdm(range(1, numeroPagine+1)):
        linkWithPage = link + f"&pagina={currentIndex}"

        driver.get(linkWithPage)

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'titconsulto')))
        except Exception as e:
            return linkSet
        elencoWebElementList = driver.find_elements(
            By.CLASS_NAME, "titconsulto")
        linkSet.update(getHrefLinks(elencoWebElementList))
    return linkSet


def getTextFromArticle(driver: webdriver.Chrome, link: str) -> str:
    """
    The function `getTextFromArticle` uses Selenium to extract text content from a webpage given a link,
    handling cookie acceptance and timeouts.

    :param driver: The `driver` parameter is an instance of the `webdriver.Chrome` class, which is used
    for controlling the Chrome web browser during automated testing or web scraping tasks
    :type driver: webdriver.Chrome
    :param link: The `link` parameter in the `getTextFromArticle` function is a string that represents
    the URL of the article from which you want to extract text. This function uses a Selenium WebDriver
    instance (`driver`) to navigate to the provided link and extract text from a specific element on the
    page
    :type link: str
    :return: The function `getTextFromArticle` returns the text content of the element with the ID
    'question' on the webpage specified by the input link. If the question element is empty or not
    found, it will print a message indicating that the question is empty. If there is a timeout waiting
    for the page to load, it will print a message indicating that the page load timed out.
    """
    driver.get(link)
    try:
        accept_cookies_button = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "pt-accept-all")))
        accept_cookies_button.click()
    except:
        pass
    try:
        questionWebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, 'question'))
        )
        questionText = questionWebElement.get_attribute("outerText")
        if (questionText is None or questionText == ""):
            print("QUESTION IS EMPTY")

        return questionText

    except:
        print("Timed out waiting for page to load")
        return
