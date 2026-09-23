"""Publicação pela API do Instagram, no fluxo de **login do Instagram**.

Duas etapas, sempre: cria-se um *container* de mídia e depois publica-se o container. Carrossel tem
uma etapa a mais — cada imagem vira um container filho antes de o carrossel ser montado.

**Por que `graph.instagram.com` e não `graph.facebook.com`:** existem dois caminhos para publicar
numa conta profissional. O de *login do Facebook* exige que a conta esteja vinculada a uma Página
que o app enxergue — e, na configuração desta conta, `/me/accounts` devolvia zero Páginas mesmo com
todas as permissões concedidas. O de *login do Instagram* não depende de Página: o token é emitido
para a conta do Instagram direto. É o que está em uso aqui desde 23.09.2026, e o token dele começa
com `IGAA`. Ver `kb/setup-meta.md`.
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
    return f"https://graph.instagram.com/{versao}"


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
    """Publica uma imagem ou um carrossel. Devolve o id do post."""
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


def conta() -> dict:
    """Ficha da conta conectada. Serve de teste rápido de que o token ainda vale."""
    token, usuario = _credenciais()
    resposta = requests.get(
        f"{_base()}/{usuario}",
        params={
            "fields": "id,username,account_type,media_count,followers_count",
            "access_token": token,
        },
        timeout=TEMPO_LIMITE,
    )
    corpo = resposta.json()
    if "error" in corpo:
        raise ErroDaMeta(corpo["error"].get("message", str(corpo)))
    return corpo


def renovar_token() -> tuple[str, int]:
    """Estende o token por mais 60 dias. Devolve (token novo, segundos até expirar).

    No fluxo de login do Instagram a renovação não precisa da chave secreta: basta o próprio token,
    desde que tenha mais de 24 horas de vida e menos de 60 dias.
    """
    token, _ = _credenciais()
    resposta = requests.get(
        "https://graph.instagram.com/refresh_access_token",
        params={"grant_type": "ig_refresh_token", "access_token": token},
        timeout=TEMPO_LIMITE,
    )
    corpo = resposta.json()
    if "error" in corpo:
        raise ErroDaMeta(corpo["error"].get("message", str(corpo)))
    return corpo["access_token"], int(corpo.get("expires_in", 0))
