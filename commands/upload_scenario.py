from discord_bot import bot, user_drafts
import aiohttp
from scenarios import load_scenario_json
from discord.ext import commands

class uploadScenarioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="upload_scenario")
    async def upload_scenario(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("❌ Error: Please attach a `.json` scenario file.")
            return
    
        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith(".json"):
            await ctx.send("❌ Error: Attachment must be a `.json` file.")
            return
        
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as resp:
                if resp.status != 200:
                    await ctx.send("❌ Error: Could not download file.")
                    return
                content = await resp.text()
            
        try:
            world = load_scenario_json(content)
            user_drafts[ctx.author.id] = world
            await ctx.send("📥 Scenario uploaded and loaded into draft! Use `!start_custom` to begin.")
        except Exception as e:
            await ctx.send(f"❌ Error parsing scenario: {str(e)}")

async def setup(bot):
    await bot.add_cog(uploadScenarioCog(bot))
