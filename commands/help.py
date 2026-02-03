from discord_bot import bot
from discord.ext import commands
from utils.embeds import Embeds
import discord

class HelpCog(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        self._original_help = bot.help_command
        bot.help_command = None
    
    @commands.command(name="help")
    async def help(self, ctx):
        embed_simulation = Embeds.create_info_embed(
            "Simulation Commands",
            "Core commands to run and manage your geopolitical simulation."
        )
        
        embed_simulation.add_field(
            name="▸ Start Simulation",
            value="```>!start```\nInitialize a new simulation with default parameters.",
            inline=False
        )
        
        embed_simulation.add_field(
            name="▸ Advance Time",
            value="```>!step <years>```\nProgress the simulation by a specified number of years.\n*Example: `>!step 5` advances 5 years*",
            inline=False
        )
        
        embed_simulation.add_field(
            name="▸ Current Status",
            value="```>!status```\nView the current state of all factions and regions.",
            inline=False
        )
        
        embed_simulation.add_field(
            name="▸ Metrics Dashboard",
            value="```>!metrics```\nDisplay comprehensive metrics and statistics for the simulation.",
            inline=False
        )
        
        embed_simulation.add_field(
            name="▸ Historical Timeline",
            value="```>!history```\nReview the complete event history of your simulation.",
            inline=False
        )
        
        embed_simulation.add_field(
            name="▸ Compare Factions",
            value="```>!compare <faction1_id> <faction2_id>```\nGenerate a detailed comparison between two factions.\n*Example: `>!compare 1 3`*",
            inline=False
        )
        
        embed_simulation.add_field(
            name="▸ Rankings",
            value="```>!rankings```\nView power rankings and standings of all factions.",
            inline=False
        )
        
        embed_simulation.add_field(
            name="▸ Save Draft",
            value="```>!capture_draft```\nCreate a snapshot of the current simulation state for later use.",
            inline=False
        )
        
        embed_simulation.add_field(
            name="▸ Load Session",
            value="```>!load <session_id>```\nRestore a previously saved simulation session.\n*Example: `>!load my_session_001`*",
            inline=False
        )
        
        embed_simulation.set_footer(text="Tip: Use >!help to view this menu anytime")
        
        embed_creation = Embeds.create_info_embed(
            "Scenario Creation Tools",
            "Build custom scenarios with complete control over factions, regions, and parameters."
        )
        
        embed_creation.add_field(
            name="▸ New Scenario",
            value="```>!new_scenario```\nInitiate the creation of a custom scenario from scratch.",
            inline=False
        )
        
        embed_creation.add_field(
            name="▸ Available Traits",
            value="```>!traits```\nList all faction traits and their effects on gameplay.",
            inline=False
        )
        
        embed_creation.add_field(
            name="▸ Add Faction",
            value="```>!add_faction```\nCreate a new faction with custom attributes and ideology.",
            inline=False
        )
        
        embed_creation.add_field(
            name="▸ Add Region",
            value="```>!add_region```\nDefine a new geographic region with specific characteristics.",
            inline=False
        )
        
        embed_creation.add_field(
            name="▸ Assign Territory",
            value="```>!assign_region <region_id> <faction_id>```\nAllocate a region to a specific faction's control.\n*Example: `>!assign_region region_1 faction_2`*",
            inline=False
        )
        
        embed_creation.add_field(
            name="▸ Import Scenario",
            value="```>!upload_scenario <file>```\nLoad a complete scenario from a JSON configuration file.",
            inline=False
        )
        
        embed_creation.add_field(
            name="▸ Preview Draft",
            value="```>!view_draft```\nReview your scenario configuration before launching.",
            inline=False
        )
        
        embed_creation.add_field(
            name="▸ Launch Custom Simulation",
            value="```>!start_custom```\nBegin simulation with your custom scenario configuration.",
            inline=False
        )
        
        embed_creation.set_footer(text="Custom scenarios allow for unique geopolitical experiments")
        
        embed_structural = Embeds.create_info_embed(
            "Structural Stability Metrics",
            "Key indicators measuring system balance and power distribution."
        )
        
        embed_structural.add_field(
            name="▸ Hegemony Index (HHI)",
            value=(
                "**Definition:** Herfindahl-Hirschman Index measuring power concentration.\n\n"
                "**High HHI (>0.25):** Hegemonic system with one dominant faction\n"
                "**Medium HHI (0.15-0.25):** Balanced multipolar system\n"
                "**Low HHI (<0.15):** Highly fragmented power distribution\n\n"
                "*Critical for predicting stability and conflict likelihood*"
            ),
            inline=False
        )
        
        embed_structural.add_field(
            name="▸ Power Gini Coefficient",
            value=(
                "**Definition:** Statistical measure of power inequality between factions.\n\n"
                "**High Gini (>0.6):** Severe power disparity, potential instability\n"
                "**Medium Gini (0.4-0.6):** Moderate inequality, competitive balance\n"
                "**Low Gini (<0.4):** Relatively equal power distribution\n\n"
                "*Indicates fairness and competitive balance in the system*"
            ),
            inline=False
        )
        
        embed_structural.add_field(
            name="▸ Ideological Polarization",
            value=(
                "**Definition:** Measures ideological distance and divergence between factions.\n\n"
                "**High Polarization (>70):** Extreme ideological differences, cooperation unlikely\n"
                "**Medium Polarization (40-70):** Significant but manageable differences\n"
                "**Low Polarization (<40):** Similar worldviews, easier diplomacy\n\n"
                "*Affects alliance formation and diplomatic success rates*"
            ),
            inline=False
        )
        
        embed_structural.set_footer(text="These metrics indicate system-wide stability patterns")
        
        embed_dynamics = Embeds.create_info_embed(
            "Global Dynamics Metrics",
            "World-level indicators tracking overall system health and tensions."
        )
        
        embed_dynamics.add_field(
            name="▸ Global Tension",
            value=(
                "**Definition:** Aggregate measure of conflicts, rivalries, and system stress.\n\n"
                "**High Tension (>75):** Multiple active conflicts, war imminent\n"
                "**Medium Tension (40-75):** Diplomatic disputes, occasional skirmishes\n"
                "**Low Tension (<40):** Peaceful era, stable relations\n\n"
                "*Primary indicator for predicting major wars and system shocks*"
            ),
            inline=False
        )
        
        embed_dynamics.add_field(
            name="▸ Average Legitimacy",
            value=(
                "**Definition:** Mean legitimacy score across all factions, reflecting public support.\n\n"
                "**High Avg (>70):** Strong popular backing, stable governance\n"
                "**Medium Avg (40-70):** Mixed public opinion, some discontent\n"
                "**Low Avg (<40):** Widespread dissatisfaction, risk of revolts\n\n"
                "*Correlates with internal stability and resistance to external pressure*"
            ),
            inline=False
        )
        
        embed_dynamics.add_field(
            name="▸ Average Infrastructure",
            value=(
                "**Definition:** Mean infrastructure development across all factions.\n\n"
                "**High Avg (>70):** Advanced economies, efficient logistics\n"
                "**Medium Avg (40-70):** Developing capabilities, mixed modernization\n"
                "**Low Avg (<40):** Limited development, vulnerable supply chains\n\n"
                "*Indicates overall technological and economic development level*"
            ),
            inline=False
        )
        
        embed_dynamics.set_footer(text="Monitor these to understand global trends and patterns")
        
        embed_advancement = Embeds.create_info_embed(
            "Advancement Metrics",
            "Tracking technological progress and knowledge accumulation."
        )
        
        embed_advancement.add_field(
            name="▸ Global Knowledge",
            value=(
                "**Definition:** Cumulative research and technological advancement across the system.\n\n"
                "**High Knowledge (>80):** Advanced technology era, breakthrough innovations\n"
                "**Medium Knowledge (40-80):** Industrial/information age capabilities\n"
                "**Low Knowledge (<40):** Pre-industrial or early industrial stage\n\n"
                "*Unlocks new possibilities and determines military/economic potential*\n"
                "*Higher knowledge accelerates all faction capabilities and strategies*"
            ),
            inline=False
        )
        
        embed_advancement.set_footer(text="Knowledge drives long-term competitive advantages")
        
        embed_faction = Embeds.create_info_embed(
            "Faction-Specific Metrics",
            "Individual faction performance indicators and power measurements."
        )
        
        embed_faction.add_field(
            name="▸ Composite Power Index (CPI)",
            value=(
                "**Definition:** Holistic power measurement combining military, economic, and influence.\n\n"
                "**Components:**\n"
                "• Military strength (30%)\n"
                "• Economic capacity (25%)\n"
                "• Diplomatic influence (20%)\n"
                "• Technological advancement (15%)\n"
                "• Territorial control (10%)\n\n"
                "*The ultimate measure of a faction's overall global standing*"
            ),
            inline=False
        )
        
        embed_faction.add_field(
            name="▸ Strategic Depth",
            value=(
                "**Definition:** Resilience measure based on territory size, diversity, and resources.\n\n"
                "**High Depth (>70):** Multiple regions, diverse resources, hard to defeat\n"
                "**Medium Depth (40-70):** Adequate buffer zones, some redundancy\n"
                "**Low Depth (<40):** Vulnerable to concentrated attacks, limited fallback\n\n"
                "*Critical for assessing defensive capabilities and endurance in prolonged conflicts*"
            ),
            inline=False
        )
        
        embed_faction.add_field(
            name="▸ Urbanization Rate",
            value=(
                "**Definition:** Percentage of population living in urban centers.\n\n"
                "**High Urbanization (>70%):** Modern economy, vulnerable to disruption\n"
                "**Medium Urbanization (40-70%):** Balanced development\n"
                "**Low Urbanization (<40%):** Rural economy, dispersed population\n\n"
                "*Affects economic output, military recruitment, and target vulnerability*"
            ),
            inline=False
        )
        
        embed_faction.set_footer(text="Use these for targeted strategic analysis")
        
        embed_socioeconomic = Embeds.create_info_embed(
            "Socio-Economic Metrics",
            "Economic performance and societal health indicators."
        )
        
        embed_socioeconomic.add_field(
            name="▸ Economic Intensity",
            value=(
                "**Definition:** Ratio of economic output to population size (GDP per capita proxy).\n\n"
                "**High Intensity (>1.5):** Wealthy, productive economy\n"
                "**Medium Intensity (0.8-1.5):** Moderate prosperity\n"
                "**Low Intensity (<0.8):** Struggling economy, limited resources\n\n"
                "*Determines military funding capacity and technological investment potential*"
            ),
            inline=False
        )
        
        embed_socioeconomic.add_field(
            name="▸ Support Gap",
            value=(
                "**Definition:** Difference between legitimacy score and actual popular support.\n\n"
                "**Large Gap (>30):** Disconnect between perception and reality, instability risk\n"
                "**Moderate Gap (15-30):** Normal political tensions\n"
                "**Small Gap (<15):** Aligned governance and public sentiment\n\n"
                "*Warning indicator for potential revolutions or regime changes*"
            ),
            inline=False
        )
        
        embed_socioeconomic.add_field(
            name="▸ Population",
            value=(
                "**Definition:** Total population under faction control.\n\n"
                "**Large Population (>100M):** Major demographic power, large workforce\n"
                "**Medium Population (30-100M):** Significant regional player\n"
                "**Small Population (<30M):** Limited manpower, must rely on quality over quantity\n\n"
                "*Fundamental resource determining military size and economic potential*"
            ),
            inline=False
        )
        
        embed_socioeconomic.set_footer(text="Economic health drives long-term competitiveness")
        
        embed_reference = Embeds.create_info_embed(
            "Quick Reference Guide",
            "Essential tips for effective simulation management."
        )
        
        embed_reference.add_field(
            name="Getting Started",
            value=(
                "1. Use `>!start` for a quick default simulation\n"
                "2. Use `>!new_scenario` for custom configurations\n"
                "3. Run `>!step 1` to begin the simulation timeline\n"
                "4. Check `>!status` regularly to monitor developments"
            ),
            inline=False
        )
        
        embed_reference.add_field(
            name="Monitoring Progress",
            value=(
                "• `>!metrics` provides high-level overview\n"
                "• `>!rankings` shows competitive standings\n"
                "• `>!history` reveals cause-and-effect chains\n"
                "• `>!compare` enables direct faction analysis"
            ),
            inline=False
        )
        
        embed_reference.add_field(
            name="Important Notes",
            value=(
                "• Save drafts regularly with `>!capture_draft`\n"
                "• Large time steps (>1000 years) may cause instability\n"
                "• Custom scenarios require all regions to be assigned\n"
                "• Metric interpretations depend on scenario context"
            ),
            inline=False
        )
        
        embed_reference.add_field(
            name="Need More Help?",
            value=(
                "• Review documentation: [https://github.com/naveoo/Diane/blob/main/README.md]\n"
                "• Report issues to the development team\n"
                "• Share feedback to improve the simulation"
            ),
            inline=False
        )
        
        
        await ctx.send(embed=embed_simulation)
        await ctx.send(embed=embed_creation)
        await ctx.send(embed=embed_structural)
        await ctx.send(embed=embed_dynamics)
        await ctx.send(embed=embed_advancement)
        await ctx.send(embed=embed_faction)
        await ctx.send(embed=embed_socioeconomic)
        await ctx.send(embed=embed_reference)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))