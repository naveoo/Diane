from discord_bot import engine, bot
from discord import Embed, Color
from core.metrics import GeopoliticalMetrics
from discord.ext import commands
from utils.embeds import Embeds

class compareCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="compare")
    async def compare_factions(self, ctx, fid1: str, fid2: str):
        if not engine.world:
            await ctx.send(embed=Embeds.create_error_embed("No active simulation to capture."))
            return
    
        comparison = GeopoliticalMetrics.compare_factions(engine.world, fid1, fid2)
    
        if "error" in comparison:
            await ctx.send(embed=Embeds.create_error_embed(comparison['error']))
            return
    
        f1 = comparison["faction_1"]
        f2 = comparison["faction_2"]
    
        embed = Embeds.create_info_embed(
            title=f"⚔️ {f1['name']} vs {f2['name']}",
            description=f"Alliance Status: {'Allied' if comparison['are_allied'] else 'Not Allied'}",
        )
    
        embed.add_field(
            name="Power Ratio",
            value=f"`{comparison['power_ratio']}:1` ({f1['name']} advantage)" if comparison['power_ratio'] > 1 else f"`1:{1/comparison['power_ratio']:.2f}` ({f2['name']} advantage)",
            inline=False
        )
    
        embed.add_field(
            name="Wealth Ratio",
            value=f"`{comparison['wealth_ratio']}:1`",
            inline=False
        )
    
        m1 = f1['metrics']
        m2 = f2['metrics']
    
        embed.add_field(
            name=f"{f1['name']} Metrics",
            value=f"CPI: `{m1['composite_power_index']}`\nThreat: `{m1['threat_level']}`\nDipl. Influence: `{m1['diplomatic_influence']}`",
            inline=True
        )
    
        embed.add_field(
            name=f"{f2['name']} Metrics",
            value=f"CPI: `{m2['composite_power_index']}`\nThreat: `{m2['threat_level']}`\nDipl. Influence: `{m2['diplomatic_influence']}`",
            inline=True
        )
    
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(compareCog(bot))