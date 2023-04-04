import requests
import selectorlib
import smtplib, ssl
from email.message import EmailMessage
import time
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"
sql_connection = sqlite3.connect("events.db")
print("Connected to DB")

def get_text_content(URL):
    response = requests.get(url=URL)
    response_html_content = response.text
    return response_html_content


def extract_content(html_content):
    extractor = selectorlib.Extractor.from_yaml_file(yaml_filename="extraxt.yaml")
    extracted_content = extractor.extract(html_content)["tours"]
    print(extracted_content)
    return extracted_content


def store_events(event):
    row = event.split(",")
    row = [col.strip() for col in row]
    cursor = sql_connection.cursor()
    cursor.execute("INSERT INTO events(name, city, date) VALUES(?,?,?)",row)
    sql_connection.commit()


def check_stored_events(event):
    row = event.split(",")
    row = [col.strip() for col in row]
    name, city, date = row
    print(name)
    print(city)
    print(date)
    cursor = sql_connection.cursor()
    cursor.execute("SELECT * FROM events WHERE name=? AND city=? AND date=?",(name,city,date))
    retrieved_rows = cursor.fetchall()
    return retrieved_rows



def send_email(event):
    host = "smtp.gmail.com"
    port = 465

    username = "sarthakcoza@gmail.com"
    password = "yjzqrrsxwuoffmmc"

    context = ssl.create_default_context()

    msg = EmailMessage()
    msg.set_content(f'New Event Found: {event}')

    msg['Subject'] = 'New Event'
    msg['From'] = "sarthakcoza@gmail.com"
    msg['To'] = "sarthak.udemy044@gmail.com"

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.send_message(msg)
    print("An email has been sent!")


if __name__ == '__main__':
    while True:
        content = get_text_content(URL)
        event = extract_content(content)

        if event != "No upcoming tours":
            stored_events = check_stored_events(event)
            if not stored_events:
                store_events(event)
                send_email(event)

        time.sleep(3600)
