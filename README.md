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

### Graphing Customization
For the graphing program, `graph.py`, you can create a `graph` key in `config.json`.  
The following options are available:
```json
{
    "graph": {
        "markerColor": "HEX color code for the horizontal lines",
        "lineColor": "HEX color code for the data line",
        "showAllData": "whether to show ALL recorded data",
        "showInterval": "how often to show data (in minutes, 20 recommended)",
        "showXLabel": "show the time as the x label or not, if not, shows minutes from midnight"
    }
}
```
