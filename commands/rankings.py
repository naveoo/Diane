from discord_bot import engine, bot
from discord import Embed, Color
from core.metrics import GeopoliticalMetrics
from discord.ext import commands

class rankingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="rankings")
    async def show_rankings(self, ctx, category: str = "power"):
        if not engine.world:
            await ctx.send("❌ Error: No session active.")
            return
    
        if category.lower() == "power":
            rankings = GeopoliticalMetrics.get_power_rankings(engine.world)
            title = "🏆 Power Rankings (Composite Power Index)"
            fields = [(r["name"], f"CPI: `{r['composite_power']}` | Power: `{r['raw_power']}` | Knowledge: `{r['knowledge']}`") for r in rankings[:10]]
        elif category.lower() == "economy":
            rankings = GeopoliticalMetrics.get_economic_rankings(engine.world)
            title = "💰 Economic Rankings (Total Wealth)"
            fields = [(r["name"], f"Wealth: `{r['total_wealth']}` | Credits: `{r['credits']}` | Materials: `{r['materials']}`") for r in rankings[:10]]
        elif category.lower() == "stability":
            rankings = GeopoliticalMetrics.get_stability_rankings(engine.world)
            title = "🛡️ Stability Rankings"
            fields = [(r["name"], f"Score: `{r['stability_score']}` | Legitimacy: `{r['legitimacy']}` | Cohesion: `{r['avg_cohesion']}`") for r in rankings[:10]]
        else:
            await ctx.send("❌ Invalid category. Use: `power`, `economy`, or `stability`.")
            return
    
        embed = Embed(title=title, color=Color.gold())
        for i, (name, value) in enumerate(fields, 1):
            embed.add_field(name=f"{i}. {name}", value=value, inline=False)
    
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(rankingsCog(bot))
