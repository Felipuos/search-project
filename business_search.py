from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


### PLAN 1: (FETCH THE LINK OF ALL BUSINESSES ON GOOGLE MAPS)

search = input("Say a niche and a city: " )
webhook = input("provide a webhook to receive the information: ")
search = search.replace(" ", "+")
services = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=services) 

driver.get(f"https://www.google.com.br/maps/search/{search}")
time.sleep(5) 

panel = driver.find_element(By.XPATH, '//div[@role="feed"]')

for _ in range(10):
    
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", panel) #simulate a mouse scroll to load all results
    time.sleep(2)

# Get all the articles in the HTML that are the business listing boxes
articles = driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')

links = []

for article in articles: 
    try:
        link = article.find_element(By.TAG_NAME, "a").get_attribute("href") # find the "a" tag and get the href where the links to the business cards are
        links.append(link)
    except:
        pass

for l in links:
    print(l) 


print("Total links:", len(links))  
wait = WebDriverWait(driver, 10)

### PLAN 2: (GET THE INFORMATION FROM EACH CARD AND FILL IN A SPREADSHEET)

for l in links:
        try:
                driver.get(l)
                name = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//h1[contains(@class,"DUwDvf")]')
                    )
                ).text

                # time = wait.until(
                #         EC.presence_of_element_located(
                #             (By.XPATH, '//li[contains(@class,"G8aQO")]')
                #             )
                #         ).text

                outline = driver.find_elements(By.XPATH, '//span[@role="img"]')
                assessment = None
                for e in outline:
                    texts = e.get_attribute("aria-label")
                    if not texts:
                        continue
                    if "," in texts:
                        assessment = texts

                blocks = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//div[contains(@class,"rogA2c")]')
                    )
                )

                address = None
                contact = None
                for block in blocks:
                    texts = block.text.strip()
                    if texts.startswith("-") or texts.startswith("(") or texts.startswith("+"):
                        contact = texts

                    elif():
                        address = texts

                print(f"name: {name}")
                print(f"address: {address}")
                print(f"contact: {contact}")
                print(f'assessment: {assessment}')

                post = requests.post(webhook,
                                       json= {
                                           "name":name,
                                           "address":address,
                                           "contact":contact,
                                           "assessment":assessment
                                       }
                                       
                                       
                                       )
        except Exception as e:
            print("Unexpected error in the main process:", e)
            print("Error captured:", e)





