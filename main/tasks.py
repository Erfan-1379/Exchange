from decouple import config
import requests
from celery import shared_task
from .models import Currency
import re

URL = config('ARZ_URL')

def convert_farsi_numbers(text):
    farsi_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"
    translation_table = str.maketrans(farsi_digits, english_digits)
    return text.translate(translation_table)

@shared_task
def fetch_currency_data():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            currencies = response.json()
            for currency in currencies:
                name = currency["name"].strip()
                price_str = currency["price"].strip().replace(",", "")
                price = float(convert_farsi_numbers(price_str))

                Currency.objects.update_or_create(
                    name=name, defaults={'price': price}
                )
            return "Data updated successfully"
        return f"Error: Invalid response code {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
