from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from tqdm.notebook import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time


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


def cleanRispostaFromContent(input: str) -> str:
    """
    The function `cleanRispostaFromContent` extracts and returns the content following the first
    occurrence of an all-uppercase word in the input string.

    :param input: The function `cleanRispostaFromContent` takes a string input and attempts to remove
    any leading uppercase words from the input string. If there are one or more consecutive uppercase
    words at the beginning of the input string, it will return the remaining content after those words.
    If there are no uppercase words
    :type input: str
    :return: The function `cleanRispostaFromContent` takes a string input and searches for a sequence of
    one or more uppercase letters at a word boundary. If such a sequence is found, it returns the
    substring of the input starting from the end of the matched sequence and stripped of leading and
    trailing whitespaces. If no match is found, it returns the original input string.
    """
    match = re.search(r'\b[A-Z]+\b', input)

    if match:
        return input[match.end():].strip()
    else:
        return input


def cleanRispostaFromText(input: str) -> str:
    """
    This Python function takes a string input, splits it by newline characters, and returns the 6th
    element (index 5) from the resulting list.

    :param input: I see that you have a function `cleanRispostaFromText` that takes a string input and
    splits it by newline characters. It then returns the 6th element (index 5) from the resulting list
    :type input: str
    :return: The function `cleanRispostaFromText` takes a string input, splits it by newline characters,
    and then returns the 6th element (index 5) from the resulting list.
    """
    splittedInput = input.split("\n")
    return splittedInput[5]


def cleanDomandaFromContent(input: str) -> tuple[str]:
    """
    The function `cleanDomandaFromContent` extracts and cleans a specific portion of text related to
    questions from a given input string.

    :param input: The `cleanDomandaFromContent` function takes a string input and processes it to
    extract relevant information. It looks for a specific pattern in the input string related to dates
    and capital letters to split the content into two parts
    :type input: str
    :return: The function `cleanDomandaFromContent` returns a tuple of two strings. The first string is
    the content before the second capital letter that appears after a date in the input string. The
    second string is the content after the second capital letter that appears after a date in the input
    string.
    """
    firstPass = input.split("Domande")[1].split("Risposta")[0]
    match = re.search(
        r'\d{1,2} (gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre) \d{4}', firstPass)
    secondPass = firstPass[match.end():].strip()
    capitals = re.finditer(r'[A-Z]', secondPass)
    try:
        next(capitals)
        split_index = next(capitals).start()
    except StopIteration:
        split_index = len(secondPass)

    if split_index > 50:
        return "", secondPass

    return secondPass[:split_index], secondPass[split_index:]


def cleanDomandaFromText(input: str) -> tuple[str]:
    """
    This Python function extracts and returns specific lines from a given input text.

    :param input: A string with new line character
    :type input: str
    :return: A tuple containing two strings: the 5th and 6th lines of the input text after splitting it
    by newline characters.
    """
    splittedInput = input.split("\n")
    return (splittedInput[4], splittedInput[5])


def printToFile(title: str, domanda: str, risposta: str) -> None:
    """
    This Python function takes a title, question, and answer as input, formats them into a text string,
    and writes them to a file in a specified directory.

    :param title: The `title` parameter is a string that represents the title or name of the file that
    will be created. It is used to name the file along with a timestamp to make it unique
    :type title: str
    :param domanda: The parameter `domanda` represents the question asked by the user
    :type domanda: str
    :param risposta: The parameter `risposta` in the `printToFile` function represents the answer
    provided by the doctor in response to the user's question.
    :type risposta: str
    """
    basePath = "./Data/"
    text = ""

    text += "###UTENTE###\n"
    text += domanda.strip() + "\n\n"

    text += "###DOTTORE###\n"
    text += risposta.strip() + "\n\n"

    with open(basePath + re.sub(r'(?u)[^-\w.]', '', title) + "_" + str(time.time()) + ".txt", 'w', encoding="utf-16") as f:
        f.write(text)
