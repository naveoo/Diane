from discord_bot import engine
from discord_bot import bot
from discord.ext import commands

class stepCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="step")
    async def step_sim(self, ctx, ticks: int = 1):
        if not engine.session_id:
            await ctx.send("❌ Error: No session active. Use `!start` first.")
            return
    
        await ctx.send(f"⏳ Running **{ticks}** ticks...")
    
        events = engine.step(ticks)
    
        if events:
            display_events = events[-10:]
            events_str = "\n".join(display_events)
            if len(events) > 10:
                events_str = f"... (showing last 10 of {len(events)} events) ...\n" + events_str
            await ctx.send(f"📜 **Latest Events:**\n```\n{events_str}\n```")
    
        await ctx.send(f"✅ Simulation advanced to tick **{engine.current_tick}**.")

async def setup(bot):
    await bot.add_cog(stepCog(bot))
