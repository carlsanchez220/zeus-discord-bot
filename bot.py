import discord
import asyncio
from datetime import datetime, timedelta
import pytz
from discord.ext import commands

TOKEN = "MTQ1NTE2MTM0NzczMzE5Njk0NA.GEuT01._jk2a4wtkDXxFmdcUdDA_0ePasLqLuJzQIWPmw"
CHANNEL_ID = 1455030674946789376
SEASON_IMAGE_URL = "https://cdn.discordapp.com/attachments/1455030580185141261/1455175846519111701/baddies.PNG?ex=6953c59d&is=6952741d&hm=dd52300618d267de8c51c64a1d4951ac56db4aeb6d9cd7e9d0937984612f4a87&"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
cst = pytz.timezone("US/Central")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.loop.create_task(sunday_announcement())

# ✅ COMMAND: !baddies
@bot.command()
async def baddies(ctx):
    await ctx.send("@everyone **baddie baddie shot o clock** 🔥")

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

        await asyncio.sleep(604800)

bot.run(TOKEN)


