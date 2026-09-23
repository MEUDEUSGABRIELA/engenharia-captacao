"""Assinatura da marca: o lockup no topo e a barra de contato no rodapé.

Reproduz o padrão que o próprio feed já estabeleceu — símbolo mais "GABRIELA LIMA" e a linha de
especialidades no alto, barra com WhatsApp e @ embaixo. Os textos vêm de `kb/identidade.yaml`;
nada aqui é escrito à mão no código.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from .. import config
from .paleta import APOIO, CORPO, FORTE, LARGURA, MARGEM, TITULO, VERDE, fonte

LOGO = config.RAIZ / "templates" / "logo.png"
ALTURA_TOPO = 118
ALTURA_RODAPE = 96


def lockup(imagem: Image.Image, cor_nome, cor_linha) -> int:
    """Símbolo + nome + especialidades, no topo. Devolve o y onde o conteúdo pode começar."""
    desenho = ImageDraw.Draw(imagem)
    perfil = config.identidade()
    x = MARGEM
    y = MARGEM - 14

    if LOGO.exists():
        logo = Image.open(LOGO).convert("RGBA")
        logo.thumbnail((96, 96), Image.LANCZOS)
        imagem.paste(logo, (x, y), logo)
        x += logo.width + 20

    desenho.text((x, y + 8), "GABRIELA LIMA", font=fonte(TITULO, 52), fill=cor_nome)
    desenho.text(
        (x + 3, y + 62),
        "ENGENHARIA AMBIENTAL, CIVIL E SEGURANÇA",
        font=fonte(CORPO, 21),
        fill=cor_linha,
    )
    _ = perfil
    return MARGEM + ALTURA_TOPO


def barra_contato(imagem: Image.Image, sobre_claro: bool = False) -> None:
    """Barra verde do rodapé, com telefone e @ — igual em todo post."""
    desenho = ImageDraw.Draw(imagem)
    contato = config.identidade()["contato"]
    perfil = config.identidade()["perfil"]

    altura = ALTURA_RODAPE
    topo = imagem.height - altura
    desenho.rectangle([0, topo, LARGURA, imagem.height], fill=VERDE)

    fonte_tel = fonte(FORTE, 34)
    fonte_arroba = fonte(CORPO, 29)
    tinta = (12, 40, 26)

    desenho.text((MARGEM, topo + 20), contato["telefone"], font=fonte_tel, fill=tinta)
    arroba = perfil["handle"]
    largura = desenho.textlength(arroba, font=fonte_arroba)
    desenho.text((LARGURA - MARGEM - largura, topo + 26), arroba, font=fonte_arroba, fill=tinta)
    _ = sobre_claro
    _ = APOIO
