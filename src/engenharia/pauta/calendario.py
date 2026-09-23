"""Leitura da pauta. `data/pauta/calendario.yaml` é a fonte da verdade do que é publicado."""

from __future__ import annotations

from datetime import date

from .. import config


def carregar() -> list[dict]:
    dados = config.carregar_yaml(config.PAUTA)
    posts = dados.get("posts") or []
    for post in posts:
        # PyYAML devolve `date` para 2026-09-24 sem aspas; normalizamos para string ISO.
        if isinstance(post.get("data"), date):
            post["data"] = post["data"].isoformat()
    return posts


def do_dia(dia: str) -> dict | None:
    """O post daquela data, ou None se a pauta não tem nada para o dia."""
    for post in carregar():
        if post.get("data") == dia:
            return post
    return None


def marcar_publicado(dia: str, post_id: str) -> None:
    """Registra na pauta que o dia já foi ao ar, para não republicar.

    Edita o YAML como texto, preservando comentários e formatação — reescrever com `yaml.dump`
    destruiria o arquivo que a responsável técnica edita à mão.
    """
    texto = config.PAUTA.read_text(encoding="utf-8")
    linhas = texto.splitlines()
    inicio = None
    for indice, linha in enumerate(linhas):
        if linha.strip().startswith("- data:") and dia in linha:
            inicio = indice
            break
    if inicio is None:
        raise ValueError(f"data {dia} não encontrada na pauta")
    for indice in range(inicio, len(linhas)):
        if linhas[indice].strip().startswith("status:"):
            recuo = len(linhas[indice]) - len(linhas[indice].lstrip())
            linhas[indice] = " " * recuo + f"status: publicado  # {post_id}"
            config.PAUTA.write_text("\n".join(linhas) + "\n", encoding="utf-8")
            return
        if indice > inicio and linhas[indice].strip().startswith("- data:"):
            break
    raise ValueError(f"post de {dia} não tem campo status")
