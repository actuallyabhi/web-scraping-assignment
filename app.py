from bs4 import BeautifulSoup
import pandas as pd 
import requests
import random
import time

BASE_URL = "https://www.amazon.in/s?k=bags"
HEADERS =  ({
    'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"
})

# scraper function
def scrape_catalogue(page):
    try:
        # send the http request 
        res = requests.get(f"{BASE_URL}&page={page}", headers=HEADERS)
        print(f"Request status code for page {page}: {res.status_code}")
        if (res.status_code != 200):
            print("Error loading webpage, Error code=",res.status_code)
            return
        # parse the html content
        soup = BeautifulSoup(res.content, 'html.parser')
        # get all product rows
        rows = soup.find_all('div',class_='sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16')

        # Select the product details section
        data_sections = []
        for x in rows:
            row_data = x.select('.s-list-col-right > .sg-col-inner > .a-section.a-spacing-small.a-spacing-top-small')
            if (len(row_data) > 0):
                prod_data = {}
                prod_data["url"]= row_data[0].find('a')['href'].split("ref=")[0]
                prod_data["name"] = row_data[0].select(".a-size-medium.a-color-base.a-text-normal")[0].text
                prod_data["price"]= row_data[0].find('span', class_="a-price-whole").text
                ratings = row_data[0].find('div', class_="a-row a-size-small")
                if ratings is not None:
                    prod_data["rating"] =  ratings.find('span', class_="a-icon-alt").text.split(" ")[0]
                    prod_data["number_of_reviews"] = ratings.find('span', class_="a-size-base").text
                else:
                    prod_data[ratings] = '0'
                    prod_data["number_of_reviews"] = '0'
                data_sections.append(prod_data)
        # convert the json to csv and append it the file
        df = pd.DataFrame(data_sections)
        df.to_csv('amazon_products_listing.csv', mode='a', header=False, index=False)
        print(f"Page {page} scraped successfully")
    except Exception as e:
        print(e)
        print(f"Some error occured while scraping page {page}")
        return
      

def random_delay(upper_bound = 30):
    delay = random.randint(20,upper_bound)
    time.sleep(delay)


if __name__ == "__main__":
    for page in range(8, 21):
        scrape_catalogue(page)
        random_delay()
    print("Scraping completed")