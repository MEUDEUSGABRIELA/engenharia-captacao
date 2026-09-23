"""Paleta, medidas e fontes da identidade visual.

As cores **não foram inventadas**: saíram do feed que a responsável técnica já publicava e do SVG da
marca. Verde sobre fundo escuro é o padrão dela; a marca aparece no topo, não escondida no rodapé;
e o rodapé traz a barra de contato com WhatsApp e @, igual em todo post.
"""

from __future__ import annotations

from pathlib import Path

from PIL import ImageFont

from .. import config

LARGURA, ALTURA = 1080, 1350  # 4:5, o formato que ocupa mais tela no feed
MARGEM = 84

TINTA = (22, 36, 46)  # fundo escuro do feed
VERDE = (0, 191, 99)  # o verde da marca, tirado do SVG da logo
PAPEL = (255, 255, 255)
CREME = (242, 237, 228)
APOIO = (154, 174, 186)
GRAFITE = (65, 81, 87)  # cinza da marca, para uso sobre fundo claro

# Mantidos por compatibilidade com composições que ainda citam os nomes antigos.
DESTAQUE = VERDE
MALHA = (32, 50, 62)

FONTES = config.RAIZ / "templates" / "fontes"
TITULO = FONTES / "BarlowCondensed-Bold.ttf"
CORPO = FONTES / "Barlow-Medium.ttf"
FORTE = FONTES / "Barlow-Bold.ttf"

_ALTERNATIVAS = (
    r"C:\Windows\Fonts\segoeuib.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)


def fonte(arquivo: Path, tamanho: int) -> ImageFont.FreeTypeFont:
    if arquivo.exists():
        return ImageFont.truetype(str(arquivo), tamanho)
    # Sem a fonte do projeto a arte ainda sai, mas fora da identidade: é erro de instalação.
    for alternativa in _ALTERNATIVAS:
        if Path(alternativa).exists():
            return ImageFont.truetype(alternativa, tamanho)
    return ImageFont.load_default(tamanho)
