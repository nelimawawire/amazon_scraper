'''
    Amazon Web Scraper, using selenium and Beautiful Soup

    Created Jan 26th, 2021
    Author: Nelima W

'''

from selenium import webdriver
from bs4 import BeautifulSoup
import csv


def create_webdriver():
    driver = webdriver.Chrome()
    return driver 



def generate_search_url(search_term, page):
    ''' Generate a url from search term, and for each subsequent page'''

    template = 'https://www.amazon.com/s?k={}'
    search_term = search_term.replace(' ', '+')
    base_url = template.format(search_term)
    page_url = base_url + '&page={}'
    if page ==1:
        return base_url
    else:
        return page_url.format(page)




def extract_product_cards(driver):
    ''' Create a soup object containing products'''

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})

    return results



def extract_record_from_product_cards(item):
    '''Extract description, price, rating and rating_count, and return a record'''

    atag = item.h2.a
    #description
    description = atag.text.strip()

    #price
    try:
        price_card = item.find('span', 'a-price')
        price = price_card.find('span', 'a-offscreen').text
    except AttributeError:
        return

    # rating and rating_count
    try:
        rating = item.i.text
        rating_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except:
        rating = ''
        rating_count = ''

    result = (description, price, rating, rating_count)

    return result 


def generate_filename(search_term):
    '''Generate a filename for each search, based on search query'''

    filename = '_'.join(search_term.split(' ')) + '.csv'
    return filename 


def save_data_to_csv(record, filename , new_file=False):
    header = ['description', 'price', 'rating', 'No of Reviews']

    if new_file:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)

    else:
        with open(filename, 'a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(record)



def run(search_term):

    '''
        1. Create a webdriver
        2. Generate a csv file
        3. Generate a search url based on page number
        4. Extract a product card
        5. Extract a record from product card
        6. Save to file
        7. Close the webdriver 

    '''

    driver = create_webdriver()
    filename = generate_filename(search_term)
    save_data_to_csv(None, filename, new_file=True) #Initialize file 

    for page in range(1, 21): #Amazon allows a max of 20 pages
        url = generate_search_url(search_term, page)
        driver.get(url.format(page))
        cards = extract_product_cards(driver)
        

    for card in cards:
        record = extract_record_from_product_cards(card)
        if record:
            save_data_to_csv(record, filename)

    driver.close()


if __name__ == '__main__':
    search_query = 'fruity fragrances for women'
    run(search_query)





