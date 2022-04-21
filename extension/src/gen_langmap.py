# get html of https://en.wikipedia.org/wiki/List_of_Wikipedias
import requests
response = requests.get("https://en.wikipedia.org/wiki/List_of_Wikipedias")
html = response.text


# parse html
import bs4
soup = bs4.BeautifulSoup(html, "html.parser")

# get table
tables = soup.find_all("table")
tables = [table for table in tables if table.find("caption")]
tables = [table for table in tables if table.find("caption").text == "Details of Wikipedia editions"]
table = tables[0]

# get rows
body = table.find("tbody")
rows = body.find_all("tr")[1:] # except header

langs = {}
for row in rows:
    lang = row.find("th").find("a").text
    code = row.find_all("td")[1].text
    langs[code] = lang

# save to json
import json
with open("languages.json", "w", encoding='utf-8') as f:
    json.dump(langs, f, ensure_ascii=False, indent=4)
