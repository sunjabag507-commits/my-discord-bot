import discord
from discord.ext import commands
import datetime
import json
import os

# 봇 설정
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 출석 데이터 로드 (간이 데이터베이스)
def load_data():
    try:
        with open('attendance.json', 'r') as f:
            return json.load(f)
    except:
         return{}
        
def save_data(data):
    with open('attendance.json', 'w') as f:
        json.dump(data, f, indent=4)
        
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
@bot.command()
async def 출석(ctx):
    user_id = str(ctx.author.id)
    today = str(datetime.date.today())
    
    data = load_data()
    
    if user_id not in data:
        data[user_id] =[]
        
    if today in data[user_id]:
        await ctx.send(f"{ctx.author.mention}님, 오늘은 이미 출석체크를 하셨습니다.")
    else:
        data[user_id].append(today)
        save_data(data)
        count = len(data[user_id])
        await ctx.send(f"{ctx.author.mention}님, 출석 완료! (총 {count}회 출석)")
        
keep_alive()
bot.run(os.environ.get('MTQ4MDg0MDUzNjY0MTM3MjMyMQ.GdtXAA.Hmp7G4eVPZj5BIcoq5NzFHErRu4Co9IFJEJek0'))
        
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I am alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
