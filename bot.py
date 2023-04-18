# WRITTEN BY AIDAN LEMAY
# aidanlemay.com
# admin@aidanlemay.com for more details
import discord
from discord.ext import commands
import storage
from requests_html import HTMLSession
from datetime import datetime, timedelta
import requests
from typing import Optional

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

monems = "https://cc.k9fgt.me/api/v1/calls?system=us.ny.monroe&talkgroup=1077"
henfire = "https://cc.k9fgt.me/api/v1/calls?system=us.ny.monroe&talkgroup=1654"
ritpub = "https://cc.k9fgt.me/api/v1/calls?system=us.ny.monroe&talkgroup=3070"

# Sync Functions

def get_source():
    try:
        session = HTMLSession()
        response = session.get("https://www.monroecounty.gov/incidents911.rss")
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_source_clearcut(url):
    try:
        data = requests.get(url=url)
        response = data.json()
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_feed_monroe():
    response = get_source()

    out = list()

    with response as r:
        items = r.html.find("item", first=False)

        for item in items:        

            title = item.find('title', first=True).text

            if not title.startswith("PARKING INCIDENT"):
                description = item.find('description', first=True).text

                pubdate = item.find('pubDate', first=True).text

                out.append(title + " | " + description + " | " + pubdate)

    return out

def get_feed_roc():
    response = get_source()

    out = list()

    with response as r:
        items = r.html.find("item", first=False)

        for item in items:        

            title = item.find('title', first=True).text

            if not title.startswith("PARKING INCIDENT"):

                guid = item.find('guid', first=True).text

                if "ROCE" in guid:

                    description = item.find('description', first=True).text

                    pubdate = item.find('pubDate', first=True).text

                    out.append(title + " | " + description + " | " + pubdate)

    return out

def get_feed_hen():
    response = get_source()

    out = list()

    with response as r:
        items = r.html.find("item", first=False)

        for item in items:        

            title = item.find('title', first=True).text

            if not title.startswith("PARKING INCIDENT"):

                guid = item.find('guid', first=True).text

                if "HENE" in guid:

                    description = item.find('description', first=True).text

                    pubdate = item.find('pubDate', first=True).text

                    out.append(title + " | " + description + " | " + pubdate)

    return out

def get_unfiltered():
    response = get_source()

    out = list()

    with response as r:
        items = r.html.find("item", first=False)

        for item in items:        

            title = item.find('title', first=True).text

            description = item.find('description', first=True).text

            pubdate = item.find('pubDate', first=True).text

            out.append(title + " | " + description + " | " + pubdate)

    return out

# End Sync Functions

# Async Commands

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord. Activity(type=discord.ActivityType.listening, name=' /helpme for a list of commands'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.remove_command('help')

@bot.command()
async def helpme(ctx):
    """Gets Status of RPI Server"""
    await ctx.send("""
    ```\MC Emergency Services Discord Bot Help!
    \n\nCreated by Aidan LeMay using Discord.py
    \nhttps://github.com/aidan-lemay/MC-Emergency-Bot
    \n\n__Command Help:__
    \n/helpme: Display this help window
    \n/tg [TG ID] [Keyword (Optional)]: Returns calls from the specified TG with optional keywords (Case Sensitive) from the last 24 hours
    \n/tgs [X String: Optional Keyword Matching String]: Returns list of active talkgroups with optional keywords
    \n/ems [X String: Optional Keyword Matching String]: Returns X# of Calls from TG 1077 (MC EMS Dispatch) with optional keywords (Case Sensitive)
    \n/rite: Returns all calls within the last 24 hours from TG 1077 that contain "RIT", "6359", or "DEFIB 63"
    \n/hfd [X String: Optional Keyword Matching String]: Returns X# of Calls from TG 1654 (HFD Dispatch) with optional keywords (Case Sensitive)
    \n/ritf: Returns all calls within the last 24 hours from TG 1654 that contain "RIT"
    \n/m911 [X#: Optional Quantity]: Returns X# of Monroe County 911 Events from https://www.monroecounty.gov/incidents911.rss with all 'PARKING INCIDENT's filtered out
    \n/h911 [X#: Optional Quantity]: Returns X# of Henrietta area 911 Events from https://www.monroecounty.gov/incidents911.rss with all 'PARKING INCIDENT's filtered out
    \n/r911 [X#: Optional Quantity]: Returns X# of Rochester area 911 Events from https://www.monroecounty.gov/incidents911.rss with all 'PARKING INCIDENT's filtered out
    \n/a911 [X#: Optional Quantity]: Returns X# of Monroe County 911 Events from https://www.monroecounty.gov/incidents911.rss with no data filtered out
    \n/pogle or /polge: fun
    \n\nVisit the creator here! https://aidanlemay.com/```
    """)

@bot.command()
async def ems(ctx, keyword: Optional[str]):
    response = get_source_clearcut(monems)
    message = "```Monroe County EMS Call Transcripts:\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            curtime = datetime.today()
            timestamp = datetime.fromtimestamp(data['startTime'])
            calltime = datetime.fromtimestamp(data['startTime'])
            mintime = curtime - timedelta(hours = 24)
            text = data['transcript']['text']

            if (keyword is not None):
                # Get all calls within num range with matching keywords
                if (calltime > mintime and keyword in text):
                    message += str(timestamp) + " | " + text + "\n\n"
            else:
                # Get all calls within num range
                if (calltime > mintime):
                    message += str(timestamp) + " | " + text + "\n\n"
        
    message = message[ 0 : 1997 ]

    message += "```"

    await ctx.send(message)

@bot.command()
async def rite(ctx):
    response = get_source_clearcut(monems)
    message = "```RIT EMS Call Transcripts:\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            timestamp = datetime.fromtimestamp(data['startTime'])
            text = data['transcript']['text']

            # Get all calls within num range with matching keywords
            if ("RIT" in text or "6359" in text or "6-3-5-9" in text or "Defib 63" in text or "DEFIB 63" in text):
                message += str(timestamp) + " | " + text + "\n\n"

    message = message[ 0 : 1997 ]
    message += "```"

    await ctx.send(message)

@bot.command()
async def hfd(ctx, keyword: Optional[str]):
    response = get_source_clearcut(henfire)
    message = "```Henrietta Fire Department Call Transcripts:\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            curtime = datetime.today()
            timestamp = datetime.fromtimestamp(data['startTime'])
            calltime = datetime.fromtimestamp(data['startTime'])
            mintime = curtime - timedelta(hours = 24)
            text = data['transcript']['text']

            if (keyword is not None):
                # Get all calls within num range with matching keywords
                if (calltime > mintime and keyword in text):
                    message += str(timestamp) + " | " + text + "\n\n"
            else:
                # Get all calls within num range
                if (calltime > mintime):
                    message += str(timestamp) + " | " + text + "\n\n"
        
    message = message[ 0 : 1997 ]

    message += "```"

    await ctx.send(message)

@bot.command()
async def ritf(ctx):
    response = get_source_clearcut(henfire)
    message = "```RIT Fire Related Call Transcripts:\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            timestamp = datetime.fromtimestamp(data['startTime'])
            text = data['transcript']['text']

            # Get all calls within num range with matching keywords
            if ("RIT" in text):
                message += str(timestamp) + " | " + text + "\n\n"

    message = message[ 0 : 1997 ]
    message += "```"

    await ctx.send(message)

@bot.command()
async def tgs(ctx, keyword: Optional[str]):
    response = get_source_clearcut("https://cc.k9fgt.me/api/v1/talkgroups?system=us.ny.monroe&active=true")
    message = "```List of Active Monroe County Talkgroups:\n------------------------\n\n"

    for data in response:
        tg = data['id']
        category = data['category']
        name = data['name']
        transcribed = data['transcribe']        

        if (keyword is not None):
            if (keyword in category or keyword in name):
                message += "TGID: " + str(tg) + " | Name: " + name + " | Transcribed: " + str(transcribed) + "\n\n"
        elif (keyword is None):
            message += "TGID: " + str(tg) + " | Name: " + name + " | Transcribed: " + str(transcribed) + "\n\n"

    message = message[ 0 : 1997 ]
    message += "```"

    await ctx.send(message)

@bot.command()
async def tg(ctx, talkgroup: Optional[int], keyword: Optional[str]):

    response = get_source_clearcut("https://cc.k9fgt.me/api/v1/calls?system=us.ny.monroe&talkgroup=" + str(talkgroup).strip())
    message = "```Custom Call Data from TG" + str(talkgroup).strip() + ":\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            curtime = datetime.today()
            timestamp = datetime.fromtimestamp(data['startTime'])
            calltime = datetime.fromtimestamp(data['startTime'])
            mintime = curtime - timedelta(hours = 24)
            text = data['transcript']['text']

            if (keyword is not None):
                # Get all calls within num range with matching keywords
                if (calltime > mintime and keyword in text):
                    message += str(timestamp) + " | " + text + "\n\n"
            else:
                # Get all calls within num range
                if (calltime > mintime):
                    message += str(timestamp) + " | " + text + "\n\n"
    
    message = message[ 0 : 1997 ]
    message += "```"

    await ctx.send(message)

@bot.command()
async def pub(ctx, password: Optional[str], keyword: Optional[str]):

    if password != storage.pspass:
        await ctx.send("Incorrect Password")
    else:

        response = get_source_clearcut(ritpub)
        message = "```RIT Public Safety Call Transcripts:\n\n"

        for data in response:
            if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
                curtime = datetime.today()
                timestamp = datetime.fromtimestamp(data['startTime'])
                calltime = datetime.fromtimestamp(data['startTime'])
                mintime = curtime - timedelta(hours = 24)
                text = data['transcript']['text']

                
                if (keyword is not None):
                    # Get all calls within num range with matching keywords
                    if (calltime > mintime and keyword in text):
                        message += str(timestamp) + " | " + text + "\n\n"
                else:
                    # Get all calls within num range
                    if (calltime > mintime):
                        message += str(timestamp) + " | " + text + "\n\n"
        
        message = message[ 0 : 1997 ]
        message += "```"

        await ctx.send(message)

@bot.command()
async def polge(ctx):
    """Returns a picture of polge"""
    embed = discord.Embed(title="pogle", description="pogle", color=0x06275c) #creates embed
    pogle = discord.File("./pogle.png", filename="image.png")
    embed.set_image(url="attachment://image.png")
    await ctx.send(file=pogle, embed=embed)

@bot.command()
async def pogle(ctx):
    """Returns a picture of pogle"""
    embed = discord.Embed(title="pogle", description="pogle", color=0x06275c) #creates embed
    pogle = discord.File("./pogle.png", filename="image.png")
    embed.set_image(url="attachment://image.png")
    await ctx.send(file=pogle, embed=embed)

@bot.command()
async def m911(ctx, num: Optional[int]):

    if num == None:
        num = 1

    df = get_feed_monroe()

    fSize = len(df)

    if fSize == 0:
        message = "No Monroe County Events Found"

    else:
        if num > fSize:
            num = fSize
        elif num < 1:
            num = 1

        message = "```\nMonroe County 911 Events:\n"

        # for i in df:
        j = 0
        while j < num:
            message += "-> " + df[j] + "\n\n"
            j+=1

        message += "```"

    await ctx.send(message)

@bot.command()
async def r911(ctx, num: Optional[int]):

    if num == None:
        num = 1
    df = get_feed_roc()

    fSize = len(df)

    if fSize == 0:
        message = "No Rochester Area Events Found"

    else:
        if num > fSize:
            num = fSize
        elif num < 1:
            num = 1

        message = "```\nRochester Area 911 Events:\n"

        # for i in df:
        j = 0
        while j < num:
            message += "-> " + df[j] + "\n\n"
            j+=1

        message += "```"    

    await ctx.send(message)

@bot.command()
async def h911(ctx, num: Optional[int]):

    if num == None:
        num = 1
    df = get_feed_hen()

    fSize = len(df)

    if fSize == 0:
        message = "No Henrietta Area Events Found"

    else:
        if num > fSize:
            num = fSize
        elif num < 1:
            num = 1

        message = "```\nHenrietta Area 911 Events:\n"

        # for i in df:
        j = 0
        while j < num:
            message += "-> " + df[j] + "\n\n"
            j+=1

        message += "```"    

    await ctx.send(message)

@bot.command()
async def a911(ctx, num: Optional[int]):

    if num == None:
        num = 1
    df = get_unfiltered()

    fSize = len(df)

    if fSize == 0:
        message = "No Monroe County Events Found"

    else:
        if num > fSize:
            num = fSize
        elif num < 1:
            num = 1

        message = "```ALL Monroe County 911 Events:\n"

        # for i in df:
        j = 0
        while j < num:
            message += "-> " + df[j] + "\n\n"
            j+=1

        message += "```"   

    await ctx.send(message)

@bot.command()
async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
    """A global error handler cog."""

    if isinstance(error, commands.CommandNotFound):
        message = "Sorry, this command was not found. Please check your input and try again!"
    elif isinstance(error, commands.CommandOnCooldown):
        message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} second(s)."
    elif isinstance(error, commands.MissingPermissions):
        message = "You are missing the required permissions to run this command!"
    elif isinstance(error, commands.UserInputError):
        message = "Something about your input was wrong, please check your input and try again!"
    else:
        message = "Oh no! Something went wrong while running the command!"

    await ctx.send(message, delete_after=5)
    await ctx.message.delete(delay=5)

bot.run(storage.tstore)