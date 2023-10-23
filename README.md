# iiPythonx/weather  

An efficient weather monitoring application using [OpenWeatherMap](https://openweathermap.org) and [Python](https://python.org).  


### Initial setup
+ Clone the repository ([Download ZIP](https://github.com/iiPythonx/weather/archive/refs/heads/main.zip) or `git clone https://github.com/iiPythonx/weather`)
+ Change into the repo directory (`cd weather`)
+ Install the requirements (`pip install -U -r reqs.txt`)
+ Setup the config.toml file according to [Configuration](#configuration)

### Launching

Recommended usage:
```sh
python3 -m uvicorn src:app --host 0.0.0.0 --port 8080
```

Alternatively, you can launch via `launch_worker.py`:
```sh
python3 launch_worker.py
```

### Configuration

Before you can actually use the recorder, you need to create a `config.toml` file with the following template:
```toml
# OpenWeatherMap related stuff
openweather_api_key = "https://home.openweathermap.org/api_keys"
openweather_city_id = 0123456
scrape_interval     = 10

# If you want to change the default database location:
# database_location   = "/var/weather/db"
```

`openweather_city_id` can be obtained from [OpenWeatherMap](https://openweathermap.org), as well as `openweather_api_key`.

### Running inside docker

This repository contains a very basic `Dockerfile` for running it inside of docker-heavy workflows.  
The following would setup running from inside docker:
```sh
git clone https://github.com/iiPythonx/weather
cd weather
nano config.toml  # add your configuration
docker compose up -d
```
