from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


### PLAN 1: (FETCH THE LINK OF ALL BUSINESSES ON GOOGLE MAPS)
@ -16,21 +19,21 @@ driver = webdriver.Chrome(service=services)
driver.get(f"https://www.google.com.br/maps/search/{search}")
time.sleep(5) 

painel = driver.find_element(By.XPATH, '//div[@role="feed"]')
panel = driver.find_element(By.XPATH, '//div[@role="feed"]')

for _ in range(10):
    
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", painel) #simulate a mouse scroll to load all results
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", panel) #simulate a mouse scroll to load all results
    time.sleep(2)

# Get all the articles in the HTML that are the business listing boxes
artigos = driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')
articles = driver.find_elements(By.CSS_SELECTOR, 'div[role="article"]')

links = []

for artigo in artigos: 
for article in articles: 
    try:
        link = artigo.find_element(By.TAG_NAME, "a").get_attribute("href") # find the "a" tag and get the href where the links to the business cards are
        link = article.find_element(By.TAG_NAME, "a").get_attribute("href") # find the "a" tag and get the href where the links to the business cards are
        links.append(link)
    except:
        pass
@ -40,8 +43,70 @@ for l in links:


print("Total links:", len(links))  

wait = WebDriverWait(driver, 10)

### PLAN 2: (GET THE INFORMATION FROM EACH CARD AND FILL IN A SPREADSHEET)

# loading....
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

                enviar = requests.post("https://teste-n8n.rcjgun.easypanel.host/webhook/e36ed4a3-7f13-411c-a8df-40dce34dd244",
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




