from discord_bot import bot, user_drafts
import aiohttp
from scenarios import load_scenario_json
from discord.ext import commands
from utils.embeds import Embeds

class uploadScenarioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="upload_scenario")
    async def upload_scenario(self, ctx):
        if not ctx.message.attachments:
            await ctx.send(embed=Embeds.create_error_embed("No attachment found. Please attach a `.json` scenario file."))
            return
    
        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith(".json"):
            await ctx.send(embed=Embeds.create_error_embed("Invalid file type. Please attach a `.json` file."))
            return
        
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as resp:
                if resp.status != 200:
                    await ctx.send(embed=Embeds.create_error_embed("Could not download file."))
                    return
                content = await resp.text()
            
        try:
            world = load_scenario_json(content)
            user_drafts[ctx.author.id] = world
            await ctx.send(embed=Embeds.create_success_embed("Scenario uploaded", "Scenario uploaded and loaded into draft! Use `!start_custom` to begin."))
        except Exception as e:
            await ctx.send(embed=Embeds.create_error_embed(f"Error parsing scenario: {str(e)}"))

async def setup(bot):
    await bot.add_cog(uploadScenarioCog(bot))
