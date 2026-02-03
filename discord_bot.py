import os
import logging
import json
import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv

from core.engine import SimulationEngine
from scenarios import create_demo_scenario, load_scenario_json, world_from_dict, world_to_dict
from domains.faction import Faction
from domains.region import Region
from domains.world import World
from core.visualizer import MetricsVisualizer

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DiscordBot")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

engine = SimulationEngine("diane_simulation.db")
user_drafts = {}

@bot.event
async def on_ready():
    logger.info(f"Bot logged in as {bot.user}")
    print(f"Logged in as {bot.user}")

@bot.command(name="start")
async def start_sim(ctx, name: str = "New Session"):
    engine.create_session(name)
    world = create_demo_scenario()
    engine.initialize_world(world)
    await ctx.send(f"🚀 Session **{name}** started! ID: `{engine.session_id}`")

@bot.command(name="step")
async def step_sim(ctx, ticks: int = 1):
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

@bot.command(name="status")
async def status_sim(ctx):
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

@bot.command(name="metrics")
async def world_metrics(ctx):
    if not engine.world:
        await ctx.send("❌ Error: No session active.")
        return

    metrics = engine.get_metrics()
    w = metrics["world"]
    
    w_embed = discord.Embed(
        title="📊 Geopolitical Analytics Report", 
        description="Complex world-state analysis and statistical indicators.",
        color=discord.Color.dark_magenta()
    )
    
    struct_val = (
        f"**Hegemony (HHI)**: `{w['hegemony_hhi']}`\n"
        f"**Power Gini**: `{w['power_gini']}`\n"
        f"**Polarization**: `{w['polarization_score']}`"
    )
    w_embed.add_field(name="⚖️ Structural Stability", value=struct_val, inline=True)
    
    dyn_val = (
        f"**Global Tension**: `{w['global_tension']}`\n"
        f"**Avg Legitimacy**: `{w['avg_legitimacy']}`\n"
        f"**Avg Infra**: `{w['avg_infrastructure']}%`"
    )
    w_embed.add_field(name="📈 Global Dynamics", value=dyn_val, inline=True)
    
    tech_val = f"**Global Knowledge**: `{w['global_knowledge']}`"
    w_embed.add_field(name="🎓 Advancement", value=tech_val, inline=False)
    
    await ctx.send(embed=w_embed)
    
    try:
        power_chart = MetricsVisualizer.create_power_distribution_chart(engine.world)
        await ctx.send(file=discord.File(power_chart, 'power_distribution.png'))
        
        resource_chart = MetricsVisualizer.create_resource_security_chart(metrics)
        await ctx.send(file=discord.File(resource_chart, 'resource_security.png'))
        
        indicators_chart = MetricsVisualizer.create_world_indicators_chart(metrics)
        await ctx.send(file=discord.File(indicators_chart, 'world_indicators.png'))
    except Exception as e:
        logger.error(f"Chart generation error: {e}")
        await ctx.send("⚠️ Charts could not be generated.")
    
    f_metrics = metrics["factions"]
    sorted_f = sorted(f_metrics.items(), key=lambda x: x[1]['composite_power_index'], reverse=True)[:3]
    
    for fid, m in sorted_f:
        f = engine.world.factions[fid]
        f_embed = discord.Embed(title=f"🔎 Deep Analysis: {f.name}", color=discord.Color.from_str(f.color))
        
        geo_val = (
            f"**Composite Power (CPI)**: `{m['composite_power_index']}`\n"
            f"**Strategic Depth**: `{m['strategic_depth_index']}`\n"
            f"**Urbanization**: `{m['urbanization_rate']}%`"
        )
        f_embed.add_field(name="🌍 Geopolitical Footprint", value=geo_val, inline=True)
        
        soc_val = (
            f"**Econ Intensity**: `{m['economic_intensity']}`\n"
            f"**Support Gap**: `{m['support_gap']}`\n"
            f"**Population**: `{m['total_population']}`"
        )
        f_embed.add_field(name="📈 Socio-Economics", value=soc_val, inline=True)
        
        await ctx.send(embed=f_embed)

@bot.command(name="rankings")
async def show_rankings(ctx, category: str = "power"):
    if not engine.world:
        await ctx.send("❌ Error: No session active.")
        return
    
    from metrics import GeopoliticalMetrics
    
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
    
    embed = discord.Embed(title=title, color=discord.Color.gold())
    for i, (name, value) in enumerate(fields, 1):
        embed.add_field(name=f"{i}. {name}", value=value, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="compare")
async def compare_factions(ctx, fid1: str, fid2: str):
    if not engine.world:
        await ctx.send("❌ Error: No session active.")
        return
    
    from metrics import GeopoliticalMetrics
    comparison = GeopoliticalMetrics.compare_factions(engine.world, fid1, fid2)
    
    if "error" in comparison:
        await ctx.send(f"❌ {comparison['error']}")
        return
    
    f1 = comparison["faction_1"]
    f2 = comparison["faction_2"]
    
    embed = discord.Embed(
        title=f"⚔️ {f1['name']} vs {f2['name']}",
        description=f"Alliance Status: {'Allied 🤝' if comparison['are_allied'] else 'Not Allied'}",
        color=discord.Color.red() if not comparison['are_allied'] else discord.Color.green()
    )
    
    embed.add_field(
        name="💪 Power Ratio",
        value=f"`{comparison['power_ratio']}:1` ({f1['name']} advantage)" if comparison['power_ratio'] > 1 else f"`1:{1/comparison['power_ratio']:.2f}` ({f2['name']} advantage)",
        inline=False
    )
    
    embed.add_field(
        name="💰 Wealth Ratio",
        value=f"`{comparison['wealth_ratio']}:1`",
        inline=False
    )
    
    m1 = f1['metrics']
    m2 = f2['metrics']
    
    embed.add_field(
        name=f"📊 {f1['name']} Metrics",
        value=f"CPI: `{m1['composite_power_index']}`\nThreat: `{m1['threat_level']}`\nDipl. Influence: `{m1['diplomatic_influence']}`",
        inline=True
    )
    
    embed.add_field(
        name=f"📊 {f2['name']} Metrics",
        value=f"CPI: `{m2['composite_power_index']}`\nThreat: `{m2['threat_level']}`\nDipl. Influence: `{m2['diplomatic_influence']}`",
        inline=True
    )
    
    await ctx.send(embed=embed)

@bot.command(name="load")
async def load_sim(ctx, session_id: str):
    try:
        engine.load_session(session_id)
        await ctx.send(f"📂 Loaded session `{session_id}` at tick **{engine.current_tick}**.")
    except Exception as e:
        await ctx.send(f"❌ Failed to load session: {str(e)}")

@bot.command(name="new_scenario")
async def new_scenario(ctx):
    user_drafts[ctx.author.id] = World(factions={}, regions={})
    await ctx.send("🆕 New draft scenario created! Use `!add_faction` and `!add_region` to build it.")

@bot.command(name="capture_draft")
async def capture_draft(ctx):
    if not engine.world:
        await ctx.send("❌ Error: No active simulation to capture.")
        return
        
    world_dict = world_to_dict(engine.world)
    user_drafts[ctx.author.id] = world_from_dict(world_dict)
    await ctx.send("📸 Active simulation state captured into your draft! You can now modify it and use `!start_custom`.")

@bot.command(name="add_faction")
async def add_faction(ctx, fid: str, name: str, power: float = 50.0, legitimacy: float = 50.0, resources: float = 50.0, *traits: str):
    if ctx.author.id not in user_drafts:
        await ctx.send("❌ Error: Use `!new_scenario` first.")
        return
    
    from domains.power import Power
    from domains.economy import Resources
    
    faction = Faction(
        id=fid, 
        name=name, 
        power=Power(army=power), 
        legitimacy=legitimacy, 
        resources=Resources(credits=resources, food=50.0, energy=50.0, materials=50.0) # Defaults for realism
    )
    faction.traits = set(traits)
    user_drafts[ctx.author.id].factions[fid] = faction
    await ctx.send(f"✅ Faction **{name}** added to draft (Power: {power}, Legit: {legitimacy}).\n*Default food/energy/materials (50.0) assigned for stability.*")

@bot.command(name="add_region")
async def add_region(ctx, rid: str, name: str, owner_id: str = None, env_type: str = "RURAL", infra: float = 20.0):
    if ctx.author.id not in user_drafts:
        await ctx.send("❌ Error: Use `!new_scenario` first.")
        return
    
    from domains.region_meta import EnvironmentType, RegionSocioEconomic
    env = EnvironmentType.from_str(env_type)
    se = RegionSocioEconomic(infrastructure=infra, cohesion=100.0)
    
    region = Region(id=rid, name=name, population=1000, owner=owner_id, environment=env, socio_economic=se)
    user_drafts[ctx.author.id].regions[rid] = region
    
    if owner_id and owner_id in user_drafts[ctx.author.id].factions:
        user_drafts[ctx.author.id].factions[owner_id].regions.add(rid)
        
    await ctx.send(f"✅ Region **{name}** added ({env.value}, Infra: {infra}%).")

@bot.command(name="traits")
async def list_traits(ctx):
    traits = [
        "Militarist", "Pacifist", "Industrialist", "Technocrat", 
        "Populist", "Diplomat", "Imperialist", "Autocrat"
    ]
    await ctx.send(f"🎭 **Available Traits:**\n`" + "`, `".join(traits) + "`")

@bot.command(name="start_custom")
async def start_custom(ctx, name: str = "Custom Session"):
    if ctx.author.id not in user_drafts:
        await ctx.send("❌ Error: No draft found. Use `!new_scenario` or `!upload_scenario`.")
        return
    
    world = user_drafts[ctx.author.id]
    if not world.factions or not world.regions:
        await ctx.send("⚠️ Warning: Your draft is empty or incomplete.")
        return
        
    engine.create_session(name)
    engine.initialize_world(world)
    await ctx.send(f"🚀 Custom session **{name}** started! ID: `{engine.session_id}`")

@bot.command(name="upload_scenario")
async def upload_scenario(ctx):
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
        from scenarios import load_scenario_json
        world = load_scenario_json(content)
        user_drafts[ctx.author.id] = world
        await ctx.send("📥 Scenario uploaded and loaded into draft! Use `!start_custom` to begin.")
    except Exception as e:
        await ctx.send(f"❌ Error parsing scenario: {str(e)}")

@bot.command(name="view_draft")
async def view_draft(ctx):
    if ctx.author.id not in user_drafts:
        await ctx.send("❌ Error: No draft found.")
        return
    
    world = user_drafts[ctx.author.id]
    embed = discord.Embed(title="📝 Draft Scenario", color=discord.Color.orange())
    
    factions_str = ", ".join(f"{f.name} ({f.id})" for f in world.factions.values()) or "None"
    regions_str = ", ".join(f"{r.name} ({r.id})" for r in world.regions.values()) or "None"
    
    embed.add_field(name="Factions", value=factions_str, inline=False)
    embed.add_field(name="Regions", value=regions_str, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="assign_region")
async def assign_region(ctx, rid: str, fid: str):
    if ctx.author.id not in user_drafts:
        await ctx.send("❌ Error: Use `!new_scenario` first.")
        return
    
    draft = user_drafts[ctx.author.id]
    if rid not in draft.regions:
        await ctx.send(f"❌ Error: Region `{rid}` not found in draft.")
        return
    if fid not in draft.factions:
        await ctx.send(f"❌ Error: Faction `{fid}` not found in draft.")
        return
    
    old_owner = draft.regions[rid].owner
    if old_owner and old_owner in draft.factions:
        draft.factions[old_owner].regions.discard(rid)
        
    draft.regions[rid].owner = fid
    draft.factions[fid].regions.add(rid)
    
    await ctx.send(f"✅ Region **{draft.regions[rid].name}** assigned to **{draft.factions[fid].name}**.")

@bot.command(name="history")
async def show_history(ctx):
    if not engine.session_id:
        await ctx.send("❌ Error: No session active.")
        return
    
    await ctx.send("📊 Generating historical charts... This may take a moment.")
    
    try:
        snapshots = engine.persistence.get_all_snapshots(engine.session_id)
        
        if len(snapshots) < 2:
            await ctx.send("❌ Not enough historical data. Run more ticks first.")
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
        await ctx.send(f"✅ Historical analysis complete! Ticks: {min_tick} → {max_tick}")
        
    except Exception as e:
        logger.error(f"History chart error: {e}")
        await ctx.send(f"⚠️ Error generating historical charts: {str(e)}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    await ctx.send(f"⚠️ Error: {str(error)}")

if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: BOT_TOKEN not found in .env")
    else:
        bot.run(TOKEN)
