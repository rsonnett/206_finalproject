import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import os

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

def main():
    path = os.path.dirname(os.path.abspath(__file__))

    conn = sqlite3.connect(path + "/" + 'SI_final_project.db')
    cursor = conn.cursor()
    month_counts = get_month_counts_from_db(conn)
    if month_counts:
        plot_normal_distribution(month_counts)
    else:
        print("No data found in the holiday_month table.")
    conn.close()

if __name__ == "__main__":
    main()