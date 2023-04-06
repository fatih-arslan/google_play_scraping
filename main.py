from google_play_scraper import Sort, reviews
import requests
from bs4 import BeautifulSoup
import re
from googletrans import Translator
import csv

chars_to_replace = {"ı": "i", "ç": "c", "¢": "c", "ş": "s", "ü": "u", "ö": "o", "ğ": "g",
                    "û": "u", "î": "i", "ô": "o", "ø": "o", "ã": "a", "ä": "a", "å": "a", "à":
                    "a", "â": "a", "á": "a","è": "e", "é": "e", "ê": "e", "ë": "e", "ì":
                    "i", "í": "i", "ï": "i", "ò": "o", "ó": "o",  "õ": "o", "ù": "u", "ú": "u", ""
                    "ý": "y", "ÿ": "y", "ƒ": "f"
                    }

url = "https://play.google.com/store/apps?hl=tr&gl=US"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
apps = soup.findAll("div", {"class": re.compile("^VfPpkd-WsjYwc")})

links = []
for app in apps:
    link_piece_1 = "https://play.google.com"
    link_piece_2 = app.find("a").get("href")
    link = link_piece_1 + link_piece_2
    links.append(link)

links = list(set(links))

comments = []
translator = Translator()
#file = open("google_play_review_data6.csv", "w", newline="")
#writer = csv.writer(file)
first_line = ["comment", "positivity", "language_key"]
# writer.writerow(first_line)
comment_count = 0
positive_count = 0
negative_count = 0
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
        extracted_data = result[0]
        for data in extracted_data:
            print("new data")
            content = data["content"].strip().lower()
            score = data["score"]
            if score != 3 and translator.detect(content).lang == "tr":
                print(content)
                for char in content:
                    if not char.isascii():
                        if char in chars_to_replace:
                            content = content.replace(char, chars_to_replace[char])
                            print("non-ascii char replaced")
                        else:
                            content = content.replace(char, "")
                            print("non-ascii char removed")
                positivity = 1 if score > 3 else 0
                if content != "" and content not in comments:
                    line = [content, positivity, "tr"]
                    print(content)
                    #writer.writerow(line)
                    #comments.append(content)

                    print(score)
                    print(comment_count,line)
                    positive_count += positivity
                    negative_count += abs(positivity -1)
                    comment_count += 1
    except Exception as e:
        print(f"exception: {e}")


