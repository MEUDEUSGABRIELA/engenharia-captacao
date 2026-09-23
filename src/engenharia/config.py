"""Caminhos do projeto e leitura do `kb/`.

Nenhum valor de negócio mora em código: telefone, hashtags, termos proibidos e pauta vêm de
arquivo. Se um valor precisa mudar, muda no `kb/` ou em `data/`, nunca aqui.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
KB = RAIZ / "kb"
DADOS = RAIZ / "data"
PAUTA = DADOS / "pauta" / "calendario.yaml"
ATIVOS = DADOS / "ativos"
SAIDA = DADOS / "saida"

# Marcadores que impedem publicação (regras invioláveis 2 e 9 do CLAUDE.md).
MARCADORES_BLOQUEIO = ("[CONFERIR", "⟨PENDENTE")


def carregar_yaml(caminho: Path) -> dict:
    with caminho.open(encoding="utf-8") as arquivo:
        return yaml.safe_load(arquivo) or {}


def hashtags() -> dict:
    return carregar_yaml(KB / "hashtags.yaml")


def identidade() -> dict:
    """Quem assina: nome, CREA, empresa, contato e handle. Nada disso mora em código."""
    return carregar_yaml(KB / "identidade.yaml")


def segmentos() -> dict:
    """Público, etiqueta da arte, bloco de hashtag e peso na pauta, por segmento."""
    return carregar_yaml(KB / "segmentos.yaml")


def termos_proibidos() -> list[str]:
    """Lê a lista do bloco YAML de `kb/regras-publicidade.md`.

    A lista vive no documento que a responsável técnica lê, não num arquivo separado — assim não
    existem duas listas para divergir.
    """
    texto = (KB / "regras-publicidade.md").read_text(encoding="utf-8")
    blocos = re.findall(r"```yaml\n(.*?)```", texto, re.DOTALL)
    for bloco in blocos:
        dados = yaml.safe_load(bloco) or {}
        if "termos_proibidos" in dados:
            return [termo.lower() for termo in dados["termos_proibidos"]]
    raise ValueError("kb/regras-publicidade.md não tem bloco yaml com termos_proibidos")


def env(nome: str, padrao: str | None = None) -> str | None:
    """Variável de ambiente, aceitando também um `.env` na raiz (fora do Git)."""
    if nome in os.environ:
        return os.environ[nome]
    arquivo = RAIZ / ".env"
    if arquivo.exists():
        for linha in arquivo.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            if chave.strip() == nome:
                return valor.strip().strip('"').strip("'")
    return padrao


def pasta_do_dia(data: str) -> Path:
    pasta = SAIDA / data
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta
