"""Configuração das credenciais da Meta, em um comando.

O que este módulo poupa: trocar o token curto pelo de longa duração na mão, descobrir o id da conta
do Instagram navegando pelo Graph API Explorer, e montar o `.env` sem errar um caractere.

    python -m engenharia.configurar --app-id 123 --app-secret abc --token-curto EAA...
    python -m engenharia.configurar --conferir

**A chave secreta do app não é guardada em lugar nenhum.** Ela é usada só na troca do token e
descartada quando o processo termina — por isso ela não vai para o `.env` nem para o GitHub.
"""

from __future__ import annotations

import argparse
import sys
import time

import requests

from . import config

TEMPO_LIMITE = 60


def _base() -> str:
    return f"https://graph.facebook.com/{config.env('GRAPH_VERSION', 'v21.0')}"


def _get(caminho: str, **parametros) -> dict:
    resposta = requests.get(f"{_base()}/{caminho}", params=parametros, timeout=TEMPO_LIMITE)
    corpo = resposta.json() if resposta.content else {}
    if "error" in corpo:
        erro = corpo["error"]
        raise SystemExit(
            f"A Meta recusou a chamada a /{caminho}:\n"
            f"  {erro.get('message')}\n"
            f"  (code {erro.get('code')}, subcode {erro.get('error_subcode')})\n"
            "Ver kb/setup-meta.md — os motivos mais comuns são token expirado, permissão que não foi "
            "marcada na hora de gerar o token, ou conta do Instagram ainda não convertida em Comercial."
        )
    return corpo


def trocar_por_longa_duracao(app_id: str, app_secret: str, token_curto: str) -> str:
    resposta = _get(
        "oauth/access_token",
        grant_type="fb_exchange_token",
        client_id=app_id,
        client_secret=app_secret,
        fb_exchange_token=token_curto,
    )
    token = resposta.get("access_token")
    if not token:
        raise SystemExit(f"A Meta respondeu sem access_token: {resposta}")
    return token


def descobrir_conta(token: str) -> tuple[str, str, str]:
    """Devolve (id da conta do Instagram, nome da Página, nome de usuário do Instagram)."""
    paginas = _get("me/accounts", access_token=token).get("data", [])
    if not paginas:
        raise SystemExit(
            "Nenhuma Página do Facebook apareceu para este token.\n"
            "A API exige uma Página vinculada à conta do Instagram — ver passo 2 de kb/setup-meta.md."
        )

    encontradas = []
    for pagina in paginas:
        ficha = _get(
            pagina["id"], fields="instagram_business_account{id,username},name", access_token=token
        )
        conta = ficha.get("instagram_business_account")
        if conta:
            encontradas.append((conta["id"], ficha.get("name", "?"), conta.get("username", "?")))

    if not encontradas:
        raise SystemExit(
            "As Páginas apareceram, mas nenhuma tem conta do Instagram vinculada.\n"
            "Confira o passo 1 (conta Comercial) e o passo 2 (vínculo) de kb/setup-meta.md."
        )
    if len(encontradas) > 1:
        print("Mais de uma conta encontrada:")
        for indice, (conta_id, pagina, usuario) in enumerate(encontradas, start=1):
            print(f"  {indice}. @{usuario} (id {conta_id}) — Página {pagina}")
        print("Usando a primeira. Se não for essa, edite IG_USER_ID no .env à mão.")
    return encontradas[0]


def dias_ate_expirar(token: str) -> int | None:
    resposta = _get("debug_token", input_token=token, access_token=token)
    expira = resposta.get("data", {}).get("expires_at")
    if not expira:
        return None
    return max(0, int((expira - time.time()) // 86400))


def escrever_env(token: str, ig_user_id: str) -> None:
    """Escreve o `.env`, preservando o que já estiver lá (inclusive HOSPEDAGEM_BASE)."""
    caminho = config.RAIZ / ".env"
    valores = {
        "IG_TOKEN": token,
        "IG_USER_ID": ig_user_id,
        "HOSPEDAGEM_BASE": config.env("HOSPEDAGEM_BASE", "") or "",
        "GRAPH_VERSION": config.env("GRAPH_VERSION", "v21.0"),
    }
    linhas = [
        "# Gerado por `python -m engenharia.configurar`. NÃO versionar — está no .gitignore.",
        "# A chave secreta do app não é guardada aqui de propósito: ela só serve para trocar o token.",
        "",
    ]
    linhas += [f"{chave}={valor}" for chave, valor in valores.items()]
    caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"Escrito: {caminho}")


def _conferir() -> int:
    token = config.env("IG_TOKEN")
    usuario = config.env("IG_USER_ID")
    if not token or not usuario:
        print("Falta IG_TOKEN ou IG_USER_ID. Rode a configuração primeiro (ver kb/setup-meta.md).")
        return 1

    ficha = _get(usuario, fields="username,name,followers_count,media_count", access_token=token)
    dias = dias_ate_expirar(token)
    print(f"Conta conectada: @{ficha.get('username')} ({ficha.get('name', '')})")
    print(f"  seguidores: {ficha.get('followers_count', '?')} · publicações: {ficha.get('media_count', '?')}")
    if dias is None:
        print("  token sem data de expiração informada pela Meta")
    else:
        print(f"  token expira em {dias} dias")
        if dias <= 7:
            print("  ATENÇÃO: renove agora — ver passo 8 de kb/setup-meta.md")

    base = config.env("HOSPEDAGEM_BASE")
    print(f"  hospedagem: {base or 'NÃO configurada — sem ela só dá para rodar com --dry-run'}")
    return 0


def main() -> int:
    analisador = argparse.ArgumentParser(description="Configura as credenciais da Meta.")
    analisador.add_argument("--app-id", help="ID do app no Meta for Developers")
    analisador.add_argument("--app-secret", help="Chave secreta do app — usada e descartada")
    analisador.add_argument("--token-curto", help="Token gerado no Graph API Explorer")
    analisador.add_argument("--conferir", action="store_true", help="testa o que já está configurado")
    argumentos = analisador.parse_args()

    if argumentos.conferir:
        return _conferir()

    if not (argumentos.app_id and argumentos.app_secret and argumentos.token_curto):
        analisador.error("informe --app-id, --app-secret e --token-curto (ou use --conferir)")

    print("Trocando o token curto pelo de longa duração...")
    token = trocar_por_longa_duracao(argumentos.app_id, argumentos.app_secret, argumentos.token_curto)
    dias = dias_ate_expirar(token)
    print(f"  ok — o novo token expira em {dias if dias is not None else '?'} dias")

    print("Procurando a conta do Instagram...")
    ig_user_id, pagina, usuario = descobrir_conta(token)
    print(f"  encontrada: @{usuario} (id {ig_user_id}), pela Página {pagina}")

    escrever_env(token, ig_user_id)
    print("\nFalta só o HOSPEDAGEM_BASE (a URL pública de onde a Meta busca a imagem).")
    print("Depois: python -m engenharia.configurar --conferir")
    return 0


if __name__ == "__main__":
    sys.exit(main())
