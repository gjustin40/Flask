import requests
from bs4 import BeautifulSoup

def get_info(fruit_name):
    page = requests.get('https://en.wikipedia.org/wiki/{}'.format(fruit_name))
    html = page.text
    soup = BeautifulSoup(html, 'html.parser')

    for p in soup.find_all('p'):
        if 'banana' in p.text:
            break
    
    info = p.text
    return info

# print(get_info('banana'))