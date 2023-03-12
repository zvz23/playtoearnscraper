import requests
import parsel
import db
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from pprint import pprint
from time import sleep
import mimetypes
from uuid import uuid4
import os
import shutil
import sys


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
    crypto_tokens_container = selector.xpath("//div[contains(@class, 'related_token')]//span[@class='symbol']/text()").getall()
    nft_tokens_container = selector.xpath("//div[contains(@class, 'related_nft')]/span/text()")
    crypto_tokens = []
    for token in crypto_tokens_container:
        crypto_tokens.append(token.strip()[1:-1].upper())
    game_info['CRYPTO_TOKENS'] = None if len(crypto_tokens) == 0 else ','.join(crypto_tokens)
    game_info['NFT_TOKENS'] = None if len(nft_tokens_container) == 0 else ','.join(nft_tokens_container)
    images_container = selector.xpath("//div[contains(@class, 'dapp_image_container')]//a/@href").getall()
    game_info['IMAGES'] = None if len(images_container) == 0 else ','.join(images_container)
    game_info['DESCRIPTION'] = selector.xpath("normalize-space(//div[@class='detail']//p)").get()
    game_info['WEBSITE'] = selector.xpath("//div[@class='social']/a[contains(@id, 'website')]/@href").get()
    game_info['TWITTER'] = selector.xpath("//div[@class='social']/a[contains(@id, 'twitter')]/@href").get()
    game_info['DISCORD'] = selector.xpath("//div[@class='social']/a[contains(@id, 'discord')]/@href").get()
    game_info['TELEGRAM'] = selector.xpath("//div[@class='social']/a[contains(@id, 'telegram')]/@href").get()
    game_info['YOUTUBE'] = selector.xpath("//div[@class='social']/a[contains(@id, 'youtube')]/@href").get()

    return game_info
    
def parse_game_uc(html: str):
    selector = parsel.Selector(text=html)
    game_info = {}
    name = selector.xpath("//div[@class='headline-dapp']/h1/text()").get()
    if name is None:
        return None
    game_info['NAME'] = name.strip()
    game_info['PROFILE_PIC'] = selector.xpath("//div[@class='dapp_profilepic']/img/@src").get()
    game_info['RANKING'] = selector.xpath("//span[contains(@class, 'total_rank')]/text()").get()
    game_info['NFT_SUPPORT'] = selector.xpath("//a[@data-original-title='NFT Support']/text()").get()
    free_to_play_container = selector.xpath("//div/span[contains(text(), 'Free-To-Play')]/../a/text()").getall()
    game_info['FREE_TO_PLAY'] = None if len(free_to_play_container) == 0 else ','.join(free_to_play_container)
    play_to_earn_container = selector.xpath("//div/span[contains(text(), 'Play-To-Earn')]/../a/text()").getall()
    game_info['PLAY_TO_EARN'] = None if len(play_to_earn_container) == 0 else ','.join(play_to_earn_container)
    genres_container = selector.xpath("//div[@class='dapp_categories']/a/text()").getall()
    game_info['GENRES'] = None if len(genres_container) == 0 else ','.join([genre.strip() for genre in genres_container])
    devices_container = selector.xpath("//div[@class='dapp_devices']/a/@data-original-title").getall()
    game_info['DEVICES'] = None if len(devices_container) == 0 else ','.join(devices_container)
    social_score = selector.xpath("//span[@class='socialscore_number']/text()").get()
    game_info['SOCIAL_SCORE'] = None if social_score is None else social_score.strip()
    platforms_container = selector.xpath("//div[@class='dapp_platforms']/a/@data-original-title").getall()
    game_info['PLATFORMS'] = None if len(platforms_container) == 0 else ','.join(platforms_container)
    crypto_tokens_container = selector.xpath("//div[contains(@class, 'related_token')]//span[@class='symbol']/text()").getall()
    nft_tokens_container = selector.xpath("//div[contains(@class, 'related_nft')]/span/text()")
    crypto_tokens = []
    for token in crypto_tokens_container:
        crypto_tokens.append(token.strip()[1:-1].upper())
    game_info['CRYPTO_TOKENS'] = None if len(crypto_tokens) == 0 else ','.join(crypto_tokens)
    game_info['NFT_TOKENS'] = None if len(nft_tokens_container) == 0 else ','.join(nft_tokens_container)
    images_container = selector.xpath("//div[contains(@class, 'dapp_image_container')]//a/@href").getall()
    game_info['IMAGES'] = None if len(images_container) == 0 else ','.join(images_container)
    game_info['DESCRIPTION'] = selector.xpath("normalize-space(//div[@class='detail']//p)").get()
    game_info['WEBSITE'] = selector.xpath("//div[@class='social']/a[contains(@id, 'website')]/@href").get()
    game_info['TWITTER'] = selector.xpath("//div[@class='social']/a[contains(@id, 'twitter')]/@href").get()
    game_info['DISCORD'] = selector.xpath("//div[@class='social']/a[contains(@id, 'discord')]/@href").get()
    game_info['TELEGRAM'] = selector.xpath("//div[@class='social']/a[contains(@id, 'telegram')]/@href").get()
    game_info['YOUTUBE'] = selector.xpath("//div[@class='social']/a[contains(@id, 'youtube')]/@href").get()

    return game_info


def get_tokens(html: str):
    #//div[contains(@class, 'related_nft')]/span/text()
    selector = parsel.Selector(text=html)
    crypto_tokens_list = []
    crypto_tokens = selector.xpath("//div[contains(@class, 'related_token')]//span[@class='symbol']/text()").getall()
    for token in crypto_tokens:
        crypto_tokens_list.append(token.strip()[1:-1].upper())
    nft_tokens_list = selector.xpath("//div[contains(@class, 'related_nft')]/span/text()").getall()
    tokens = {
        'crypto': None if len(crypto_tokens_list) == 0 else ','.join(crypto_tokens_list),
        'nft': None if len(nft_tokens_list) == 0 else ','.join(nft_tokens_list)
    }
    return tokens



def main():
    with requests.Session() as s:
        s.headers.update({'User-Agent': USER_AGENT})
        urls = db.get_urls_without_info()
        print(f"FOUND {len(urls)} GAMES WITHOUT INFO")
        for url in urls:
            print("GETTING INFO FOR ", url['URL'])
            response = s.get(url['URL'])
            if response.status_code != 200:
                print("ERROR ", url['URL'])
                log_errors(url['URL'])
                continue
            game_info = parse_game(response.text)
            if game_info is None:
                print("ERROR NO NAME ", url['URL'])
                log_errors(url['URL'])
                continue
            db.update_info(url['ID'], game_info)
    print("FINISHED SCRAPING")

def main_uc():
    driver = uc.Chrome()
    urls = db.get_urls_without_info()
    print(f"FOUND {len(urls)} GAMES WITHOUT INFO")
    for url in urls:
        print("GETTING INFO FOR ", url['URL'])
        driver.get(url['URL'])
        game_info = parse_game(driver.page_source)
        if game_info is None:
            print("ERROR NO NAME ", url['URL'])
            log_errors(url['URL'])
            continue
        db.update_info(url['ID'], game_info)


def update_tokens_uc():
    games = db.get_games_without_tokens()
    driver = uc.Chrome(user_data_dir=r'C:\Users\Ziegfred\AppData\Local\Google\Chrome\User Data')
    for game in games:
        print("SCRAPING ", game['URL'])
        driver.get(game['URL'])
        tokens = get_tokens(driver.page_source)
        if tokens['crypto'] is not None:
            db.update_game_column(game['ID'], 'CRYPTO_TOKENS', tokens['crypto'])
        if tokens['nft'] is not None:
            db.update_game_column(game['ID'], 'NFT_TOKENS', tokens['nft'])
        if tokens['crypto'] is not None or tokens['nft'] is not None:
            print("FOUND TOKENS: ")
            pprint(tokens)
        else:
            print("NO TOKENS")
    driver.quit()

def update_tokens_req():
    games = db.get_games_without_tokens()
    with requests.Session() as s:
        s.headers.update({'User-Agent': USER_AGENT})
    for game in games:
        print("SCRAPING ", game['URL'])
        response = s.get(game['URL'])
        if response.status_code != 200:
            log_errors(game['URL'])
            print("ERROR ", game['URL'])
            continue
        tokens = get_tokens(response.text)
        if tokens['crypto'] is not None:
            db.update_game_column(game['ID'], 'CRYPTO_TOKENS', tokens['crypto'])
        if tokens['nft'] is not None:
            db.update_game_column(game['ID'], 'NFT_TOKENS', tokens['nft'])
        if tokens['crypto'] is not None or tokens['nft'] is not None:
            print("FOUND TOKENS: ")
            pprint(tokens)
        else:
            print("NO TOKENS")

def download_images():
    games = db.get_game_images()
    with requests.Session() as s:
        s.headers.update({'User-Agent': USER_AGENT})
        for game in games:
            id_str = str(game['ID'])
            print("GETTING IMAGES FROM ", id_str)
            game_images_path = os.path.join('images', id_str)
            if os.path.exists(game_images_path):
                if len(os.listdir(game_images_path)) > 0:
                    print(f"SKIPPING {game['ID']} already has images")
                    continue
            else:
                os.mkdir(game_images_path)

            images = game['IMAGES'].split(',')
            if game['PROFILE_PIC'] is not None:
                images.append(game['PROFILE_PIC'])
            for image in images:
                response = s.get(image)
                extension = mimetypes.guess_extension(response.headers['content-type'])
                file_name = f'{str(uuid4())}{extension}'
                file_path = os.path.join(game_images_path, file_name)
                with open(file_path, 'wb') as f:
                    for data in response.iter_content(128):
                        f.write(data)

if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'gameinfo':
        main()
    elif command == 'gameinfouc':
        main_uc()
    elif command == 'images':
        download_images()
    elif command == 'tokens':
        update_tokens_req()
    else:
        print("UNKNOWN COMMAND")




