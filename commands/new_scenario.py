from discord_bot import bot, user_drafts
from scenarios import World
from discord.ext import commands
from utils.embeds import Embeds

class newScenarioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="new_scenario")
    async def new_scenario(self, ctx):
        user_drafts[ctx.author.id] = World(factions={}, regions={})
        await ctx.send(embed=Embeds.create_success_embed("New draft scenario created", "Use `!add_faction` and `!add_region` to build it."))

async def setup(bot):
    await bot.add_cog(newScenarioCog(bot))
