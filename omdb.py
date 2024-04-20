import json
import sqlite3
import unittest
import os
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time


API_KEY = '8e2144b6'
# #returns a dictionary with title as key and rating as value

def get_movie_titles_rtrating():     
    output_dict = {}
    url = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular?page=5"     
    try:         
        rotten_requests = requests.get(url)         
        if rotten_requests.status_code == 200: 
            html = rotten_requests.text            
            soup = BeautifulSoup(html, 'html.parser')            
            movies = soup.find_all('span', class_="p--small")     
            percentages = soup.find_all("score-pairs-deprecated", audienceScore="")        
            movie_count = 0           
            for (movie, percent) in zip(movies, percentages):                 
                movie = movie.text
                movie = movie.strip()
                percent = percent.attrs['audiencescore']
                if movie_count < 100: 
                    if movie not in output_dict: 
                        output_dict[movie] = percent                                  
                elif movie_count == 100:                     
                    break                 
                movie_count += 1 
        else:             
            print("Error fetching data from Rotten Tomatoes:", rotten_requests.status_code)     
    except Exception as e:         
        print("An error occurred:", e)     
    return output_dict

#returns release date after being looped through movie titles

def get_release_date(movie):
    url= f'http://www.omdbapi.com/?t={movie}&apikey=b979ef45'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        release_date = data.get('Released')
        return release_date
    else:
        print("Error:", response.status_code)

#returns IMDB rating after looping through movie titles

def get_imdb_rating(movie):
    url = f'http://www.omdbapi.com/?t={movie}&apikey=b979ef45'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        imdb_rating = data.get('imdbRating')
        if imdb_rating:
            return imdb_rating
        else:
            return None
    else:
        print("Error:", response.status_code)
        return None


# def main():
#     movie_titles_ratings = get_movie_titles_rtrating()
#     for title, rtrating in movie_titles_ratings.items():
#         release_date = get_release_date(title)
#         if release_date is not None:
#             imdb_rating = get_imdb_rating(title)
#             if imdb_rating is not None:
#                 if rtrating.strip() != '': 
#                     print(f"The release date for '{title}' is {release_date}. The IMDb rating is {imdb_rating} and the Rotten Tomato rating is {rtrating}.")
#                 else:
#                     print(f"The release date for '{title}' is {release_date}. The IMDb rating is {imdb_rating} but the Rotten Tomato rating was not found.")
#             else:
#                 print(f"IMDb rating not found for '{title}'")
#         else:
#             print(f"Release date not found for '{title}'")
   
# if __name__ == '__main__':
#     main()

def get_movie_titles():
    movie_titles = []
    url = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular?page=5"
    try:
        rotten_requests = requests.get(url)
        if rotten_requests.status_code == 200:
            html = rotten_requests.text
            soup = BeautifulSoup(html, 'html.parser')
            movies = soup.find_all('span', class_="p--small")
            movie_count = 0
            for movie in movies:
                movie = movie.text.strip()
                if movie_count < 100:
                    movie_titles.append(movie)
                elif movie_count == 100:
                    break
                movie_count += 1 
        else:
            print("Error fetching data from Rotten Tomatoes:", rotten_requests.status_code)
    except Exception as e:
        print("An error occurred:", e)
    return movie_titles

# movie_titles_ratings = get_movie_titles_rtrating()

# imdb_ratings = []
# rt_ratings = []
# movie_titles = []

# for title, rtrating in movie_titles_ratings.items():
#     release_date = get_release_date(title)
#     if release_date is not None:
#         imdb_rating = get_imdb_rating(title)
#         if imdb_rating is not None:
#             # Append ratings to lists
#             imdb_ratings.append(float(imdb_rating))
#             rt_ratings.append(float(rtrating))
#             movie_titles.append(title)

# # Create an array of indices for each movie
# indices = np.arange(len(movie_titles))

# # Width of each bar
# bar_width = 0.35

# # Create the figure and subplot
# fig, plot1 = plt.subplots(figsize=(15, 8))

# # Plot IMDb ratings
# plot1.barh(indices - bar_width/2, imdb_ratings, bar_width, label='IMDB Rating')

# # Plot Rotten Tomato ratings
# plot1.barh(indices + bar_width/2, rt_ratings, bar_width, label='Rotten Tomato Rating')

# # Set the y-axis labels to movie titles
# plot1.set_yticks(indices)
# plot1.set_yticklabels(movie_titles)
# plot1.set_xlabel('Ratings')
# plot1.set_ylabel('Movies')
# plot1.set_title('IMDB vs. Rotten Tomato Ratings')
# plot1.legend()

# plt.tight_layout()
# plt.show()



url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Los%20Angeles/2023-01-01/2024-04-15?unitGroup=us&key=JQ755KVD2PU6VFA6Z6EGQV7QP&include=obs"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    temperature_data = {}
    for entry in data['days']:
        date = entry['datetime']
        temperature = entry['temp']
        temperature_data[date] = temperature

#Create TemperatureData Table

conn = sqlite3.connect('/Users/lilysteinmetz/Desktop/SI_final_project.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS TemperatureData (
ID INTEGER PRIMARY KEY,
Date TEXT,
Temperature REAL
)''')

for date, temperature in temperature_data.items():
    cursor.execute('''INSERT INTO TemperatureData (Date, Temperature) VALUES (?, ?)''', (date, temperature))

conn.commit()
conn.close()

print("Table created and data inserted successfully.")

#Create Movies Table

conn = sqlite3.connect('/Users/lilysteinmetz/Desktop/SI_final_project.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS Movies (
ID INTEGER PRIMARY KEY,
Title TEXT,
ReleaseDate TEXT
)''')


titles = get_movie_titles()
for title in titles:
    release_date = get_release_date(title)
    cursor.execute('''INSERT INTO Movies (Title, ReleaseDate) VALUES (?, ?)''', (title, release_date))

conn.commit()
conn.close()

print("Table created and data inserted successfully.")

#Create Ratings table

def create_database_table():
    conn = sqlite3.connect('/Users/lilysteinmetz/Desktop/SI_final_project.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Ratings
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 IMDbRating REAL,
                 RTRating TEXT)''')
    conn.commit()
    conn.close()

def insert_into_table(imdb_rating, rt_rating):
    conn = sqlite3.connect('/Users/lilysteinmetz/Desktop/SI_final_project.db')
    c = conn.cursor()
    c.execute("INSERT INTO Ratings (IMDbRating, RTRating) VALUES (?, ?)", (imdb_rating, rt_rating))
    conn.commit()
    conn.close()

print("Table created and data inserted successfully.")

def main():
    create_database_table()
    movie_titles = get_movie_titles()
    for title in movie_titles:
        imdb_rating = get_imdb_rating(title)
        rt_rating = get_movie_titles_rtrating().get(title)
        insert_into_table(imdb_rating, rt_rating)


if __name__ == '__main__':
    main()