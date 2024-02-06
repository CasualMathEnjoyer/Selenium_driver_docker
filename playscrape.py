import time
start_time = time.time()

import csv
import asyncio
from playwright.async_api import async_playwright


async def main():
    with open('realitysoup.csv', mode='w', newline='', encoding="utf-8") as reality_csv:
        item_counter = 0
        page_int = 0
        reality_writer = csv.writer(reality_csv, delimiter=',')
        reality_writer.writerow(["size", "rooms", "price", "locality", "note", "url", "imgurl"])

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()

            while item_counter < 40:
                page_int += 1
                url = 'https://www.sreality.cz/hledani/pronajem/byty/praha?velikost=1%2Bkk,2%2Bkk,3%2Bkk&strana=' + str(
                    page_int)
                await page.goto(url)
                await page.wait_for_load_state("domcontentloaded")

                realities = await page.query_selector_all('.property.ng-scope')

                for reality in realities:
                    title_handle = await reality.query_selector('span.name.ng-binding')
                    title = await page.evaluate('(element) => element.textContent', title_handle)

                    name = 'Byt'
                    size = title.split("u ")[1]
                    rooms = size.split(" ")[0]
                    size = size.split(" ")[1].split(" ")[0]
                    if '(' in title:
                        note = title.split('(')[1].split(')')[0]
                        size = size.split(" (")[0]
                    else:
                        note = ''

                    price_handle = await reality.query_selector('span.norm-price.ng-binding')
                    price = await page.evaluate('(element) => element.textContent.split(" Kč")[0]', price_handle)

                    locality_handle = await reality.query_selector('span.locality.ng-binding')
                    locality = await page.evaluate('(element) => element.textContent', locality_handle)
                    url_handle = await reality.query_selector('a.title')

                    url = await page.evaluate('(element) => element.getAttribute("href")', url_handle)
                    url = 'https://www.sreality.cz' + url

                    img_handle = await reality.query_selector('img')
                    imgurl = await page.evaluate('(element) => element.getAttribute("src")', img_handle)

                    print(f'{name}, {rooms}, {size}, {price}, {locality}, {note}, {url} ({imgurl})')
                    reality_writer.writerow([size, rooms, price, locality, note, url, imgurl])
                    item_counter += 1

            await browser.close()


if __name__ == '__main__':
    asyncio.run(main())

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Script execution time: {elapsed_time:.2f} seconds")
