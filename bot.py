import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# --------------------
# Flask web server
# --------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

# --------------------
# Discord bot setup
# --------------------
TOKEN = os.environ.get("DISCORD_TOKEN")  # set this on Render

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def baddies(ctx):
    await ctx.send("🚨 **NEW BADDIES EPISODE OUT NOW ON ZEUS** 🔥")

bot.run(TOKEN)
