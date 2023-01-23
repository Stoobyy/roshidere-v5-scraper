from bs4 import *
import requests
import os
import json
import re
import time
from script import finish
import concurrent.futures
import shutil
import wget
# from bw import bw

last = 0

def prologue(volume):
    shutil.rmtree('Prologue')
    os.mkdir('Prologue') if not os.path.exists('Prologue') else None
    site = f'https://glucosetl.wordpress.com/roshidere-v{volume}-prologue/'
    r = requests.get(f'https://glucosetl.wordpress.com/roshidere-v{volume}-prologue/')
    soup = BeautifulSoup(r.text, "html.parser")
    image_tags = soup.find_all('img')
    urls = [img['src'] for img in image_tags]
    for url in urls:
        filename = re.search(r'/([\w_-].*(?=jpg)?w=791)', url)
        if not filename:
            continue
        name = filename.group(1).split('/')[-1].strip('?w=791')
        if 'http' not in url:
            url = '{}{}'.format(site, url)
        wget.download(url, f'Prologue/')
    print("Prologue download complete, scripting starts after all chapters are complete!")

def main(chaps):
    global last
    volume = 5
    os.mkdir(f'Chapter {chaps}') if not os.path.exists(f'Chapter {chaps}') else None
    url = f'https://glucosetl.wordpress.com/roshidere-v{volume}-c{chaps}/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    image_tags = soup.find_all('img')
    urls = [img['src'] for img in image_tags]
    for url in urls:
        filename = re.search(r'/([\w_-].*(?=jpg)?w=791)', url)
        if not filename:
            continue
        name = filename.group(1).split('/')[-1].strip('?w=791')
        if 'http' not in url:
            url = '{}{}'.format(url, url)
        wget.download(url, f'Chapter {chaps}/{name}')
    print(f"Chapter {chaps} download complete, scripting starts after all chapters are complete!")

def clearall():
    data = os.listdir()
    for i in data:
        if i.startswith('Chapter'):
            shutil.rmtree(i)

def checkForUpdates():
    links = []
    url = f'https://glucosetl.wordpress.com/the-neighboring-aarya-san-who-sometimes-acts-affectionate/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    image_tags = soup.find_all('a')
    for i in image_tags:
        try:
            data  = i['href']
        except:
            break
        if '/roshidere-v5-c' in data:
            links.append(data)
    return links


if __name__ == '__main__':
# def botScript():
    volume = 5
    prologue(volume)
    clearall()
    links = checkForUpdates()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(main, range(1, len(links)+1))
    print('Scripting started! It will take a while, please be patient as script has to download and install multiple requirements before converting.')
    finish(len(checkForUpdates())+1)