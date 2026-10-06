# FotoPrint

**FotoPrint** é um software para **Linux baseado em Debian**, desenvolvido para facilitar a organização, visualização e impressão de fotografias em diferentes layouts.

O programa foi inspirado na experiência simples dos antigos visualizadores de fotos do Windows, oferecendo uma maneira prática de selecionar várias fotografias, organizá-las automaticamente em folhas e realizar a impressão.



## Sobre o projeto

O objetivo do **FotoPrint** é tornar a impressão de fotografias simples e acessível.

O usuário pode selecionar várias imagens, escolher o tamanho das fotografias e o layout desejado. O programa calcula automaticamente quantas fotografias cabem em cada folha e cria novas páginas quando necessário.

Quando as fotografias não couberem em uma única folha, o programa criará automaticamente páginas adicionais e informará ao usuário a quantidade total de páginas que serão utilizadas.

## Principais recursos

- Seleção de uma ou várias fotografias.
- Pré-visualização das fotografias.
- Pré-visualização das páginas de impressão.
- Diversos tamanhos de fotografias.
- Diversos layouts de impressão.
- Organização automática das fotos.
- Suporte a papel A4.
- Impressão de várias fotos por página.
- Suporte a múltiplas páginas.
- Cálculo automático da quantidade de páginas.
- Aviso ao usuário sobre a quantidade de páginas.
- Preservação da proporção das fotografias.
- Geração de PDF.
- Integração com impressoras através do CUPS.
- Interface gráfica simples e intuitiva.
- Pacote `.deb` para instalação em sistemas baseados em Debian.

## Múltiplas páginas

Uma das principais funcionalidades do **FotoPrint** é a criação automática de múltiplas páginas.

Por exemplo, se o usuário selecionar:

```text
25 fotografias
8 fotografias por página
```

O programa calculará:

```text
Página 1 → 8 fotos
Página 2 → 8 fotos
Página 3 → 8 fotos
Página 4 → 1 foto

Total → 4 páginas
```

O usuário será informado antes da impressão:

```text
25 fotos selecionadas

8 fotos por página

Serão utilizadas 4 páginas.
```

Dessa forma, o usuário sempre saberá quantas folhas serão necessárias antes de iniciar a impressão.

## Layouts de impressão

O programa deverá oferecer diferentes layouts para organização das fotografias.

Entre os layouts planejados estão:

- 1 foto por página.
- 2 fotos por página.
- 4 fotos por página.
- 6 fotos por página.
- 8 fotos por página.
- Outros layouts personalizados.

Novos layouts poderão ser adicionados ao projeto futuramente.

## Tamanhos de fotografia

O programa deverá oferecer tamanhos comuns de impressão, como:

- 3 × 4 cm
- 5 × 7 cm
- 6 × 9 cm
- 7,5 × 6 cm
- 10 × 15 cm
- 13 × 18 cm
- Tamanho personalizado

Os tamanhos serão tratados como dimensões físicas de impressão.

## Pré-visualização

Antes de imprimir, o usuário poderá visualizar como as fotografias serão distribuídas na folha.

A pré-visualização deverá permitir verificar:

- posição das fotografias;
- quantidade de fotografias por página;
- tamanho das fotografias;
- número total de páginas;
- distribuição das fotografias entre as páginas.

## Sistema operacional

O **FotoPrint** é desenvolvido especificamente para **Linux**, com foco em distribuições **baseadas em Debian**.

Entre os sistemas compatíveis ou planejados estão:

- Debian
- Ubuntu
- Linux Mint
- Lubuntu
- KDE neon
- Outras distribuições derivadas do Debian/Ubuntu

A distribuição principal do software será através de um pacote:

```text
.deb
```

## Instalação

Após gerar o pacote, a instalação poderá ser realizada através do terminal:

```bash
sudo apt install ./fotoprint_1.0.0_amd64.deb
```

Também será possível instalar o pacote utilizando uma interface gráfica compatível com arquivos `.deb`.

Após a instalação, o **FotoPrint** deverá aparecer no menu de aplicativos do sistema.

## Tecnologia



- **Python**
- **PySide6**
- **Qt**
- **CUPS**
- **PDF**
- **Linux**
- **Debian Packaging**

A interface gráfica será desenvolvida com **PySide6**, enquanto o CUPS será utilizado para comunicação com o sistema de impressão do Linux.

## CUPS

O CUPS será responsável pela comunicação entre o aplicativo e as impressoras instaladas no sistema.

O programa deverá permitir ao usuário selecionar uma impressora disponível.

## PDF

O aplicativo também poderá gerar um arquivo PDF contendo todas as páginas de impressão.

Isso permitirá:

- conferir o resultado;
- salvar o trabalho;
- compartilhar o arquivo;
- imprimir posteriormente;
- utilizar outra impressora.

## Fluxo de utilização

O funcionamento principal do programa seguirá este fluxo:

```text
Selecionar fotos
       ↓
Escolher tamanho
       ↓
Escolher layout
       ↓
Escolher papel
       ↓
Calcular quantidade de páginas
       ↓
Montar páginas
       ↓
Visualizar
       ↓
Confirmar impressão
       ↓
Enviar para o CUPS
       ↓
Imprimir
```

## Estrutura do projeto

A estrutura planejada é:

```text
fotoprint/
│
├── main.py
├── README.md
├── preview.png
├── requirements.txt
├── LICENSE
│
├── src/
│   ├── __init__.py
│   │
│   ├── interface/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   └── preview.py
│   │
│   ├── printing/
│   │   ├── __init__.py
│   │   ├── printer.py
│   │   ├── layout.py
│   │   └── pages.py
│   │
│   ├── images/
│   │   ├── __init__.py
│   │   └── image_manager.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── settings.py
│
├── resources/
│   ├── icons/
│   └── images/
│
├── packaging/
│   └── debian/
│
└── tests/
```

## Desenvolvimento

Para executar o projeto durante o desenvolvimento:

```bash
python3 main.py
```

As dependências do projeto poderão ser instaladas através de:

```bash
pip install -r requirements.txt
```

## Geração do pacote DEB

O objetivo é disponibilizar o **FotoPrint** como um pacote `.deb` para sistemas Linux baseados em Debian.

Exemplo:

```text
fotoprint_1.0.0_amd64.deb
```

A instalação será feita através de:

```bash
sudo apt install ./fotoprint_1.0.0_amd64.deb
```

O usuário final não deverá precisar conhecer Python ou PySide6 para utilizar o programa.

A intenção é proporcionar uma experiência semelhante à instalação de qualquer outro aplicativo tradicional do Linux.

## Versões

### 0.1.0 — Desenvolvimento inicial

- Estrutura inicial do projeto.
- Interface gráfica.
- Seleção de imagens.
- Organização básica das fotografias.

### 0.2.0 — Layouts

- Tamanhos de fotografia.
- Layouts de impressão.
- Cálculo de fotos por página.
- Pré-visualização.

### 0.3.0 — Múltiplas páginas

- Criação automática de páginas adicionais.
- Contagem de páginas.
- Navegação entre páginas.
- Aviso ao usuário sobre a quantidade de páginas.

### 0.4.0 — Impressão

- Integração com CUPS.
- Seleção de impressora.
- Configurações básicas de impressão.

### 0.5.0 — PDF

- Geração de PDF.
- Visualização do PDF.
- Salvamento do trabalho.

### 1.0.0 — Primeira versão estável

- Interface completa.
- Layouts de impressão.
- Múltiplas páginas.
- Pré-visualização.
- Impressão.
- PDF.
- Pacote `.deb`.
- Ícone do aplicativo.
- Integração com o menu do Linux.

## Próximas funcionalidades

Possíveis funcionalidades futuras:

- Arrastar e soltar fotografias.
- Reordenar fotografias.
- Rotação individual das imagens.
- Corte automático.
- Ajuste automático.
- Margens personalizadas.
- Sangria.
- Impressão sem bordas.
- Tamanho de papel personalizado.
- Configuração de DPI.
- Mais formatos de papel.
- Histórico de impressões.
- Salvar projetos.
- Carregar projetos.
- Temas claro e escuro.
- Atalhos de teclado.
- Impressão frente e verso quando suportada pela impressora.

## Filosofia do projeto

O **FotoPrint** foi criado seguindo três princípios:

### Simplicidade

O usuário deve conseguir imprimir suas fotografias sem precisar utilizar programas complexos de edição de imagens.

### Automação

O programa deve calcular automaticamente a distribuição das fotografias e a quantidade de páginas necessárias.

### Previsibilidade

Antes de imprimir, o usuário deve saber exatamente como as fotografias serão organizadas e quantas páginas serão utilizadas.

## Status

**Em desenvolvimento.**

O **FotoPrint** está sendo desenvolvido para **Linux baseado em Debian**, com foco em impressão simples e eficiente de fotografias.

## Autor

Desenvolvido por **Carlos**.

**FotoPrint — impressão de fotografias de forma simples no Linux.**

