import requests
from bs4 import BeautifulSoup
from time import time, sleep

#Шаг 1
def get_last_news():
    url = 'https://lenta.ru/parts/news/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    }
    responce = requests.get(url=url, headers=headers).text
    with open('data.txt', 'w', encoding='utf-8') as file:
        file.write(responce)
    with open('data.txt', 'w', encoding='utf-8') as file:
        file.write(responce)
    #Шаг 2
    with open('data.txt', encoding='utf-8') as file:
        data = file.read()
    soup = BeautifulSoup(data, 'lxml')
    data_link = soup.find_all(class_='parts-page__item')
    data_list_news = []
    for item in data_link:
        url = 'https://lenta.ru/parts' + item.find('a').get('href')
        try:
            title = item.find('h3').text
        except:
            continue
        data_list_news.append(
            {
                'title': title,
                'url': url
            }
        )
    return data_list_news


def send_last_news(text):
    url = 'https://discord.com/api/v9/channels/949692477248524388/messages'  #чат группы flood
    headers = {'authorization': TOKEN,
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    data = {
        'content': text,
        'nonce': str(int(time())),
        'tts': False
    }
    requests.post(url=url, headers=headers, json=data)


def check_last_news():
    last_news = get_last_news()[0]
    while True:
        sleep(5)
        news = get_last_news()[0]
        if last_news != news:
            text = f"{news['title']}\n{news['url']}"
            send_last_news(text)
            last_news = news


if __name__ == '__main__':
    with open('config.txt', 'r', encoding='utf-8') as fin:
        TOKEN = fin.read().strip()
    check_last_news()