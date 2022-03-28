import time
from pprint import pprint

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests

GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSdncv2Pgepfev4dFfWoyzpnUZHSVxmJMUeqK4qFZlIIPzSohw/viewform" \
              "?usp=sf_link "
ZILLOW_URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B"pagination"%3A%7B%7D%2C' \
             '"usersSearchTerm"%3Anull%2C"mapBounds"%3A%7B"west"%3A-122.56276167822266%2C"east"%3A-122.30389632177734' \
             '%2C"south"%3A37.69261345230467%2C"north"%3A37.857877098316834%7D%2C"isMapVisible"%3Atrue%2C"filterState' \
             '"%3A%7B"fr"%3A%7B"value"%3Atrue%7D%2C"fsba"%3A%7B"value"%3Afalse%7D%2C"fsbo"%3A%7B"value"%3Afalse%7D%2C' \
             '"nc"%3A%7B"value"%3Afalse%7D%2C"cmsn"%3A%7B"value"%3Afalse%7D%2C"auc"%3A%7B"value"%3Afalse%7D%2C"fore' \
             '"%3A%7B"value"%3Afalse%7D%2C"pmf"%3A%7B"value"%3Afalse%7D%2C"pf"%3A%7B"value"%3Afalse%7D%2C"mp"%3A%7B' \
             '"max"%3A3000%7D%2C"price"%3A%7B"max"%3A872627%7D%2C"beds"%3A%7B"min"%3A1%7D%7D%2C"isListVisible"%3Atrue' \
             '%2C"mapZoom"%3A12%7D '

chrome_driver_location = "C:\chromedriver_win32\chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_location)

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.42",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url=ZILLOW_URL, headers=header)
contents = response.text

soup = BeautifulSoup(contents, "html.parser")

prices = soup.findAll(name="div", class_="list-card-price")
monthly_prices = [price.text for price in prices]
# price contains /mo and some others contain + . get rid of both
all_prices = [price.split("/")[0] if "/" in price else price.split("+")[0] for price in monthly_prices]

addresses = soup.select(selector="address", class_="list-card-address")
all_addresses = [address.text for address in addresses]

links = soup.select(".list-card-top a")
all_links = [link["href"] for link in links]

# enter all data in the google form and submit
for i in range(len(all_addresses)):
    driver.get(url=GOOGLE_FORM)
    time.sleep(3)

    first_input = driver.find_element(By.CSS_SELECTOR, ".Xb9hP input")
    first_input.send_keys(all_addresses[i], Keys.TAB, all_prices[i])

    # check to see if each link is complete, if it's not, complete it before entering in google form
    if all_links[i][0] == "/":
        third_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div['
                                                    '2]/div/div[1]/div/div[1]/input')

        third_input.send_keys(f"https://www.zillow.com{all_links[i]}")
        print(f"https://www.zillow.com{all_links[i]}")
    else:
        third_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div['
                                                    '2]/div/div[1]/div/div[1]/input')
        third_input.send_keys(all_links[i])
    time.sleep(2)
    submit_button = driver.find_element(By.CLASS_NAME, "NPEfkd")
    submit_button.click()
    time.sleep(2)

time.sleep(3)

driver.quit()

