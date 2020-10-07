import requests
from xml.etree import ElementTree

# product_id = '50219044'


class IkeaAvailability:
    def __init__(self):
        self.url_base = 'https://www.ikea.com/ua/uk/iows/catalog/availability/'

    def _request_availability_info(self, product_id):
        response = requests.get(self.url_base + product_id)
        if response.status_code != 200:
            # TODO better error handling.
            print('Sorry! Service is an available.')
            return False
        # TODO Can the generator through an error?
        return ElementTree.fromstring(response.content)

    @staticmethod
    def _is_product_available(response_content):
        for stock in response_content.findall('availability/localStore/stock'):
            if stock.find('isSoldInStore') is None or stock.find('availableStock') is None:
                continue
            # Does the product belongs to the store’s portfolio.
            is_in_store = True if stock.find('isSoldInStore').text == 'true' else False
            amount_available = int(stock.find('availableStock').text)
            # Check if the product is available in the stock.
            if is_in_store and amount_available:
                return True
        return False

    @staticmethod
    def _availability_forecast(response_content):
        forecast_dates = {}
        for stock in response_content.findall('availability/localStore/stock'):
            if stock.find('forecasts') is None:
                continue
            forecast_dates = {
                forecast.find('validDate').text: forecast.find('availableStock').text
                for forecast
                in stock.find('forecasts')
            }

        return forecast_dates

    def get_availability_info(self, product_id):
        # TODO Split into operations?
        response_content = self._request_availability_info(product_id)
        if self._is_product_available(response_content):
            return 'Happy to say that the product is available in stock!'
        else:
            # TODO Form a string.
            return self._availability_forecast(response_content)
