import requests
from django.conf import settings

def get_services():
    """
    Fetches the list of services from the CloutFlash API.
    """
    url = settings.CLOUTFLASH_API_URL
    params = {
        'key': settings.CLOUTFLASH_API_KEY,
        'action': 'services'
    }
    response = requests.post(url, data=params)
    response.raise_for_status()
    return response.json()

def place_order(service_id, link, quantity, username=None):
    """
    Places an order with the CloutFlash API.
    """
    url = settings.CLOUTFLASH_API_URL
    params = {
        'key': settings.CLOUTFLASH_API_KEY,
        'action': 'add',
        'service': service_id,
        'link': link,
        'quantity': quantity,
    }
    if username:
        params['username'] = username

    response = requests.post(url, data=params)
    response.raise_for_status()
    return response.json()

def get_order_status(order_id):
    """
    Checks the status of an order with the CloutFlash API.
    """
    url = settings.CLOUTFLASH_API_URL
    params = {
        'key': settings.CLOUTFLASH_API_KEY,
        'action': 'status',
        'order': order_id
    }
    response = requests.post(url, data=params)
    response.raise_for_status()
    return response.json()

def get_balance():
    """
    Gets the balance from the CloutFlash API.
    """
    url = settings.CLOUTFLASH_API_URL
    params = {
        'key': settings.CLOUTFLASH_API_KEY,
        'action': 'balance'
    }
    response = requests.post(url, data=params)
    response.raise_for_status()
    return response.json()
