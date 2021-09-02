from selenium import webdriver

DIRECTORY = 'reports'
NAME = 'PS4'
CURRENCY = '(u"\N{euro sign}")'
MIN_PRICE = '275'
MAX_PRICE = '650'
FILTERS = {
    'min' : MIN_PRICE,
    'max' : MAX_PRICE
}

BASE_URL = "http://www.amazon.de/"

def get_chrome_web_driver(options):
    return  webdriver.Chrome('./chromedriver.exe',chrome_options=options)  #theres a fx which will be just getting us the actual web driver, so here 1st v imported selenium webdriver n then v r returning webdriver,chrome which is our actual chrome n v have to specify our path to it

def get_web_driver_options():
    return  webdriver.ChromeOptions()

def set_ignore_certificate_error(options):              #1
    options.add_argument('--ignore-certificate-error')   #this 2 fxs  are options to our chrome driver, basically these are kind off deflect , so when v run our browser v deflect ignore certificate errors n also v run it in incognito

def set_browser_as_incognito(options):                 #2
    options.add_argument('--incognito')


