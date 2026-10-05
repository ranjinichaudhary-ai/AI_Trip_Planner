import os
from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper

@tool
def multiply(a:int, b:int)->int:
    """
    Multiply two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.
    
    Returns:
        int: The product of the two numbers.
    """
    return a*b

@tool
def add(a:int, b:int)->int:
    """
    Add two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.
    
    Returns:
        int: The sum of the two numbers.
    """
    return a+b

@tool
def currency_converter(from_curr:str, to_curr:str, value:float)->float:
    os.environ["ALPHA_VANTAGE_API_KEY"] = os.getenv("ALPHA_VANTAGE_API_KEY")
    alpha_vantage = AlphaVantageAPIWrapper()
    response = alpha_vantage._get_exchange_rate(from_curr, to_curr)
    exchange_rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
    return value * float(exchange_rate)