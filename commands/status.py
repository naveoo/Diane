from discord_bot import engine
from discord_bot import bot
from discord.ext import commands

class statusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="status")
    async def status_sim(self, ctx):
        if not engine.world:
            await ctx.send("❌ Error: No world initialized.")
            return
        
        active_factions = [f for f in engine.world.factions.values() if f.is_active]
        collapsed_count = len(engine.world.factions) - len(active_factions)
        
        embeds = []
        
        main_embed = discord.Embed(title="🌍 Simulation Status", color=discord.Color.blue())
        main_embed.add_field(name="Current Tick", value=str(engine.current_tick), inline=False)
        main_embed.add_field(name="Summary", value=f"Active Factions: {len(active_factions)}\nCollapsed: {collapsed_count}", inline=False)
        embeds.append(main_embed)
        
        faction_chunks = [active_factions[i:i + 10] for i in range(0, len(active_factions), 10)]
        
        for i, chunk in enumerate(faction_chunks[:5]):
            embed = discord.Embed(title=f"🚩 Active Factions (Part {i+1})", color=discord.Color.green())
            for f in chunk:
                res = f.resources
                p = f.power
                
                env_icons = ""
                total_infra = 0.0
                from domains.region_meta import EnvironmentType
                icons = {
                    EnvironmentType.URBAN: "🏙️",
                    EnvironmentType.RURAL: "🚜",
                    EnvironmentType.INDUSTRIAL: "🏭",
                    EnvironmentType.COASTAL: "⚓",
                    EnvironmentType.WILDERNESS: "🌲"
                }
                for rid in f.regions:
                    r = engine.world.get_region(rid)
                    if r:
                        env_icons += icons.get(r.environment, "📍")
                        total_infra += r.socio_economic.infrastructure
                
                avg_infra = total_infra / max(len(f.regions), 1)
                
                status = (
                    f"📊 **P**: {p.total:.1f} (⚔️{p.army:.0f} ⚓{p.navy:.0f} 🦅{p.air:.0f})\n"
                    f"📜 **L**: {f.legitimacy:.1f} | 🧠 **K**: {f.knowledge:.1f}\n"
                    f"💰 {res.credits:.0f} | 🛠️ {res.materials:.0f} | � {res.food:.0f} | ⚡ {res.energy:.0f} | �🏛️ {res.influence:.0f}\n"
                    f"📍 Regions: {len(f.regions)} {env_icons} ({avg_infra:.0f}% infra)"
                )
                embed.add_field(name=f"🚩 {f.name}", value=status, inline=False)
            embeds.append(embed)
        
        if len(faction_chunks) > 5:
            embeds[-1].set_footer(text=f"... and {len(active_factions) - 50} more active factions.")

        for e in embeds:
            await ctx.send(embed=e)

async def setup(bot):
    await bot.add_cog(statusCog(bot))
