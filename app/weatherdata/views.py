"""
This is the Django view file, here all business logic are written for fetching, manipulating and storing the weather data.
in-memory. Here we have mainly 3- APIs

1. get_weather_data: It will fetch the weather data for a city which is passed into GET request params and return json
response. Also, city name is the mandatory params here.

2. get_list_of_weather_data: It will fetch the list of weather data for a all city passed into a GET request.
This API endpoint will fetch weatherdata asynchronously for all the cities, also it stores their data on JSON file

3. get_min_max_weatherdata: This endpoint will read the weather data from the latest JSON files and return
average weather data temperature, humidity and pressure,
"""


from django.http import JsonResponse, HttpResponse

import asyncio
import concurrent.futures
import datetime
import glob
import json
import os
import requests
from requests import HTTPError

api_key = "6aa99efe0f5372d7133a7120f6195784"
base_url = "http://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={api_key}"

loop = asyncio.get_event_loop()


# *********************************************** Internal methods ***********************************************

def get_latest_file():
    """
    This method will return latest json file from the directory
    :return: newest: file
    """
    newest = max(glob.iglob('*.json'), key=os.path.getctime)
    return newest


def add_current_timestamp(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    """
    This method will return file name append with current datetime
    :param fname: fname
    :param fmt: time format
    :return: 2020-04-08-13-52-37_data.json
    """
    return datetime.datetime.now().strftime(fmt).format(fname=fname)


async def get_json(futures):
    """
    This method will fetch weather data asynchronous for provides cities and store their data on JSON file.
    :param futures:
    :return: None
    """
    data = []
    for response in await asyncio.gather(*futures):
        data.append(response.json())

    with open(add_current_timestamp('data.json'), 'w') as outfile:
        json.dump(data, outfile, indent=4)


async def get_response_data(city_names):
    """
    This method will call get_json asynchronously
    :param city_names: list: ['Bengaluru', 'Delhi', 'Mumbai']
    :return: None
    """
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(executor,
                                     requests.get,
                                     base_url.format(city_name=city_name, api_key=api_key)
                                     )
                for city_name in city_names
            ]
            await get_json(futures)

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")

    except Exception as err:
        print(f"An error ocurred: {err}")


# *********************************************** Django Views ***********************************************

def index(request):
    return HttpResponse("Hello, world. You're at the weatherdata index.")


# GET: http://127.0.0.1:8000/api/v1/get_weather_data?city_name=Delhi
def get_weather_data(request):
    """
    This API will fetch the weather data and return JsonResponse
    :param request: <class 'django.core.handlers.wsgi.WSGIRequest>: Django GET Request
    :return: JsonResponse: type: <class 'django.http.response.JsonResponse'>
    """
    city_name = request.GET.get("city_name")
    data_url = base_url.format(city_name=city_name, api_key=api_key)
    response = requests.get(data_url)
    return JsonResponse({'result': response.json()})


# GET: http://127.0.0.1:8000/api/v1/get_list_of_weather_data?city_name=Delhi,Bengaluru
def get_list_of_weather_data(request):
    """
    This API will get list of city names and call weather API Asyn. Also it will store weather data on JSON file with
    latest time stamp.
    :param request: <class 'django.core.handlers.wsgi.WSGIRequest>: Django GET Request
    :return: HttpResponse: type: <class 'django.http.response.HttpResponse'>
    """
    city_names = request.GET.get("city_name")
    city_names = city_names.split(",")
    loop.run_until_complete(get_response_data(city_names))
    loop.close()
    return HttpResponse("Request is completed successfully for city names: {}".format(city_names))


# GET: http://127.0.0.1:8000/api/v1/get_min_max_weatherdata
def get_min_max_weatherdata(request):
    """
    This API will return average weather data temperature, humidity and pressure, which is stored in JSON files
    :param request: <class 'django.core.handlers.wsgi.WSGIRequest>
    :return: JsonResponse: type: <class 'django.http.response.JsonResponse'>
    """
    humidity, pressure, temp = [], [], []
    result = {}
    newest_file = get_latest_file()
    with open(newest_file) as f:
        json_data = json.load(f)

    for i in json_data:
        data = i.get("main")
        humidity.append(data.get("humidity"))
        pressure.append(data.get("pressure"))
        temp.append(data.get("temp"))

    # find average weather data temperature, humidity and pressure
    result["avg_temp"] = sum(temp) / len(temp)
    result["avg_humidity"] = sum(humidity) / len(humidity)
    result["avg_pressure"] = sum(pressure) / len(pressure)

    return JsonResponse({"result": result})
