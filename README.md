# iiWeather
### Easy to use, efficient weather monitoring and archiving utility.
---

### Installation
- Clone the repository `git clone https://github.com/ii-Python/iiWeather`
- Move into the new directory; `cd iiWeather`
- Install dependencies; `python3 -m pip install -r reqs.txt`
- Create a config.json file
```json
{
    "apiKey": "API key from https://openweathermap.org",
    "cityID": "OpenWeatherMap ID for your city"
}
```

### Running
Simply start `python3 weather.py`, and `weather.json` will automatically begin to be populated.

To view your weather data via graph, check out `graph.py`.
