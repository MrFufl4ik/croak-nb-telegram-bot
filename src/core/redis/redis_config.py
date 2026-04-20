from dataclasses import dataclass

@dataclass
class RedisConnectConfig:
    password: str
    port: int
    logic_database: str

    @classmethod
    def from_dict(cls, data: dict) -> "RedisConnectConfig":
        return cls(**data)

    def to_dict(self) -> dict:
        return self.__dict__