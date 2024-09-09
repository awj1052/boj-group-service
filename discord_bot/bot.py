import os, db, datetime
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("BOT_CHANNEL_ID"))

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
    # await bot.change_presence(status=discord.Status.online, activity=discord.Game("대기"))

@bot.command()
async def member(ctx, *args):
    if ctx.channel.id != CHANNEL_ID: return

    message = [
        "명령어```",
        "!member list",
        "!member truncate",
        "!member add [name]",
        "!member delete [name]",
        "!member bias [name] [number]```"
    ]
    try:
        if len(args) >= 1:
            if args[0] == "list":
                response = db.get_member()
                message = []
                for row in response:
                    s = str(row[0])
                    if row[1] != 0: s+=f'({row[1]})'
                    message.append(s)
                s = "member list"
                if len(message) > 0:
                    s += "\n```" + ", ".join(message) + "```"
                await ctx.send(s)
                return
            elif args[0] == "truncate":
                rows = db.truncate_member()
                message = [
                    f"{rows}개의 행을 지웠습니다."
                ]            
            elif args[0] == "add" and len(args) >= 2:
                try:
                    db.add_member(args[1])
                    message = [
                        f"{args[1]} 을 추가했습니다."
                    ]
                except:
                    message = [
                        "이미 존재하는 아이디입니다."
                    ]
            elif args[0] == "delete" and len(args) >= 2:
                rows = db.delete_member(args[1])
                message = [
                    f"{rows}개의 행을 지웠습니다."
                ]
            elif args[0] == "bias" and len(args) >= 3:
                rows = db.update_bias(args[1], args[2])
                message = [
                    f"{rows}개의 행을 업데이트했습니다."
                ]
    except:
        message = [ "오류가 발생했습니다." ]
    await ctx.send('\n'.join(message))

@bot.command()
async def event(ctx, *args):
    if ctx.channel.id != CHANNEL_ID: return

    message = [
        "명령어```",
        "!event list",
        "!event truncate",
        "!event add [description] [start_time] [end_time] [problem_id]",
        "!event delete [id|description]```"
    ]
    try:
        if len(args) >= 1:
            if args[0] == "list":
                response = db.get_event()
                message = [
                    "ID\tDESCRIPTION\tSTART_TIME\tEND_TIME\tPROBLEM_ID"
                ]
                for row in response:
                    message.append('\t'.join(map(str,row)) + "")
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
    except:
        message = [ "오류가 발생했습니다." ]
    await ctx.send('\n'.join(message))

bot.run(TOKEN)
db.close()