from discord_bot import bot, discord, user_drafts
from discord.ext import commands

class viewDraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="view_draft")
    async def view_draft(self, ctx):
        if ctx.author.id not in user_drafts:
            await ctx.send("❌ Error: No draft found.")
            return
    
        world = user_drafts[ctx.author.id]
        embed = discord.Embed(title="📝 Draft Scenario", color=discord.Color.orange())
    
        factions_str = ", ".join(f"{f.name} ({f.id})" for f in world.factions.values()) or "None"
        regions_str = ", ".join(f"{r.name} ({r.id})" for r in world.regions.values()) or "None"
    
        embed.add_field(name="Factions", value=factions_str, inline=False)
        embed.add_field(name="Regions", value=regions_str, inline=False)
    
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(viewDraftCog(bot))
