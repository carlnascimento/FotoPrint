"""Layouts com tamanhos fixos, no estilo do assistente "Imprimir Imagens" do Windows."""
from dataclasses import dataclass
from math import ceil

IN = 25.4  # mm por polegada
EPS = 1e-6


@dataclass(frozen=True)
class Layout:
    id: str
    name: str
    count: int            # fotos por página
    width_mm: float = 0   # tamanho de cada foto (retrato)
    height_mm: float = 0
    kind: str = "fixed"   # "full" | "fixed" | "contact"


LAYOUTS = [
    Layout("full", "Página inteira", 1, kind="full"),
    Layout("20x25", "20 x 25 cm (1 por página)", 1, 200, 250),
    Layout("8x10", "8 x 10 pol. (1 por página)", 1, 8 * IN, 10 * IN),
    Layout("13x18", "13 x 18 cm (2 por página)", 2, 130, 180),
    Layout("5x7", "5 x 7 pol. (2 por página)", 2, 5 * IN, 7 * IN),
    Layout("10x15", "10 x 15 cm (2 por página)", 2, 100, 150),
    Layout("4x6", "4 x 6 pol. (2 por página)", 2, 4 * IN, 6 * IN),
    Layout("9x13", "9 x 13 cm (4 por página)", 4, 90, 130),
    Layout("3.5x5", "3,5 x 5 pol. (4 por página)", 4, 3.5 * IN, 5 * IN),
    Layout("wallet", "Carteira 2,5 x 3,125 pol. (9 por página)", 9, 2.5 * IN, 3.125 * IN),
    Layout("contact", "Folha de contato (35 por página)", 35, kind="contact"),
]

DEFAULT_LAYOUT_ID = "10x15"


def get_layout(layout_id: str) -> Layout:
    for layout in LAYOUTS:
        if layout.id == layout_id:
            return layout
    return get_layout(DEFAULT_LAYOUT_ID)


def cell_positions(layout: Layout, page_w: float, page_h: float):
    """Retorna [(x, y, largura, altura)] em mm, ou [] se o layout não cabe no papel."""
    if layout.kind == "full":
        return [(0.0, 0.0, page_w, page_h)]

    if layout.kind == "contact":
        cols, rows = (5, 7) if page_w <= page_h else (7, 5)
        margin, gap = 10.0, 2.0
        cw = (page_w - 2 * margin - gap * (cols - 1)) / cols
        ch = (page_h - 2 * margin - gap * (rows - 1)) / rows
        cells = [
            (margin + c * (cw + gap), margin + r * (ch + gap), cw, ch)
            for r in range(rows) for c in range(cols)
        ]
        return cells[:layout.count]

    # Tamanho fixo: tenta a foto em pé e depois deitada, o que couber.
    for cw, ch in ((layout.width_mm, layout.height_mm), (layout.height_mm, layout.width_mm)):
        max_cols = int(page_w // cw + EPS)
        max_rows = int(page_h // ch + EPS)
        if max_cols * max_rows < layout.count:
            continue
        best = None
        for cols in range(1, min(layout.count, max_cols) + 1):
            rows = ceil(layout.count / cols)
            if rows > max_rows:
                continue
            key = (cols * rows - layout.count, cols * rows)
            if best is None or key < best[0]:
                best = (key, cols, rows)
        if best is None:
            continue
        _, cols, rows = best
        x0 = (page_w - cols * cw) / 2
        y0 = (page_h - rows * ch) / 2
        cells = [
            (x0 + c * cw, y0 + r * ch, cw, ch)
            for r in range(rows) for c in range(cols)
        ]
        return cells[:layout.count]
    return []


def available_layouts(page_w: float, page_h: float) -> list[Layout]:
    return [l for l in LAYOUTS if cell_positions(l, page_w, page_h)]
