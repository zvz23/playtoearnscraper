import requests
import parsel
import db
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from time import sleep
import json

TEST_URL = 'https://playtoearn.net/blockchaingame/illuvium'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'


def log_errors(url: str):
    with open('errors.txt', 'a') as f:
        f.write(f'{url}\n')

def parse_game(html: str):
    selector = parsel.Selector(text=html)
    game_info = {}
    name = selector.xpath("//div[@class='headline-dapp']/h1/text()").get()
    if name is None:
        return None
    game_info['NAME'] = name.strip()
    game_info['PROFILE_PIC'] = selector.xpath("//div[@class='dapp_profilepic']/img/@src").get()
    game_info['RANKING'] = selector.xpath("//span[contains(@class, 'total_rank')]/text()").get()
    game_info['NFT_SUPPORT'] = selector.xpath("//a[@title='NFT Support']/text()").get()
    free_to_play_container = selector.xpath("//div/span[contains(text(), 'Free-To-Play')]/../a/text()").getall()
    game_info['FREE_TO_PLAY'] = None if len(free_to_play_container) == 0 else ','.join(free_to_play_container)
    play_to_earn_container = selector.xpath("//div/span[contains(text(), 'Play-To-Earn')]/../a/text()").getall()
    game_info['PLAY_TO_EARN'] = None if len(play_to_earn_container) == 0 else ','.join(play_to_earn_container)
    genres_container = selector.xpath("//div[@class='dapp_categories']/a/text()").getall()
    game_info['GENRES'] = None if len(genres_container) == 0 else ','.join([genre.strip() for genre in genres_container])
    devices_container = selector.xpath("//div[@class='dapp_devices']/a/@title").getall()
    game_info['DEVICES'] = None if len(devices_container) == 0 else ','.join(devices_container)
    social_score = selector.xpath("//span[@class='socialscore_number']/text()").get()
    game_info['SOCIAL_SCORE'] = None if social_score is None else social_score.strip()
    platforms_container = selector.xpath("//div[@class='dapp_platforms']/a/@title").getall()
    game_info['PLATFORMS'] = None if len(platforms_container) == 0 else ','.join(platforms_container)
    images_container = selector.xpath("//div[contains(@class, 'dapp_image_container')]//a/@href").getall()
    game_info['IMAGES'] = None if len(images_container) == 0 else ','.join(images_container)
    game_info['DESCRIPTION'] = selector.xpath("normalize-space(//div[@class='detail']//p)").get()
    game_info['WEBSITE'] = selector.xpath("//div[@class='social']/a[contains(@id, 'website')]/@href").get()
    game_info['TWITTER'] = selector.xpath("//div[@class='social']/a[contains(@id, 'twitter')]/@href").get()
    game_info['DISCORD'] = selector.xpath("//div[@class='social']/a[contains(@id, 'discord')]/@href").get()
    game_info['TELEGRAM'] = selector.xpath("//div[@class='social']/a[contains(@id, 'telegram')]/@href").get()
    game_info['YOUTUBE'] = selector.xpath("//div[@class='social']/a[contains(@id, 'youtube')]/@href").get()

    return game_info
    


def main():
    with requests.Session() as s:
        s.headers.update({'User-Agent': USER_AGENT})
        urls = db.get_urls_without_info()
        print(f"FOUND {len(urls)} GAMES WITHOUT INFO")
        for url in urls:
            print("GETTING INFO FOR ", url['URL'])
            response = s.get(url['URL'])
            if response.status_code != 200:
                log_errors(url['URL'])
                continue
            game_info = parse_game(response.text)
            db.update_info(url['ID'], game_info)
    
if __name__ == '__main__':
    main()



