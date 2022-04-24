import csv
import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
import time

ua = UserAgent()
cur_time = datetime.now().strftime('%d_%m_%Y_%H_%M')


def get_html(url):
    headers = {
        'User Agent': ua.random,
        'accept': 'application/json, text/plain, */*'
    }

    res = requests.get(url=url, headers=headers)

    return res.text


def get_pages_counts(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pages_counts = soup.find(
        'ul', class_='pagination').find_all('li')[-2].text.strip()
    return int(pages_counts)


def make_json(data):
    with open(f'{cur_time}.json', 'a', encoding='utf8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)    


def main():
    with open(f'{cur_time}.csv', 'a', encoding='utf8') as t:
        writer = csv.writer(t)
        writer.writerow((
            "Название монеты", 
            "Тикер",
            "Ссылка",
            "Цена"
        ))
    
    time_start = time.time()
    start_url = 'https://coinmarketcap.com/?page=1'
    pages_counts = get_pages_counts(start_url)
    json_data = []
    for i in range(1, pages_counts + 1):
        url = f'https://coinmarketcap.com/?page={i}'
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        trs = soup.find('tbody')

        for tr in trs:
            tds = tr.find_all('td')
            try:
                link = 'https://coinmarketcap.com' + tds[2].find('a').get(
                    'href').strip()
            except:
                link = ''
            if tr.get('class') is None:
                try:
                    coin_name = tds[2].find('a').find(
                        'p', class_='iworPT').text.strip()
                except:
                    coin_name = ''
                try:
                    link = 'https://coinmarketcap.com' + tds[2].find('a').get(
                        'href').strip()
                except:
                    link = ''
                try:
                    ticker = tds[2].find('a').find(
                        'p', class_='coin-item-symbol').text.strip()
                except:
                    ticker = ''
                try:
                    img = tds[2].find('a').find('img').get('src').strip()
                except:
                    img = ''
                try:
                    symbols = [',', '$']
                    price = tds[3].find('div').text.strip()
                    for symbol in symbols:
                        price = price.replace(symbol, '')
                except:
                    price = ''
            else:
                try:
                    coin_name = tds[2].find('a').find_all(
                        'span')[1].text.strip()
                except:
                    coin_name = ''
                try:
                    ticker = tds[2].find('a').find_all('span')[2].text.strip()
                except:
                    coin_name = ''
                try:
                    symbols = [',', '$']
                    price = tds[3].find('span').text.strip()
                    for symbol in symbols:
                        price = price.replace(symbol, '')
                except:
                    price = ''
            data = {
                'coin_name': coin_name,
                'ticker': ticker,
                'link': link,
                'price': price
            }
            json_data.append(data)
            with open(f'{cur_time}.csv', 'a', encoding='utf8') as t:
                writer = csv.writer(t)
                writer.writerow((
                    coin_name, 
                    ticker,
                    link,
                    price
                ))
        print(f'[PROGRESS] {i}/{pages_counts}')
    make_json(json_data)
    print(f'Время выполнения скрипта: {time.time() - time_start}')


if __name__ == '__main__':
    main()