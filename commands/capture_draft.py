from bot import engine, bot, user_drafts
from scenarios import world_to_dict, world_from_dict
from discord.ext import commands
from utils.embeds import Embeds

class captureDraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="capture_draft")
    async def capture_draft(self, ctx):
        if not engine.world:
            await ctx.send(embed=Embeds.create_error_embed("No active simulation to capture."))
            return
        
        world_dict = world_to_dict(engine.world)
        user_drafts[ctx.author.id] = world_from_dict(world_dict)
        await ctx.send(embed=Embeds.create_success_embed("Draft captured", "Active simulation state captured into your draft! You can now modify it and use `!start_custom`."))

async def setup(bot):
    await bot.add_cog(captureDraftCog(bot))
