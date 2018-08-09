import requests
import os
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime as dt
from datetime import timedelta
from slackclient import SlackClient

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)
urls = {
    'Amica Tellus': "https://www.lounaat.info/lounas/amica-tellus/helsinki",
    # 'POR': "http://www.por.fi/Menu-Pitajanmaki",
    'Theron': "https://www.lounaat.info/lounas/theron-catering-pitjnmki/helsinki",
    # 'Factory': "http://www.ravintolafactory.com/lounasravintolat/ravintolat/helsinki-pitajanmaki/",
    'Blancco': "https://www.lounaat.info/lounas/blancco-pitajanmaki/helsinki",
    'Smarteat': "https://www.lounaat.info/lounas/smarteat-pitsku/helsinki",
    'Amica Lasihelmi': "https://www.lounaat.info/lounas/amica-lasihelmi/helsinki",
    'Sodexo Atomitie': "https://www.lounaat.info/lounas/sodexo-atomitie/helsinki",
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
    try:
        amica_tags = SoupStrainer(id='menu')
        tag = amica_tags        # Default to lounaat.info
        if (restaurant == 'POR'):
            por_tags = SoupStrainer(id='Printable')
            tag = por_tags
        elif (restaurant == 'Factory'):
            # Load whole page since Factory has no good ids to parse into
            soup = BeautifulSoup(html_txt, 'html.parser')
            # Find parent of lounaslista text, which holds whole week in multiple <p>'s (*sigh :( )
            s = soup.find(lambda tag: tag.name == "h2" and tag.text.lower().startswith("lounaslista")).parent.text
            # Find today and tomorrow from the huge string which has whole week lunch and some bloat text
            s = (s[s.lower().find(weekday) + len(weekday):s.lower().find(WEEKDAYS[(dt.today() + timedelta(days=1)).weekday()])])
            # Get rid of date text that is following the weekday and return the text
            s = (s[s.find("\n") + len("\n"):])
            return s
        else:       # lounaat.info parse
            soup = BeautifulSoup(html_txt, 'html.parser', parse_only=tag)
            raw_html = soup.find(lambda tag: tag.name == "h3" and tag.text.lower().startswith(weekday)).parent.parent
            lst = []
            for elem in raw_html.find_all("p"):
                lst.append(" ".join(elem.text.split()))
            return '\n'.join(lst)
    except Exception:
        return ""       # Default failed parse


def main():
    wd = weekday_str()
    # print(wd)
    for (restaurant, url) in urls.items():
        resp = requests.get(url)
        print("{0}: {1}".format(restaurant, resp.status_code))
        text = parse(resp.text, wd, restaurant)
        # with open("test.html", 'a', encoding='utf-8') as f:
        #     f.write(text)
        bolded_header = "*{0}:*\n".format(restaurant)
        sc.api_call(
            "chat.postMessage",
            channel="CAXPL9EUR",
            text=bolded_header + text,
        )


main()
