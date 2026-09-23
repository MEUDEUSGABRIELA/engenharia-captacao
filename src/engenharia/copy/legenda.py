"""Montagem da legenda final: o texto da pauta mais o bloco de hashtags.

O módulo **não escreve conteúdo técnico**. O texto que vai ao ar é o que está em
`data/pauta/calendario.yaml`, escrito e conferido por gente. Aqui só se acrescenta hashtag.
"""

from __future__ import annotations

import random

from .. import config

BLOCO_POR_SEGMENTO = {
    "sst": "segurancadotrabalho",
    "civil": "civil",
    "ambiental": "ambiental",
}


def sortear_hashtags(segmento: str, semente: str) -> list[str]:
    """12 a 18 hashtags: as fixas do bloco local e do segmento, mais rotativas sorteadas.

    O sorteio é determinístico pela data (mesma data, mesmo conjunto), para que um `--dry-run` e a
    publicação de verdade mostrem exatamente as mesmas hashtags.
    """
    blocos = config.hashtags()
    local = blocos["local"]
    nome_bloco = BLOCO_POR_SEGMENTO.get(segmento)
    if nome_bloco is None:
        return []
    tema = blocos[nome_bloco]

    sorteio = random.Random(semente)
    escolhidas = list(local["fixas"]) + list(tema["fixas"])
    escolhidas += sorteio.sample(local["rotativas"], k=min(4, len(local["rotativas"])))
    escolhidas += sorteio.sample(tema["rotativas"], k=min(6, len(tema["rotativas"])))

    vistas: list[str] = []
    for tag in escolhidas:
        if tag not in vistas:
            vistas.append(tag)
    return vistas


def montar(post: dict) -> str:
    """Legenda exata que vai ao ar, hashtags incluídas."""
    corpo = (post.get("legenda") or "").strip()
    tags = sortear_hashtags(post.get("segmento", ""), semente=str(post.get("data")))
    if not tags:
        return corpo
    return corpo + "\n\n" + " ".join("#" + tag for tag in tags)
