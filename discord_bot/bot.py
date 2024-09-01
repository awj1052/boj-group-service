import os, db, datetime
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("BOT_CHANNEL_ID")

COMMAND_PREFIX = "!"
DATETIME_FORMAT = "%Y-%m-%d/%H:%M:%S"

def str2datetime(s):
    return datetime.datetime.strptime(s, DATETIME_FORMAT)

import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print('Logged on as {0}'.format(bot.user.name))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("대기"))

@bot.command()
async def event(ctx, *args):
    message = [
        "명령어",
        "!event list",
        "!event truncate",
        "!event add [description] [start_time] [end_time] [problem_id]",
        "!event delete [id|description]```"
    ]
    if len(args) >= 1:
        if args[0] == "list":
            response = db.get_event()
            message = [
                "ID\tDESCRIPTION\tSTART_TIME\tEND_TIME\tPROBLEM_ID"
            ]
            for row in response:
                message.append('\t'.join(map(str,row)))
        elif args[0] == "truncate":
            rows = db.truncate_event()
            message = [
                f"{rows}개의 행을 지웠습니다."
            ]
        elif args[0] == "add" and len(args) >= 5:
            try:
                start_time = str2datetime(args[2])
                end_time = str2datetime(args[3])
                db.add_event(args[1], start_time, end_time, args[4])
                message = [
                    "이벤트를 추가했습니다."
                ]
            except:
                message = [
                    f"시간 형식은 다음과 같습니다. ```{DATETIME_FORMAT}```"
                ]
        elif args[0] == "delete" and len(args) >= 2:
            rows = 0
            try:
                id = int(args[1])
                rows = db.delete_event_by_id(id)
            except:
                rows = db.delete_event_by_description(args[1])
            message = [
                f"{rows}개의 행을 지웠습니다."
            ]
    await ctx.send('\n'.join(message))

bot.run(TOKEN)
db.close()