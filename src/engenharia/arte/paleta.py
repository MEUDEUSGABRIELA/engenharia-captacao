"""Paleta, medidas e fontes da identidade visual. Fonte única para todas as composições."""

from __future__ import annotations

from pathlib import Path

from PIL import ImageFont

from .. import config

LARGURA, ALTURA = 1080, 1350  # 4:5, o formato que ocupa mais tela no feed
MARGEM = 84

TINTA = (10, 26, 40)  # azul de prancha, quase preto
PAPEL = (243, 241, 236)  # off-white de papel técnico
DESTAQUE = (230, 150, 20)  # âmbar de sinalização
MALHA = (22, 44, 64)  # linhas da malha sobre a tinta
APOIO = (150, 172, 190)

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
