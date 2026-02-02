from dataclasses import dataclass

@dataclass(slots=True)
class Resources:
    credits: float = 0.0
    materials: float = 0.0
    food: float = 0.0
    energy: float = 0.0
    influence: float = 0.0

    def __add__(self, other: 'Resources') -> 'Resources':
        return Resources(
            credits=self.credits + other.credits,
            materials=self.materials + other.materials,
            food=self.food + other.food,
            energy=self.energy + other.energy,
            influence=self.influence + other.influence
        )

    def __sub__(self, other: 'Resources') -> 'Resources':
        return Resources(
            credits=self.credits - other.credits,
            materials=self.materials - other.materials,
            food=self.food - other.food,
            energy=self.energy - other.energy,
            influence=self.influence - other.influence
        )

    def __mul__(self, factor: float) -> 'Resources':
        return Resources(
            credits=self.credits * factor,
            materials=self.materials * factor,
            food=self.food * factor,
            energy=self.energy * factor,
            influence=self.influence * factor
        )

    def clamp(self, min_val: float, max_val: float) -> 'Resources':
        return Resources(
            credits=max(min_val, min(max_val, self.credits)),
            materials=max(min_val, min(max_val, self.materials)),
            food=max(min_val, min(max_val, self.food)),
            energy=max(min_val, min(max_val, self.energy)),
            influence=max(min_val, min(max_val, self.influence))
        )

    def to_dict(self) -> dict:
        return {
            "credits": self.credits,
            "materials": self.materials,
            "food": self.food,
            "energy": self.energy,
            "influence": self.influence
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Resources':
        if not data:
            return cls()
        return cls(
            credits=data.get("credits", 0.0),
            materials=data.get("materials", 0.0),
            food=data.get("food", 0.0),
            energy=data.get("energy", 0.0),
            influence=data.get("influence", 0.0)
        )
