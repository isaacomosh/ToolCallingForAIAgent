def get_weather(city):
    """
    Get weather information for a city.
    """
    weather_data={
        "nairobi":{
            "temperature": 24,
            "condition":"Sunny"
        },
        "mombasa":{
            "temperature":29,
            "condition":"Partly cloudy"
        }
    }
    city_key=city.lower()
    if city_key in weather_data:
        return{
            "city":city,
            **weather_data[city_key]
        }
    return{
        "city":city,
        "temperature":None,
        "condition":"Weather data not available"
    }

#This dictionary allows us to map the name
#returned by the LLM to an actual Python function
AVAILABLE_TOOLS={
    "get_weather":get_weather
}