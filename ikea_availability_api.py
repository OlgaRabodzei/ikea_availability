import requests
from xml.etree import ElementTree

# product_id_low_availability = '50219044'
# product_id_high_availability = '90263902'


class IkeaAvailability:
    def __init__(self, product_id):
        url_base = 'https://www.ikea.com/ua/uk/iows/catalog/availability/'
        response = requests.get(url_base + product_id)
        if response.status_code != 200:
            # TODO better error handling.
            # raise Exception('Sorry! Service is an available.')
            return
        # TODO Can the generator raise an error?
        self.response_content = ElementTree.fromstring(response.content)

    def is_product_available(self):
        for stock in self.response_content.findall('availability/localStore/stock'):
            if stock.find('isSoldInStore') is None or stock.find('availableStock') is None:
                continue
            # Does the product belongs to the store’s portfolio.
            is_in_store = True if stock.find('isSoldInStore').text == 'true' else False
            amount_available = int(stock.find('availableStock').text)
            # Check if the product is available in the stock.
            if is_in_store and amount_available:
                return True
        return False

    def availability_forecast(self):
        forecast_dates = {}
        for stock in self.response_content.findall('availability/localStore/stock'):
            if stock.find('forecasts') is None:
                continue
            forecast_dates = {
                forecast.find('validDate').text: forecast.find('availableStock').text
                for forecast
                in stock.find('forecasts')
            }

        return forecast_dates
