from random import randint
from time import sleep
from datetime import datetime
import requests


def scrape_data():
    current_time = datetime.now()
    current_timestamp = current_time.strftime('%d-%m-%Y-%H_%M_%S')
    url = "https://tnreginet.gov.in/portal/SimpleCaptcha"
    res = requests.get(url, stream=True)
    with open('data/src/image_{}.png'.format(current_timestamp), 'wb') as f:
        for chunk in res.iter_content():
            f.write(chunk)
    return res


def collect_data(n=1000):
    for i in range(n):
        res = scrape_data()
        print('count: {}, status: {}'.format(i, res.status_code))
        sleep(randint(2, 7))


if __name__ == '__main__':
    collect_data()
