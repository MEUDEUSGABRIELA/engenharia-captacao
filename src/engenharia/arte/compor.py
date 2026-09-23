"""Composição da arte do post.

A tipografia é **composta em código**, nunca gerada dentro da imagem por IA: assim ela é exata,
editável e idêntica todo dia.

A identidade visual é emprestada do desenho técnico, que é a linguagem da própria profissão: malha
de fundo como papel milimetrado, cota de dimensão marcando o título, e um **carimbo** no rodapé —
a tarja que toda prancha tem, com marca, responsável, registro e contato em células.

**A imagem carrega a ideia.** Um post que compara PGR e PCMSO recebe um diagrama de comparação, não
uma foto de capacete: nenhuma foto diz "estas duas coisas são diferentes". O campo `visual` da pauta
escolhe a composição (ver `composicoes.py`). Foto real entra onde a foto *é* o assunto — bastidor,
campo, equipamento.

Nada aqui depende de banco de imagem, licença ou IA generativa. Além do custo, foto realista de IA
em perfil técnico custa alcance (a Meta penaliza pessoa gerada sem rótulo) e custa credibilidade,
que é o ativo de quem assina laudo.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw

from .. import config
from . import composicoes, marca
from .paleta import (
    ALTURA,
    APOIO,
    CORPO,
    DESTAQUE,
    FORTE,
    LARGURA,
    MALHA,
    MARGEM,
    PAPEL,
    TINTA,
    TITULO,
    VERDE,
    fonte as _fonte,
)

try:  # foto de iPhone vem em HEIC, que o Pillow só abre com este registro
    from pillow_heif import register_heif_opener

    register_heif_opener()
except ImportError:  # pragma: no cover - ambiente sem a dependência opcional
    pass

LOGO = config.RAIZ / "templates" / "logo.png"
ALTURA_CARIMBO = 108


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


def _carimbo(imagem: Image.Image, linhas: tuple[str, str], sobre_foto: bool) -> None:
    """O carimbo da prancha: tarja com células e a marca, no rodapé."""
    desenho = ImageDraw.Draw(imagem)
    topo = ALTURA - MARGEM - ALTURA_CARIMBO
    direita = LARGURA - MARGEM

    if sobre_foto:
        desenho.rectangle([MARGEM, topo, direita, topo + ALTURA_CARIMBO], fill=TINTA)
    desenho.rectangle([MARGEM, topo, direita, topo + ALTURA_CARIMBO], outline=APOIO, width=2)
    desenho.rectangle([MARGEM, topo, MARGEM + 14, topo + ALTURA_CARIMBO], fill=DESTAQUE)

    texto_x = MARGEM + 34
    if LOGO.exists():
        logo = Image.open(LOGO).convert("RGBA")
        lado = ALTURA_CARIMBO - 28
        logo.thumbnail((lado, lado), Image.LANCZOS)
        imagem.paste(logo, (texto_x, topo + (ALTURA_CARIMBO - logo.height) // 2), logo)
        texto_x += logo.width + 26
        desenho.line(
            [(texto_x - 13, topo + 12), (texto_x - 13, topo + ALTURA_CARIMBO - 12)],
            fill=APOIO,
            width=2,
        )

    desenho.line([(texto_x - 13, topo + 58), (direita, topo + 58)], fill=APOIO, width=2)
    desenho.text((texto_x, topo + 16), linhas[0], font=_fonte(FORTE, 31), fill=PAPEL)
    desenho.text((texto_x, topo + 70), linhas[1], font=_fonte(CORPO, 25), fill=APOIO)


def _fundo_de_foto(caminho: Path) -> Image.Image:
    """Foto real recortada para 4:5, escurecida na faixa onde o texto entra."""
    foto = Image.open(caminho).convert("RGB")
    proporcao = max(LARGURA / foto.width, ALTURA / foto.height)
    novo = (int(foto.width * proporcao) + 1, int(foto.height * proporcao) + 1)
    foto = foto.resize(novo, Image.LANCZOS)
    esquerda = (foto.width - LARGURA) // 2
    # Recorte enviesado para cima: em retrato o rosto fica no terço superior, e cortar
    # pelo centro decepa o capacete.
    topo = int((foto.height - ALTURA) * 0.25)
    foto = foto.crop((esquerda, topo, esquerda + LARGURA, topo + ALTURA))

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


def _cabecalho(
    desenho: ImageDraw.ImageDraw,
    etiqueta: str | None,
    indice: tuple[int, int] | None,
    y: int = MARGEM,
) -> None:
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
        desenho.text(
            (LARGURA - MARGEM - largura_texto, y + 14), texto, font=fonte_indice, fill=APOIO
        )


def _escrever_titulo(
    desenho: ImageDraw.ImageDraw, titulo: str, topo: int, limite: int, tamanhos: tuple[int, ...]
) -> int:
    """Escreve o título encolhendo até caber. Devolve o y logo abaixo dele."""
    for tamanho in tamanhos:
        fonte_titulo = _fonte(TITULO, tamanho)
        largura_em_caracteres = max(10, int(LARGURA * 2.05 / tamanho))
        linhas: list[str] = []
        for pedaco in titulo.split("\n"):
            linhas += textwrap.wrap(pedaco, width=largura_em_caracteres) or [""]
        altura_linha = int(tamanho * 0.96)
        if altura_linha * len(linhas) <= limite - topo - 52:
            break

    _cota(desenho, topo)
    y = topo + 48
    for linha in linhas:
        desenho.text((MARGEM, y), linha, font=fonte_titulo, fill=PAPEL)
        y += altura_linha
    return y


def _tela(
    titulo: str,
    carimbo: tuple[str, str],
    foto: Path | None = None,
    etiqueta: str | None = None,
    indice: tuple[int, int] | None = None,
    visual: dict | None = None,
) -> Image.Image:
    if foto:
        imagem = _fundo_de_foto(foto)
        desenho = ImageDraw.Draw(imagem)
    else:
        imagem = Image.new("RGB", (LARGURA, ALTURA), TINTA)
        desenho = ImageDraw.Draw(imagem)
        _malha(desenho)

    topo_conteudo = marca.lockup(imagem, PAPEL, APOIO)
    desenho = ImageDraw.Draw(imagem)
    _cabecalho(desenho, etiqueta, indice, topo_conteudo)

    base = ALTURA - marca.ALTURA_RODAPE - 54
    composicao = composicoes.TIPOS.get((visual or {}).get("tipo", ""))

    inicio = topo_conteudo + (78 if etiqueta else 24)

    if composicao:
        # Com diagrama, o título é manchete curta no topo e a composição ocupa o corpo.
        fim_titulo = _escrever_titulo(desenho, titulo, inicio, inicio + 330, (70, 62, 54, 48))
        composicao(imagem, visual or {}, fim_titulo + 54, base)
    elif foto:
        # Sobre foto o texto desce para a faixa escurecida — nunca por cima do rosto.
        fonte_titulo = _fonte(TITULO, 92)
        linhas = []
        for pedaco in titulo.split("\n"):
            linhas += textwrap.wrap(pedaco, width=max(10, int(LARGURA * 2.05 / 92))) or [""]
        altura_total = int(92 * 0.96) * len(linhas)
        _escrever_titulo(desenho, titulo, max(inicio, base - altura_total - 48), base, (92, 80, 70, 60))
    else:
        _escrever_titulo(
            desenho, titulo, inicio + max(0, (base - inicio - 300) // 2), base,
            (118, 104, 92, 80, 70, 60, 52),
        )

    marca.barra_contato(imagem)
    _ = carimbo
    return imagem


def _artes_prontas(dia: str, destino: Path) -> list[Path]:
    """Artes já exportadas da Canva para o dia, copiadas para o pacote de saída.

    É o caminho preferido: a arte sai na identidade real da marca, feita a partir dos próprios
    designs da responsável técnica. A geração em código continua existindo como rede de segurança
    para o dia que não tiver arte pronta na fila.
    """
    pasta = config.ARTES / dia
    if not pasta.exists():
        return []
    origens = sorted(
        p for p in pasta.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg")
    )
    copiadas = []
    for origem in origens:
        imagem = Image.open(origem).convert("RGB")
        arquivo = destino / f"{origem.stem}.jpg"
        imagem.save(arquivo, quality=93)
        copiadas.append(arquivo)
    return copiadas


def compor(post: dict, destino: Path) -> tuple[list[Path], list[str]]:
    """Gera as imagens do post. Devolve os arquivos e os avisos do que não deu para usar."""
    avisos: list[str] = []
    destino.mkdir(parents=True, exist_ok=True)

    prontas = _artes_prontas(str(post.get("data", "")), destino)
    if prontas:
        return prontas, avisos
    avisos.append(
        f"sem arte pronta em data/artes/{post.get('data')}/ — caiu para a geração em código"
    )
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

    visual = post.get("visual")
    if visual and foto:
        avisos.append("post tem visual e foto; a foto foi ignorada em favor do diagrama")
        foto = None
    if not visual and not foto and post.get("formato") != "carrossel":
        avisos.append("post sem visual nem foto — a capa saiu só com tipografia")

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
        visual,
    ).save(arquivos[0], quality=93)

    for indice, texto in enumerate(telas, start=2):
        arquivo = destino / f"{indice:02d}-tela.jpg"
        _tela(texto, carimbo, None, None, (indice, total)).save(arquivo, quality=93)
        arquivos.append(arquivo)

    return arquivos, avisos
