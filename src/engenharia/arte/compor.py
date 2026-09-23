"""Composição da arte do post.

A tipografia é **composta em código**, nunca gerada dentro da imagem por IA: assim ela é exata,
editável e idêntica todo dia.

A identidade visual é emprestada do desenho técnico, que é a linguagem da própria profissão: malha
de fundo como papel milimetrado, cota de dimensão marcando o título, e um **carimbo** no rodapé —
a tarja que toda prancha tem, com responsável, registro e contato em células. É o que diferencia
este perfil de um cartão de frases com fundo colorido.

Quando existe foto real do trabalho (`ativo` na pauta), ela é o fundo; quando não existe, a arte é
de template — e nenhuma foto de obra é inventada.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .. import config

try:  # foto de iPhone vem em HEIC, que o Pillow só abre com este registro
    from pillow_heif import register_heif_opener

    register_heif_opener()
except ImportError:  # pragma: no cover - ambiente sem a dependência opcional
    pass

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


def _fonte(arquivo: Path, tamanho: int) -> ImageFont.FreeTypeFont:
    if arquivo.exists():
        return ImageFont.truetype(str(arquivo), tamanho)
    # Sem a fonte do projeto a arte ainda sai, mas fora da identidade: é erro de instalação.
    for alternativa in (
        r"C:\Windows\Fonts\segoeuib.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        if Path(alternativa).exists():
            return ImageFont.truetype(alternativa, tamanho)
    return ImageFont.load_default(tamanho)


def _malha(desenho: ImageDraw.ImageDraw, passo: int = 54) -> None:
    """Papel milimetrado discreto: dá textura sem competir com o texto."""
    for x in range(0, LARGURA, passo):
        desenho.line([(x, 0), (x, ALTURA)], fill=MALHA, width=1)
    for y in range(0, ALTURA, passo):
        desenho.line([(0, y), (LARGURA, y)], fill=MALHA, width=1)


def _cota(desenho: ImageDraw.ImageDraw, y: int, largura: int = 210) -> None:
    """Uma cota de dimensão — linha com as setinhas nas pontas, como em planta."""
    x1, x2 = MARGEM, MARGEM + largura
    desenho.line([(x1, y), (x2, y)], fill=DESTAQUE, width=4)
    for x, sentido in ((x1, 1), (x2, -1)):
        desenho.polygon(
            [(x, y), (x + sentido * 16, y - 8), (x + sentido * 16, y + 8)], fill=DESTAQUE
        )


LOGO = config.RAIZ / "templates" / "logo.png"


def _carimbo(imagem: Image.Image, linhas: tuple[str, str], sobre_foto: bool) -> None:
    """O carimbo da prancha: tarja com células e a logo, no rodapé."""
    desenho = ImageDraw.Draw(imagem)
    altura = 108
    topo = ALTURA - MARGEM - altura
    direita = LARGURA - MARGEM

    if sobre_foto:
        desenho.rectangle([MARGEM, topo, direita, topo + altura], fill=TINTA)
    desenho.rectangle([MARGEM, topo, direita, topo + altura], outline=APOIO, width=2)
    desenho.rectangle([MARGEM, topo, MARGEM + 14, topo + altura], fill=DESTAQUE)

    texto_x = MARGEM + 34
    if LOGO.exists():
        # A logo ocupa a célula da esquerda; o texto desloca para a direita dela.
        logo = Image.open(LOGO).convert("RGBA")
        lado = altura - 28
        logo.thumbnail((lado, lado), Image.LANCZOS)
        imagem.paste(logo, (texto_x, topo + (altura - logo.height) // 2), logo)
        texto_x += logo.width + 26
        desenho.line(
            [(texto_x - 13, topo + 12), (texto_x - 13, topo + altura - 12)], fill=APOIO, width=2
        )

    desenho.line([(texto_x - 13, topo + 58), (direita, topo + 58)], fill=APOIO, width=2)
    desenho.text((texto_x, topo + 16), linhas[0], font=_fonte(FORTE, 31), fill=PAPEL)
    desenho.text((texto_x, topo + 70), linhas[1], font=_fonte(CORPO, 25), fill=APOIO)


def _fundo_de_foto(caminho: Path) -> Image.Image:
    """Foto real recortada para 4:5, escurecida para o texto ter contraste."""
    foto = Image.open(caminho).convert("RGB")
    proporcao = max(LARGURA / foto.width, ALTURA / foto.height)
    novo = (int(foto.width * proporcao) + 1, int(foto.height * proporcao) + 1)
    foto = foto.resize(novo, Image.LANCZOS)
    esquerda = (foto.width - LARGURA) // 2
    # Recorte enviesado para cima: em retrato o rosto fica no terço superior, e cortar
    # pelo centro decepa o capacete.
    topo = int((foto.height - ALTURA) * 0.25)
    foto = foto.crop((esquerda, topo, esquerda + LARGURA, topo + ALTURA))

    # O véu escurece só a faixa de baixo, onde o texto vai. O rosto fica limpo em cima.
    veu = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
    desenho = ImageDraw.Draw(veu)
    inicio = int(ALTURA * 0.42)
    for y in range(ALTURA):
        if y < inicio:
            opacidade = int(30 * (y / inicio))
        else:
            avanco = (y - inicio) / (ALTURA - inicio)
            opacidade = int(30 + 205 * avanco**0.85)
        desenho.line([(0, y), (LARGURA, y)], fill=(6, 18, 30, opacidade))
    return Image.alpha_composite(foto.convert("RGBA"), veu).convert("RGB")


def _tela(
    titulo: str,
    carimbo: tuple[str, str],
    foto: Path | None = None,
    etiqueta: str | None = None,
    indice: tuple[int, int] | None = None,
) -> Image.Image:
    if foto:
        imagem = _fundo_de_foto(foto)
        desenho = ImageDraw.Draw(imagem)
    else:
        imagem = Image.new("RGB", (LARGURA, ALTURA), TINTA)
        desenho = ImageDraw.Draw(imagem)
        _malha(desenho)

    y = MARGEM

    if etiqueta:
        fonte_etiqueta = _fonte(FORTE, 27)
        texto = etiqueta.upper()
        largura_texto = desenho.textbbox((0, 0), texto, font=fonte_etiqueta)[2]
        desenho.rectangle([MARGEM, y, MARGEM + largura_texto + 40, y + 52], fill=DESTAQUE)
        desenho.text((MARGEM + 20, y + 11), texto, font=fonte_etiqueta, fill=TINTA)

    if indice:
        atual, total = indice
        fonte_indice = _fonte(CORPO, 28)
        texto = f"{atual:02d}/{total:02d}"
        largura_texto = desenho.textbbox((0, 0), texto, font=fonte_indice)[2]
        desenho.text((LARGURA - MARGEM - largura_texto, y + 14), texto, font=fonte_indice, fill=APOIO)

    # O título ocupa o bloco central. Encolhe até caber, sem nunca cortar palavra.
    topo_bloco = MARGEM + 150
    fundo_bloco = ALTURA - MARGEM - 108 - 116
    disponivel = fundo_bloco - topo_bloco

    for tamanho in (118, 104, 92, 80, 70, 60, 52):
        fonte = _fonte(TITULO, tamanho)
        largura_em_caracteres = max(10, int(LARGURA * 2.05 / tamanho))
        linhas = []
        for pedaco in titulo.split("\n"):
            linhas += textwrap.wrap(pedaco, width=largura_em_caracteres) or [""]
        altura_linha = int(tamanho * 0.96)
        if altura_linha * len(linhas) <= disponivel - 52:
            break

    altura_total = altura_linha * len(linhas)
    if foto:
        # Sobre foto o texto desce para a faixa escurecida — nunca por cima do rosto.
        y = fundo_bloco - altura_total
    else:
        y = topo_bloco + max(0, (disponivel - altura_total - 52) // 2)
    _cota(desenho, y)
    y += 48
    for linha in linhas:
        desenho.text((MARGEM, y), linha, font=fonte, fill=PAPEL)
        y += altura_linha

    _carimbo(imagem, carimbo, sobre_foto=foto is not None)
    return imagem


def compor(post: dict, destino: Path) -> tuple[list[Path], list[str]]:
    """Gera as imagens do post. Devolve os arquivos e os avisos do que não deu para usar."""
    avisos: list[str] = []
    rodape = config.identidade()["rodape"]
    carimbo = (rodape["linha_1"], rodape["linha_2"])
    destino.mkdir(parents=True, exist_ok=True)

    foto = None
    ativo = post.get("ativo")
    if ativo and not str(ativo).startswith("⟨PENDENTE"):
        caminho = config.ATIVOS / str(ativo)
        if caminho.exists():
            foto = caminho
        else:
            avisos.append(f"ativo declarado e não encontrado: {caminho}")
    elif ativo:
        avisos.append("ativo pendente — a arte saiu de template, sem foto real")

    ficha = config.segmentos().get(post.get("segmento", ""))
    etiqueta = ficha["etiqueta"] if ficha else None

    telas = post.get("telas") or []
    total = len(telas) + 1

    arquivos = [destino / "01-capa.jpg"]
    _tela(
        post.get("titulo") or post.get("tema", ""),
        carimbo,
        foto,
        etiqueta,
        (1, total) if telas else None,
    ).save(arquivos[0], quality=93)

    for indice, texto in enumerate(telas, start=2):
        arquivo = destino / f"{indice:02d}-tela.jpg"
        _tela(texto, carimbo, None, None, (indice, total)).save(arquivo, quality=93)
        arquivos.append(arquivo)

    return arquivos, avisos
