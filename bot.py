import os
import discord
import asyncio
from datetime import datetime, timedelta
import pytz
from discord.ext import commands
from flask import Flask
from threading import Thread

# --------------------
# Flask web server (keeps bot alive on Render)
# --------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

# ----------------------
# Discord bot setup
# ----------------------
TOKEN = os.getenv("DISCORD_TOKEN")  # Set this in Render environment variables
CHANNEL_ID = 1455030674946789376  # Replace with your Discord channel ID
SEASON_IMAGE_URL = "https://cdn.discordapp.com/attachments/1455030580185141261/1455175846519111701/baddies.PNG"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
cst = pytz.timezone("US/Central")

# ----------------------
# Scheduled Sunday Announcement
# ----------------------
async def sunday_announcement():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.now(cst)

        # Calculate next Sunday at 5 PM CST
        days_ahead = (6 - now.weekday()) % 7  # 6 = Sunday
        next_sunday = now + timedelta(days=days_ahead)
        target_time = next_sunday.replace(hour=17, minute=0, second=0, microsecond=0)

        if now >= target_time:
            target_time += timedelta(days=7)

        wait_seconds = (target_time - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        # Send the announcement
        channel = bot.get_channel(CHANNEL_ID)
        guild = channel.guild

        # Find the role named "Baddies"
        role = discord.utils.get(guild.roles, name="Baddies")

        embed = discord.Embed(
            title="🚨 NEW BADDIES EPISODE OUT NOW 🚨",
            description=(
                f"🔥 {role.mention if role else '@Baddies'} A new episode just dropped on Zeus Network!\n\n"
                "👀 Don’t miss it\n"
                "📺 Watch now: [Zeus Network](https://www.thezeusnetwork.com/)"
            ),
            color=0xff0055
        )
        embed.set_image(url=SEASON_IMAGE_URL)
        embed.set_footer(text="Zeus Network • Sundays")

        await channel.send(embed=embed)

        # Wait 7 days until next Sunday
        await asyncio.sleep(604800)  # 7 days in seconds

# ----------------------
# Bot events & commands
# ----------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    bot.loop.create_task(sunday_announcement())

@bot.command()
async def baddies(ctx):
    await ctx.send("@everyone **baddie baddie shot o clock** 🔥")

@bot.command()
async def postbaddies(ctx):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name="Baddies")

    embed = discord.Embed(
        title="🚨 NEW BADDIES EPISODE OUT NOW 🚨",
        description=(
            f"🔥 {role.mention if role else '@Baddies'} A new episode just dropped on Zeus Network!\n\n"
            "👀 Don’t miss it\n"
            "📺 Watch now: [Zeus Network](https://www.thezeusnetwork.com/)"
        ),
        color=0xff0055
    )
    embed.set_image(url=SEASON_IMAGE_URL)
    embed.set_footer(text="Zeus Network • Sundays")
    await ctx.send(embed=embed)

# ----------------------
# Run the bot
# ----------------------
bot.run(TOKEN)
