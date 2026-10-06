import sys
from pathlib import Path

from .qt import QApplication, QIcon

from .main_window import MainWindow


def load_icon() -> QIcon:
    """Ícone do tema (instalado pelo .deb) com o PNG embutido como alternativa."""
    icon = QIcon.fromTheme("fotoprint")
    if icon.isNull():
        icon = QIcon(str(Path(__file__).with_name("icon.png")))
    return icon


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("FotoPrint")
    app.setApplicationDisplayName("FotoPrint")
    app.setOrganizationName("FotoPrint")
    app.setDesktopFileName("fotoprint")  # liga a janela ao fotoprint.desktop (ícone na barra de tarefas)
    app.setWindowIcon(load_icon())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
