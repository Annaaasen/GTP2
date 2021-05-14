def scraper(super_page,
            url_locator,
            url_prefix,
            sub_locator,
            super_unwanted=0,
            sub_unwanted=0,
            ):
    """
    super_page : super pages.
    url_locator : name of class containing the url's

    """
    text_file = open('articles.txt', 'w', encoding='utf-8')

    for i in range(1, 21):
        # Collect first page of artists’ list
        page = requests.get(super_page)

        # Create a BeautifulSoup object
        soup = BeautifulSoup(page.text, 'html.parser')

        """
        f = csv.writer(open('test.csv', 'w'))
        f.writerow(['Name', 'Link'])
        """

        # Remove unwanted class
        if super_unwanted != 0:
            unwanted = soup.find(class_ = super_unwanted)
            unwanted.extract()

        url_list = []

        # Filling in all the url's from the webpage.
        for url in soup.find(class_=url_locator).find_all('a'):
            url_ = url.get('href')
            if url_ == None:
                pass
            elif url_[0:5] != 'http':
                url_list.append(url_prefix + url_)
            else:
                url_list.append(url_)

        # Enumerationg trough all the url's, extracting the text.
        for j, url in enumerate(url_list):
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

            """ For one apperant strange reason, we must use a different code below than
            that we used earlies. Why? I do not know! """

            content = soup1.find_all('div', class_ = sub_locator)

            for element in content:
                for sentence in element.text.split(". "):
                    # Check whether sentence only contains whitespace.
                    if sentence.isspace() == False or not not sentence:
                    # .strip is to remove whitespace at both edges.
                        text_file.write(sentence.strip() + '.\n')
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
    return text_file
