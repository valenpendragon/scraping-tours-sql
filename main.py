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


def send_email():
    print("Email sent.")


def store(extracted, datafile="./data/data.txt"):
    """
    This function adds the most recent concert to the datafile.
    :param extracted:
    :return:
    """
    with open(datafile, "a") as file:
        file.write(extracted + "\n")


def read_data(datafile="./data/data.txt"):
    """
    This function reads the lines in the datafile and returns them
    as a list.
    :param datafile: str, optional
    :return: list of str
    """
    with open(datafile, "r") as file:
        content = file.readlines()
    content = [item.replace("\n", "") for item in content]
    return content


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    data = read_data()
    print(data)
    if extracted != "No upcoming tours":
        if extracted not in data:
            send_email()
            store(extracted)
