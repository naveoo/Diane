from discord_bot import engine, bot
from discord.ext import commands

class loadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="load")
    async def load_sim(self, ctx, session_id: str):
        try:
            engine.load_session(session_id)
            await ctx.send(f"📂 Loaded session `{session_id}` at tick **{engine.current_tick}**.")
        except Exception as e:
            await ctx.send(f"❌ Failed to load session: {str(e)}")

async def setup(bot):
    await bot.add_cog(loadCog(bot))
