"""Composição da arte do post.

A tipografia é **composta em código**, nunca gerada dentro da imagem por IA: assim ela é exata,
editável e idêntica todo dia. Quando existe foto real do trabalho (`ativo` na pauta), ela é o fundo;
quando não existe, a arte é de template — e nenhuma foto de obra é inventada.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .. import config

LARGURA, ALTURA = 1080, 1350  # 4:5, o formato que ocupa mais tela no feed
MARGEM = 90

FUNDO = (14, 34, 51)  # azul profundo
DESTAQUE = (245, 166, 35)  # âmbar de sinalização
TEXTO = (255, 255, 255)
APOIO = (168, 189, 206)

CANDIDATAS_NEGRITO = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
CANDIDATAS_REGULAR = [
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def _fonte(tamanho: int, negrito: bool = True) -> ImageFont.FreeTypeFont:
    for caminho in CANDIDATAS_NEGRITO if negrito else CANDIDATAS_REGULAR:
        if Path(caminho).exists():
            return ImageFont.truetype(caminho, tamanho)
    # Sem fonte instalada a arte ainda sai, mas feia: é sinal de ambiente mal configurado.
    return ImageFont.load_default(tamanho)


def _quebrar(texto: str, largura_em_caracteres: int) -> list[str]:
    """Respeita as quebras escritas na pauta e quebra o que ficou comprido demais."""
    linhas: list[str] = []
    for pedaco in texto.split("\n"):
        linhas += textwrap.wrap(pedaco, width=largura_em_caracteres) or [""]
    return linhas


def _fundo_de_foto(caminho: Path) -> Image.Image:
    """Foto real recortada para 4:5, escurecida para o texto ter contraste."""
    foto = Image.open(caminho).convert("RGB")
    proporcao = max(LARGURA / foto.width, ALTURA / foto.height)
    novo = (int(foto.width * proporcao) + 1, int(foto.height * proporcao) + 1)
    foto = foto.resize(novo, Image.LANCZOS)
    esquerda = (foto.width - LARGURA) // 2
    topo = (foto.height - ALTURA) // 2
    foto = foto.crop((esquerda, topo, esquerda + LARGURA, topo + ALTURA))

    veu = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
    desenho = ImageDraw.Draw(veu)
    for y in range(ALTURA):
        opacidade = int(40 + 175 * (y / ALTURA) ** 1.6)
        desenho.line([(0, y), (LARGURA, y)], fill=(8, 20, 32, opacidade))
    return Image.alpha_composite(foto.convert("RGBA"), veu).convert("RGB")


def _tela(titulo: str, rodape: str, foto: Path | None = None, etiqueta: str | None = None) -> Image.Image:
    imagem = _fundo_de_foto(foto) if foto else Image.new("RGB", (LARGURA, ALTURA), FUNDO)
    desenho = ImageDraw.Draw(imagem)

    if etiqueta:
        fonte_etiqueta = _fonte(30, negrito=True)
        caixa = desenho.textbbox((0, 0), etiqueta.upper(), font=fonte_etiqueta)
        largura_texto = caixa[2] - caixa[0]
        desenho.rectangle(
            [MARGEM, MARGEM, MARGEM + largura_texto + 44, MARGEM + 62],
            fill=DESTAQUE,
        )
        desenho.text((MARGEM + 22, MARGEM + 14), etiqueta.upper(), font=fonte_etiqueta, fill=FUNDO)

    # O título encolhe até caber: post que corta frase no meio não presta.
    for tamanho in (86, 78, 70, 62, 54, 48):
        fonte = _fonte(tamanho, negrito=True)
        largura_em_caracteres = max(12, int(LARGURA * 1.9 / tamanho))
        linhas = _quebrar(titulo, largura_em_caracteres)
        altura_linha = int(tamanho * 1.24)
        altura_total = altura_linha * len(linhas)
        if altura_total <= ALTURA - 2 * MARGEM - 300:
            break

    y = ALTURA - MARGEM - 170 - altura_total
    desenho.rectangle([MARGEM, y - 46, MARGEM + 130, y - 36], fill=DESTAQUE)
    for linha in linhas:
        desenho.text((MARGEM, y), linha, font=fonte, fill=TEXTO)
        y += altura_linha

    fonte_rodape = _fonte(30, negrito=False)
    desenho.text((MARGEM, ALTURA - MARGEM - 40), rodape, font=fonte_rodape, fill=APOIO)
    return imagem


def compor(post: dict, destino: Path) -> tuple[list[Path], list[str]]:
    """Gera as imagens do post. Devolve os arquivos e os avisos do que não deu para usar."""
    avisos: list[str] = []
    rodape = "@meudeusgabrielaengenharia  ·  (18) 99641-8959"
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

    etiqueta = {"sst": "segurança do trabalho", "civil": "engenharia civil", "ambiental": "ambiental"}.get(
        post.get("segmento", ""), None
    )

    arquivos = [destino / "01-capa.jpg"]
    _tela(post.get("titulo") or post.get("tema", ""), rodape, foto, etiqueta).save(
        arquivos[0], quality=92
    )

    for indice, texto in enumerate(post.get("telas") or [], start=2):
        arquivo = destino / f"{indice:02d}-tela.jpg"
        _tela(texto, rodape, None, None).save(arquivo, quality=92)
        arquivos.append(arquivo)

    return arquivos, avisos
