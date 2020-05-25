#weather test
from pyowm import OWM
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
import datetime

OWM_API_Key = 'c19412f77f267f8de7781eb6b6ffb56d'
owm = OWM(OWM_API_Key) #language='it' can be added to change language
reg = owm.city_id_registry()

async def weather_current_(ctx,city,country_code):
    try:
        response = "``` \n"
        city = city.lower()
        city = city.capitalize()
        country_code = country_code.upper()
        mycity = reg.ids_for(city,country=country_code)
        obs = owm.weather_at_id(mycity[0][0])
        w=obs.get_weather()
        temp = w.get_temperature(unit='celsius')

        response += "Current weather for "+city+" ("+country_code+")"+'\n'
        response += "Reference time: "+str(w.get_reference_time(timeformat='iso'))+'\n'
        response += "General status: "+str(w.get_detailed_status())+'\n'
        response += "Cloud coverage: "+str(w.get_clouds())+'\n'
        response += "Wind speed: "+str(w.get_wind()["speed"])+'\n'
        response += "Humidity: "+str(w.get_humidity())+'\n'
        response += "Temperature Stats: "+'\n'
        response += "\t "+"--Minimum: "+str(temp["temp_min"])+'\n'
        response += "\t "+"--Current: "+str(temp["temp"])+'\n'
        response += "\t "+"--Maximum: "+str(temp["temp_max"])+'\n'
        response += "Sunrise time: "+ str(w.get_sunrise_time('iso'))+'\n'
        response += "Sunset time: "+ str(w.get_sunset_time('iso'))+'\n'
        response += '```'
        await ctx.send(response)
    except:
        error = "ExceptionError: Please check that you have spelled the city and the country CODE correctly! \n Example of country codes are: Italy-IT, Great Britain-GB, United States-US, Germany-DE, Spain-ES, Marocco-MA, France-FR, etc.. \n Cities are to be written in English: EG. Milan is correct, Milano is wrong."
        await ctx.send(error)


async def weather_five_days_(ctx,city,country_code):
    try:
        response = "```\n"
        response += "Printing a 5-day forecast for the city "+str(city)+" ("+str(country_code)+")"+'\n \n'
        city = city.lower()
        country_code = country_code.upper()
        data = city+","+country_code
        fc = owm.three_hours_forecast(data)
        f = fc.get_forecast()
        list = f.get_weathers() #weather objects
        for weather in f:
            response += str(weather.get_reference_time('date'))+"    "+str(weather.get_status())+"\t"+"Min temp:"+str(weather.get_temperature(unit='celsius')["temp_min"])+" \t"+"Max temp:"+str(weather.get_temperature(unit='celsius')["temp_max"])+'\n'
        response+="```"
        await ctx.send(reponse)
    except:
        error = "ExceptionError: Please check that you have spelled the city and the country CODE correctly! \n Example of country codes are: Italy-IT, Great Britain-GB, United States-US, Germany-DE, Spain-ES, Marocco-MA, France-FR, etc.. \n Cities are to be written in English: EG. Milan is correct, Milano is wrong."
        await ctx.(error)
