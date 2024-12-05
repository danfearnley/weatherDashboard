import requests

def getData(weatherAPIKey, place, days, option=None):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&units=metric&appid={weatherAPIKey}"
    response = requests.get(url)
    data = response.json()
    unfilteredData = data["list"]
    unfilteredData = unfilteredData[:8 * days] # return the number of days. Multiplied by 8 as gives every 3 hours
    
    filteredData = []
    for item in unfilteredData:
        focusData = {}
        focusData["date"] = item["dt_txt"].split()[0] # get date
        focusData["data"] = {}
        focusData["data"]["time"] = item["dt_txt"].split()[1] # get time
        focusData["data"]["realTemp"] = item["main"]["temp"] # get temp details
        focusData["data"]["feelTemp"] = item["main"]["feels_like"]
        focusData["data"]["minTemp"] = item["main"]["temp_min"]
        focusData["data"]["maxTemp"] = item["main"]["temp_max"]
        focusData["data"]["weather"] = item["weather"][0]["main"] # get weather
        focusData["dateTime"] = item["dt_txt"]
        filteredData.append(focusData)
    
    return filteredData

if __name__ == "__main__":
    print(getData("1274c280a3cd37b84c0ab3ca2791fd03", "Methley", 2, "Weather"))