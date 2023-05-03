import requests
import selectorlib

URL = "http://programmer100.pythonanywhere.com/tours/"
# Note: Sometimes, we need a header to make it appear that the scraping function
# is actually a browser instead of a scraping bot. requests.get has an optional
# argument, headers. An example header string is stored in the extras directory.


def scrape(url):
    """
    Scrape the page source from the URL and return it as a string.
    :param url: str of a url
    :return:
    """
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    """
    Extracts the data belonging to id="displaytime" in the page source text
    and returns that data.
    :param source:
    :return:
    """
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


if __name__ == "__main__":
    scraped = scrape(URL)
    print(scraped)
    extracted = extract(scraped)
    print(extracted)
