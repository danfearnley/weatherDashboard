import requests

def getData(weatherAPIKey, place, days=None, option=None):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={weatherAPIKey}"
    response = requests.get(url)
    data = response.json()
    return data

if __name__ == "__main__":
    print(getData("1274c280a3cd37b84c0ab3ca2791fd03", "Leeds"))