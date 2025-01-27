import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSeYaVm4UYiTXzdDLaxcSX1xk2PWGRqD8ksQf0yeL6Q-hCtTkg/viewform?usp=sf_link'
zillow_clone_url = 'https://appbrewery.github.io/Zillow-Clone/'

response = requests.get(zillow_clone_url)
yc_web_page = response.text
soup = BeautifulSoup(yc_web_page, 'html.parser')

prices = soup.find_all(name= 'span', class_= 'PropertyCardWrapper__StyledPriceLine')
price_list_unfinished = [price.getText().strip() for price in prices]
price_list = []

for price in price_list_unfinished:
    cleaned_price = price.split('+')[0]
    cleaned_price = cleaned_price.split(' ')[0]
    cleaned_price = cleaned_price.split('/')[0]
    price_list.append(cleaned_price)
    
addresses = soup.find_all(name= 'address')
address_list = [adr.getText().strip() for adr in addresses]
    
links = soup.find_all(class_= 'property-card-link')
link_list = [link['href'] for link in links]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options= chrome_options)
driver.get(form_url)

for p, a, l in zip(price_list, address_list, link_list):
    addr_inp = driver.find_element(By.XPATH, value= '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(2)
    addr_inp.send_keys(a)

    price_inp = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_inp.send_keys(p)

    link_inp = driver.find_element(By.XPATH, value= '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_inp.send_keys(l)

    submit_button = driver.find_element(By.XPATH, value= '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
    time.sleep(1)
    another_button = driver.find_element(By.XPATH, value= '/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()
driver.quit()