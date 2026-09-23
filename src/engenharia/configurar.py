"""Configuração e conferência das credenciais do Instagram.

    python -m engenharia.configurar --token IGAA...   # descobre o id da conta e escreve o .env
    python -m engenharia.configurar --conferir        # testa o que já está configurado
    python -m engenharia.configurar --renovar         # estende o token por mais 60 dias

O token vem da tela **Configuração da API com login empresarial no Instagram**, no painel do app
(ver `kb/setup-meta.md`). Ele começa com `IGAA` e é emitido para a conta do Instagram diretamente —
não depende de Página do Facebook.
"""

from __future__ import annotations

import argparse
import sys

import requests

from . import config
from .publicacao import graph

TEMPO_LIMITE = 60


def descobrir_conta(token: str) -> dict:
    """Ficha da conta dona do token: id, username, tipo de conta."""
    resposta = requests.get(
        f"https://graph.instagram.com/{config.env('GRAPH_VERSION', 'v21.0')}/me",
        params={
            "fields": "id,username,account_type,media_count,followers_count",
            "access_token": token,
        },
        timeout=TEMPO_LIMITE,
    )
    corpo = resposta.json()
    if "error" in corpo:
        erro = corpo["error"]
        raise SystemExit(
            f"A API recusou o token:\n  {erro.get('message')}\n"
            "Ver kb/setup-meta.md — o motivo mais comum é token expirado ou gerado no fluxo errado "
            "(o daqui começa com IGAA, do login do Instagram)."
        )
    if corpo.get("account_type") != "BUSINESS":
        print(
            f"ATENÇÃO: a conta está como {corpo.get('account_type')!r}, não BUSINESS. "
            "A API de publicação exige conta Comercial."
        )
    return corpo


def escrever_env(token: str, ig_user_id: str) -> None:
    """Escreve o `.env`, preservando o que já estiver configurado."""
    caminho = config.RAIZ / ".env"
    valores = {
        "IG_TOKEN": token,
        "IG_USER_ID": ig_user_id,
        "HOSPEDAGEM_BASE": config.env("HOSPEDAGEM_BASE", "") or "",
        "GRAPH_VERSION": config.env("GRAPH_VERSION", "v21.0"),
    }
    linhas = [
        "# Gerado por `python -m engenharia.configurar`. NÃO versionar — está no .gitignore.",
        "# Token do fluxo de login do Instagram (começa com IGAA). Renovar a cada ~60 dias:",
        "#   python -m engenharia.configurar --renovar",
        "",
    ]
    linhas += [f"{chave}={valor}" for chave, valor in valores.items()]
    caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"Escrito: {caminho}")


def _conferir() -> int:
    try:
        ficha = graph.conta()
    except graph.ErroDaMeta as erro:
        print(f"Não deu para falar com a API: {erro}")
        return 1

    print(f"Conta conectada: @{ficha.get('username')} (id {ficha.get('id')})")
    print(f"  tipo: {ficha.get('account_type')}")
    print(f"  seguidores: {ficha.get('followers_count', '?')} · publicações: {ficha.get('media_count', '?')}")
    base = config.env("HOSPEDAGEM_BASE")
    print(f"  hospedagem: {base or 'NÃO configurada — sem ela só dá para rodar com --dry-run'}")
    return 0


def _renovar() -> int:
    token, segundos = graph.renovar_token()
    escrever_env(token, config.env("IG_USER_ID", ""))
    print(f"Token renovado — vale por mais {segundos // 86400} dias.")
    print("Atualize também o secret no GitHub:")
    print('  gh secret set IG_TOKEN --body "<o token novo do .env>"')
    return 0


def main() -> int:
    analisador = argparse.ArgumentParser(description="Configura as credenciais do Instagram.")
    analisador.add_argument("--token", help="token gerado no painel do app (começa com IGAA)")
    analisador.add_argument("--conferir", action="store_true", help="testa o que já está configurado")
    analisador.add_argument("--renovar", action="store_true", help="estende o token por mais 60 dias")
    argumentos = analisador.parse_args()

    if argumentos.conferir:
        return _conferir()
    if argumentos.renovar:
        return _renovar()
    if not argumentos.token:
        analisador.error("informe --token (ou use --conferir / --renovar)")

    ficha = descobrir_conta(argumentos.token)
    print(f"Conta encontrada: @{ficha['username']} (id {ficha['id']}) — {ficha.get('account_type')}")
    escrever_env(argumentos.token, ficha["id"])
    print("\nConfira com: python -m engenharia.configurar --conferir")
    return 0


if __name__ == "__main__":
    sys.exit(main())
