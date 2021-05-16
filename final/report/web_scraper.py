import request
from bs4 import BeautifulSoup

def scraper(super_page,
            url_locator,
            url_prefix,
            sub_locator,
            super_unwanted=0,
            sub_unwanted=0,
            ):
    """
    super_page : URL to the main web page.
    url_locator : name of HTML class containing the URLs to the subpages.
    url_prefix : URL to main web domaine.
    sub_locator : name of HTML class in sub page containing the text to extract.
    super_unwanted : class in the main web page that isn't preferable to scrape.
    sub_unwated : classes in sub web page that isn't preferable to scrape.
    """

    # Create a .txt file for the scraped text:
    text_file = open('articles.txt', 'w', encoding='utf-8')

    # Iterating trough the list of pages:
    for i in range(1, 21):
        page = requests.get(super_page)
        # Create a BeautifulSoup object:
        soup = BeautifulSoup(page.text, 'html.parser')

        # Remove unwanted class:
        if super_unwanted != 0:
            unwanted = soup.find(class_ = super_unwanted)
            unwanted.extract()

        # Create a list for the URLs of the scientific articles on the current
        # page:
        url_list = []

        # Filling in all the URLs from the webpage.
        for url in soup.find(class_=url_locator).find_all('a'):
            url_ = url.get('href')
            if url_ == None:
                pass
            # If the URL does not start with 'http', we add the main web domain:
            elif url_[0:5] != 'http':
                url_list.append(url_prefix + url_)
            # If a URL already has a full URL, append it right to the list:
            else:
                url_list.append(url_)

        # Enumerationg trough all the url's, extracting the text.
        for j, url in enumerate(url_list):
            # Counter, to se the progress:
            print(f'{i+1} : {j+1}/{len(url_list)}')

            pagepage = requests.get(url)
            soup1 = BeautifulSoup(pagepage.text, 'html.parser')

            # Remove unwanted classes
            if sub_unwanted != 0:
                if len(sub_unwanted) != 1:
                    for unwanted in sub_unwanted:
                        soup1.find(class_ = unwanted).extract()
                else:
                    soup1.find(class_ = unwanted).extract()

            # Find all the classes containing the preferred text:
            content = soup1.find_all('div', class_ = sub_locator)

            # Extract the text and write in to the .txt file.
            # Every sentence is placed on a new line.
            for element in content:
                for sentence in element.text.split(". "):
                    # Check whether sentence only contains whitespace.
                    if sentence.isspace() == False or not not sentence:
                    # .strip is to remove whitespace at both edges.
                        text_file.write(sentence.strip() + '.\n')

    print('Finished')
    text_file.close()
    return text_file


if __name__ == '__main__':
    url = 'https://www.nature.com/subjects/climate-change/srep?searchType=journalSearch&sort=PubDate&page=2'
    url_locator = 'ma0 mb-negative-2 clean-list'
    url_prefix = 'https://www.nature.com'
    sub_unwanted_ = ['c-article-references', 'c-bibliographic-information']
    sub_locator = 'c-article-section__content'
    text_file = scraper(url, url_locator, url_prefix, sub_locator, sub_unwanted = sub_unwanted_)
