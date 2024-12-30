from datetime import datetime
import requests
import csv
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}

def get_page_html(url):
    try:
        res = requests.get(url=url, headers=REQUEST_HEADER)
        res.raise_for_status()  # Memastikan tidak ada error HTTP
        return res.text
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def get_product_title(soup):
    product_title = soup.find('span', id='productTitle')
    if product_title:
        return product_title.text.strip()
    return "Product title not found"

def extract_product_info(url):
    product_info = {}
    print(f'Scrapping URL: {url}')
    html = get_page_html(url=url)
    if not html:
        return None
    soup = BeautifulSoup(html, 'lxml')
    product_info['Nama barang'] = get_product_title(soup)
    return product_info

if __name__ == '__main__':
    try:
        with open('product_amazon.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                url = row[0]
                product_info = extract_product_info(url)
                if product_info:
                    print(product_info)
    except FileNotFoundError:
        print("File 'product_amazon.csv' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
