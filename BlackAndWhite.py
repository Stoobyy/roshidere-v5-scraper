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
# from script import checkForUpdates
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive


def starter():
    os.remove('Roshidere.txt') if os.path.exists('Roshidere.txt') else None
    os.remove('Roshidere.epub') if os.path.exists('Roshidere.epub') else None
    print('Deleted existing files. Starting script.')
    with open(f'Roshidere.txt', 'a') as f:
        f.write('Roshidere Volume 5\n')
        f.write("Scrapped and EPUB'd by Stooby\nTranslated by [Glucose Translations](https://glucosetl.files.wordpress.com/)\n\n")
        f.write('# Illustrations\n')
        files = os.listdir('./Pictures/')
        for i in files:
            f.write(f'![Image {i}](Pictures/{i})\n')
        print('Cover image added. Starting chapter 1.')

def script(chaps):
    with open('Roshidere.txt', 'a') as a:
        a.write(f'\n# Chapter {chaps}\n')
        files = os.listdir(f'./Chapter {chaps}/')
        for i in files:
            a.write(f'![Page](Chapter {chaps}/{i})\n')
        print(f'Chapter {chaps} complete.')

def epub():
    subprocess.Popen(['pandoc', 'Roshidere.txt', '-o', 'Roshidere.epub', '--epub-cover-image', 'Cover.png', '--metadata', 'title="Roshidere Volume 5"'])
    time.sleep(3)

def webhook(last):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1058597249770340352/QMg9jatnnBbbrqVZmk7oZNvUyw43wDUl3eRKVWtvCQlmstRPlWUQI3N5S5It4TKTcvvG', username="Roshidere Updater")
    embed = DiscordEmbed(title='Update', description=f'Roshidere Volume 5 Chapters Prologue-{last}', color=242424, url = 'https://lankyrapidprofiler.leany.repl.co/download')
    embed.set_timestamp()
    embed.set_footer(text='Made by Stooby with <3')
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/971761146325532712/1058690008472625193/Cover.png?width=408&height=582')
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

# def gdriveUpload(last):
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()      
#     drive = GoogleDrive(gauth)  
#     f = drive.CreateFile({'title': f'Roshidere Volume 5 Chapters Prologue-{last}.epub', 'mimeType': 'application/epub+zip'})
#     f.SetContentFile(os.path.join(os.getcwd(), 'Roshidere.epub'))
#     f.Upload()
#     print('Uploaded to Google Drive.')
#     webhook = DiscordWebhook(url='https://discord.com/api/webhooks/1058597249770340352/QMg9jatnnBbbrqVZmk7oZNvUyw43wDUl3eRKVWtvCQlmstRPlWUQI3N5S5It')
#     embed = DiscordEmbed(title='Update', description=f'Roshidere Volume 5 Chapters Prologue-{last}', color=242424)
#     embed.set_author()

def run():
    last = len(checkForUpdates())
    starter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(script, range(1, last + 1))
    epub()
    return True
