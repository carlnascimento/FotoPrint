from dataclasses import dataclass
from pathlib import Path

from .layout import DEFAULT_LAYOUT_ID, get_layout


@dataclass
class Photo:
    path: Path


@dataclass
class Page:
    number: int
    photos: list[Photo]


@dataclass
class PrintSettings:
    paper: str = "A4"
    orientation: str = "Retrato"
    layout_id: str = DEFAULT_LAYOUT_ID
    fit_frame: bool = True  # preenche o quadro cortando o excesso (como no Windows)

    @property
    def photos_per_page(self) -> int:
        return get_layout(self.layout_id).count
