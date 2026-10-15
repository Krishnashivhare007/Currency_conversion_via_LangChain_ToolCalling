from langchain_community.tools import tool
import requests


@tool
def get_conversion_factor(base_currency:str,target_currency:str)->float:
    """
    This function fetches the currency conversion factor between a given base currency and a target currency
    """
    url = f'https://v6.exchangerate-api.com/v6/ee66a527a76b1de9eda24427/pair/{base_currency}/{target_currency}'

    response = requests.get(url)

    return response.json()['conversion_rate']

print(get_conversion_factor.invoke({'base_currency':'USD','target_currency':'INR'}))

