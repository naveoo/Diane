from bot import engine
from scenarios import create_demo_scenario
from bot import bot
from discord.ext import commands
from utils.embeds import Embeds

class startCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="start")
    async def start_sim(self, ctx, name: str = "New Session"):
        engine.create_session(name)
        world = create_demo_scenario()
        engine.initialize_world(world)
        await ctx.send(embed=Embeds.create_success_embed("Session started", f"Session **{name}** started! ID: `{engine.session_id}`"))

async def setup(bot):
    await bot.add_cog(startCog(bot))