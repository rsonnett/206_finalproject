import requests
import sqlite3

def get_holidays(api_key, year):
    country_code = "US"
    url = f"https://calendarific.com/api/v2/holidays?api_key={api_key}&country={country_code}&year={year}"
    response = requests.get(url)
    data = response.json()

    if "response" in data and "holidays" in data["response"]:
        return [(holiday["name"], holiday["date"]["iso"]) for holiday in data["response"]["holidays"]]
    else:
        print(f"No holidays found for the year {year}")
        return []

def print_holidays(holidays):
    for holiday in holidays:
        print(f"{holiday[0]}: {holiday[1]}")

def create_holidays_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('''DROP TABLE IF EXISTS Holidays''')  # Drop the existing table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Holidays (
                            Holiday TEXT,
                            Date TEXT,
                            Month TEXT
                          )''')  # Recreate the table
        conn.commit()
        print("Holidays table created successfully.")
    except sqlite3.Error as e:
        print("Error creating Holidays table:", e)

def insert_into_holidays_table(conn, holidays):
    cursor = conn.cursor()
    inserted_holidays = set()  # To keep track of inserted holidays
    for holiday, date_iso in holidays:
        # Check if the holiday is already inserted
        if (holiday, date_iso) not in inserted_holidays:
            month = date_iso.split("-")[1]
            try:
                cursor.execute("INSERT INTO Holidays (Holiday, Date, Month) VALUES (?, ?, ?)", (holiday, date_iso, month))
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
        create_holidays_table(conn)
        insert_into_holidays_table(conn, all_holidays)
        print("Data inserted successfully into the Holidays table.")
        conn.close()
    else:
        print("No holidays found for the specified years.")