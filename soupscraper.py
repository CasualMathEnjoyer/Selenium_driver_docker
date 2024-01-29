from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import csv

# options = Options()
# options.add_argument('--headless=new')
# driver = webdriver.Chrome(options=options)

print("1")
from selenium.webdriver.chrome.options import Options
print("2")

options = Options()
options.add_argument('--headless=new')
print("3")
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME, options=options)


with open('realitysoup.csv', mode='w', newline='',  encoding="utf-8") as reality_csv:
    item_conter = 0
    page = 0
    reality_writer = csv.writer(reality_csv, delimiter=',')
    reality_writer.writerow(["size", "rooms", "price", "locality", "note", "url", "imgurl"])
    while item_conter < 40:
        page += 1
        # url = 'https://www.sreality.cz/hledani/prodej/byty?strana=' + str(page)
        url = 'https://www.sreality.cz/hledani/pronajem/byty/praha?velikost=1%2Bkk,2%2Bkk,3%2Bkk&strana=' + str(page)
        driver.get(url)
        driver.implicitly_wait(0.5)
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        realities = soup.find_all('div', class_="property ng-scope")
        item_conter += len(realities)


        for reality in realities:
            title = reality.find('span', class_='name ng-binding').text
            name = 'Byt'
            size = title.split("u ")[1]
            rooms = size.split(" ")[0]
            size = size.split(" ")[1].split(" ")[0]
            if '(' in title:
                note = title.split('(')[1].split(')')[0]
                size = size.split(" (")[0]
            else:
                note = ''
            price = reality.find('span', class_='norm-price ng-binding').text
            price = price.split(" Kč")[0]
            try:
                price = price.split(" ")[0] + price.split(" ")[1]
            except ValueError or IndexError:
                price = '0'
            locality = reality.find('span', class_='locality ng-binding').text
            url = 'https://www.sreality.cz' + reality.find('a', class_='title')['href']
            imgurl = reality.find('img')['src']
            print(f'{name}, {rooms}, {size}, {price}, {locality}, {note}, {url} ({imgurl})')
            reality_writer.writerow([size, rooms, price, locality, note, url, imgurl])
            # maybe add some numbering system?

    #driver.find_element(By.CLASS_NAME, "").click()
print(item_conter)
