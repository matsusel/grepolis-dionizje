import math
import threading
import datetime
import discord
import requests
from flask import Flask, request

webhook_url = 'set your webhook url'
bot_token = 'set your token'

ROLE_ID = 'role_ID'
CHANNEL_ID = 'channel_ID'

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)
perms = [[], [], [], [], []]
invs = [[], [], [], [], []]
webhooks_to_send = []
already_alarmed = []
app = Flask(__name__)
printlock = threading.Lock()
queuelock = threading.Lock()


base_score = [500, 150, 50, 20]
score_matrix = [{
        "first_skill_points": {
            "multiplier": 15,
            "power": 0.9
        },
        "second_skill_points": {
            "multiplier": 25,
            "power": 0.6
        },
        "third_skill_points": {
            "multiplier": 20,
            "power": 0.7
        }
},
    {
        "first_skill_points": {
            "multiplier": 80,
            "power": 0.7
        },
        "second_skill_points": {
            "multiplier": 60,
            "power": 0.85
        },
        "third_skill_points": {
            "multiplier": 100,
            "power": 0.5
        }
    },
    {
        "first_skill_points": {
            "multiplier": 1.3,
            "power": 0.75
        },
        "second_skill_points": {
            "multiplier": 1.8,
            "power": 0.6
        },
        "third_skill_points": {
            "multiplier": 0.8,
            "power": 0.95
        }
    },
    {
        "first_skill_points": {
            "multiplier": 0.6,
            "power": 0.95
        },
        "second_skill_points": {
            "multiplier": 1.8,
            "power": 0.6
        },
        "third_skill_points": {
            "multiplier": 1.1,
            "power": 0.8
        }
    }]


def get_values_perms_invs(x):
    queuelock.acquire()
    ret = {
        "perms": perms[x].copy(),
        "invites": invs[x].copy()
    }
    queuelock.release()
    safe_print("Got alliance" + str(x+1) + " request. Sending " + str(ret))
    queuelock.acquire()
    perms[x].clear()
    invs[x].clear()
    queuelock.release()
    return ret


@app.route('/alliance1', methods=['GET'])
def alliance1():
    return get_values_perms_invs(0)


@app.route('/alliance2', methods=['GET'])
def alliance2():
    return get_values_perms_invs(1)


@app.route('/alliance3', methods=['GET'])
def alliance3():
    return get_values_perms_invs(2)


@app.route('/alliance4', methods=['GET'])
def alliance4():
    return get_values_perms_invs(3)


@app.route('/alliance5', methods=['GET'])
def alliance5():
    return get_values_perms_invs(4)


@app.route('/attack', methods=['POST'])
def attack():
    # send_webhook(request.data.decode('utf-8'))
    mov_id = request.get_json()["id"]
    mess = request.get_json()["message"]
    if mov_id not in already_alarmed:
        already_alarmed.append(mov_id)
        send_webhook(mess)
    return "OK"


def send_webhook(text):
    safe_print("To send: " + text)
    payload = {
        'content': text + ' @everyone',
        'username': 'Informator',
        'avatar_url': 'https://i.imgur.com/wuowbcp.png',
        'tts': True
    }
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        safe_print('Data sent')
    except requests.exceptions.RequestException as e:
        safe_print(f'Error: {e}')


def safe_print(message):
    printlock.acquire()
    print(message)
    printlock.release()


@client.event
async def on_ready():
    safe_print('Logged as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.content.lower().startswith('upki '):
        if message.author not in message.guild.roles[len(message.guild.roles)-1].members and message.author not in message.guild.roles[len(message.guild.roles)-2].members:
            await message.channel.send("Brak dostepu do tej komendy")
            return
        parts = message.content.split(" ", 2)
        if len(parts) != 3:
            await message.channel.send("Nieprawidlowa liczba argumentow")
            return
        if parts[1] not in ["1", "2", "3", "4"]:  # dopisac obsluge wyjatku
            await message.channel.send("Nieprawidlowy numer sojuszu")
            return
        alliance_number = int(parts[1])
        queuelock.acquire()
        perms[alliance_number - 1].append(parts[2])
        queuelock.release()
        safe_print('Added ' + parts[2] + ' to leadership ' + parts[1] + '. Queue: ' + str(perms))
        await message.channel.send("Zarejestrowano. Nadanie uprawnien moze potrwac kilka minut.")
        log_to_file(message.author.name + ": " + message.content)

    elif message.content.lower().startswith('zap '):
        parts = message.content.split(" ", 2)
        if len(parts) != 3:
            await message.channel.send("Nieprawidlowa liczba argumentow")
            return
        if parts[1] not in ["1", "2", "3", "4", "5"]:  # dopisac obsluge wyjatku
            await message.channel.send("Nieprawidlowy numer sojuszu")
            return
        alliance_number = int(parts[1])
        queuelock.acquire()
        invs[alliance_number - 1].append(parts[2])
        queuelock.release()
        safe_print('Added ' + parts[2] + ' to invite ' + parts[1] + '. Queue: ' + str(invs))
        await message.channel.send("Zarejestrowano. Wyslanie zaproszenia moze potrwac kilka minut.")
        log_to_file(message.author.name + ": " + message.content)

    elif message.content.lower().startswith('lvl '):
        parts = message.content.split(" ")
        if len(parts) != 2:
            await message.channel.send("Nieprawidlowa liczba argumentow")
            return
        try:
            val = int(parts[1])
        except:
            await message.channel.send("Nieprawidlowy poziom")
            return
        if val > 350 or val < 1:
            await message.channel.send("Zbyt wysoki/niski poziom")
            return
        dist = test_skill_distribution(val)
        to_send = "Wyniki dla " + message.content + "\nKonkurencja 1: " + str(dist[0]["skills"][0]) + "/" + str(dist[0]["skills"][1]) + "/" + str(dist[0]["skills"][2]) + ": " + str(math.floor(dist[0]["score"])) + "\nKonkurencja 2: " + str(dist[1]["skills"][0]) + "/" + str(dist[1]["skills"][1]) + "/" + str(dist[1]["skills"][2]) + ": " + str(math.floor(dist[1]["score"])) + "\nKonkurencja 3: " + str(dist[2]["skills"][0]) + "/" + str(dist[2]["skills"][1]) + "/" + str(dist[2]["skills"][2]) + ": " + str(math.floor(dist[2]["score"])) + "\nKonkurencja 4: " + str(dist[3]["skills"][0]) + "/" + str(dist[3]["skills"][1]) + "/" + str(dist[3]["skills"][2]) + ": " + str(math.floor(dist[3]["score"]))
        await message.channel.send(to_send)

    elif message.content.lower().startswith("ev "):
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
            k = 2
            jedn1 = 'Panes'
        elif arg1 == '2':
            k = 3
            jedn1 = 'Sileny'
        elif arg1 == '3':
            k = 5
            jedn1 = 'Fallofor'
        elif arg1 == '4':
            k = 2
            jedn1 = 'Kanephoroi'
        elif arg1 == '5':
            k = 3
            jedn1 = 'Driady'
        elif arg1 == '6':
            k = 6
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
            m = 6
            jedn2 = 'Panes'
        elif arg3.lower() == 'noże' or arg3.lower() == 'noze':
            m = 7
            jedn2 = 'Sileny'
        elif arg3.lower() == 'osły' or arg3.lower() == 'osly':
            m = 15
            jedn2 = 'Fallofor'
        elif arg3.lower() == 'kozy':
            m = 3
            jedn2 = 'Kanephoroi'
        elif arg3.lower() == 'leopardy':
            m = 8
            jedn2 = 'Driady'
        elif arg3.lower() == 'pędzle' or arg3.lower() == 'pedzle':
            m = 20
            jedn2 = 'Arcykaplani'
        else:
            await message.channel.send("Bledny argument numer 3. Powinien to byc wyraz w liczbie mnogiej w mianowniku, "
                                       "np. wozki, kozy, osly. Polskie znaki sa uznawane.")
            return
        a = x * k
        b = math.ceil(a / (m - 1))
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
                res = math.ceil(int(args[1]) / 21)
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
            res = math.ceil((ships * 5 + units + free) / 21)
            await message.channel.send(f"Zbuduj jeszcze {res - ships} transow, zeby bylo ich lacznie {res}")

        else:
            await message.channel.send("Nalezy podac tylko liczbe wolnych mieszkancow lub kolejno liczbe wolnych "
                                       "mieszkancow, aktualna liczbe transow i aktualna liczbe wojska")
            return

def time_until_target(hour, minute, tz_offset):
    now = datetime.utcnow()
    target_time = (now + timedelta(hours=tz_offset)).replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target_time < now + timedelta(hours=tz_offset):
        target_time += timedelta(days=1)
    return (target_time - now).total_seconds()


def schedule_ping():
    while True:
        seconds_until_ping = time_until_target(17, 00, 1)
        time.sleep(seconds_until_ping)
        client.loop.create_task(send_ping())

async def send_ping():
    guild = discord.utils.get(client.guilds)
    role = discord.utils.get(guild.roles, id=ROLE_ID)
    channel = client.get_channel(CHANNEL_ID)

    if role and channel:
        await channel.send(f"{role.mention} Trening!")
    else:
        safe_print("Nie znaleziono roli lub kanału!")

def thread_ping():
    safe_print("Ping thread active.")
    schedule_ping()

def thread_discord():
    safe_print("Discord thread active.")
    client.run(bot_token)


def get_skill_effect(skill, points):
    return skill["multiplier"] * math.pow(points, skill["power"])


def get_score_as_individual_sum(player_points, a):
    keys = list(score_matrix[a].keys())
    return base_score[a] + sum(get_skill_effect(score_matrix[a][skill], player_points[i]) for i, skill in enumerate(keys))


def test_skill_distribution(skill_point_count):
    best_dist = [{"skills": [], "score": -1}, {"skills": [], "score": -1}, {"skills": [], "score": -1},
                {"skills": [], "score": -1}]
    for s1 in range(skill_point_count + 1):
        for s2 in range(skill_point_count - s1 + 1):
            for s3 in range(skill_point_count - s1 - s2 + 1):
                for i in range(0, 4):
                    current_dist = {"skills": [s1, s2, s3], "score": get_score_as_individual_sum([s1, s2, s3], i)}
                    if current_dist["score"] > best_dist[i]["score"]:
                        best_dist[i] = current_dist

    return best_dist


def log_to_file(text, log_file='log.txt'):
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f'{current_datetime}: {text}\n'
    with open(log_file, 'a') as f:
        f.write(log_message)
    f.close()


print("Starting...")
x = threading.Thread(target=thread_discord)
y = threading.Thread(target=thread_ping)
x.start()
y.start()
safe_print("Starting server")
app.run(port=8002, host="0.0.0.0")
