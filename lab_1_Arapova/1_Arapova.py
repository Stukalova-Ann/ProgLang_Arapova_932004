from bs4 import BeautifulSoup
import requests
from queue import Queue
from threading import Thread
import time
import sys

class News:
    def __init__(self, title="", date="", annotation="", resource=""):
        self.title = title
        self.date = date
        self.annotation = annotation
        self.resource = resource

    def __str__(self):
        return f"{self.resource} {self.date} \n{self.title} \n{self.annotation}"
urls = ['https://www.eg.ru/showbusiness/', 
        'https://www.riatomsk.ru/novosti', 
        'https://rb.ru/tag/fashion/']

def stars_news():
    all_news = []
    html = requests.get(urls[0]).text
    soup = BeautifulSoup(html, 'html.parser')
    news_divs = soup.find_all('div', class_='section_item')
    for div in news_divs:
            blocks = div.find('div', class_='section_item-body')
            
            block1 = blocks.find('a', class_ = 'section_item-body-link')
            block2 = blocks.find('div', class_ = 'section_item-meta desknow')
            
            title = block1.find('h2').text.strip()
            annotation = block1.find('div').text.strip()
            date = block2.find('span', class_='section_item-date-time').text.strip()
            
            all_news.append(
                News(
                    resource='eg.ru - SHOWBUSINESS   ',
                    date=date,
                    title=title,
                    annotation=annotation,
                    )
            )
    return all_news


def tomsk_news():
    all_news = [] 
    html = requests.get(urls[1]).text
    soup = BeautifulSoup(html, 'html.parser')
    
    news_divs = soup.find_all('div', class_='rubNewAbout')
    
    for div in news_divs:
        blocks = div.find_all('div', recursive=False)
        
        title = blocks[0].text.strip().replace('\n', ' ')
        time = blocks[1].find('span').text.strip() 
        day = blocks[1].find('div').text.strip()
        date = time + ' ' + day
        
        annotation = blocks[2].text.strip().replace('\n', ' ')
        
        all_news.append(
            News(
                resource='riatomsk.ru   ',
                date = date,
                title = title,
                annotation = annotation,
                
            )
        )
    return all_news


def fashion_news():
    all_news = []
    html = requests.get(urls[2]).text
    soup = BeautifulSoup(html, 'html.parser')
    
    news_divs = soup.find_all('div', class_='news-item')

    for div in news_divs:
        blocks = div.find('div', class_ = 'news-item__text')
        
        date = blocks.find('time').text.strip()
        title = blocks.find('h2').text.strip()
        annotation = blocks.find('div', class_ = 'news-item__details').text.strip()
        
        all_news.append(
            News(
                resource = 'BR.ru - FASHION   ',
                title = title, 
                date = date, 
                annotation = annotation
            )
        )

    return all_news


def get_all_news():
    return [*stars_news(), *tomsk_news(), *fashion_news()]

def background_task(q):
    while True:
        news = get_all_news()
        for i in news:
            q.put(i)
        time.sleep(60 * 5)

if __name__ == '__main__':
    q = Queue()    
    background_thread = Thread(target=background_task, daemon=True, args=[q])
    shown_news = set()
    try:
        background_thread.start()
        while True:
            if not q.empty():
                a = q.get()
                if a.title not in shown_news:
                    shown_news.add(a.title)
                    print(a)
                    print(flush=True)
            else:
                time.sleep(0.5)
                
    except (KeyboardInterrupt, SystemExit):
        print('EXIT')
        sys.exit()
