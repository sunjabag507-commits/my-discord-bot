import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# 렌더가 죽이지 못하게 아주 가벼운 웹 서버만 유지
app = Flask('')
@app.route('/')
def home(): return "OK"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# 봇 본체
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'성공! 봇 이름: {bot.user.name}')

# --- 여기에 본인 명령어 추가 ---

if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ.get('DISCORD_TOKEN'))
