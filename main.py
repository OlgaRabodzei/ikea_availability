import requests
from xml.etree import ElementTree
import sys

url = 'https://www.ikea.com/ua/uk/iows/catalog/availability/50219044/'
response = requests.get(url)

if response.status_code != 200:
    print('Sorry! Service is an available.')
    sys.exit()

response_content = ElementTree.fromstring(response.content)

for store in response_content.find('availability'):
    # TODO: Not hard code the ID, as it could be diff per country.
    # Ukraine store ID.
    if store.get('buCode') == '588':
        stock = store.find('stock')
        amount_available = stock.find('availableStock').text
        print(f'Available in stock: {amount_available}')
        # Forecast
        for forecast in stock.find('forecasts'):
            f_available = forecast.find('availableStock').text
            f_date = forecast.find('validDate').text
            print(f'{f_date} : {f_available}')