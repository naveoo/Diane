from discord_bot import engine
from discord_bot import bot
from discord.ext import commands
from utils.embeds import Embeds

class stepCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="step")
    async def step_sim(self, ctx, ticks: int = 1):
        if not engine.session_id:
            await ctx.send(embed=Embeds.create_error_embed("No active simulation to capture."))
            return
    
        await ctx.send(embed=Embeds.create_info_embed(title="Simulation running", description=f"Running **{ticks}** ticks..."))
    
        events = engine.step(ticks)
    
        if events:
            display_events = events[-10:]
            events_str = "\n".join(display_events)
            if len(events) > 10:
                events_str = f"... (showing last 10 of {len(events)} events) ...\n" + events_str
            await ctx.send(embed=Embeds.create_info_embed(title="Latest Events", description=f"```\n{events_str}\n```"))
    
        await ctx.send(embed=Embeds.create_success_embed(title="Ticks runned",description=f"Simulation advanced to tick **{engine.current_tick}**."))

async def setup(bot):
    await bot.add_cog(stepCog(bot))
