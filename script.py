from PIL import Image
from pytesseract import pytesseract
import os
import sys
import subprocess
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import concurrent.futures
import requests
from bs4 import *

dic = {}


def script(chap):
    global dic
    path_to_tesseract = r'C:\Users\amrit\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' #change this to your tesseract path, or just change amrit to your profile name
    pytesseract.tesseract_cmd = path_to_tesseract
    files = os.listdir(f'./Chapter {chap}/')
    dic[chap] = [] if chap not in dic else dic[chap]
    for i in files:
        img = Image.open(f'./Chapter {chap}/{i}')
        text = pytesseract.image_to_string(img)
        if text == '':
            dic[chap].append(f'![Image {i}](Chapter {chap}/{i})\n')
        else:
            dic[chap].append(text)
    print(f'Chapter {chap} complete.')

def prologue():
    global dic
    path_to_tesseract = r'C:\Users\amrit\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' #change this to your tesseract path, or just change amrit to your profile name
    pytesseract.tesseract_cmd = path_to_tesseract
    files = os.listdir(f'./Prologue/')
    dic[0] = [] if 0 not in dic else dic[0]
    for i in files:
        img = Image.open(f'./Prologue/{i}')
        text = pytesseract.image_to_string(img)
        if text == '':
            dic[0].append(f'![Image {i}](Prologue/{i})\n')
        else:
            dic[0].append(text)
    print('Prologue complete.')

def compile():
    with open(f'Roshidere.txt', 'a') as f:
        f.write('Roshidere Volume 5\n')
        f.write("Scrapped and EPUB'd by Stooby\nTranslated by [Glucose Translations](https://glucosetl.files.wordpress.com/)\n\n")
        f.write('# Illustrations\n')
        files = os.listdir('./Pictures/')
        for i in files:
            f.write(f'![Image {i}](Pictures/{i})\n')
        f.write('\n# Prologue\n')
        for i in dic[0]:
            f.write(i)
        f.write('\nPrologue complete.\n')
        for i in range(1, len(dic)):
            f.write(f'\n# Chapter {i}\n')
            for j in dic[i]:
                f.write(j)
            f.write('\nChapter complete.\n')
            print(f'Chapter {i} complete.')
        print('Prologue complete.')
    

def run(last):
    subprocess.Popen(['pandoc', 'Roshidere.txt', '-o', 'Roshidere.epub', '--epub-cover-image', 'Cover.png', '--metadata', 'title="Roshidere Volume 5"'])
    print('Scripting complete. Output is Roshidere.epub')
    time.sleep(10)
    webhook(last)

def webhook(last = 'None'):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1064570668462649445/TMyONY5uTbSAOdke7m4TqXVChXqLDwOcIDXUIi8iOUQEbq18XO6E2oh_mZ3iq4Sko6q2', username="Roshidere Updater")
    embed = DiscordEmbed(title='Update', description=f'Roshidere Volume 5 Chapters Prologue-{last}', color=242424)
    embed.set_timestamp()
    embed.set_footer(text='Made by Stooby with <3')
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/971761146325532712/1058690008472625193/Cover.png?width=408&height=582')
    with open("Roshidere.epub", "rb") as f:
        webhook.add_file(file=f.read(), filename='Roshidere.epub')
    webhook.add_embed(embed)
    response = webhook.execute()
    print('Discord webhook sent.')

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

def remove():
    os.remove('Roshidere.txt') if os.path.exists('Roshidere.txt') else None
    os.remove('Roshidere.epub') if os.path.exists('Roshidere.epub') else None

def finish(last):
    remove()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(script, range(1, len(checkForUpdates())+1))
    prologue()
    compile()
    last = checkForUpdates()
    run(last)

