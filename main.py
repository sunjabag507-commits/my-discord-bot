import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# 1. 렌더용 가짜 웹 서버 설정
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # 렌더가 정해주는 포트를 사용하거나 기본 10000번 사용
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# 2. 디스코드 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# --- 본인의 봇 명령어들을 이 아래에 붙여넣으세요 ---

# --- --------------------------------------- ---

# 3. 봇 실행
if __name__ == "__main__":
    keep_alive() # 웹 서버 먼저 켜기
    token = os.environ.get('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("토큰이 설정되지 않았습니다. Render의 Environment를 확인하세요.")
