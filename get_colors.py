from bs4 import BeautifulSoup
import requests
import json

url = 'https://colorscheme.ru/color-names.html'
page = requests.get(url)
print(page.status_code)

soup = BeautifulSoup(page.text, 'html.parser')

list_0 = soup.findAll('td')

names = list_0[1::6]

for i in range(len(names)):
  names[i] = str(names[i])[4::][:-5:]

slots = list_0[::6]

for i in range(len(slots)):
  slots[i] = str(slots[i])[13::][:-7:]

dictionary = dict(zip(slots, names))

with open("color_names.json", 'w') as file:
        json.dump(dictionary, file, indent = 4)
