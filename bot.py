import os
import logging
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

from core.engine import SimulationEngine

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DiscordBot")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

engine = SimulationEngine("diane_simulation.db")
user_drafts = {}

async def load_commands():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                await bot.load_extension(f"commands.{filename[:-3]}")
                logger.info(f"Commande chargée : {filename}")
            except Exception as e:
                logger.error(f"Erreur lors du chargement de {filename} : {e}")

@bot.event
async def on_ready():
    logger.info(f"Bot connected as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!help for commands list"))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    logger.error(f"Erreur de commande : {error}")
    await ctx.send(f"⚠️ Erreur : {str(error)}")

if __name__ == "__main__":
    if not TOKEN:
        logger.error("❌ ERREUR : BOT_TOKEN non trouvé dans le fichier .env")
    else:
        asyncio.run(load_commands())
        bot.run(TOKEN)
