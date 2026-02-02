from dataclasses import dataclass

@dataclass(slots=True)
class Power:
    army: float = 0.0
    navy: float = 0.0
    air: float = 0.0

    @property
    def total(self) -> float:
        return self.army + self.navy + self.air

    def __add__(self, other: 'Power') -> 'Power':
        return Power(
            army=self.army + other.army,
            navy=self.navy + other.navy,
            air=self.air + other.air
        )

    def __sub__(self, other: 'Power') -> 'Power':
        return Power(
            army=max(0.0, self.army - other.army),
            navy=max(0.0, self.navy - other.navy),
            air=max(0.0, self.air - other.air)
        )

    def __mul__(self, factor: float) -> 'Power':
        return Power(
            army=self.army * factor,
            navy=self.navy * factor,
            air=self.air * factor
        )

    def clamp(self, min_val: float, max_val: float) -> 'Power':
        # Clamping individual branches to avoid extreme concentrations
        # while keeping total within bounds is complex, so we clamp branches
        return Power(
            army=max(min_val, min(max_val, self.army)),
            navy=max(min_val, min(max_val, self.navy)),
            air=max(min_val, min(max_val, self.air))
        )

    def to_dict(self) -> dict:
        return {
            "army": self.army,
            "navy": self.navy,
            "air": self.air
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Power':
        if not data:
            return cls()
        return cls(
            army=data.get("army", 0.0),
            navy=data.get("navy", 0.0),
            air=data.get("air", 0.0)
        )
