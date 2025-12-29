import os
import discord
import asyncio
from datetime import datetime, timedelta
import pytz
from discord.ext import commands

# ----------------------
# Discord bot setup
# ----------------------
TOKEN = os.getenv("TOKEN")  # Make sure your token is stored as an environment variable
CHANNEL_ID = 1455030674946789376
SEASON_IMAGE_URL = "https://cdn.discordapp.com/attachments/1455030580185141261/1455175846519111701/baddies.PNG"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
cst = pytz.timezone("US/Central")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Start the Sunday announcement task
    bot.loop.create_task(sunday_announcement())

# ✅ COMMAND: !baddies
@bot.command()
async def baddies(ctx):
    await ctx.send("@everyone **baddie baddie shot o clock** 🔥")

# ✅ COMMAND: !postbaddies
@bot.command()
async def postbaddies(ctx):
    embed = discord.Embed(
        title="🚨 NEW BADDIES EPISODE OUT NOW 🚨",
        description=(
            "**A new episode just dropped on Zeus Network** 🔥\n\n"
            "👀 Don’t miss it\n"
            "📺 Watch now on Zeus Network\n"
            "Click here www.thezeusnetwork.com and enjoy!"
        ),
        color=0xff0055
    )
    embed.set_image(url=SEASON_IMAGE_URL)
    embed.set_footer(text="Zeus Network • Sundays")
    await ctx.send("@everyone", embed=embed)

# ✅ SUNDAY POST
async def sunday_announcement():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.now(cst)
        days_ahead = (6 - now.weekday()) % 7
        next_sunday = now + timedelta(days=days_ahead)
        target_time = next_sunday.replace(hour=17, minute=0, second=0, microsecond=0)

        if now >= target_time:
            target_time += timedelta(days=7)

        wait_seconds = (target_time - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        channel = bot.get_channel(CHANNEL_ID)
        embed = discord.Embed(
            title="🚨 NEW BADDIES EPISODE OUT NOW 🚨",
            description=(
                "**A new episode just dropped on Zeus Network** 🔥\n\n"
                "👀 Don’t miss it\n"
                "📺 Watch now on Zeus"
            ),
            color=0xff0055
        )
        embed.set_image(url=SEASON_IMAGE_URL)
        embed.set_footer(text="Zeus Network • Sundays")
        await channel.send("@everyone", embed=embed)

        # Wait 7 days until the next Sunday
        await asyncio.sleep(604800)

# ----------------------
# Run the bot
# ----------------------
bot.run(TOKEN)
