import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from typing import Dict, Any, List, Optional
from domains.world import World
import math

class MetricsVisualizer:
    @staticmethod
    def create_power_distribution_chart(world: World) -> io.BytesIO:
        try:
            factions = [f for f in world.factions.values() if f.is_active]
            
            if not factions:
                fig, ax = plt.subplots(figsize=(10, 8))
                ax.text(0.5, 0.5, 'No active factions', ha='center', va='center', 
                       fontsize=16, color='white')
                ax.set_facecolor('#2C2F33')
                fig.patch.set_facecolor('#2C2F33')
                ax.axis('off')
            else:
                names = [f.name for f in factions]
                powers = [max(f.power.total, 0.01) for f in factions]
                colors = [getattr(f, 'color', '#808080') for f in factions]
                
                fig, ax = plt.subplots(figsize=(10, 8))
                wedges, texts, autotexts = ax.pie(
                    powers, 
                    labels=names, 
                    autopct='%1.1f%%',
                    colors=colors,
                    startangle=90,
                    textprops={'color': 'white', 'weight': 'bold'}
                )
                
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(10)
                
                ax.set_title('Power Distribution', fontsize=16, weight='bold', pad=20, color='white')
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33')
            buf.seek(0)
            plt.close(fig)
            
            return buf
        except Exception as e:
            plt.close('all')
            raise Exception(f"Error creating power distribution chart: {str(e)}")
    
    @staticmethod
    def create_resource_security_chart(metrics: Dict[str, Any]) -> io.BytesIO:
        try:
            world_metrics = metrics.get('world', {})
            
            categories = ['Food Security', 'Energy Security']
            values = [
                world_metrics.get('food_security_index', 0),
                world_metrics.get('energy_security_index', 0)
            ]
            colors = ['#27AE60', '#F39C12']
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=2)
            
            ax.set_ylabel('Security Index', fontsize=12, weight='bold', color='white')
            ax.set_title('Global Resource Security', fontsize=16, weight='bold', pad=20, color='white')
            
            max_value = max(values) if values and max(values) > 0 else 10
            ax.set_ylim(0, max_value * 1.2)
            ax.grid(axis='y', alpha=0.3, linestyle='--', color='white')
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}',
                       ha='center', va='bottom', fontsize=12, weight='bold', color='white')
            
            ax.set_facecolor('#2C2F33')
            fig.patch.set_facecolor('#2C2F33')
            ax.tick_params(colors='white')
            ax.yaxis.label.set_color('white')
            ax.xaxis.set_tick_params(labelcolor='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33')
            buf.seek(0)
            plt.close(fig)
            
            return buf
        except Exception as e:
            plt.close('all')
            raise Exception(f"Error creating resource security chart: {str(e)}")
    
    @staticmethod
    def create_faction_comparison_radar(world: World, faction_ids: List[str]) -> io.BytesIO:
        try:
            categories = ['Power', 'Legitimacy', 'Resources', 'Knowledge', 'Regions']
            num_vars = len(categories)
            
            angles = [n / float(num_vars) * 2 * math.pi for n in range(num_vars)]
            angles += angles[:1]
            
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
            
            plotted_any = False
            for fid in faction_ids[:5]:
                if fid not in world.factions:
                    continue
                
                faction = world.factions[fid]
                if not faction.is_active:
                    continue
                
                values = [
                    min(faction.power.total / 10, 15),
                    min(faction.legitimacy / 10, 15),
                    min((faction.resources.credits + faction.resources.materials) / 50, 15),
                    min(faction.knowledge / 10, 15),
                    min(len(faction.regions), 15)
                ]
                values += values[:1]
                
                color = getattr(faction, 'color', '#808080')
                ax.plot(angles, values, 'o-', linewidth=2, label=faction.name, color=color)
                ax.fill(angles, values, alpha=0.15, color=color)
                plotted_any = True
            
            if not plotted_any:
                ax.text(0, 0, 'No factions to compare', ha='center', va='center',
                       fontsize=14, color='white')
            
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories, size=12, weight='bold', color='white')
            ax.set_ylim(0, 15)
            ax.set_title('Faction Comparison', size=16, weight='bold', pad=30, color='white')
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), framealpha=0.9)
            ax.grid(True, alpha=0.3, color='white')
            
            ax.set_facecolor('#2C2F33')
            fig.patch.set_facecolor('#2C2F33')
            ax.tick_params(colors='white')
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33', bbox_inches='tight')
            buf.seek(0)
            plt.close(fig)
            
            return buf
        except Exception as e:
            plt.close('all')
            raise Exception(f"Error creating faction comparison radar: {str(e)}")
    
    @staticmethod
    def create_world_indicators_chart(metrics: Dict[str, Any]) -> io.BytesIO:
        try:
            world_metrics = metrics.get('world', {})
            
            indicators = {
                'Hegemony (HHI)': world_metrics.get('hegemony_hhi', 0) * 100,
                'Power Gini': world_metrics.get('power_gini', 0) * 100,
                'Global Tension': world_metrics.get('global_tension', 0),
                'Avg Legitimacy': world_metrics.get('avg_legitimacy', 0),
                'Polarization': world_metrics.get('polarization_score', 0) * 100,
                'Fragmentation': world_metrics.get('diplomatic_fragmentation', 0) * 100
            }
            
            names = list(indicators.keys())
            values = list(indicators.values())
            colors = ['#E74C3C', '#E67E22', '#F39C12', '#27AE60', '#3498DB', '#9B59B6']
            
            fig, ax = plt.subplots(figsize=(12, 8))
            bars = ax.barh(names, values, color=colors, edgecolor='white', linewidth=1.5)
            
            ax.set_xlabel('Index Value', fontsize=12, weight='bold', color='white')
            ax.set_title('World Geopolitical Indicators', fontsize=16, weight='bold', pad=20, color='white')
            
            max_value = max(values) if values and max(values) > 0 else 100
            ax.set_xlim(0, max_value * 1.15)
            ax.grid(axis='x', alpha=0.3, linestyle='--', color='white')
            
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width + max_value * 0.02, bar.get_y() + bar.get_height()/2.,
                       f'{width:.1f}',
                       ha='left', va='center', fontsize=11, weight='bold', 
                       color='white', bbox=dict(boxstyle='round', facecolor=colors[i], alpha=0.8))
            
            ax.set_facecolor('#2C2F33')
            fig.patch.set_facecolor('#2C2F33')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.set_tick_params(labelcolor='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33')
            buf.seek(0)
            plt.close(fig)
            
            return buf
        except Exception as e:
            plt.close('all')
            raise Exception(f"Error creating world indicators chart: {str(e)}")
    
    @staticmethod
    def create_power_evolution_chart(historical_data: List[Dict[str, Any]]) -> io.BytesIO:
        try:
            if not historical_data:
                fig, ax = plt.subplots(figsize=(14, 8))
                ax.text(0.5, 0.5, 'No historical data available', ha='center', va='center',
                       fontsize=16, color='white', transform=ax.transAxes)
                ax.set_facecolor('#2C2F33')
                fig.patch.set_facecolor('#2C2F33')
                ax.axis('off')
            else:
                fig, ax = plt.subplots(figsize=(14, 8))
                
                faction_data = {}
                for snapshot in historical_data:
                    tick = snapshot.get('tick', 0)
                    factions = snapshot.get('factions', {})
                    
                    for fid, faction in factions.items():
                        if fid not in faction_data:
                            faction_data[fid] = {
                                'name': faction.get('name', fid),
                                'color': faction.get('color', '#808080'),
                                'ticks': [],
                                'power': []
                            }
                        faction_data[fid]['ticks'].append(tick)
                        faction_data[fid]['power'].append(faction.get('power', 0))
                
                for fid, data in faction_data.items():
                    if data['ticks']:
                        ax.plot(data['ticks'], data['power'], 
                               label=data['name'], color=data['color'], 
                               linewidth=2.5, marker='o', markersize=4)
                
                ax.set_xlabel('Tick', fontsize=12, weight='bold', color='white')
                ax.set_ylabel('Total Power', fontsize=12, weight='bold', color='white')
                ax.set_title('Faction Power Evolution', fontsize=16, weight='bold', pad=20, color='white')
                ax.legend(loc='best', framealpha=0.9)
                ax.grid(True, alpha=0.3, linestyle='--', color='white')
                
                ax.set_facecolor('#2C2F33')
                fig.patch.set_facecolor('#2C2F33')
                ax.tick_params(colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33')
            buf.seek(0)
            plt.close(fig)
            
            return buf
        except Exception as e:
            plt.close('all')
            raise Exception(f"Error creating power evolution chart: {str(e)}")
    
    @staticmethod
    def create_legitimacy_evolution_chart(historical_data: List[Dict[str, Any]]) -> io.BytesIO:
        try:
            if not historical_data:
                fig, ax = plt.subplots(figsize=(14, 8))
                ax.text(0.5, 0.5, 'No historical data available', ha='center', va='center',
                       fontsize=16, color='white', transform=ax.transAxes)
                ax.set_facecolor('#2C2F33')
                fig.patch.set_facecolor('#2C2F33')
                ax.axis('off')
            else:
                fig, ax = plt.subplots(figsize=(14, 8))
                
                faction_data = {}
                for snapshot in historical_data:
                    tick = snapshot.get('tick', 0)
                    factions = snapshot.get('factions', {})
                    
                    for fid, faction in factions.items():
                        if fid not in faction_data:
                            faction_data[fid] = {
                                'name': faction.get('name', fid),
                                'color': faction.get('color', '#808080'),
                                'ticks': [],
                                'legitimacy': []
                            }
                        faction_data[fid]['ticks'].append(tick)
                        faction_data[fid]['legitimacy'].append(faction.get('legitimacy', 0))
                
                for fid, data in faction_data.items():
                    if data['ticks']:
                        ax.plot(data['ticks'], data['legitimacy'], 
                               label=data['name'], color=data['color'], 
                               linewidth=2.5, marker='s', markersize=4)
                
                ax.set_xlabel('Tick', fontsize=12, weight='bold', color='white')
                ax.set_ylabel('Legitimacy', fontsize=12, weight='bold', color='white')
                ax.set_title('Faction Legitimacy Evolution', fontsize=16, weight='bold', pad=20, color='white')
                ax.set_ylim(0, 105)
                ax.legend(loc='best', framealpha=0.9)
                ax.grid(True, alpha=0.3, linestyle='--', color='white')
                
                ax.set_facecolor('#2C2F33')
                fig.patch.set_facecolor('#2C2F33')
                ax.tick_params(colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33')
            buf.seek(0)
            plt.close(fig)
            
            return buf
        except Exception as e:
            plt.close('all')
            raise Exception(f"Error creating legitimacy evolution chart: {str(e)}")
    
    @staticmethod
    def create_resources_evolution_chart(historical_data: List[Dict[str, Any]]) -> io.BytesIO:
        try:
            if not historical_data:
                fig, ax = plt.subplots(figsize=(14, 8))
                ax.text(0.5, 0.5, 'No historical data available', ha='center', va='center',
                       fontsize=16, color='white', transform=ax.transAxes)
                ax.set_facecolor('#2C2F33')
                fig.patch.set_facecolor('#2C2F33')
                ax.axis('off')
            else:
                fig, ax = plt.subplots(figsize=(14, 8))
                
                ticks = []
                total_credits = []
                total_materials = []
                total_food = []
                total_energy = []
                
                for snapshot in historical_data:
                    tick = snapshot.get('tick', 0)
                    factions = snapshot.get('factions', {})
                    
                    ticks.append(tick)
                    
                    credits = sum(f.get('resources', {}).get('credits', 0) for f in factions.values())
                    materials = sum(f.get('resources', {}).get('materials', 0) for f in factions.values())
                    food = sum(f.get('resources', {}).get('food', 0) for f in factions.values())
                    energy = sum(f.get('resources', {}).get('energy', 0) for f in factions.values())
                    
                    total_credits.append(credits)
                    total_materials.append(materials)
                    total_food.append(food)
                    total_energy.append(energy)
                
                if ticks:
                    ax.plot(ticks, total_credits, label='Credits', color='#F1C40F', 
                           linewidth=2.5, marker='o', markersize=5)
                    ax.plot(ticks, total_materials, label='Materials', color='#95A5A6', 
                           linewidth=2.5, marker='s', markersize=5)
                    ax.plot(ticks, total_food, label='Food', color='#27AE60', 
                           linewidth=2.5, marker='^', markersize=5)
                    ax.plot(ticks, total_energy, label='Energy', color='#3498DB', 
                           linewidth=2.5, marker='d', markersize=5)
                
                ax.set_xlabel('Tick', fontsize=12, weight='bold', color='white')
                ax.set_ylabel('Total Resources', fontsize=12, weight='bold', color='white')
                ax.set_title('Global Resource Evolution', fontsize=16, weight='bold', pad=20, color='white')
                ax.legend(loc='best', framealpha=0.9)
                ax.grid(True, alpha=0.3, linestyle='--', color='white')
                
                ax.set_facecolor('#2C2F33')
                fig.patch.set_facecolor('#2C2F33')
                ax.tick_params(colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
            
            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33')
            buf.seek(0)
            plt.close(fig)
            
            return buf
        except Exception as e:
            plt.close('all')
            raise Exception(f"Error creating resources evolution chart: {str(e)}")