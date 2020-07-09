#weather test
from pyowm import OWM
from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient

OWM_API_Key = 'c19412f77f267f8de7781eb6b6ffb56d'

desc_weather_current = """Utility command
60 seconds cooldown per user \n
Get excellent information on the weather of a city. The parameters are <city> and <country_code>.
Both parameters are case insensitive, but need to be exact or the command will give an error.
Some country codes are:
    -Italy: IT
    -Great Britain: GB / United Kingdom: UK  --> Some functions take GB while some take UK, be careful
    -Spain: ES
    -France: FR
    -United States: US
    -Germany: DE
    -Marocco: MA
    -etc...
"""

desc_weather_5days = """Utility command
60 seconds cooldown per user \n
Get excellent information on a 5-days weather forecast of a city. The parameters are <city> and <country_code>.
Both parameters are case insensitive, but need to be exact or the command will give an error.
Only the most important information is desplayed, such as general weather and minimum/maximum temperature.
Some country codes are:
    -Italy: IT
    -Great Britain: GB / United Kingdom: UK  --> Some functions take GB while some take UK, be careful
    -Spain: ES
    -France: FR
    -United States: US
    -Germany: DE
    -Marocco: MA
    -etc...
"""

class Weather(commands.Cog,name="Weather"):
    def __init__(self):
        self.owm = OWM(OWM_API_Key) #language='it' can be added to change language
        self.reg = self.owm.city_id_registry()

    @commands.command(name="weather-current")
    async def weather_current_(self,ctx,city,country_code):
        try:
            response = "``` \n"
            city = city.lower()
            city = city.capitalize()
            country_code = country_code.upper()
            mycity = self.reg.ids_for(city,country=country_code)
            obs = self.owm.weather_at_id(mycity[0][0])
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
            error = "ExceptionError: Please check that you have spelled the city and the country CODE correctly! \nExample of country codes are: Italy-IT, Great Britain-GB, United States-US, Germany-DE, Spain-ES, Marocco-MA, France-FR, etc.. \nCities are to be written in English: EG. Milan is correct, Milano is wrong."
            await ctx.send(error)

    @commands.command(name="weather-5days")
    async def weather_five_days_(self,ctx,city,country_code):
        try:
            response = "```\n"
            response += "Printing a 5-day forecast for the city "+str(city)+" ("+str(country_code)+")"+'\n \n'
            city = city.lower()
            country_code = country_code.upper()
            data = city+","+country_code
            fc = self.owm.three_hours_forecast(data)
            f = fc.get_forecast()
            list = f.get_weathers() #weather objects
            for weather in f:
                response += str(weather.get_reference_time('date'))+"    "+str(weather.get_status())+"\t"+"Min temp:"+str(weather.get_temperature(unit='celsius')["temp_min"])+" \t"+"Max temp:"+str(weather.get_temperature(unit='celsius')["temp_max"])+'\n'
            response+="```"
            await ctx.send(reponse)
        except:
            error = "ExceptionError: Please check that you have spelled the city and the country CODE correctly! \nExample of country codes are: Italy-IT, Great Britain-GB, United States-US, Germany-DE, Spain-ES, Marocco-MA, France-FR, etc.. \nCities are to be written in English: EG. Milan is correct, Milano is wrong."
            await ctx.send(error)