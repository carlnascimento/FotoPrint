from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from .layout import cell_positions, get_layout
from .models import Page, PrintSettings


PAPER_MM = {
    "A4": (210, 297),
    "A5": (148, 210),
    "Letter": (215.9, 279.4),
}


def mm_to_px(mm: float, dpi: int = 150) -> int:
    return round(mm / 25.4 * dpi)


def page_size_mm(settings: PrintSettings):
    width_mm, height_mm = PAPER_MM[settings.paper]
    if settings.orientation == "Paisagem":
        width_mm, height_mm = height_mm, width_mm
    return width_mm, height_mm


def page_size_px(settings: PrintSettings, dpi: int = 150):
    width_mm, height_mm = page_size_mm(settings)
    return mm_to_px(width_mm, dpi), mm_to_px(height_mm, dpi)


def render_page(page: Page, settings: PrintSettings, dpi: int = 150) -> Image.Image:
    width, height = page_size_px(settings, dpi)
    canvas = Image.new("RGB", (width, height), "white")
    canvas.info["dpi"] = (dpi, dpi)

    layout = get_layout(settings.layout_id)
    cells = cell_positions(layout, *page_size_mm(settings))

    for photo, (cx, cy, cw_mm, ch_mm) in zip(page.photos, cells):
        x0, y0 = mm_to_px(cx, dpi), mm_to_px(cy, dpi)
        cell_w = mm_to_px(cx + cw_mm, dpi) - x0
        cell_h = mm_to_px(cy + ch_mm, dpi) - y0

        try:
            image = ImageOps.exif_transpose(Image.open(photo.path)).convert("RGB")
            # Gira a foto para acompanhar a orientação do quadro (exceto folha de contato)
            if layout.kind != "contact" and (image.width > image.height) != (cell_w > cell_h):
                image = image.rotate(90, expand=True)
            if settings.fit_frame:
                image = ImageOps.fit(image, (cell_w, cell_h), Image.LANCZOS)
                px, py = x0, y0
            else:
                image = ImageOps.contain(image, (cell_w, cell_h), Image.LANCZOS)
                px = x0 + (cell_w - image.width) // 2
                py = y0 + (cell_h - image.height) // 2
            canvas.paste(image, (px, py))
        except Exception:
            draw = ImageDraw.Draw(canvas)
            draw.rectangle((x0, y0, x0 + cell_w, y0 + cell_h), outline="black", width=2)
            draw.text((x0 + 10, y0 + 10), "Erro ao carregar foto", fill="black")

    return canvas


def save_page(image: Image.Image, filename: Path, dpi: int = 150):
    image.save(filename, "PNG", dpi=(dpi, dpi))


def render_all(pages, settings: PrintSettings, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    result = []
    for page in pages:
        filename = output_dir / f"pagina-{page.number:03d}.png"
        save_page(render_page(page, settings), filename)
        result.append(filename)
    return result
