from bot import bot, engine
from core.visualizer import MetricsVisualizer
import json
import discord
from discord.ext import commands
from utils.embeds import Embeds

class historyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="history")
    async def show_history(self, ctx):
        if not engine.session_id:
            await ctx.send(embed=Embeds.create_error_embed("No active simulation to capture."))
            return
    
        await ctx.send(embed=Embeds.create_info_embed("Generating historical charts... This may take a moment."))
    
        try:
            snapshots = engine.persistence.get_sampled_snapshots(engine.session_id, max_points=100)
        
            if len(snapshots) < 2:
                await ctx.send(embed=Embeds.create_error_embed("Not enough historical data. Run more ticks first."))
                return
        
            historical_data = []
            for tick, world_json in snapshots:
                world_data = json.loads(world_json)
            
                factions_dict = {}
                for fid, f_data in world_data['factions'].items():
                    power_total = f_data['power'].get('army', 0) + f_data['power'].get('navy', 0) + f_data['power'].get('air', 0)
                    factions_dict[fid] = {
                        'name': f_data['name'],
                        'color': f_data.get('color', '#808080'),
                        'power': power_total,
                        'legitimacy': f_data.get('legitimacy', 50),
                        'resources': f_data.get('resources', {}),
                        'is_active': f_data.get('is_active', True)
                    }
                
                historical_data.append({
                    'tick': tick,
                    'factions': factions_dict
                })
        
            power_chart = MetricsVisualizer.create_power_evolution_chart(historical_data)
            await ctx.send(file=discord.File(power_chart, 'power_evolution.png'))
        
            legitimacy_chart = MetricsVisualizer.create_legitimacy_evolution_chart(historical_data)
            await ctx.send(file=discord.File(legitimacy_chart, 'legitimacy_evolution.png'))
        
            resources_chart = MetricsVisualizer.create_resources_evolution_chart(historical_data)
            await ctx.send(file=discord.File(resources_chart, 'resources_evolution.png'))
        
            min_tick, max_tick = engine.persistence.get_tick_range(engine.session_id)
            await ctx.send(embed=Embeds.create_success_embed("Historical analysis complete", f"Ticks: {min_tick} → {max_tick}"))
        
        except Exception as e:
            await ctx.send(embed=Embeds.create_error_embed(f"Error generating historical charts: {str(e)}"))

async def setup(bot):
    await bot.add_cog(historyCog(bot))  
