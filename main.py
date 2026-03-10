import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread
from datetime import datetime

# 1. Render 서버 유지용 웹 서버 설정
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Render가 주는 포트를 자동으로 사용
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# 2. 봇 설정 및 출석 저장용 변수
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 출석 명단 (봇이 재시작되면 초기화됩니다)
attendance_list = {}

# 3. 명령어 추가

# [출석체크 명령어]
@bot.command()
async def 출석(ctx):
    user_id = ctx.author.id
    today = datetime.now().strftime("%Y-%m-%d")

    if user_id in attendance_list and attendance_list[user_id] == today:
        await ctx.send(f'⚠️ {ctx.author.display_name}님, 이미 오늘 출석체크를 하셨습니다! 내일 다시 만나요! 🤗')
    else:
        attendance_list[user_id] = today
        await ctx.send(f'✅ {ctx.author.display_name}님, {today} 출석 완료! 반갑습니다! ✨')

# [핑 확인 명령어]
@bot.command()
async def 핑(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 퐁! 현재 지연 시간은 **{latency}ms**입니다.')

# 4. 이벤트 처리
@bot.event
async def on_ready():
    print(f'성공! 봇 이름: {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # 명령어를 인식하도록 처리 (이게 있어야 !핑, !출석이 작동함)
    await bot.process_commands(message)

# 5. 실행
# 코드 맨 아랫부분
if __name__ == "__main__":
    keep_alive() # 웹 서버 실행
    
    # Render의 Environment에 적은 이름이랑 똑같아야 합니다!
    token = os.environ.get('DISCORD_TOKEN') 
    
    if token:
        bot.run(token)
    else:
        # 지금 이 메시지가 로그에 뜨고 있는 거예요!
        print("알림: DISCORD_TOKEN이 설정되지 않았습니다.")
