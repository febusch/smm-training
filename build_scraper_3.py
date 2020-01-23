from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# GLOBAL VARIABLES
url = 'https://www.job-room.ch/job-search/dea5789c-3dc1-11ea-ab6f-005056ac086d'
executable_path = './chromedriver'
driver = webdriver.Chrome(executable_path=executable_path)
driver.get(url)
wait = WebDriverWait(driver, 10)


def get_selenium_element(type_name, value):
    return wait.until(ec.element_to_be_clickable((type_name, value))).get_attribute('outerHTML')


def selenium_tag_element(tag):
    return get_selenium_element(By.TAG_NAME, tag)


def soupify(src, tag):

    soup = BeautifulSoup(src, "lxml")
    soup_element_only = soup.find(tag)
    cleaned_soup = clean_soup(soup_element_only)

    return cleaned_soup


def stringify(soup):

    return str(soup).replace("\n", "")


def clean_soup(soup):
    things_to_throw_out = ["svg", "script", "img", "button"]

    for thing in things_to_throw_out:
        for elem in soup(thing):
            elem.decompose()

    return soup


def html_string_by_tag(tag):
    """
    :param tag: tag name of the HTML element that is to be processed
    :return: cleaned and formatted string
    """

    # WAIT EXPLICITLY UNTIL ELEMENT EXISTS AND THEN GET THEM
    element = selenium_tag_element(tag)

    # TURN ELEMENTS INTO SOUPS
    element_html = soupify(element, tag)

    # TURN SOUPS INTO OUTPUT STRINGS
    element_string = stringify(element_html)

    return element_string


def insert_head_with_utf_8(soup_string):
    return '<html><head><meta charset="utf-8"/></head><body>' + soup_string + '</body></html>'


def main():
    """
    Use this function to build a scraper for content of jobroom.ch.
    The objective is to extract the content of an ad, in this case located
    at https://www.job-room.ch/job-search/dea5789c-3dc1-11ea-ab6f-005056ac086d

    Since the content of this page is rendered dynamically, we have to use
    selenium webdriver to extract it.
    """

    content = html_string_by_tag('alv-job-content')
    address = html_string_by_tag('alv-post-address')
    center = html_string_by_tag('alv-job-center-context')

    raw_string = content + address + center
    output = insert_head_with_utf_8(raw_string)

    # FINISHING UP
    driver.close()
    print(output)


if __name__ == '__main__':
    main()

