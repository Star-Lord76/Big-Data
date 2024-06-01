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
    driver.get(link)
    linkSet = set()
    for currentIndex in tqdm(range(1, numeroPagine+1)):
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'elencoA')))
        except:
            break
        elencoWebElementList = driver.find_elements(By.CLASS_NAME, "elencoA")
        linkSet.update(getHrefLinks(elencoWebElementList))
        try:
            driver.execute_script(f"document.getElementById('pgg').value='{
                currentIndex}'; paginazione.submit();")
        except:
            return linkSet
    return linkSet


def getTextFromArticle(driver: webdriver.Chrome, link: str) -> tuple[tuple]:
    """
    This Python function uses Selenium to extract text content from a specified article link and then
    processes the text to return a tuple containing questions and answers.

    :param link: The `link` parameter in the `getTextFromArticle` function is a string that represents
    the URL of the article from which you want to extract text
    :type link: str
    :return: The function `getTextFromArticle` returns a tuple containing a single string element, which
    is the result of calling the `getQandA` function on the text content of the article element located
    by its class name 'txtArticolo'.
    """
    driver.get(link)
    try:
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, 'txtArticolo'), '')
        )
    except:
        print("Timed out waiting for page to load")
    article = driver.find_element(By.CLASS_NAME, 'txtArticolo')
    domanda = article.text
    typeDomanda = "FROM_TEXT"
    if (domanda is None or domanda == ""):
        domanda = article.get_attribute("textContent")
        typeDomanda = "FROM_CONTENT"

    typeRisposta = "FROM_TEXT"
    espertoRispostaWeb = driver.find_element(By.CLASS_NAME, "espertoRispostaM")
    espertoRisposta = espertoRispostaWeb.text
    if (espertoRisposta is None or espertoRisposta == ""):
        espertoRisposta = espertoRispostaWeb.get_attribute("textContent")
        typeRisposta = "FROM_CONTENT"

    return [[domanda, typeDomanda], [espertoRisposta, typeRisposta]]
