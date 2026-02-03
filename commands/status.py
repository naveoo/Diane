import discord
from bot import engine
from bot import bot
from discord.ext import commands
from utils.embeds import Embeds

class statusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="status")
    async def status_sim(self, ctx):
        if not engine.world:
            await ctx.send(embed=Embeds.create_error_embed("No active simulation to capture."))
            return
        
        active_factions = [f for f in engine.world.factions.values() if f.is_active]
        collapsed_count = len(engine.world.factions) - len(active_factions)
        
        embeds = []
        
        main_embed = Embeds.create_info_embed(title="Simulation Status")
        main_embed.add_field(name="Current Tick", value=str(engine.current_tick), inline=False)
        main_embed.add_field(name="Summary", value=f"Active Factions: {len(active_factions)}\nCollapsed: {collapsed_count}", inline=False)
        embeds.append(main_embed)
        
        faction_chunks = [active_factions[i:i + 10] for i in range(0, len(active_factions), 10)]
        
        for i, chunk in enumerate(faction_chunks[:5]):
            embed = Embeds.create_info_embed(title=f"Active Factions (Part {i+1})")
            for f in chunk:
                res = f.resources
                p = f.power
                
                env_icons = ""
                total_infra = 0.0
                from domains.region_meta import EnvironmentType
                icons = {
                    EnvironmentType.URBAN: "env",
                    EnvironmentType.RURAL: "rur",
                    EnvironmentType.INDUSTRIAL: "ind",
                    EnvironmentType.COASTAL: "coa",
                    EnvironmentType.WILDERNESS: "wil"
                }
                for rid in f.regions:
                    r = engine.world.get_region(rid)
                    if r:
                        env_icons += icons.get(r.environment)
                        total_infra += r.socio_economic.infrastructure
                
                avg_infra = total_infra / max(len(f.regions), 1)
                
                status = (
                    f"**P**: {p.total:.1f} (Army: {p.army:.0f} | Navy: {p.navy:.0f} | Air: {p.air:.0f})\n"
                    f"**L**: {f.legitimacy:.1f} | **K**: {f.knowledge:.1f}\n"
                    f"Credits: {res.credits:.0f} | Materials: {res.materials:.0f} | Food: {res.food:.0f} | Energy: {res.energy:.0f} | Influence: {res.influence:.0f}\n"
                    f"Regions: {len(f.regions)} {env_icons} ({avg_infra:.0f}% infra)"
                )
                embed.add_field(name=f"{f.name}", value=status, inline=False)
            embeds.append(embed)
        
        if len(faction_chunks) > 5:
            embeds[-1].set_footer(text=f"... and {len(active_factions) - 50} more active factions.")

        for e in embeds:
            await ctx.send(embed=e)

async def setup(bot):
    await bot.add_cog(statusCog(bot))
