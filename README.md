# selectolaxpath
XPATH for Selectolax, specifically designed to be plug-and-pay with playwright

Example:
'''
from selectolax_functions import find_element_by_xpath, find_elements_by_xpath, find_element_by_css

async def get_balances(html):
    html = psource
    coinbal = D(find_element_by_xpath(html, '//*[@id=\"balance\"]/b[1]').text(strip=True))
    fiatbal = D(find_element_by_xpath(html, '//*[@id=\"balance\"]/b[2]').text(strip=True))
    return dict(coinbal=coinbal, fiatbal=fiatbal)
'''
