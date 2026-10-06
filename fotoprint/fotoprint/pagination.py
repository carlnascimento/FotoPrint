from .models import Page, Photo


def build_pages(photos: list[Photo], photos_per_page: int) -> list[Page]:
    """Divide as fotos em páginas automaticamente."""
    if photos_per_page <= 0:
        raise ValueError("photos_per_page deve ser maior que zero")

    pages = []
    for start in range(0, len(photos), photos_per_page):
        chunk = photos[start:start + photos_per_page]
        pages.append(Page(len(pages) + 1, chunk))
    return pages
