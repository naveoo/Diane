import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from typing import Dict, Any, List
from domains.world import World

class MetricsVisualizer:
    @staticmethod
    def create_power_distribution_chart(world: World) -> io.BytesIO:
        factions = [f for f in world.factions.values() if f.is_active]
        
        names = [f.name for f in factions]
        powers = [f.power.total for f in factions]
        colors = [f.color if hasattr(f, 'color') else '#808080' for f in factions]
        
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
        
        ax.set_title('Power Distribution', fontsize=16, weight='bold', pad=20)
        
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_resource_security_chart(metrics: Dict[str, Any]) -> io.BytesIO:
        world_metrics = metrics['world']
        
        categories = ['Food Security', 'Energy Security']
        values = [
            world_metrics.get('food_security_index', 0),
            world_metrics.get('energy_security_index', 0)
        ]
        colors = ['#27AE60', '#F39C12']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=2)
        
        ax.set_ylabel('Security Index', fontsize=12, weight='bold')
        ax.set_title('Global Resource Security', fontsize=16, weight='bold', pad=20)
        ax.set_ylim(0, max(values) * 1.2 if values else 10)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=12, weight='bold')
        
        ax.set_facecolor('#2C2F33')
        fig.patch.set_facecolor('#2C2F33')
        ax.tick_params(colors='white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_faction_comparison_radar(world: World, faction_ids: List[str]) -> io.BytesIO:
        categories = ['Power', 'Legitimacy', 'Resources', 'Knowledge', 'Regions']
        num_vars = len(categories)
        
        angles = [n / float(num_vars) * 2 * 3.14159 for n in range(num_vars)]
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        for fid in faction_ids[:5]:
            if fid not in world.factions:
                continue
            
            faction = world.factions[fid]
            if not faction.is_active:
                continue
            
            values = [
                faction.power.total / 10,
                faction.legitimacy / 10,
                (faction.resources.credits + faction.resources.materials) / 50,
                faction.knowledge / 10,
                len(faction.regions)
            ]
            values += values[:1]
            
            color = faction.color if hasattr(faction, 'color') else '#808080'
            ax.plot(angles, values, 'o-', linewidth=2, label=faction.name, color=color)
            ax.fill(angles, values, alpha=0.15, color=color)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=12, weight='bold')
        ax.set_ylim(0, 15)
        ax.set_title('Faction Comparison', size=16, weight='bold', pad=30)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True, alpha=0.3)
        
        ax.set_facecolor('#2C2F33')
        fig.patch.set_facecolor('#2C2F33')
        ax.tick_params(colors='white')
        ax.title.set_color('white')
        
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_world_indicators_chart(metrics: Dict[str, Any]) -> io.BytesIO:
        world_metrics = metrics['world']
        
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
        
        ax.set_xlabel('Index Value', fontsize=12, weight='bold')
        ax.set_title('World Geopolitical Indicators', fontsize=16, weight='bold', pad=20)
        ax.set_xlim(0, max(values) * 1.15 if values else 100)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{width:.1f}',
                   ha='left', va='center', fontsize=11, weight='bold', 
                   color='white', bbox=dict(boxstyle='round', facecolor=colors[i], alpha=0.8))
        
        ax.set_facecolor('#2C2F33')
        fig.patch.set_facecolor('#2C2F33')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_power_evolution_chart(historical_data: List[Dict[str, Any]]) -> io.BytesIO:
        fig, ax = plt.subplots(figsize=(14, 8))
        
        faction_data = {}
        for snapshot in historical_data:
            tick = snapshot['tick']
            for fid, faction in snapshot['factions'].items():
                if fid not in faction_data:
                    faction_data[fid] = {
                        'name': faction['name'],
                        'color': faction.get('color', '#808080'),
                        'ticks': [],
                        'power': []
                    }
                faction_data[fid]['ticks'].append(tick)
                faction_data[fid]['power'].append(faction['power'])
        
        for fid, data in faction_data.items():
            ax.plot(data['ticks'], data['power'], 
                   label=data['name'], color=data['color'], 
                   linewidth=2.5, marker='o', markersize=4)
        
        ax.set_xlabel('Tick', fontsize=12, weight='bold')
        ax.set_ylabel('Total Power', fontsize=12, weight='bold')
        ax.set_title('Faction Power Evolution', fontsize=16, weight='bold', pad=20)
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        ax.set_facecolor('#2C2F33')
        fig.patch.set_facecolor('#2C2F33')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_legitimacy_evolution_chart(historical_data: List[Dict[str, Any]]) -> io.BytesIO:
        fig, ax = plt.subplots(figsize=(14, 8))
        
        faction_data = {}
        for snapshot in historical_data:
            tick = snapshot['tick']
            for fid, faction in snapshot['factions'].items():
                if fid not in faction_data:
                    faction_data[fid] = {
                        'name': faction['name'],
                        'color': faction.get('color', '#808080'),
                        'ticks': [],
                        'legitimacy': []
                    }
                faction_data[fid]['ticks'].append(tick)
                faction_data[fid]['legitimacy'].append(faction['legitimacy'])
        
        for fid, data in faction_data.items():
            ax.plot(data['ticks'], data['legitimacy'], 
                   label=data['name'], color=data['color'], 
                   linewidth=2.5, marker='s', markersize=4)
        
        ax.set_xlabel('Tick', fontsize=12, weight='bold')
        ax.set_ylabel('Legitimacy', fontsize=12, weight='bold')
        ax.set_title('Faction Legitimacy Evolution', fontsize=16, weight='bold', pad=20)
        ax.set_ylim(0, 105)
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        ax.set_facecolor('#2C2F33')
        fig.patch.set_facecolor('#2C2F33')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33')
        buf.seek(0)
        plt.close()
        
        return buf
    
    @staticmethod
    def create_resources_evolution_chart(historical_data: List[Dict[str, Any]]) -> io.BytesIO:
        fig, ax = plt.subplots(figsize=(14, 8))
        
        ticks = []
        total_credits = []
        total_materials = []
        total_food = []
        total_energy = []
        
        for snapshot in historical_data:
            ticks.append(snapshot['tick'])
            credits = sum(f['resources'].get('credits', 0) for f in snapshot['factions'].values())
            materials = sum(f['resources'].get('materials', 0) for f in snapshot['factions'].values())
            food = sum(f['resources'].get('food', 0) for f in snapshot['factions'].values())
            energy = sum(f['resources'].get('energy', 0) for f in snapshot['factions'].values())
            
            total_credits.append(credits)
            total_materials.append(materials)
            total_food.append(food)
            total_energy.append(energy)
        
        ax.plot(ticks, total_credits, label='Credits', color='#F1C40F', linewidth=2.5, marker='o')
        ax.plot(ticks, total_materials, label='Materials', color='#95A5A6', linewidth=2.5, marker='s')
        ax.plot(ticks, total_food, label='Food', color='#27AE60', linewidth=2.5, marker='^')
        ax.plot(ticks, total_energy, label='Energy', color='#3498DB', linewidth=2.5, marker='d')
        
        ax.set_xlabel('Tick', fontsize=12, weight='bold')
        ax.set_ylabel('Total Resources', fontsize=12, weight='bold')
        ax.set_title('Global Resource Evolution', fontsize=16, weight='bold', pad=20)
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        ax.set_facecolor('#2C2F33')
        fig.patch.set_facecolor('#2C2F33')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=150, facecolor='#2C2F33')
        buf.seek(0)
        plt.close()
        
        return buf
