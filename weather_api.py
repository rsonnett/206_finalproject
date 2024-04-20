import requests

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


    


    
    


