"""URL pública da imagem.

A Graph API não recebe o arquivo: ela recebe uma **URL** e busca a imagem sozinha. Por isso a arte
do dia precisa estar publicamente acessível no momento da publicação.

Como isso é resolvido a custo zero: o workflow do GitHub Actions faz commit de
`data/saida/<data>/` antes de publicar, e a imagem passa a existir em `raw.githubusercontent.com`.
Este módulo só monta a URL correspondente.

**Decisão registrada em 23.09.2026: o repositório é público.** `raw.githubusercontent.com` não
serve arquivo de repositório privado sem token, e a Meta acessa sem token. O que fica visível é a
arte, a legenda e o código — conteúdo que vai ao ar de qualquer forma. As fotos de vistoria não
vão: `data/ativos/` está no `.gitignore`.
"""

from __future__ import annotations

from pathlib import Path

from .. import config


class HospedagemNaoConfigurada(RuntimeError):
    pass


def url_publica(caminho: Path) -> str:
    """URL que a Meta vai acessar para buscar a imagem.

    `HOSPEDAGEM_BASE` é a raiz pública do repositório, sem barra no fim. Exemplo:
    `https://raw.githubusercontent.com/<usuario>/<repositorio>/main`
    """
    base = config.env("HOSPEDAGEM_BASE")
    if not base:
        raise HospedagemNaoConfigurada(
            "HOSPEDAGEM_BASE não configurada — ver kb/setup-meta.md. "
            "Sem ela só é possível rodar com --dry-run."
        )
    relativo = caminho.resolve().relative_to(config.RAIZ).as_posix()
    return f"{base.rstrip('/')}/{relativo}"
