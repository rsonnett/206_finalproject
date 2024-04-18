import json
import sqlite3
import unittest
import os
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

API_KEY = '8e2144b6'
#returns a dictionary with title as key and rating as value

# def get_movie_titles_rtrating():     
#     output_dict = {}
#     url = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular?page=5"     
#     try:         
#         rotten_requests = requests.get(url)         
#         if rotten_requests.status_code == 200: 
#             html = rotten_requests.text            
#             soup = BeautifulSoup(html, 'html.parser')            
#             movies = soup.find_all('span', class_="p--small")     
#             percentages = soup.find_all("score-pairs-deprecated", audienceScore="")        
#             movie_count = 0           
#             for (movie, percent) in zip(movies, percentages):                 
#                 movie = movie.text
#                 movie = movie.strip()
#                 percent = percent.attrs['audiencescore']
#                 if movie_count < 100: 
#                     if movie not in output_dict: 
#                         output_dict[movie] = percent                                  
#                 elif movie_count == 100:                     
#                     break                 
#                 movie_count += 1 
#         else:             
#             print("Error fetching data from Rotten Tomatoes:", rotten_requests.status_code)     
#     except Exception as e:         
#         print("An error occurred:", e)     
#     return output_dict

#returns release date after being looped through movie titles

# def get_release_date(movie):
#     url= f'http://www.omdbapi.com/?t={movie}&apikey=b979ef45'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         release_date = data.get('Released')
#         return release_date
#     else:
#         print("Error:", response.status_code)

#returns IMDB rating after looping through movie titles

# def get_imdb_rating(movie):
#     url = f'http://www.omdbapi.com/?t={movie}&apikey=b979ef45'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         imdb_rating = data.get('imdbRating')
#         if imdb_rating:
#             return imdb_rating
#         else:
#             return None
#     else:
#         print("Error:", response.status_code)
#         return None

# def get_rating():
#     percentages = []     
#     url = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular?page=5"     
#     try:         
#         rotten_requests = requests.get(url)         
#         if rotten_requests.status_code == 200: 
#             html = rotten_requests.text            
#             soup = BeautifulSoup(html, 'html.parser')             
#             movies = soup.find_all(attrs= "score-pairs-deprecated audienceScore")              
#             movie_count = 0             
#             for percent in movies:                                
#                 if movie_count < 100:                     
#                     percentages.append(percent)                 
#                 elif movie_count == 100:                     
#                     break                 
#                 movie_count += 1         
#         else:             
#             print("Error fetching data from Rotten Tomatoes:", rotten_requests.status_code)     
#     except Exception as e:         
#         print("An error occurred:", e)     
#     return percentages

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

def	get_movie_titles():
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

def get_release_date(movie):
    url = f'http://www.omdbapi.com/?t={movie}&apikey=b979ef45'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        release_date = data.get('Released')
        return release_date
    else:
        print("Error:", response.status_code)


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



fig = plt.figure (1, figsize=(10,5))
plot1 = plt.subplot (1,2,1)
plot2=plt.subplot (1,2,2)
plot1.barh(imdb, rt)
plot1.set_title("IMDB vs. Rotten Tomato ratings")
plot1.set_ylabel("Weather")
plot1.set_xlabel("Temperature")