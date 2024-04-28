import requests
import sqlite3

def get_holidays(api_key, year):
    country_code = "US"
    url = f"https://calendarific.com/api/v2/holidays?api_key={api_key}&country={country_code}&year={year}"
    response = requests.get(url)
    data = response.json()

    holidays = []

    if "response" in data and "holidays" in data["response"]:
        for holiday in data["response"]["holidays"]:
            holiday_name = holiday["name"]
            holiday_date_iso = holiday["date"]["iso"]
            holidays.append((holiday_name, holiday_date_iso))
    else:
        print(f"No holidays found for the year {year}")

    return holidays

def create_holiday_month_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('''DROP TABLE IF EXISTS holiday_month''')  # Drop the existing table
        cursor.execute('''CREATE TABLE IF NOT EXISTS holiday_month (
                            holiday TEXT,
                            month TEXT
                          )''')  # Recreate the table
        conn.commit()
        print("holiday_month table created successfully.")
    except sqlite3.Error as e:
        print("Error creating holiday_month table:", e)

def insert_into_holiday_month_table(conn, holidays):
    cursor = conn.cursor()
    inserted_holidays = set()  # To keep track of inserted holidays
    for holiday, date_iso in holidays:
        # Check if the holiday is already inserted
        if (holiday, date_iso) not in inserted_holidays:
            month = date_iso.split("-")[1]
            try:
                cursor.execute("INSERT INTO holiday_month (holiday, month) VALUES (?, ?)", (holiday, month))
                conn.commit()
                inserted_holidays.add((holiday, date_iso))  # Add inserted holiday to the set
            except sqlite3.Error as e:
                print("Error inserting holiday data:", e)

if __name__ == "__main__":
    api_key = "hW94DfGsUQ2UHH0ZBmg92B6zwI8c8upl"
    years = [2023, 2024]
    all_holidays = []
    for year in years:
        holidays = get_holidays(api_key, year)
        if holidays:
            all_holidays.extend(holidays)

    if all_holidays:
        conn = sqlite3.connect('SI_final_project.db')
        create_holiday_month_table(conn)
        insert_into_holiday_month_table(conn, all_holidays)
        print("Data inserted successfully into the holiday_month table.")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Holidays")  # Check for data in the Holidays table
        result = cursor.fetchone()
        if result[0] > 0:
            print("Data found in the Holidays table.")
        else:
            print("No data found in the Holidays table.")
        conn.close()
    else:
        print("No holidays found for the specified years.")

import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def get_month_counts_from_db(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT month, COUNT(*) FROM holiday_month GROUP BY month")
    month_counts = cursor.fetchall()
    return month_counts

def plot_normal_distribution(month_counts):
    months, counts = zip(*month_counts)
    x = np.arange(len(months))
    plt.bar(x, counts, align='center', alpha=0.5)
    plt.xticks(x, months)
    plt.xlabel('Month')
    plt.ylabel('Frequency')
    plt.title('Holiday Distribution by Month')
    plt.show()

if __name__ == "__main__":
    conn = sqlite3.connect('SI_final_project.db')
    month_counts = get_month_counts_from_db(conn)
    if month_counts:
        plot_normal_distribution(month_counts)
    else:
        print("No data found in the holiday_month table.")
    conn.close()