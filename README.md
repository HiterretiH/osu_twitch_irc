# Description
Useful twitch chatbot for osu! streamers 

# Table of Contents
- [Features](#features)
- [Usage](#usage)
- [Config variables desription](#config-variables-desription)
- [How to edit text commands](#how-to-edit-text-commands)

# Features
- Simple text commands
- Current map and skin (!map, !np, !song, !skin)
- Song request from twitch chat (bot catch map urls in chat messages and send to osu! user)

# Usage
1. Download repository
2. Download [gosumemory](https://github.com/l3lackShark/gosumemory/releases)
3. Fill in config.py
4. Run gosumemory 
5. Run main.py with python

# Config variables desription
| Variable | Description | Where you can get it |
| :---: | :---: | :---: |
| osuirc_name | Bot osu account username | https://osu.ppy.sh/p/irc |
| osuirc_password | Bot Bancho IRC account password (not from main account) | https://osu.ppy.sh/p/irc |
| osuirc_destination | Username of usu account, which will receive song requests from chat. Should be different with `osuirc_name` | Account page |
| osuapi_id | Oauth application id (you need to create it first) | https://osu.ppy.sh/home/account/edit#new-oauth-application |
| osuapi_secret | Oauth application secret | https://osu.ppy.sh/home/account/edit#new-oauth-application |
| twitch_name | Bot twitch account username | Account page |
| twitch_password | Bot OAuth twitch IRC token (including "oauth:") | https://twitchapps.com/tmi/ |
| twitch_channel | Twitch channel name on which bot will work | Account page |

# How to edit text commands
Open `commands.txt`
You will see following examples:
```
hi, hello :: hi
o/ :: o/
!profile :: https://osu.ppy.sh/users/2
```
- To the left of `::` there is comma-separated list of commands
- To the right of `::` there is reply message for this commands
- Lines, started with `#` - comments and will be skipped on file reading

For given examples:
- If someone send "hi" or "hello" in chat, Bot will reply with "@username, hi"
- If someone send "o/" in chat, Bot will reply with "@username, o/"
- If someone send "!profile" in chat, Bot will reply with "@username, https://osu.ppy.sh/users/2"

If you want to add your own conmmands, just add new lines with them in file
