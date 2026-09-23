"""Gera `templates/logo.png` a partir do SVG da marca.

    python -m engenharia.arte.logo

O PNG é **gerado**, não editado à mão: o que muda é o SVG, e o PNG é regerado. Mesma convenção do
`projects/laudos`, que também trata o vetorial como fonte da verdade da marca.
"""

from __future__ import annotations

import io
import sys

from PIL import Image
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

from .. import config

ORIGEM = config.RAIZ / "templates" / "logo-simbolo.svg"
DESTINO = config.RAIZ / "templates" / "logo.png"
LARGURA_ALVO = 600  # bem acima do necessário no carimbo, para não pixelizar


def gerar() -> None:
    if not ORIGEM.exists():
        raise SystemExit(f"SVG da marca não encontrado: {ORIGEM}")

    desenho = svg2rlg(str(ORIGEM))
    escala = LARGURA_ALVO / desenho.width
    desenho.width *= escala
    desenho.height *= escala
    desenho.scale(escala, escala)

    # Fundo transparente: a logo vai sobre o carimbo escuro.
    dados = renderPM.drawToString(desenho, fmt="PNG", bg=0xFFFFFF)
    imagem = Image.open(io.BytesIO(dados)).convert("RGBA")

    # renderPM não faz transparência; o branco do fundo vira alfa zero.
    pixels = imagem.load()
    for y in range(imagem.height):
        for x in range(imagem.width):
            r, g, b, _ = pixels[x, y]
            if r > 248 and g > 248 and b > 248:
                pixels[x, y] = (r, g, b, 0)

    imagem.save(DESTINO)
    print(f"Gerado: {DESTINO} ({imagem.width}x{imagem.height})")


if __name__ == "__main__":
    sys.exit(gerar())
