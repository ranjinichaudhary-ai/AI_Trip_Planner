import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from utils.weather_info import WeatherForecastTool
from langchain.tools import tool


class WeatherInfoTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        # WeatherForecastTool functionality will be available in the utils
        # capture the service
        self.weather_service = WeatherForecastTool(self.api_key)
        # capture the list of tools
        self.weather_tool_list = self._setup_tools()

    #private function
    # responsible for creating a tool
    def _setup_tools(self) -> List:
        """Set up all tools for the weather forecast tool."""
        @tool
        def get_current_weather(city: str)-> str:
            """Get the current weather for a city."""
            weather_data=self.weather_service.get_current_weather(city)
            if weather_data:
                temp=weather_data.get("main", {}).get("temp",'N/A')
                desc=weather_data.get("weather", [{}])[0].get("description",'N/A')
                return f"Current weather in {city}: {temp}°C, {desc}"
            return f"Could not fetch weather for {city}"

        @tool
        def get_weather_forecast(city: str)-> str:
            """Get the weather forecast for a city."""
            forecast_data=self.weather_service.get_weather_forecast(city)
            if forecast_data and 'list' in forecast_data:
                forecast_summary=[]
                for i in range(len(forecast_data['list'])):
                    item=forecast_data['list'][i]
                    date=item['dt_txt'].split(' ')[0]
                    temp=item['main']['temp']
                    desc=item['weather'][0]['description']
                    forecast_summary.append(f"{date}: {temp}°C, {desc}")
                return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
            return f"Could not fetch forecast for {city}"
        
        # we are going to capture real time data using WeatherForecastTool function
        # return this tool with the entire functionality
        # all the tools will be associated with llm we are going to bind it with LLM
        return [get_current_weather, get_weather_forecast]
    