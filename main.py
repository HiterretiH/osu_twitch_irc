import osu
import twitch
import gosumemory
import config
import re
from threading import Timer

req_cnt = 0
req_max = 45  # 45 api requests per minute
req_timeout = 60
def send_beatmap(name, beatmap):
    global req_cnt
    if req_cnt >= req_max:
        Timer(5, send_beatmap, [name, beatmap]).start()
        return
    req_cnt += 1
    info = osuapi.get_beatmap( beatmap[beatmap.rfind("/")+1:] )
    Timer(req_timeout, req_cnt_decrement).start()

    if len(info.keys()) == 1:
        twitchbot.reply(name, "error getting map info")
        return

    if info.get('mode') != "osu":
        twitchbot.reply(name, "only osu maps can be requested")
        return

    msg = f"""PRIVMSG {config.osuirc_destination} {name}: ({info.get('status')}) [osu.ppy.sh/b/{info.get('id')} 
{info.get('beatmapset').get('artist')} - {info.get('beatmapset').get('title')} [{info.get('version')}]] 
{info.get('total_length')//60}:{"%02i" % (info.get('total_length')%60)} ⏰, 
{info.get('difficulty_rating')} ⭐, {info.get('bpm')} bpm, {info.get('ar')} ar, 
{info.get('cs')} cs, {info.get('drain')} hp, {info.get('accuracy')} od, {info.get('max_combo')} max combo""".replace('\n', '')

    osubot.send(msg)
    twitchbot.reply(name, "request sent")

def req_cnt_decrement():
    global req_cnt
    req_cnt -= 1


osubot = osu.OsuBot(config.osuirc_name, config.osuirc_password)
osuapi = osu.OsuApi(config.osuapi_id, config.osuapi_secret)
twitchbot = twitch.TwitchBot(config.twitch_name, config.twitch_password, '#'+config.twitch_channel)

pattern = "osu.ppy.sh/b[\w/]*/\d{4,8}"
msg_sep = F"PRIVMSG {config.twitch_channel} :"

osubot.connect()
twitchbot.connect()
osuapi.get_token()

commands = dict()
with open("commands.txt", "r") as f:
    for line in f.readlines():
        if line.startswith("#"):
            continue
        if "::" in line:
            keys, repl = line.split("::")
            keys = keys.split(",")
            repl = repl.strip()
            for k in keys:
                commands.update({k.strip().lower(): repl})

while True:
    res = twitchbot.receive(2048).decode()
    if res:
        if "PING :tmi.twitch.tv" in res:
            twitchbot.send("PONG :tmi.twitch.tv")
            continue

        if "PRIVMSG" not in res:
            continue

        name = res[1:res.find("!")]
        msg = res[res.find(msg_sep) + len(msg_sep):].strip().lower()
        if name == config.twitch_name:
            continue

        maps = set(re.findall(pattern, msg))
        if len(maps) > 0:
            for beatmap in maps:
                send_beatmap(name, beatmap)
        elif msg[0] == "!" and len(msg) > 1:
            msg = msg[1:]
            if msg in ("map", "np", "song"):
                print(f"{name}: !{msg}")
                twitchbot.reply(name, f"https://osu.ppy.sh/b/{gosumemory.get_data()['menu']['bm']['id']}")
            elif msg == "skin":
                print(f"{name}: !{msg}")
                twitchbot.reply(name, f"current skin: {gosumemory.get_data()['settings']['folders']['skin']}")
            elif commands.get(msg):
                print(f"{name}: !{msg}")
                twitchbot.reply(name, commands.get(msg))
