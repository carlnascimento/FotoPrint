from pathlib import Path
import tempfile

from .qt import (
    Qt,
    QIcon,
    QPixmap,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from .layout import available_layouts, get_layout, DEFAULT_LAYOUT_ID
from .models import Photo, PrintSettings
from .pagination import build_pages
from .printing import list_printers, print_files
from .renderer import PAPER_MM, render_page, save_page


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FotoPrint")
        self.resize(1100, 720)

        self.photos: list[Photo] = []
        self.pages = []
        self.current_page = 0
        self.preview_file = None

        self.build_ui()
        self.recalculate()

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QHBoxLayout(central)

        left = QVBoxLayout()

        self.add_button = QPushButton("Adicionar fotos")
        self.add_button.clicked.connect(self.add_photos)
        left.addWidget(self.add_button)

        self.clear_button = QPushButton("Limpar seleção")
        self.clear_button.clicked.connect(self.clear_photos)
        left.addWidget(self.clear_button)

        self.photo_list = QListWidget()
        self.photo_list.setIconSize(self.photo_list.iconSize())
        left.addWidget(self.photo_list, 1)

        main.addLayout(left, 1)

        center = QVBoxLayout()

        self.preview = QLabel("Nenhuma foto selecionada")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setMinimumSize(500, 500)
        self.preview.setStyleSheet(
            "background: #eeeeee; border: 1px solid #bbbbbb;"
        )
        center.addWidget(self.preview, 1)

        navigation = QHBoxLayout()
        self.previous_button = QPushButton("◀ Página anterior")
        self.previous_button.clicked.connect(self.previous_page)
        self.next_button = QPushButton("Próxima página ▶")
        self.next_button.clicked.connect(self.next_page)
        self.page_label = QLabel("Página 0 de 0")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        navigation.addWidget(self.previous_button)
        navigation.addWidget(self.page_label, 1)
        navigation.addWidget(self.next_button)
        center.addLayout(navigation)

        main.addLayout(center, 3)

        right = QVBoxLayout()

        settings_box = QGroupBox("Configuração da impressão")
        form = QFormLayout(settings_box)

        self.paper_combo = QComboBox()
        self.paper_combo.addItems(["A4", "A5", "Letter"])
        self.paper_combo.currentIndexChanged.connect(self.on_paper_changed)
        form.addRow("Papel:", self.paper_combo)

        self.orientation_combo = QComboBox()
        self.orientation_combo.addItems(["Retrato", "Paisagem"])
        self.orientation_combo.currentIndexChanged.connect(self.recalculate)
        form.addRow("Orientação:", self.orientation_combo)

        self.layout_combo = QComboBox()
        self.populate_layouts()
        self.layout_combo.currentIndexChanged.connect(self.recalculate)
        form.addRow("Tamanho:", self.layout_combo)

        self.copies_spin = QSpinBox()
        self.copies_spin.setRange(1, 99)
        self.copies_spin.setValue(1)
        self.copies_spin.valueChanged.connect(self.recalculate)
        form.addRow("Cópias de cada foto:", self.copies_spin)

        self.fit_check = QCheckBox("Ajustar foto ao quadro (corta o excesso)")
        self.fit_check.setChecked(True)
        self.fit_check.stateChanged.connect(self.recalculate)
        form.addRow(self.fit_check)

        right.addWidget(settings_box)

        self.summary = QLabel()
        self.summary.setWordWrap(True)
        self.summary.setStyleSheet("font-size: 15px; padding: 12px;")
        right.addWidget(self.summary)

        self.printer_combo = QComboBox()
        self.printer_combo.addItem("Impressora padrão")
        for printer in list_printers():
            self.printer_combo.addItem(printer)
        right.addWidget(self.printer_combo)

        self.pdf_button = QPushButton("Exportar páginas para PDF")
        self.pdf_button.clicked.connect(self.export_pdf)
        right.addWidget(self.pdf_button)

        self.print_button = QPushButton("Imprimir")
        self.print_button.clicked.connect(self.print_document)
        right.addWidget(self.print_button)

        right.addStretch()
        main.addLayout(right, 1)

    def populate_layouts(self):
        width, height = PAPER_MM[self.paper_combo.currentText()]
        previous = self.layout_combo.currentData() or DEFAULT_LAYOUT_ID
        self.layout_combo.blockSignals(True)
        self.layout_combo.clear()
        for layout in available_layouts(width, height):
            self.layout_combo.addItem(layout.name, layout.id)
        index = self.layout_combo.findData(previous)
        self.layout_combo.setCurrentIndex(index if index >= 0 else 0)
        self.layout_combo.blockSignals(False)

    def on_paper_changed(self):
        self.populate_layouts()
        self.recalculate()

    def settings(self) -> PrintSettings:
        return PrintSettings(
            paper=self.paper_combo.currentText(),
            orientation=self.orientation_combo.currentText(),
            layout_id=self.layout_combo.currentData(),
            fit_frame=self.fit_check.isChecked(),
        )

    def expanded_photos(self):
        copies = self.copies_spin.value()
        return [photo for photo in self.photos for _ in range(copies)]

    def add_photos(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar fotos",
            str(Path.home()),
            "Imagens (*.jpg *.jpeg *.png *.bmp *.webp *.tif *.tiff)",
        )
        for filename in files:
            path = Path(filename)
            if not any(p.path == path for p in self.photos):
                self.photos.append(Photo(path))
        self.refresh_photo_list()
        self.recalculate()

    def clear_photos(self):
        self.photos.clear()
        self.refresh_photo_list()
        self.recalculate()

    def refresh_photo_list(self):
        self.photo_list.clear()
        for photo in self.photos:
            item = QListWidgetItem(photo.path.name)
            pixmap = QPixmap(str(photo.path))
            if not pixmap.isNull():
                item.setIcon(QIcon(pixmap))
            self.photo_list.addItem(item)

    def recalculate(self):
        settings = self.settings()
        self.pages = build_pages(self.expanded_photos(), settings.photos_per_page)
        if self.pages:
            self.current_page = min(self.current_page, len(self.pages) - 1)
        else:
            self.current_page = 0

        total = len(self.pages)
        self.summary.setText(
            f"<b>{len(self.photos)} fotos selecionadas</b><br>"
            f"Tamanho: {get_layout(settings.layout_id).name}<br>"
            f"<b>Total: {total} página(s)</b>"
        )
        self.update_preview()

    def update_preview(self):
        if not self.pages:
            self.preview.setText("Nenhuma foto selecionada")
            self.page_label.setText("Página 0 de 0")
            self.previous_button.setEnabled(False)
            self.next_button.setEnabled(False)
            self.print_button.setEnabled(False)
            self.pdf_button.setEnabled(False)
            return

        settings = self.settings()
        page = self.pages[self.current_page]

        temp_dir = Path(tempfile.gettempdir()) / "fotoprint"
        temp_dir.mkdir(exist_ok=True)
        self.preview_file = temp_dir / f"preview-{page.number}.png"

        image = render_page(page, settings, dpi=100)
        image.save(self.preview_file, "PNG")

        pixmap = QPixmap(str(self.preview_file))
        self.preview.setPixmap(
            pixmap.scaled(
                self.preview.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

        self.page_label.setText(f"Página {page.number} de {len(self.pages)}")
        self.previous_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < len(self.pages) - 1)
        self.print_button.setEnabled(True)
        self.pdf_button.setEnabled(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.pages:
            self.update_preview()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_preview()

    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.update_preview()

    def render_pages(self):
        settings = self.settings()
        output_dir = Path(tempfile.mkdtemp(prefix="fotoprint-print-"))
        files = []
        for page in self.pages:
            image = render_page(page, settings, dpi=150)
            filename = output_dir / f"pagina-{page.number:03d}.png"
            save_page(image, filename, dpi=150)
            files.append(filename)
        return files

    def export_pdf(self):
        if not self.pages:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "Salvar PDF", "fotoprint.pdf", "PDF (*.pdf)"
        )
        if not filename:
            return

        settings = self.settings()
        images = [render_page(page, settings, dpi=150).convert("RGB") for page in self.pages]

        images[0].save(
            filename,
            "PDF",
            resolution=150,
            save_all=True,
            append_images=images[1:],
        )

        QMessageBox.information(
            self,
            "PDF criado",
            f"PDF criado com {len(images)} página(s).",
        )

    def print_document(self):
        if not self.pages:
            return

        answer = QMessageBox.question(
            self,
            "Confirmar impressão",
            f"Serão impressas {len(self.pages)} página(s) "
            f"para {len(self.photos)} foto(s).\n\nDeseja continuar?",
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        files = self.render_pages()
        printer = self.printer_combo.currentText()
        printer = None if printer == "Impressora padrão" else printer

        success, message = print_files(files, printer, media=self.paper_combo.currentText())
        if success:
            QMessageBox.information(
                self,
                "Impressão enviada",
                f"{len(self.pages)} página(s) foram enviadas para a impressora.",
            )
        else:
            QMessageBox.critical(self, "Erro de impressão", message)
