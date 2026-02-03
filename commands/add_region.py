from discord_bot import bot, user_drafts
from discord.ext import commands
from domains.region import Region
from domains.region_meta import EnvironmentType, RegionSocioEconomic
from utils.embeds import Embeds

class addRegionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="add_region")
    async def add_region(self, ctx, rid: str, name: str, owner_id: str = None, env_type: str = "RURAL", infra: float = 20.0):
        if ctx.author.id not in user_drafts:
            await ctx.send(embed=Embeds.create_error_embed("Use `!new_scenario` first."))
            return
    
        env = EnvironmentType.from_str(env_type)
        se = RegionSocioEconomic(infrastructure=infra, cohesion=100.0)
    
        region = Region(id=rid, name=name, population=1000, owner=owner_id, environment=env, socio_economic=se)
        user_drafts[ctx.author.id].regions[rid] = region
    
        if owner_id and owner_id in user_drafts[ctx.author.id].factions:
            user_drafts[ctx.author.id].factions[owner_id].regions.add(rid)
        
        await ctx.send(embed=Embeds.create_success_embed("Region added", f"Region **{name}** added ({env.value}, Infra: {infra}%)."))

async def setup(bot):
    await bot.add_cog(addRegionCog(bot))
