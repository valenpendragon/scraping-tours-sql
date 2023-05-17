import requests
import selectorlib
import smtplib
import os
import ssl
import sqlite3
from pathlib import Path

URL = "http://programmer100.pythonanywhere.com/tours/"
# Note: Sometimes, we need a header to make it appear that the scraping function
# is actually a browser instead of a scraping bot. requests.get has an optional
# argument, headers. An example header string is stored in the extras directory.

DATABASE = Path("G:\\Users\\valen\\Documents\\Valen\\python\\python-mega-course\\scraping-tours-sql\\data\\data.db")
connection = sqlite3.connect(DATABASE)


class Event:
    def scrape(self, url):
        """
        Scrape the page source from the URL and return it as a string.
        :param url: str of a url
        :return:
        """
        response = requests.get(url)
        source = response.text
        return source

    def extract(self, source):
        """
        Extracts the data belonging to id="displaytime" in the page source text
        and returns that data.
        :param source:
        :return:
        """
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


def send_email(message):
    # Creating the email header information.
    host = "smtp.gmail.com"
    port = 465
    username = "valenpendragon@gmail.com"
    # Get this password before prepping the email.
    password = os.getenv("PASSWORD")
    receiver = "valenpendragon@hotmail.com"
    context = ssl.create_default_context()
    message = message
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


def store(extracted):
    """
    This function adds the most recent concert tour data to the database.

    Before making the database query, it will also clean up parts of the data
    strings to eliminate trailing and leading blank spaces.
    :param extracted: str
    :return:
    """
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read_data(extracted):
    """
    This function reads the lines in the datafile and returns a string of the
    row, if any, in the database matching the extracted tour. An empty list
    indicates that there are no matching entries in the database.

    Before making the database query, it will also clean up parts of the data
    strings to eliminate trailing and leading blank spaces.
    :param database: Path, optional
    :return: list of tuple or empty list
    """
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))
    rows = cursor.fetchall()
    print(f"rows: {rows}")
    return rows


if __name__ == "__main__":
    event = Event()
    scraped = event.scrape(URL)
    extracted = event.extract(scraped)
    print(extracted)

    if extracted != "No upcoming tours":
        data = read_data(extracted)
        print(data)
        if not data:
            send_email(message="New event was found.")
            print("Email sent.")
            store(extracted)
            print(f"{extracted} written to database.")
