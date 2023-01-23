import discord
from discord.ext import commands, pages
import os
import time
from scraper import *
import asyncio
from keep_alive import keep_alive
import datetime

client = commands.Bot(command_prefix=commands.when_mentioned_or('>'),
                      intents=discord.Intents.all())


@client.event
async def on_ready():
    global startup_time
    print('Bot is ready.')
    startup_time = datetime.datetime.now().timestamp()
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Activity(
                                     type=discord.ActivityType.playing,
                                     name='with Alya'))


@client.command()
async def ping(ctx):
    await ctx.reply(f"{client.latency * 1000 : .2f}ms", mention_author=False)


@client.slash_command(name="ping", description="Pings the bot")
async def ping(ctx):
    await ctx.respond(f"{client.latency * 1000 : .2f}ms")


@client.command()
async def status(ctx):
    current_time = datetime.now().timestamp()
    time = current_time - startup_time
    time = str(datetime.timedelta(seconds=time))
    value = ""
    if "," in time:
        time = time.split(",")
        value += time[0] + " , "
        time = time[1]
    else:
        value += "0 days , "
    time = time.split(":")
    value += f"{time[0]} hours , {time[1]} minutes and {int(float(time[2]))} seconds"
    await ctx.respond(f"I have been online for `{value}`")

@client.slash_command()
async def status(ctx):
    current_time = datetime.now().timestamp()
    time = current_time - startup_time
    time = str(datetime.timedelta(seconds=time))
    value = ""
    if "," in time:
        time = time.split(",")
        value += time[0] + " , "
        time = time[1]
    else:
        value += "0 days , "
    time = time.split(":")
    value += f"{time[0]} hours , {time[1]} minutes and {int(float(time[2]))} seconds"
    await ctx.respond(f"I have been online for `{value}`")

@client.slash_command(name='script', description='Starts the script')
async def script(ctx):
    await ctx.respond('Done!', ephemeral=True)
    embed = discord.Embed(
        title="Roshidere v5",
        description=
        "Script is running, please wait for a bit for it to finish.",
        color=10038562)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text='Made by Stooby with <3')
    embed.set_thumbnail(
        url=
        'https://media.discordapp.net/attachments/971761146325532712/1058690008472625193/Cover.png?width=408&height=582'
    )
    sent = await ctx.send(embed=embed)
    data = botScript()
    newEmbed = discord.Embed(
        title="Roshidere v5",
        description=f"Roshidere Volume 5 Chapters Prologue-{data}",
        color=10181046,
        url='https://LankyRapidProfiler.leany.repl.co/download')
    newEmbed.set_thumbnail(
        url=
        'https://media.discordapp.net/attachments/971761146325532712/1058690008472625193/Cover.png?width=408&height=582'
    )
    newEmbed.timestamp = datetime.datetime.utcnow()
    newEmbed.set_footer(text='Made by Stooby with <3')
    await sent.edit(embed=newEmbed)


@client.slash_command(name="epub", description="Runs pandoc")
async def epub(ctx):
    await ctx.respond("Running pandoc...")
    pandoc_bin = None
    await asyncio.create_subprocess_exec('./pandoc', 'Roshidere.txt', '-o',
                                         'Roshidere.epub',
                                         '--epub-cover-image', 'Cover.png',
                                         '--metadata',
                                         'title="Roshidere Volume 5"')
    embed = discord.Embed(
        title='EPUB Created!',
        description='Roshidere Volume 5',
        color=15844367,
        url='https://LankyRapidProfiler.leany.repl.co/download')
    await ctx.respond(embed=embed)


@client.slash_command(name='latest', description='Gets the latest chapter')
async def latest(ctx):
    data = len(checkForUpdates())
    embed = discord.Embed(title='Latest Chapter',
                          description=f'Chapter {data}',
                          color=10038562)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text='Made by Stooby with <3')
    await ctx.respond(embed=embed)


@client.slash_command(name='help', description='Gets the help menu')
async def help(ctx):
    embed = discord.Embed(title='Help Menu',
                          description='List of commands',
                          color=2895667)
    embed.add_field(name='🔦script', value='Runs the script', inline=True)
    embed.add_field(name='📗epub', value='Runs pandoc', inline=True)
    embed.add_field(name='🕔latest',
                    value='Gets the latest chapter',
                    inline=True)
    embed.add_field(name='📌ping', value='Pings the bot', inline=True)
    embed.add_field(name='⌚status',
                    value='Gets the status of the bot',
                    inline=True)
    embed.add_field(name='❓help', value='Gets the help menu', inline=True)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text='Made by Stooby with <3')
    await ctx.respond(embed=embed)


@client.slash_command(name='status', description='Gets the status of the bot')
async def status(ctx):
    current_time = datetime.datetime.now().timestamp()
    time = current_time - startup_time
    time = str(datetime.timedelta(seconds=time))
    value = ""
    if "," in time:
        time = time.split(",")
        value += time[0] + " , "
        time = time[1]
    else:
        value += "0 days , "
    time = time.split(":")
    value += f"{time[0]} hours , {time[1]} minutes and {int(float(time[2]))} seconds"
    await ctx.respond(f"I have been online for `{value}`",
                      mention_author=False)

class Select(discord.ui.Select):
    def __init__(self):
        options = [i for i in os.listdir() if 'Chapter' in i]
        super().__init__(placeholder="Waiting for selection...", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        embed = 

class SelectView(discord.ui.View):
    def __init__(self, *, timeout):
        super().__init__(timeout=timeout)
        self.add_item(Select())


@client.slash_command()
async def read(ctx):
    await ctx.respond('Select a chapter to read', view=SelectView(timeout=None))
    


token = os.environ['TOKEN']

keep_alive()
client.run(token)
