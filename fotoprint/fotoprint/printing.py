import subprocess
from pathlib import Path


def list_printers() -> list[str]:
    try:
        result = subprocess.run(
            ["lpstat", "-p"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return []

    printers = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0] == "printer":
            printers.append(parts[1])
    return printers


def print_files(
    files: list[Path],
    printer: str | None = None,
    media: str | None = None,
    ppi: int = 150,
) -> tuple[bool, str]:
    if not files:
        return False, "Nenhuma página para imprimir."

    command = ["lp"]
    if printer:
        command += ["-d", printer]
    # ppi evita que o CUPS redimensione a imagem: preserva o tamanho real das fotos
    command += ["-o", f"ppi={ppi}"]
    if media:
        command += ["-o", f"media={media}"]
    command += [str(path) for path in files]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return False, "O comando 'lp' não está instalado. Instale cups-client."

    if result.returncode != 0:
        return False, result.stderr.strip() or "Falha ao enviar para a impressora."

    return True, result.stdout.strip()
