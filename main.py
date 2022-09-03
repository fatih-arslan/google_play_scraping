from google_play_scraper import Sort, reviews
import requests
from bs4 import BeautifulSoup
import re
from googletrans import Translator
import csv

d = {"ı":"i","ç":"c", "¢":"c","ş":"s","ü":"u","ö":"o","ğ":"g", "û":"u", "î":"i", "ô":"o", "ø":"o","ã":"a","ä":"a","å":"a","à":"a","â":"a","á":"a",
     "è":"e","é":"e","ê":"e", "ë":"e", "ì":"i", "í":"i", "ï":"i", "ò":"o", "ó":"o",  "õ":"o", "ù":"u", "ú":"u", "ý":"y", "ÿ":"y","ƒ":"f"
    }

url = "https://play.google.com/store/apps?hl=tr&gl=US"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
apps = soup.findAll("div", {"class": re.compile("^VfPpkd-WsjYwc")})
links = []
for app in apps:
    link_piece_1 = "https://play.google.com"
    link_piece_2 = app.find("a").get("href");
    link = link_piece_1 + link_piece_2
    links.append(link)

links = list(set(links))

comments = []
translator = Translator()
file = open("google_play_review_data6.csv", "w", newline="")
writer = csv.writer(file)
first_line = ["comment", "positivity", "language_key"]
# writer.writerow(first_line)
c = 0
p = 0
n = 0
for link in links:
    link_pieces = link.split("=")
    id = link_pieces[1]
    result = reviews(
        app_id=id,
        lang='tr',  # defaults to 'en'
        country='TR',  # defaults to 'us'
        sort=Sort.MOST_RELEVANT,  # defaults to Sort.NEWEST
        count=1000,  # defaults to 100
        filter_score_with=None  # defaults to None(means all score)
    )
    try:
        l = result[0]
        for j in l:
            content = j["content"].strip().lower()
            score = j["score"]
            if score != 3 and translator.detect(content).lang == "tr":
                for char in content:
                    if not char.isascii():
                        if char in d:
                            content = content.replace(char,d[char])
                        else:
                            content = content.replace(char,"")
                positivity = 1 if score > 3 else 0
                if content != "" and content not in comments:
                    line = [content, positivity, "tr"]
                    #writer.writerow(line)
                    #comments.append(content)

                    print(score)
                    print(c,line)
                    p += positivity
                    n += abs(positivity -1)
                    c += 1
    except Exception as e:
        print(e)


