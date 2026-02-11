import random
from domains.world import World
from domains.region_meta import WeatherType, WeatherState
from deltas.builder import DeltaBuilder
from .base import BaseSystem

class WeatherSystem(BaseSystem):
    def compute_delta(self, world: World, builder: DeltaBuilder) -> None:
        from core.defaults import Rules
        
        for region_id, region in world.regions.items():
            current_weather = region.weather
            
            if current_weather.duration > 0:
                new_duration = current_weather.duration - 1
                if new_duration > 0:
                    continue
            
            if random.random() < Rules.Weather.WEATHER_CHANGE_CHANCE:
                new_weather_type = self._get_next_weather(region.weather.type, region.environment)
                new_intensity = random.uniform(0.7, 1.5)
                new_duration = random.randint(1, 5)
                
                new_weather = WeatherState(
                    type=new_weather_type,
                    intensity=new_intensity,
                    duration=new_duration
                )
                
                region.weather = new_weather
                
                builder.add_event(f"🌦️ Weather changed to {new_weather_type.value} in {region.name} (intensity: {new_intensity:.1f}, duration: {new_duration} turns)")
    
    def _get_next_weather(self, current: WeatherType, environment) -> WeatherType:
        from domains.region_meta import EnvironmentType
        
        if environment == EnvironmentType.COASTAL:
            weights = {
                WeatherType.SUNNY: 0.2,
                WeatherType.CLOUDY: 0.25,
                WeatherType.RAIN: 0.3,
                WeatherType.STORM: 0.15,
                WeatherType.DROUGHT: 0.05,
                WeatherType.SNOW: 0.03,
                WeatherType.HEATWAVE: 0.02
            }
        elif environment in [EnvironmentType.URBAN, EnvironmentType.INDUSTRIAL]:
            weights = {
                WeatherType.SUNNY: 0.25,
                WeatherType.CLOUDY: 0.35,
                WeatherType.RAIN: 0.2,
                WeatherType.STORM: 0.05,
                WeatherType.DROUGHT: 0.05,
                WeatherType.SNOW: 0.05,
                WeatherType.HEATWAVE: 0.05
            }
        else:
            weights = {
                WeatherType.SUNNY: 0.3,
                WeatherType.CLOUDY: 0.2,
                WeatherType.RAIN: 0.2,
                WeatherType.STORM: 0.1,
                WeatherType.DROUGHT: 0.1,
                WeatherType.SNOW: 0.05,
                WeatherType.HEATWAVE: 0.05
            }
        
        if current in weights:
            weights[current] *= 1.5
        
        total = sum(weights.values())
        normalized = {k: v/total for k, v in weights.items()}
        
        return random.choices(list(normalized.keys()), weights=list(normalized.values()))[0]
