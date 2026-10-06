# FotoPrint

Aplicativo Linux para seleção, composição, pré-visualização e impressão de fotos em múltiplos layouts.

## Tecnologias

- Python 3
- PySide6
- CUPS
- Pillow

## Executar em modo desenvolvimento

```bash
sudo apt install python3 python3-pip python3-pyside6 cups-client python3-pil
cd fotoprint
python3 -m fotoprint
```

## Gerar pacote .deb

```bash
./build-deb.sh
```

O pacote será criado em `dist/`.

## Recursos da primeira versão

- Seleção múltipla de fotos
- Miniaturas
- Papel A4/A5/Letter, retrato/paisagem
- Tamanhos fixos como no assistente "Imprimir Imagens" do Windows: página inteira,
  20x25 cm, 8x10 pol., 13x18 cm, 5x7 pol., 10x15 cm, 4x6 pol., 9x13 cm, 3,5x5 pol.,
  carteira (9) e folha de contato (35). Só aparecem os tamanhos que cabem no papel.
- Ajuste da foto ao quadro (corta o excesso) ou foto inteira
- Cópias de cada foto
- Cálculo automático de múltiplas páginas e indicador "Página X de Y"
- Pré-visualização
- Impressão via CUPS (tamanho real preservado)
- Exportação da composição para PDF
