# iiPythonx/weather  

An efficient weather monitoring application using [OpenWeatherMap](https://openweathermap.org) and [Python](https://python.org).  


### Initial setup
+ Clone the repository (Download ZIP or `git clone https://github.com/iiPythonx/weather`)
+ Change into the repo directory (`cd weather`)
+ Install the requirements (`pip install -U -r reqs.txt`)
+ Setup the config.json file according to [Configuration](#configuration)

### Launching

To launch the weather recorder, you can simply run `weather.py` with your Python interpreter.

### Configuration

Before you can actually use the recorder, you need to create a `config.json` file with the following template:
```json
{
    "main": {
        "owm": {
            "city_id": 0000000,
            "api_key": "Obtain this from https://openweathermap.org"
        },
        "save_interval": 10
    },
    "web": {
        "addr": ["0.0.0.0", 8080]
    }
}
```

The OWM city ID is obtained from [OpenWeatherMap](https://openweathermap.org), same with the `api_key`.  
The `addr` property tells Flask where to bind the HTTP server to, choose it wisely.
