# weatherdata

This is the Django project, for fetching, manipulating and storing the weather data
in-memory.

## Dependencies

1. You just need Python3, visit the python official link to install [python](https://www.python.org/downloads/)

2. Install Django for Rest API calls

```bash
pip install django
```

## Description:

This is the Django project, for fetching, manipulating and storing the weather data
in-memory.

For storing the weather data we could have used <b>parquet</b> file format. But I am using <b>JSON</b> file for storing weather data.

For asynchronous call I am using asyncio and concurrent.futures python library, we could have used <b>Celery</b> and <b>RabbitMQ</b> as a backend, which will also give the same result.

<b>Note</b>: Due to lack of System Memory I am not using Spark related stuff, because I had to install Java and Spark in my local system which was causing system low.



## Run Python file:
```bash
python manage.py runserver
```

## Sample API calls
```bash
1. get_weather_data: http://127.0.0.1:8000/api/v1/get_weather_data?city_name=Delhi

2. get_list_of_weather_data: http://127.0.0.1:8000/api/v1/get_list_of_weather_data?city_name=Delhi,Bengaluru

3. get_min_max_weatherdata: http://127.0.0.1:8000/api/v1/get_min_max_weatherdata

- First API will fetch the weather data for a city which is passed into GET request params and return json
response. Also, city name is the mandatory params here.

- Second API  will fetch the list of weather data for a all city passed into a GET request.
This API endpoint will fetch weatherdata asynchronously for all the cities, also it stores their data on JSON file

- Third endpoint will read the weather data from the latest JSON files and return
average weather data temperature, humidity and pressure,