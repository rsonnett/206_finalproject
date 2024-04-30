import json
import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def main():
    #Visualization 1
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + 'SI_final_project.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT Ratings.IMDbRating, Ratings.RTRating, Movies.Title
                        FROM Ratings 
                        JOIN Movies ON Ratings.ID = Movies.ID
                        LIMIT 25''')
    rows = cursor.fetchall()
    conn.close()
    imdb_ratings = []
    imdb_ratings_from_db = [row[0] for row in rows]
    for imdb_rating in imdb_ratings_from_db:
        imdb_rating = str(imdb_rating)
        imdb_ratings.append(imdb_rating)
    rtratings_from_db = [row[1] for row in rows]
    rtratingL= []
    for rtrating in rtratings_from_db:
        rtrating = int(rtrating) / 10
        rtratingL.append(rtrating)
    titles_from_db = [row[2] for row in rows]
    fig, plot1 = plt.subplots(figsize=(10, 5))
    bar_width = 0.35
    bar_positions_imdb = range(len(titles_from_db))
    bar_positions_rt = [pos + bar_width for pos in bar_positions_imdb]
    plot1.bar(bar_positions_imdb, imdb_ratings, bar_width, color='b', label='IMDb Ratings')
    plot1.bar(bar_positions_rt, rtratingL, bar_width, color='r', label='Rotten Tomatoes Ratings')
    plot1.set_xticks([pos + bar_width / 2 for pos in bar_positions_imdb])
    plot1.set_xticklabels(titles_from_db, rotation=90)
    plot1.set_xlabel('Movie Titles')
    plot1.set_ylabel('Rating')
    plot1.set_title('IMDb vs. Rotten Tomatoes Ratings')
    plot1.legend()
    plt.tight_layout()
    

    # Visualization 2: Release Date vs. Movie Titles
    conn = sqlite3.connect(path + "/" + 'SI_final_project.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT Title, ReleaseDate FROM Movies LIMIT 25''')
    rows = cursor.fetchall()
    conn.close()

    titles_from_db = [row[0] for row in rows]
    release_dates_from_db = [row[1] if row[1] else "Unknown" for row in rows]

    plt.figure(figsize=(10, 6))  
    plt.scatter(titles_from_db, release_dates_from_db, color='blue', marker='o')
    plt.plot(titles_from_db, release_dates_from_db, color='red', linestyle='-', linewidth=0.5)
    plt.xticks(rotation=90)
    plt.xlabel('Movie Titles')
    plt.ylabel('Release Dates')
    plt.title('Release Dates vs. Movie Titles')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()