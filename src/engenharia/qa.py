"""Conferência antes de publicar.

O que este módulo recusa não é questão de gosto: é o que a regra inviolável do projeto proíbe de ir
ao ar. Um achado aqui para a publicação final (`--final` é o padrão quando não há `--dry-run`).
"""

from __future__ import annotations

from . import config

PILARES = {"alerta-legal", "erro-caro", "bastidor", "pergunta", "servico", "feriado"}
FORMATOS = {"estatico", "carrossel", "reels", "nenhum"}
SEGMENTOS = {"sst", "civil", "ambiental", "nenhum"}
LIMITE_LEGENDA = 2200  # limite do Instagram, hashtags incluídas


def conferir_post(post: dict) -> list[str]:
    """Achados estruturais da entrada de pauta. Lista vazia = pauta íntegra."""
    achados = []
    for campo in ("data", "pilar", "segmento", "formato", "tema"):
        if not post.get(campo):
            achados.append(f"campo obrigatório vazio: {campo}")
    if post.get("pilar") not in PILARES:
        achados.append(f"pilar desconhecido: {post.get('pilar')!r}")
    if post.get("formato") not in FORMATOS:
        achados.append(f"formato desconhecido: {post.get('formato')!r}")
    if post.get("segmento") not in SEGMENTOS:
        achados.append(f"segmento desconhecido: {post.get('segmento')!r}")
    if post.get("formato") == "carrossel" and not post.get("telas"):
        achados.append("carrossel sem telas")
    return achados


def conferir_legenda(legenda: str) -> list[str]:
    """Achados que impedem a publicação de um texto."""
    achados = []
    for marcador in config.MARCADORES_BLOQUEIO:
        if marcador in legenda:
            achados.append(f"legenda contém {marcador} — precisa de conferência humana antes de ir ao ar")
    minuscula = legenda.lower()
    for termo in config.termos_proibidos():
        if termo in minuscula:
            achados.append(f"termo proibido na legenda: {termo!r} (kb/regras-publicidade.md)")
    if len(legenda) > LIMITE_LEGENDA:
        achados.append(f"legenda com {len(legenda)} caracteres; o Instagram corta em {LIMITE_LEGENDA}")
    if not legenda.strip():
        achados.append("legenda vazia")
    return achados


def conferir_pauta(posts: list[dict]) -> list[str]:
    """Confere a pauta inteira. Usado por `--conferir`, antes de qualquer coisa ser montada."""
    achados = []
    datas = [post.get("data") for post in posts]
    repetidas = {data for data in datas if datas.count(data) > 1}
    for data in sorted(repetidas):
        achados.append(f"data repetida na pauta: {data}")
    for post in posts:
        if post.get("status") == "feriado":
            continue
        prefixo = f"{post.get('data')}: "
        achados += [prefixo + achado for achado in conferir_post(post)]
    return achados
