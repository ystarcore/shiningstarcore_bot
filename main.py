from telegram import Bot
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import asyncio
import httpx

TOKEN = "6946404169:AAGe2HCw9cnS-taw-sbNebZ6CqGNC_9Rz1U"
CHATID = "-1002106245609"
url = "https://www.peopleperhour.com/freelance-jobs/technology-programming"

bot = Bot(token=TOKEN)


with open('store.txt', 'r') as file:
    try:
        flag = int(file.read())
    except:
        flag = 0


async def fetchData():
    try:
        global flag
    
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        projects = soup.find("div", {'class': "list⤍List⤚3R-r9"}).findAll('a', {'class': 'item__url⤍ListItem⤚20ULx'})

        getId = lambda str: int(str.get("href").strip().split('-')[-1])

        if flag == 0: flag = getId(projects[0])
            
        links = [link.get('href').strip() for link in projects if getId(link) > flag]
        links.reverse()

        for link in links:
            dom = requests.get(link)
            
            domx = BeautifulSoup(dom.text, "html.parser")  
            
            name = domx.find("div", {'class': "member-name-container"}).find("h5").text.strip()
            review = domx.find("div", {'class': "member-name-container"}).find('span', {'class':'js-tooltip'}).text.replace('\n', '').replace(' ', '')
            location = domx.find("div", {'class': "location-container"}).text.strip()
            title = domx.find("header", {'class': "clearfix"}).find('h1').text.strip()
            items = domx.find("ul", {'class': "info"}).findAll('li')[2:]
            strs = [li.text.strip() for li in items]
            strs.append(domx.find("div", {'class': "budget"}).find('label').text.strip())
            strs.append(domx.find("div", {'class': "budget"}).find('div').text.strip())  
            dscp = domx.find("div", {'class': "project-description"}).text.strip()[:3000]
            options = '    '.join(['✅ ' + str(x) for x in strs])
            client = f'☹️ {name} / {review}'
            if int(review.split('%')[0]) > 50: client = f'🙂 {name} / {review}'
            tokyo_timezone = pytz.timezone('Asia/Tokyo')
            time = datetime.now(tz=tokyo_timezone).strftime("%H:%M:%S  %Y-%m-%d")

            text = f'{client}    🔰 {location}    🕙 {time}\n\n {options}```\n{title}\n\n{dscp}\n```{link}'
            
            await bot.send_message(chat_id=CHATID, text=text, parse_mode="MARKDOWN")
            
            flag = int(link.split('-')[-1])
            
            with open('store.txt', 'w') as file:
                file.write(f'{flag}')
    except Exception as e:
        print(f"An error occurred: {e}")


async def main():
    while True:
        await fetchData()
        await asyncio.sleep(4)
    

if __name__ == "__main__":
    asyncio.run(main())