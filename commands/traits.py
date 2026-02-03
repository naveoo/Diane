from discord_bot import bot
from discord.ext import commands

class traitsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="traits")
    async def list_traits(self, ctx):
        traits = [
            "Militarist", "Pacifist", "Industrialist", "Technocrat", 
            "Populist", "Diplomat", "Imperialist", "Autocrat"
        ]
        await ctx.send(f"🎭 **Available Traits:**\n`" + "`, `".join(traits) + "`")

async def setup(bot):
    await bot.add_cog(traitsCog(bot))