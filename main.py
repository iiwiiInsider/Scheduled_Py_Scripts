import os
import csv
import smtplib
import random
import datetime

EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")

today = datetime.datetime.now()
today_tuple = (today.month, today.day)

birthdays_dict = {}

with open("birthdays.csv", newline='') as file:
    raw_header = file.readline().strip()
    raw_header = raw_header.replace("\ufeff", "")
    raw_header = raw_header.strip('"')
    header = raw_header.split(",")

    reader = csv.reader(file)

    for row in reader:
        if len(row) == 1:
            row = row[0].strip('"').split(",")

        row_dict = dict(zip(header, row))

        try:
            month = int(row_dict["month"])
            day = int(row_dict["day"])
        except Exception:
            print("Bad row:", row_dict)
            continue

        birthdays_dict[(month, day)] = row_dict

if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]

    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"

    with open(file_path) as letter_file:
        contents = letter_file.read().replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday!\n\n{contents}"
        )

print("Script executed successfully.")
