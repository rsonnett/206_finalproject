import sqlite3

def get_average_ratings_for_holidays():
    conn = sqlite3.connect('SI_final_project.db')
    cursor = conn.cursor()

    relevant_holidays = ["New Year's Day", "Martin Luther King Jr. Day", "Valentine's Day", "Presidents' Day", "St. Patrick's Day", "April Fools' Day", "Easter Sunday", "Memorial Day", "Independence Day", "Labor Day", "Halloween", "Veterans Day", "Thanksgiving Day", "Christmas Day"]
    ratings = {"imdb": {}, "Rotten Tomato": {}}

    for holiday in relevant_holidays:
        cursor.execute("SELECT imdbrating, RTRating FROM Movies INNER JOIN Holidays ON Movies.ReleaseDate = Holidays.Date WHERE Holiday = ?", (holiday,))
        rows = cursor.fetchall()
        imdb_ratings = [float(row[0]) for row in rows if row[0] is not None]
        rt_ratings = [float(row[1]) for row in rows if row[1] is not None]
        if imdb_ratings:
            ratings["imdb"][holiday] = sum(imdb_ratings) / len(imdb_ratings)
        if rt_ratings:
            ratings["Rotten Tomato"][holiday] = sum(rt_ratings) / len(rt_ratings)

    conn.close()
    return ratings