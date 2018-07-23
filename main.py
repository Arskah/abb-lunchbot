import requests
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime as dt

# all_tags = SoupStrainer(id=['menu', 'Printable', 'after_section_1', 'page-42', 'textwidget'])
amica_tags = SoupStrainer(id='menu')
por_tags = SoupStrainer(id='Printable')
theron_tags = SoupStrainer(id='after_section_1')
factory_tags = SoupStrainer(id='lounaslista') # Fix
blancco_tags = SoupStrainer(id='page-42')     # Fix
smarteat_tags = SoupStrainer(id='textwidget') # Fix



urls = {
    'Amica Tellus': "http://www.lounaat.info/lounas/amica-tellus/helsinki",
    'POR': "http://www.por.fi/Menu-Pitajanmaki",
    'Theron': "http://eatwork.fi/tilat/valimotie-27/",
    'Factory': "http://www.ravintolafactory.com/lounasravintolat/ravintolat/helsinki-pitajanmaki/",
    'Blancco': "http://www.ravintolablancco.com/lounas-ravintolat/pitajanmaki/",
    'Smarteat': "http://www.smarteat.fi/menu-pitskun-kanttiini/",
    'Amica Lasihelmi': "http://www.lounaat.info/lounas/amica-lasihelmi/helsinki",
}

WEEKDAYS = [
    "maanantai",
    "tiistai",
    "keskiviikko",
    "torstai",
    "perjantai",
    "lauantai",
    "sunnuntai"
]


def weekday_str():
    return WEEKDAYS[dt.today().weekday()]


def parse(html_txt, weekday, restaurant):
    tag = amica_tags        # Default to lounaat.info
    if (restaurant == 'POR'):
        tag = por_tags
    elif (restaurant == 'Theron'):
        tag = theron_tags
    elif (restaurant == 'Factory'):
        tag = factory_tags
    elif (restaurant == 'Blancco'):
        tag = blancco_tags
    elif (restaurant == 'Smarteat'):
        tag = smarteat_tags
    soup = BeautifulSoup(html_txt, 'html.parser', parse_only=tag)
    return soup.prettify()


def main():
    wd = weekday_str()
    print(wd)
    for (name, url) in urls.items():
        resp = requests.get(url)
        print("{0}: {1}".format(name, resp.status_code))
        text = parse(resp.text, wd, name)
        # print(text)
        with open("test.html", 'a', encoding='utf-8') as f:
            f.write(text)


main()
