from bot import bot, discord, user_drafts
from discord.ext import commands
from utils.embeds import Embeds

class viewDraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="view_draft")
    async def view_draft(self, ctx):
        if ctx.author.id not in user_drafts:
            await ctx.send(embed=Embeds.create_error_embed("No draft found."))
            return
    
        world = user_drafts[ctx.author.id]
        embed = Embeds.create_info_embed(title="Draft Scenario")
    
        factions_str = ", ".join(f"{f.name} ({f.id})" for f in world.factions.values()) or "None"
        regions_str = ", ".join(f"{r.name} ({r.id})" for r in world.regions.values()) or "None"
    
        embed.add_field(name="Factions", value=factions_str, inline=False)
        embed.add_field(name="Regions", value=regions_str, inline=False)
    
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(viewDraftCog(bot))
