import requests
from bs4 import BeautifulSoup
from time import time

urls = [
    "http://www.lounaat.info/lounas/amica-tellus/helsinki",
    "http://www.por.fi/Menu-Pitajanmaki",
    "http://eatwork.fi/tilat/valimotie-27/",
    "http://www.ravintolafactory.com/lounasravintolat/ravintolat/helsinki-pitajanmaki/",
    "http://www.ravintolablancco.com/lounas-ravintolat/pitajanmaki/",
    "http://www.smarteat.fi/menu-pitskun-kanttiini/",
    "http://www.lounaat.info/lounas/amica-lasihelmi/helsinki",
]


def parse(html_txt):
    soup = BeautifulSoup(html_txt, 'html.parser')
    return soup.get_text()


def main():
    for url in urls:
        # print (url)
        # print(requests.get(url))
        resp = requests.get(url)
        print(resp.status_code)
        text = parse(resp.text)
        with open("test.txt", 'a', encoding='utf-8') as f:
            f.write(text)


main()
