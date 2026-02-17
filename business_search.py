from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


### PLAN 1: (FETCH THE LINK OF ALL BUSINESSES ON GOOGLE MAPS)

search = input("Say a niche and a city: " )
search = search.replace(" ", "+")
services = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=services) 


driver.get(f"https://www.google.com.br/maps/search/{search}")
time.sleep(5) 

painel = driver.find_element(By.XPATH, '//div[@role="feed"]')

for _ in range(10):
    
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", painel) #simulate a mouse scroll to load all results
    time.sleep(2)

# Get all the articles in the HTML that are the business listing boxes
artigos = driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')

links = []

for artigo in artigos: 
    try:
        link = artigo.find_element(By.TAG_NAME, "a").get_attribute("href") # find the "a" tag and get the href where the links to the business cards are
        links.append(link)
    except:
        pass

for l in links:
    print(l) 


print("Total links:", len(links))  


### PLAN 2: (GET THE INFORMATION FROM EACH CARD AND FILL IN A SPREADSHEET)

# loading....