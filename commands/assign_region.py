from discord_bot import bot, user_drafts
from discord.ext import commands
from utils.embeds import Embeds

class assignRegionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="assign_region")
    async def assign_region(self, ctx, rid: str, fid: str):
        if ctx.author.id not in user_drafts:
            await ctx.send(embed=Embeds.create_error_embed("Use `!new_scenario` first."))
            return
    
        draft = user_drafts[ctx.author.id]
        if rid not in draft.regions:
            await ctx.send(embed=Embeds.create_error_embed(f"Region `{rid}` not found in draft."))
            return
        if fid not in draft.factions:
            await ctx.send(embed=Embeds.create_error_embed(f"Faction `{fid}` not found in draft."))
            return
    
        old_owner = draft.regions[rid].owner
        if old_owner and old_owner in draft.factions:
            draft.factions[old_owner].regions.discard(rid)
        
        draft.regions[rid].owner = fid
        draft.factions[fid].regions.add(rid)
    
        await ctx.send(embed=Embeds.create_success_embed("Region assigned", f"Region **{draft.regions[rid].name}** assigned to **{draft.factions[fid].name}**."))

async def setup(bot):
    await bot.add_cog(assignRegionCog(bot))
