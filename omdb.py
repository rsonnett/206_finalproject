import json
import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


API_KEY = '8e2144b6'
#returns a dictionary with title as key and rating as value

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
                     
            for (movie, percent) in zip(movies, percentages):                 
                movie = movie.text
                movie = movie.strip()
                percent = percent.attrs['audiencescore']
                if movie not in output_dict: 
                    output_dict[movie] = percent   
                
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

url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Los%20Angeles/2023-01-01/2024-04-15?unitGroup=us&key=JQ755KVD2PU6VFA6Z6EGQV7QP&include=obs"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    temperature_data = {}
    for entry in data['days']:
        date = entry['datetime']
        temperature = entry['temp']
        temperature_data[date] = temperature

    print(temperature_data)

else:
    print("Failed to retrieve data from the API:", response.status_code)


#Table 1- Temperature Data
# path = os.path.dirname(os.path.abspath(__file__))

# conn = sqlite3.connect(path + "/" + 'SI_final_project.db')
# cursor = conn.cursor()

# cursor.execute('''CREATE TABLE IF NOT EXISTS TemperatureData (
# ID INTEGER PRIMARY KEY,
# Date TEXT,
# Temperature REAL
# )''')

# for date, temperature in temperature_data.items():
#     cursor.execute('''INSERT INTO TemperatureData (Date, Temperature) VALUES (?, ?)''', (date, temperature))

# conn.commit()
# conn.close()

# print("Table created and data inserted successfully.")

#Table 2- Ratings

def create_database_table():
    path = os.path.dirname(os.path.abspath(__file__))

    conn = sqlite3.connect(path + "/" + 'SI_final_project.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Ratings
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 IMDbRating REAL,
                 RTRating TEXT)''')
    conn.commit()
    conn.close()

def insert_into_table(imdb_rating, rt_rating):
    path = os.path.dirname(os.path.abspath(__file__))

    conn = sqlite3.connect(path + "/" + 'SI_final_project.db')
    c = conn.cursor()
    c.execute("INSERT INTO Ratings (IMDbRating, RTRating) VALUES (?, ?)", (imdb_rating, rt_rating))
    conn.commit()
    conn.close()

print("Table created and data inserted successfully.")

#Table 3- Movies
def main():
    imdb_ratings = []
    release_dates = []
    titles = []
    rtratings = []
    count = 0
    path = os.path.dirname(os.path.abspath(__file__))

    conn = sqlite3.connect(path + "/" + 'SI_final_project.db')
    cursor = conn.cursor()
    
    cursor.execute('''DROP TABLE Movies''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Movies (
                            ID INTEGER PRIMARY KEY,
                            Title TEXT,
                            ReleaseDate TEXT
                        )''')
    movie_titles_ratings = get_movie_titles_rtrating()
    for title, rtrating in movie_titles_ratings.items():
        release_date = get_release_date(title)
        cursor.execute('''INSERT INTO Movies (Title, ReleaseDate) VALUES (?, ?)''', (title, release_date))
        if release_date is not None:
            imdb_rating = get_imdb_rating(title)          
            if imdb_rating is not None:              
                if count < 25:
                    try:
                        rtratingI = int(rtrating)
                        imdb_ratings.append(imdb_rating)
                        titles.append(title)
                        rtratings.append(rtratingI / 10)
                        release_dates.append(release_date)
                    except ValueError:
                        print("The string does not represent a valid integer.")              
                count += 1
                if rtrating.strip() != '': 
                    print(f"The release date for '{title}' is {release_date}. The IMDb rating is {imdb_rating} and the Rotten Tomato rating is {rtrating}.")
                else:
                    print(f"The release date for '{title}' is {release_date}. The IMDb rating is {imdb_rating} but the Rotten Tomato rating was not found.")
            else:
                print(f"IMDb rating not found for '{title}'")
        else:
            print(f"Release date not found for '{title}'")
    conn.commit()
    conn.close()
    print("Table created and data inserted successfully.")

   # Sort the data based on IMDb ratings
    sorted_data = sorted(zip(imdb_ratings, rtratings, titles))

    # Extract sorted ratings and titles
    sorted_imdb_ratings, sorted_rtratings, sorted_titles = zip(*sorted_data)

    # Create a figure and subplots
    fig, plot1 = plt.subplots(figsize=(10, 5))

    # Set the positions for the bars
    bar_width = 0.35
    bar_positions_imdb = range(len(titles))
    bar_positions_rt = [pos + bar_width for pos in bar_positions_imdb]

    # Plot IMDb ratings
    plot1.bar(bar_positions_imdb, sorted_imdb_ratings, bar_width, color='b', label='IMDb Ratings')

    # Plot Rotten Tomatoes ratings
    plot1.bar(bar_positions_rt, sorted_rtratings, bar_width, color='r', label='Rotten Tomatoes Ratings')

    # Set x-axis labels as movie titles
    plot1.set_xticks([pos + bar_width / 2 for pos in bar_positions_imdb])
    plot1.set_xticklabels(sorted_titles, rotation=90)

    # Set labels and title
    plot1.set_xlabel('Movie Titles')
    plot1.set_ylabel('Rating')
    plot1.set_title('IMDb vs. Rotten Tomatoes Ratings')
    plot1.legend()

    # Show the plot
    plt.tight_layout()


    # Visualization 2: Release Date vs. Movie Titles
    plt.figure(figsize=(10, 6))  
    plt.scatter(titles[:25], release_dates[:25], color='blue', marker='o')
    plt.plot(titles[:25], release_dates[:25], color='red', linestyle='-', linewidth=0.5)
    plt.xticks(rotation=90)
    plt.xlabel('Movie Titles')
    plt.ylabel('Release Dates')
    plt.title('Release Dates vs. Movie Titles')
    plt.tight_layout()

    plt.show()

if __name__ == '__main__':
    main()