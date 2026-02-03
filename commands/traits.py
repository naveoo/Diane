from discord_bot import bot
from discord.ext import commands
from utils.embeds import Embeds 

class traitsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="traits")
    async def list_traits(self, ctx):
        traits = [
            "Militarist", "Pacifist", "Industrialist", "Technocrat", 
            "Populist", "Diplomat", "Imperialist", "Autocrat"
        ]
        await ctx.send(embed=Embeds.create_info_embed(title="Available Traits", description=f"`" + "`, `".join(traits) + "`"))

async def setup(bot):
    await bot.add_cog(traitsCog(bot))