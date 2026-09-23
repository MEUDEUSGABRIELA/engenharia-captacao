"""Tipos de composição visual. Cada post declara qual usar, no campo `visual` da pauta.

A regra de ouro: **a imagem carrega a ideia**. Post que compara duas coisas ganha um diagrama de
comparação; post que lista ganha uma lista numerada; post que contrapõe certo e errado ganha duas
faixas. Foto real só onde a foto *é* o assunto — bastidor, campo, equipamento.

Nenhuma composição depende de banco de imagem, de licença ou de IA: tudo é desenhado em código, o
que mantém o motor gratuito, reproduzível e idêntico todo dia.
"""

from __future__ import annotations

import textwrap

from PIL import Image, ImageDraw

from .paleta import (
    ALTURA,
    APOIO,
    CORPO,
    DESTAQUE,
    FORTE,
    LARGURA,
    MARGEM,
    PAPEL,
    TINTA,
    TITULO,
    fonte,
)

ERRO = (198, 72, 60)
ACERTO = (58, 158, 110)


def _texto_quebrado(
    desenho: ImageDraw.ImageDraw,
    texto: str,
    x: int,
    y: int,
    largura_px: int,
    arquivo,
    tamanho: int,
    cor,
    entrelinha: float = 1.18,
) -> int:
    """Escreve texto quebrando por largura em pixels. Devolve o y final."""
    fonte_usada = fonte(arquivo, tamanho)
    largura_media = desenho.textlength("n", font=fonte_usada) or tamanho * 0.5
    por_linha = max(6, int(largura_px / largura_media))
    for pedaco in texto.split("\n"):
        for linha in textwrap.wrap(pedaco, width=por_linha) or [""]:
            desenho.text((x, y), linha, font=fonte_usada, fill=cor)
            y += int(tamanho * entrelinha)
    return y


def comparacao(imagem: Image.Image, visual: dict, topo: int, base: int) -> None:
    """Duas colunas rotuladas, lado a lado, separadas por um eixo.

    É a composição para post que diz "A e B não são a mesma coisa": o leitor vê a distinção
    antes de ler uma palavra da legenda.
    """
    desenho = ImageDraw.Draw(imagem)
    meio = LARGURA // 2

    # Estima a altura da coluna mais alta para centralizar o conjunto na faixa disponível,
    # em vez de deixar o diagrama grudado no topo com um vazio embaixo.
    maior = 0
    for chave in ("esquerda", "direita"):
        bloco = visual.get(chave, {})
        alto = 126 + 34
        alto += len(bloco.get("destaque", "").split("\n")) * 60 + 18
        alto += (len(bloco.get("texto", "")) // 26 + 1) * 44
        maior = max(maior, alto)
    topo = topo + max(0, (base - topo - maior) // 3)

    desenho.line([(meio, topo + 40), (meio, base - 30)], fill=APOIO, width=2)

    for lado, chave in ((0, "esquerda"), (1, "direita")):
        bloco = visual.get(chave, {})
        x = MARGEM if lado == 0 else meio + 40
        largura_col = meio - MARGEM - 40

        y = topo
        rotulo = bloco.get("rotulo", "")
        fonte_rotulo = fonte(TITULO, 76)
        desenho.text((x, y), rotulo, font=fonte_rotulo, fill=DESTAQUE)
        y += 92

        desenho.line([(x, y), (x + 84, y)], fill=DESTAQUE, width=5)
        y += 34

        destaque_txt = bloco.get("destaque", "")
        if destaque_txt:
            y = _texto_quebrado(desenho, destaque_txt, x, y, largura_col, TITULO, 60, PAPEL, 1.05)
            y += 22

        corpo_txt = bloco.get("texto", "")
        if corpo_txt:
            _texto_quebrado(desenho, corpo_txt, x, y, largura_col, CORPO, 36, APOIO, 1.3)


def contraste(imagem: Image.Image, visual: dict, topo: int, base: int) -> None:
    """Duas faixas empilhadas: o que não funciona em cima, o que funciona embaixo."""
    desenho = ImageDraw.Draw(imagem)
    altura_faixa = (base - topo - 40) // 2

    for indice, (chave, cor, marca) in enumerate(
        (("errado", ERRO, "X"), ("certo", ACERTO, "✓"))
    ):
        bloco = visual.get(chave, {})
        y0 = topo + indice * (altura_faixa + 40)
        desenho.rectangle(
            [MARGEM, y0, LARGURA - MARGEM, y0 + altura_faixa], outline=cor, width=3
        )
        desenho.rectangle([MARGEM, y0, MARGEM + 96, y0 + altura_faixa], fill=cor)
        fonte_marca = fonte(FORTE, 56)
        largura_marca = desenho.textlength(marca, font=fonte_marca)
        desenho.text(
            (MARGEM + 48 - largura_marca / 2, y0 + altura_faixa / 2 - 38),
            marca,
            font=fonte_marca,
            fill=TINTA,
        )

        x = MARGEM + 130
        largura_txt = LARGURA - MARGEM - x - 30
        y = y0 + 30
        y = _texto_quebrado(
            desenho, bloco.get("titulo", ""), x, y, largura_txt, TITULO, 52, PAPEL, 1.05
        )
        if bloco.get("texto"):
            _texto_quebrado(
                desenho, bloco["texto"], x, y + 14, largura_txt, CORPO, 31, APOIO, 1.28
            )


def lista(imagem: Image.Image, visual: dict, topo: int, base: int) -> None:
    """Itens numerados, com o número em destaque. Para post que enumera documentos ou etapas."""
    desenho = ImageDraw.Draw(imagem)
    itens = visual.get("itens", [])
    if not itens:
        return
    passo = (base - topo) // max(1, len(itens))

    for indice, item in enumerate(itens, start=1):
        y = topo + (indice - 1) * passo
        numero = f"{indice:02d}"
        fonte_numero = fonte(TITULO, 60)
        desenho.text((MARGEM, y), numero, font=fonte_numero, fill=DESTAQUE)
        x = MARGEM + 108
        desenho.line([(MARGEM + 88, y + 10), (MARGEM + 88, y + passo - 30)], fill=APOIO, width=2)
        _texto_quebrado(
            desenho, item, x, y + 2, LARGURA - MARGEM - x, TITULO, 46, PAPEL, 1.08
        )


def numero(imagem: Image.Image, visual: dict, topo: int, base: int) -> None:
    """Um número gigante com a unidade e a frase. Para dado que já é a manchete."""
    desenho = ImageDraw.Draw(imagem)
    fonte_numero = fonte(TITULO, 300)
    texto = str(visual.get("numero", ""))
    desenho.text((MARGEM, topo - 40), texto, font=fonte_numero, fill=DESTAQUE)
    largura_num = desenho.textlength(texto, font=fonte_numero)

    if visual.get("unidade"):
        desenho.text(
            (MARGEM + largura_num + 20, topo + 40),
            visual["unidade"],
            font=fonte(TITULO, 76),
            fill=PAPEL,
        )

    y = topo + 290
    _texto_quebrado(
        desenho, visual.get("texto", ""), MARGEM, y, LARGURA - 2 * MARGEM, TITULO, 64, PAPEL, 1.06
    )


TIPOS = {
    "comparacao": comparacao,
    "contraste": contraste,
    "lista": lista,
    "numero": numero,
}
