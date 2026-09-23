"""Publicação pela Instagram Graph API (Meta).

Duas etapas, sempre: cria-se um *container* de mídia e depois publica-se o container. Carrossel tem
uma etapa a mais — cada imagem vira um container filho antes de o carrossel ser montado.

A versão da API é configurável (`GRAPH_VERSION`) porque a Meta descontinua versão antiga com
regularidade — ver `kb/setup-meta.md`.
"""

from __future__ import annotations

import time

import requests

from .. import config

TEMPO_LIMITE = 60


class ErroDaMeta(RuntimeError):
    pass


def _base() -> str:
    versao = config.env("GRAPH_VERSION", "v21.0")
    return f"https://graph.facebook.com/{versao}"


def _credenciais() -> tuple[str, str]:
    token = config.env("IG_TOKEN")
    usuario = config.env("IG_USER_ID")
    if not token or not usuario:
        raise ErroDaMeta(
            "IG_TOKEN e IG_USER_ID não configurados — ver kb/setup-meta.md. "
            "Sem eles só é possível rodar com --dry-run."
        )
    return token, usuario


def _post(caminho: str, dados: dict) -> dict:
    resposta = requests.post(f"{_base()}/{caminho}", data=dados, timeout=TEMPO_LIMITE)
    corpo = resposta.json() if resposta.content else {}
    if resposta.status_code >= 400 or "error" in corpo:
        erro = corpo.get("error", {})
        raise ErroDaMeta(
            f"{resposta.status_code} em {caminho}: "
            f"{erro.get('message', resposta.text)} (code {erro.get('code')})"
        )
    return corpo


def _esperar_container(container_id: str, token: str, tentativas: int = 12) -> None:
    """A Meta baixa a imagem de forma assíncrona; publicar antes disso devolve erro."""
    for _ in range(tentativas):
        resposta = requests.get(
            f"{_base()}/{container_id}",
            params={"fields": "status_code,status", "access_token": token},
            timeout=TEMPO_LIMITE,
        ).json()
        estado = resposta.get("status_code")
        if estado == "FINISHED":
            return
        if estado == "ERROR":
            raise ErroDaMeta(f"container {container_id} falhou: {resposta.get('status')}")
        time.sleep(5)
    raise ErroDaMeta(f"container {container_id} não ficou pronto a tempo")


def publicar(urls: list[str], legenda: str) -> str:
    """Publica uma imagem ou um carrossel. Devolve o id do post na Meta."""
    token, usuario = _credenciais()
    if not urls:
        raise ErroDaMeta("nenhuma imagem para publicar")

    if len(urls) == 1:
        criacao = _post(
            f"{usuario}/media",
            {"image_url": urls[0], "caption": legenda, "access_token": token},
        )["id"]
    else:
        filhos = []
        for url in urls:
            filho = _post(
                f"{usuario}/media",
                {"image_url": url, "is_carousel_item": "true", "access_token": token},
            )["id"]
            _esperar_container(filho, token)
            filhos.append(filho)
        criacao = _post(
            f"{usuario}/media",
            {
                "media_type": "CAROUSEL",
                "children": ",".join(filhos),
                "caption": legenda,
                "access_token": token,
            },
        )["id"]

    _esperar_container(criacao, token)
    return _post(
        f"{usuario}/media_publish",
        {"creation_id": criacao, "access_token": token},
    )["id"]


def dias_ate_expirar() -> int | None:
    """Quantos dias faltam para o token vencer, ou None se a Meta não informar.

    O token de longa duração dura cerca de 60 dias. O pipeline avisa quando está perto do fim —
    a renovação é manual, de propósito: guardar uma credencial com poder de rotacionar segredos
    seria uma credencial a mais para vazar.
    """
    token, _ = _credenciais()
    resposta = requests.get(
        f"{_base()}/debug_token",
        params={"input_token": token, "access_token": token},
        timeout=TEMPO_LIMITE,
    ).json()
    expira = resposta.get("data", {}).get("expires_at")
    if not expira:
        return None
    return max(0, int((expira - time.time()) // 86400))
