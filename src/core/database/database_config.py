from dataclasses import dataclass

@dataclass
class DatabaseConnectConfig:
    user: str
    password: str
    port: int
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> "DatabaseConnectConfig":
        return cls(**data)

    def to_dict(self) -> dict:
        return self.__dict__