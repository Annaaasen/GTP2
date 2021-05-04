# Import libraries
import requests
import csv
from bs4 import BeautifulSoup

# Collect first page of artists’ list
page = requests.get('https://www.nature.com/subjects/climate-change/srep?searchType=journalSearch&sort=PubDate&page=1')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

f = csv.writer(open('test.csv', 'w'))
f.writerow(['Name', 'Link'])

# Pull all text from the BodyText div
# artist_name_list = soup.find(class_='u-container u-mt-32 u-mb-32 u-clearfix')
#artist_name_list = soup.find(class_='container cleared container-type-article-list')
artist_name_list = soup.find(class_='ma0 mb-negative-2 clean-list')

# Pull text from all instances of <a> tag within BodyText div
artist_name_list_items = artist_name_list.find_all('a')

# Create for loop to print out all artists' names
for artist_name in artist_name_list_items:
    links = 'https://www.nature.com' + artist_name.get('href')

    # Do the whole thing again, this time with each URL
    pagepage = requests.get(links)
    soup1 = BeautifulSoup(pagepage.text, 'html.parser')
    last_links = soup1.a
    # print(last_links)
    last_links.decompose()
    content = soup1.find(class_='c-article-body')
    # content = soup1.select('div[class="p"]')
    content_items = content.find_all('div[class="p"]')
    print(content_items)
