from discord_bot import bot, user_drafts
from discord.ext import commands
from domains.faction import Faction
from domains.power import Power
from domains.economy import Resources

class addFactionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="add_faction")
    async def add_faction(self, ctx, fid: str, name: str, power: float = 50.0, legitimacy: float = 50.0, resources: float = 50.0, *traits: str):
        if ctx.author.id not in user_drafts:
            await ctx.send("❌ Error: Use `!new_scenario` first.")
            return
    
        faction = Faction(
            id=fid, 
            name=name, 
            power=Power(army=power), 
            legitimacy=legitimacy, 
            resources=Resources(credits=resources, food=50.0, energy=50.0, materials=50.0) # Defaults for realism
        )
        faction.traits = set(traits)
        user_drafts[ctx.author.id].factions[fid] = faction
        await ctx.send(f"✅ Faction **{name}** added to draft (Power: {power}, Legit: {legitimacy}).\n*Default food/energy/materials (50.0) assigned for stability.*")

async def setup(bot):
    await bot.add_cog(addFactionCog(bot))