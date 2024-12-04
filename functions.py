import requests

def getData(weatherAPIKey, place, days, option=None):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&units=metric&appid={weatherAPIKey}"
    response = requests.get(url)
    data = response.json()
    filteredData = data["list"]
    filteredData = filteredData[:8 * days] # return the number of days. Multiplied by 8 as gives every 3 hours
    return filteredData

if __name__ == "__main__":
    print(getData("1274c280a3cd37b84c0ab3ca2791fd03", "Methley", 2, "Weather"))