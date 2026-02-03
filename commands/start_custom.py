from discord_bot import bot, engine, user_drafts
from discord.ext import commands

class startCustomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="start_custom")
    async def start_custom(self, ctx, name: str = "Custom Session"):
        if ctx.author.id not in user_drafts:
            await ctx.send("❌ Error: No draft found. Use `!new_scenario` or `!upload_scenario`.")
            return
    
        world = user_drafts[ctx.author.id]
        if not world.factions or not world.regions:
            await ctx.send("⚠️ Warning: Your draft is empty or incomplete.")
            return
        
        engine.create_session(name)
        engine.initialize_world(world)
        await ctx.send(f"🚀 Custom session **{name}** started! ID: `{engine.session_id}`")

async def setup(bot):
    await bot.add_cog(startCustomCog(bot))
