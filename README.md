# Weather App

> Weather app created with Flask library and SQLite database

> uses openweatherapi.org api to get current weather information

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Project Status](#project-status)


## General Information
- Purpose of this project was creating an app to display current weather in chosen cites.

## Technologies Used
- Python
- Sqlite
- Flask 
- SqlAlchemy

## Features
- Display weather for chosen city:
    - Temperature
    - State
    - City name
    - Local date and time of gathered data
    - Different background depending on the hour (day, evening, night)
- Pull information about current weather from api
- Create database to keep chosen cities displayed
- Let user add new cities
- Display alert in case of unknown city name
- Responsive design adapts to screen size

## Screenshots
<img width="600" alt="weather-app-py-screenshot" src="https://user-images.githubusercontent.com/24957921/192166670-d5e513c0-8a27-4555-9c0b-7c84af1be5a7.png">

## Setup
1. Create a new virtual environment:
```python3 -m venv venv```
2. Activate the environment:
```source venv/bin/activate```
3. Install all external dependencies:
```python -m pip install requirements.txt```
4. To run a flask development server:
```python app.py```

## Project Status
> Complete

