# Import libraries
import requests
import csv
from bs4 import BeautifulSoup

text_file = open('articles.txt', 'w', encoding='utf-8')
print('Start')

for i in range(1, 21):
    # Collect first page of artists’ list
    page = requests.get(f'https://www.nature.com/subjects/climate-change/srep?searchType=journalSearch&sort=PubDate&page={i}')

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
    for j, artist_name in enumerate(artist_name_list_items):
        print(f'{i}/{j}/{len(artist_name_list_items)}')
        links = 'https://www.nature.com' + artist_name.get('href')

        # Do the whole thing again, this time with each URL
        pagepage = requests.get(links)
        soup1 = BeautifulSoup(pagepage.text, 'html.parser')
        # last_links = soup1.a
        # print(last_links)
        # last_links.decompose()
        unwanted = soup1.find(class_ = 'c-article-references')
        unwanted.extract()
        unwanted = soup1.find(class_ = 'c-bibliographic-information')
        unwanted.extract()
        # unwanted = soup1.find(clanss_ = 'c-article-section')
        unwanted.extract()
        # content = soup1.find(class_ ='c-article-section__content')
        content = soup1.find_all('div', class_ = 'c-article-section__content')
        """
        content = soup1.find(class_='c-article-section__content')
        """
        # content = soup1.select('div[class="p"]')
        # content_items = content.find_all('div[class="p"]')
        # content_items = content.find_all('p')
        # print(content_items)
        for element in content:
            text_file.write(element.text)
            """
            file = content.text
            print(file)
            text_file.write(content.text)
            """

            """
            with open('articles.txt','r+', encoding='utf-8') as file:
                for line in file:
                    if not line.isspace():
                        file.write(line)
                        """

print('Finished')
text_file.close()
