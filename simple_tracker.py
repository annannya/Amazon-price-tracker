import time

from  main import (
get_web_driver_options,
get_chrome_web_driver,
set_ignore_certificate_error,
set_browser_as_incognito,
NAME,
CURRENCY,
FILTERS,
BASE_URL,
DIRECTORY
)
from  selenium.webdriver.common.keys import Keys
import  time

class GenerateReport:
    def __init__(self):
        pass

class AmazonAPI:
    def __init__(self,search_term,filters,base_url,currency):
        self.base_url = base_url
        self.search_term = search_term
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        print("Starting script...........")
        print(f"Looking for {self.search_term} products....")
        links = self.get_products_links()

        #time.sleep(1)
        if not links:
            print("Stopped script.")
            return
        print(f"Got {len(links)} links to products....")  #v got the links v can print the len of the links, this will show us how many links v get
        print("Getting info about products...")
        products = self.get_products_info(links)
        print(f"Got info about{len(products)} products..")
        self.driver.quit()
        return products

    def get_products_info(self, links ):      #this 3 fxs r for clearing the link's url from extra info
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)
            if product:
                products.append(product)
            return products

    def get_single_product_info(self,asin):
        print(f"Product ID: {asin} - getting data...")
        product_sort_url = self.shorten_url(asin)
        self.driver.get(f'{product_sort_url}?language=en_GB')
        time.sleep(2)
        title = self.get_title()   #v'll be getting this 3 things
        seller = self.get_seller()
        price = self.get_price()
        if title and seller and price:
            product_info = {
                'asin': asin,
                'url': product_sort_url,
                'title': title,
                'seller': seller,
                'price': price
            }
            return product_info
        return None

    def get_title(self):
        try:
            return  self.driver.find_element_by_id('productTitle').text
        except Exception as e:
            print(e)
            print(f"Can't get title of a product - {self.driver.current_url}")
            return  None

    def get_seller(self):
        try:
            return self.driver.find_element_by_id('bylineInfo').text
        except Exception as e:
            print(e)
            print(f"Can't get seller of a product - {self.driver.current_url} ")
            return None

    def get_price(self):
        price = None
        try:
            price = self.driver.find_element_by_id('priceblock_ourprice').text
            price = self.convert_price(price)
        except NoSuchElementException:
            try:
                availability = self.driver.find_element_by_id('availability').text
                if 'Available' in availability:
                    price = self.driver.find_element_by_class_name('olp-padding-right').text
                    price = price[price.find(self.currency):]
                    price = self.convert_price(price)
            except Exception as e:
                print(e)
                print(f"Can't get price of a product - {self.driver.current_url}")
                return None
        except Exception as e:
            print(e)
            print(f"Can't get price of a product - {self.driver.current_url}")
            return None
        return price


    def shorten_url(self,asin):
        return self.base_url + 'dp/' + asin  #this will remove the product name

    def get_asins(self, links):
        return [self.get_asin(links) for link in links]

    def get_asin(self,product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]


    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')#v r using //* bcoz this is one of the way to locate elements using xpath s
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(2)  #wait to load the pg
        self.driver.get(f'{self.driver.current_url}{self.price_filter}') #so basically this fx will just clear up our URL, we'll just put our current url, its a fx from the driver
        print(f"Our url:{self.driver.current_url}")
        time.sleep(2)  # wait to load the pg
        result_list = self.driver.find_element_by_class_name('s-result-list')

        links = [1000]
        try:
            results = result_list[0].find_elements_by_xpath(
              "//div[1]/div[1]/div/span[3]/div[2]/div[2]/div/span/div/div/div[2]/div[2]/div/div/div[1]/h2/a")
            links = [links.get_attribute("href") for link in results]

            return links
        except Exception as e:
            print("Didn't get any products....")
            print(e)
            return links
#noe v r going to get all the details from the products

if __name__ =='__main__':
     print("Hey!!")
     amazon = AmazonAPI(NAME, FILTERS, BASE_URL,CURRENCY)
     amazon.run()
