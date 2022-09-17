import requests
from bs4 import BeautifulSoup

url = 'https://parascrapear.com/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

blockquote_item = soup.find_all('blockquote')

for item in blockquote_item:
    autor = item.get(class_='author').text
    frase = item.find('q').text
    categoria = item.find(class_='cat').text

    print(autor, frase, categoria)
