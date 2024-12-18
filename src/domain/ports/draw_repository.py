from abc import ABC, abstractmethod
from src.domain.models.draw import Draw


class DrawRepository(ABC):
    @abstractmethod
    async def create_draw(self, group_id: int, results: dict) -> Draw:
        pass

    @abstractmethod
    async def get_draw_by_group(self, group_id: int) -> Draw:
        pass

    @abstractmethod
    async def delete_draw(self, draw_id: int) -> None:
        pass