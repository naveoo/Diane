from discord_bot import engine, bot
from core.visualizer import MetricsVisualizer
from discord import File  
from discord.ext import commands
from utils.embeds import Embeds

class metricsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="metrics")
    async def world_metrics(self, ctx):
        if not engine.world:
            await ctx.send(embed=Embeds.create_error_embed("No active simulation to capture."))
            return

        metrics = engine.get_metrics()
        w = metrics["world"]
        
        w_embed = Embeds.create_info_embed(
            title="Geopolitical Analytics Report", 
            description="Complex world-state analysis and statistical indicators.",
        )
        
        struct_val = (
            f"**Hegemony (HHI)**: `{w['hegemony_hhi']}`\n"
            f"**Power Gini**: `{w['power_gini']}`\n"
            f"**Polarization**: `{w['polarization_score']}`"
        )
        w_embed.add_field(name="Structural Stability", value=struct_val, inline=True)
        
        dyn_val = (
            f"**Global Tension**: `{w['global_tension']}`\n"
            f"**Avg Legitimacy**: `{w['avg_legitimacy']}`\n"
            f"**Avg Infra**: `{w['avg_infrastructure']}%`"
        )
        w_embed.add_field(name="Global Dynamics", value=dyn_val, inline=True)
        
        tech_val = f"**Global Knowledge**: `{w['global_knowledge']}`"
        w_embed.add_field(name="Advancement", value=tech_val, inline=False)
        
        await ctx.send(embed=w_embed)
        
        try:
            power_chart = MetricsVisualizer.create_power_distribution_chart(engine.world)
            await ctx.send(file=File(power_chart, 'power_distribution.png'))
            
            resource_chart = MetricsVisualizer.create_resource_security_chart(metrics)
            await ctx.send(file=File(resource_chart, 'resource_security.png'))
            
            indicators_chart = MetricsVisualizer.create_world_indicators_chart(metrics)
            await ctx.send(file=File(indicators_chart, 'world_indicators.png'))
        except Exception as e:
            logger.error(f"Chart generation error: {e}")
            await ctx.send(embed=Embeds.create_error_embed("Charts could not be generated."))
        
        f_metrics = metrics["factions"]
        sorted_f = sorted(f_metrics.items(), key=lambda x: x[1]['composite_power_index'], reverse=True)[:3]
        
        for fid, m in sorted_f:
            f = engine.world.factions[fid]
            f_embed = Embeds.create_info_embed(title=f"Deep Analysis: {f.name}")
            
            geo_val = (
                f"**Composite Power (CPI)**: `{m['composite_power_index']}`\n"
                f"**Strategic Depth**: `{m['strategic_depth_index']}`\n"
                f"**Urbanization**: `{m['urbanization_rate']}%`"
            )
            f_embed.add_field(name="Geopolitical Footprint", value=geo_val, inline=True)
            
            soc_val = (
                f"**Econ Intensity**: `{m['economic_intensity']}`\n"
                f"**Support Gap**: `{m['support_gap']}`\n"
                f"**Population**: `{m['total_population']}`"
            )
            f_embed.add_field(name="Socio-Economics", value=soc_val, inline=True)
            
            await ctx.send(embed=f_embed)

async def setup(bot):
    await bot.add_cog(metricsCog(bot))
