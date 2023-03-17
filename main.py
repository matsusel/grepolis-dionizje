import datetime
import math
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents, description="123")


@bot.event
async def on_ready():
    print("Ready")


@bot.event
async def on_message(message: discord.Message):
    if message.content.lower().startswith("ev "):
        msg = message.content
        args = msg.split()
        if len(args) != 4:
            await message.channel.send("Bledna liczba argumentow. Powinny byc 3 oddzielone spacja. Uzycie: ev <numer "
                                       "jednostki> <pierwsza liczba z zadania> <nazwa przyspieszacza>, np. ev 2 15 "
                                       "kozy. Pamietaj ze w tlumaczeniu jest jakis blad i Fallofor to to samo co "
                                       "Phallophoroi.")
            return
        arg1 = args[1]
        arg2 = args[2]
        arg3 = args[3]
        if arg1 == '1':
            k=2
            jedn1 = 'Panes'
        elif arg1 == '2':
            k=3
            jedn1 = 'Sileny'
        elif arg1 == '3':
            k=5
            jedn1 = 'Fallofor'
        elif arg1 == '4':
            k=2
            jedn1 = 'Kanephoroi'
        elif arg1 == '5':
            k=3
            jedn1 = 'Driady'
        elif arg1 == '6':
            k=6
            jedn1 = 'Arcykaplani'
        else:
            await message.channel.send("Bledny argument numer 1. Powinna to byc cyfra od 1 do 6 odpowiadajaca "
                                       "jednostce z paska na dole, na przyklad 1 dla Panes, 2 dla Sileny itd.")
            return
        try:
            x = int(arg2)
        except:
            await message.channel.send("Bledny argument numer 2. Powinna to byc pierwsza liczba, ktora pojawila sie "
                                       "w tresci zadania.")
            return
        if arg3.lower() == 'wózki' or arg3.lower() == 'wozki':
            m=6
            jedn2 = 'Panes'
        elif arg3.lower() == 'noże' or arg3.lower() == 'noze':
            m=7
            jedn2 = 'Sileny'
        elif arg3.lower() == 'osły' or arg3.lower() == 'osly':
            m=15
            jedn2 = 'Fallofor'
        elif arg3.lower() == 'kozy':
            m=3
            jedn2 = 'Kanephoroi'
        elif arg3.lower() == 'leopardy':
            m=8
            jedn2 = 'Driady'
        elif arg3.lower() == 'pędzle' or arg3.lower() == 'pedzle':
            m=20
            jedn2 = 'Arcykaplani'
        else:
            await message.channel.send("Bledny argument numer 3. Powinien to byc wyraz w liczbie mnogiej w mianowniku, "
                                       "np. wozki, kozy, osly. Polskie znaki sa uznawane.")
            return
        a = x*k
        b = math.ceil(a/(m-1))
        await message.channel.send(f"Do {msg} uzyj {a} {jedn1} i {b} {jedn2}")

    elif message.content.lower().startswith("ochr "):
        msg = message.content
        args = msg.split()
        if len(args) != 2:
            await message.channel.send("Nalezy podac tylko czas ochrony oddzielony dwukropkami")
            return
        timeinfo = args[1].split(":")
        if len(timeinfo) == 3:
            try:
                dt = datetime.datetime(2000, 1, 1, int(timeinfo[0]) % 24, int(timeinfo[1]), int(timeinfo[2]))
            except:
                await message.channel.send("Podaj poprawna godzine.")
                return
        elif len(timeinfo) == 2:
            try:
                dt = datetime.datetime(2000, 1, 1, int(timeinfo[0]) % 24, int(timeinfo[1]))
            except:
                await message.channel.send("Podaj poprawna godzine.")
                return
        else:
            await message.channel.send("Podaj poprawny czas (gg:mm:ss lub gg:mm)")
            return
        res1 = dt + datetime.timedelta(hours=2, minutes=24)
        res2 = res1 + datetime.timedelta(hours=2, minutes=24)
        res3 = res2 + datetime.timedelta(hours=2, minutes=24)
        await message.channel.send(f"Czasy nastepnych ochronek:\n {res1.time()} \n {res2.time()} \n {res3.time()}")

    elif message.content.lower().startswith("tra "):
        msg = message.content
        args = msg.split()
        if len(args) == 2:
            try:
                res = math.ceil(int(args[1])/21)
            except:
                await message.channel.send("Przyjmuje tylko liczby.")
                return
            await message.channel.send(f"Dla {args[1]} wolnych mieszkancow zbuduj {res} transow")
            return
        elif len(args) == 4:
            try:
                free = int(args[1])
                ships = int(args[2])
                units = int(args[3])
            except:
                await message.channel.send("Przyjmuje tylko liczby.")
                return
            res = math.ceil((ships*5 + units + free)/21)
            await message.channel.send(f"Zbuduj jeszcze {res-ships} transow, zeby bylo ich lacznie {res}")

        else:
            await message.channel.send("Nalezy podac tylko liczbe wolnych mieszkancow lub kolejno liczbe wolnych "
                                       "mieszkancow, aktualna liczbe transow i aktualna liczbe wojska")
            return


bot.run('INSERT YOUR TOKEN HERE')
