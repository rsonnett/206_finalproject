import json
import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


API_KEY = '8e2144b6'
#returns a dictionary with title as key and rating as value

def get_movie_titles():     
   
    moviesL = []
    url = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular?page=5"     
    try:         
        rotten_requests = requests.get(url)         
        if rotten_requests.status_code == 200: 
            html = rotten_requests.text            
            soup = BeautifulSoup(html, 'html.parser')            
            movies = soup.find_all('span', class_="p--small")     
                    
                     
            for movie in movies:                 
                movie = movie.text
                movie = movie.strip()
                
                if movie not in moviesL: 
                    moviesL.append(movie)
                
        else:             
            print("Error fetching data from Rotten Tomatoes:", rotten_requests.status_code)     
    except Exception as e:         
        print("An error occurred:", e)     
    return moviesL

def get_rtrating():
    
    percentagesL = []
    url = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:popular?page=5"     
    try:         
        rotten_requests = requests.get(url)         
        if rotten_requests.status_code == 200: 
            html = rotten_requests.text            
            soup = BeautifulSoup(html, 'html.parser') 
            percentages = soup.find_all("score-pairs-deprecated", audienceScore="") 

            for percent in percentages:
                percent = percent.attrs['audiencescore']
                percentagesL.append(percent)

                
    except Exception as e:         
        print("An error occurred:", e) 
    return percentagesL


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



#Table 2- Ratings

def create_database_table(conn):
    
    c = conn.cursor()
    # c.execute('''DROP TABLE Ratings''')
    c.execute('''CREATE TABLE IF NOT EXISTS Ratings
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 IMDbRating REAL,
                 RTRating TEXT)''')
    conn.commit()
    

def insert_into_table(imdb_rating, rt_rating, conn):
    
    c = conn.cursor()
    
    c.execute("INSERT INTO Ratings (IMDbRating, RTRating) VALUES (?, ?)", (imdb_rating, rt_rating))
    conn.commit()
    

    print("Table created and data inserted successfully.")

def get_date_id(release_date):
    i = 0
    release_date_list = []
    if release_date:
        release_date_list = release_date.split(" ")
    if len(release_date_list) > 1:
        if release_date_list[1] == "Jan":
            if release_date_list[2] == "2023":
                i = 1
            else:
                i = 13
        elif release_date_list[1] == "Feb":
            if release_date_list[2] == "2023":
                i = 2
            else:
                i = 14
        elif release_date_list[1] == "Mar":
            if release_date_list[2] == "2023":
                i = 3
            else:
                i = 15
        elif release_date_list[1] == "Apr":
            if release_date_list[2] == "2023":
                i = 4
            else:
                i = 16
        elif release_date_list[1] == "May":
            i = 5
        elif release_date_list[1] == "Jun":
            i = 6
        elif release_date_list[1] == "Jul":
            i = 7
        elif release_date_list[1] == "Aug":
            i = 8
        elif release_date_list[1] == "Sep":
            i = 9
        elif release_date_list[1] == "Oct":
            i = 10
        elif release_date_list[1] == "Nov":
            i = 11
        elif release_date_list[1] == "Dec":
            i = 12
    
        j = int(release_date_list[0])

        if i != 0:
            return (i*100) + j
        else:
            return 0
    else:
        return 0

def count_rows(table_name):
    path = os.path.dirname(os.path.abspath(__file__))

    conn = sqlite3.connect(path + "/" + 'SI_final_project.db')
    cursor = conn.cursor()
    
    try:
        # Execute the SQL query to count rows in the table
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        # Fetch the result
        result = cursor.fetchone()[0]
        print(f"Number of rows in '{table_name}': {result}")
        return result
    except sqlite3.Error as e:
        print("An error occurred:", e)
    
    # Close the connection
    conn.close()

#CREATE AN INDEX THAT COUNTS THE ROW THAT YOU ARE IN THE DATA THAT HAS BEEN COLLECTED SO FAR, 
#HAVE A FOR LOOP THAT LETS YOU GO UP TO 25 MORE THAN WHERE YOU BEGAN- INDEX INTO DATA USING THAT INDEX
#THEN UPDATE THE INDEX AT THE END

#Table 3- Movies
def main():
    imdb_ratings = []
    release_dates = []
    movie_titles = []
    titles = []
    rtratings = []
    
    path = os.path.dirname(os.path.abspath(__file__))

    conn = sqlite3.connect(path + "/" + 'SI_final_project.db')
    cursor = conn.cursor()
    
    # cursor.execute('''DROP TABLE Movies''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Movies (
                            ID INTEGER PRIMARY KEY,
                            Title TEXT,
                            date_id REAL,
                            ReleaseDate TEXT
                        )''')
    create_database_table(conn)
    movie_titles = get_movie_titles()
    rtratings = get_rtrating()
    i = count_rows('Movies')
    j = count_rows('Movies')
    while i < (j + 25):
        if i < len(movie_titles) and i < len(rtratings):
            release_date = get_release_date(movie_titles[i])
            date_id = get_date_id(release_date)
            cursor.execute('''INSERT INTO Movies (Title, ReleaseDate, date_id) VALUES (?, ?, ?)''', (movie_titles[i], release_date, date_id))
            i += 1
            if release_date is not None:
                imdb_rating = get_imdb_rating(movie_titles[i])     
                 
                if imdb_rating is not None:              
                    #if count < 25:
                    try:
                        rtratingI = int(rtratings[i])
                        imdb_ratings.append(imdb_rating)
                        insert_into_table(imdb_rating, rtratingI, conn)
                        titles.append(movie_titles[i])
                        rtratings.append(rtratingI / 10)
                        release_dates.append(release_date)
                    except ValueError:
                        print("The string does not represent a valid integer.")              
            
                if movie_titles[i].strip() != '': 
                    print(f"The release date for '{movie_titles[i]}' is {release_date}. The IMDb rating is {imdb_rating} and the Rotten Tomato rating is {rtratings[i]}.")
                else:
                    print(f"The release date for '{movie_titles[i]}' is {release_date}. The IMDb rating is {imdb_rating} but the Rotten Tomato rating was not found.")
            else:
                print(f"IMDb rating not found for '{movie_titles[i]}'")
        else:
            print(f"Release date not found for '{movie_titles[i]}'")

        
        if i == 24:
            j += 1
    conn.commit()
    conn.close()
    print("Table created and data inserted successfully.")

if __name__ == '__main__':
    main()