"""Pipeline do dia: pauta → legenda → arte → hospedagem → Graph API → log.

    python -m engenharia.publicar --dry-run
    python -m engenharia.publicar --data 2026-09-24 --dry-run
    python -m engenharia.publicar
    python -m engenharia.publicar --conferir
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date

from . import config, qa
from .arte import compor
from .copy import montar
from .pauta import do_dia, marcar_publicado
from .pauta.calendario import carregar
from .publicacao import publicar as publicar_na_meta
from .publicacao import url_publica

VIDEO = {".mp4", ".mov"}


def _conferir_pauta_inteira() -> int:
    posts = carregar()
    achados = qa.conferir_pauta(posts)
    if achados:
        print("Achados na pauta:")
        for achado in achados:
            print(f"  - {achado}")
        return 1
    print("Pauta íntegra.")

    # Legenda bloqueada não é erro de pauta: é dia que ainda não pode ir ao ar. Sai como aviso,
    # para a responsável técnica saber o que falta conferir antes daquela data chegar.
    bloqueados = {
        post["data"]: qa.conferir_legenda(montar(post))
        for post in posts
        if post.get("status") not in ("feriado", "publicado")
        and qa.conferir_legenda(montar(post))
    }
    if bloqueados:
        print(f"\n{len(bloqueados)} dia(s) não podem ser publicados como estão:")
        for dia, motivos in sorted(bloqueados.items()):
            for motivo in motivos:
                print(f"  - {dia}: {motivo}")
    else:
        print("Todas as legendas estão liberadas para publicação.")
    return 0


def executar(dia: str, dry_run: bool, forcar: bool) -> int:
    post = do_dia(dia)
    if post is None:
        print(f"{dia}: a pauta não tem post para hoje. Nada a fazer.")
        return 0
    if post.get("status") == "feriado":
        print(f"{dia}: feriado na pauta — só Stories, nada no feed.")
        return 0
    if post.get("status") == "publicado" and not forcar:
        print(f"{dia}: já publicado. Use --forcar para republicar.")
        return 0

    achados = qa.conferir_post(post)
    if achados:
        print(f"{dia}: pauta com problema:")
        for achado in achados:
            print(f"  - {achado}")
        return 1

    legenda = montar(post)
    achados_legenda = qa.conferir_legenda(legenda)

    if post.get("formato") == "reels":
        ativo = str(post.get("ativo") or "")
        if ativo and not ativo.startswith("⟨PENDENTE") and any(ativo.lower().endswith(e) for e in VIDEO):
            print(
                f"{dia}: este post é Reels com vídeo ({ativo}). A publicação de vídeo pela API "
                "ainda não está implementada aqui — publique este manualmente."
            )
            return 1
        print(f"{dia}: Reels sem vídeo disponível — caindo para arte estática do mesmo pilar.")

    pasta = config.pasta_do_dia(dia)
    arquivos, avisos = compor(post, pasta)
    (pasta / "legenda.txt").write_text(legenda, encoding="utf-8")

    for aviso in avisos:
        print(f"  aviso: {aviso}")

    registro = {
        "data": dia,
        "pilar": post.get("pilar"),
        "segmento": post.get("segmento"),
        "formato": post.get("formato"),
        "tema": post.get("tema"),
        "arquivos": [arquivo.name for arquivo in arquivos],
        "caracteres_legenda": len(legenda),
        "avisos": avisos,
        "achados": achados_legenda,
        "publicado": False,
        "post_id": None,
    }

    if achados_legenda:
        print(f"{dia}: a legenda não pode ir ao ar como está:")
        for achado in achados_legenda:
            print(f"  - {achado}")
        if not dry_run:
            (pasta / "log.json").write_text(
                json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            return 1

    if dry_run:
        (pasta / "log.json").write_text(
            json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"{dia}: pacote montado em {pasta}")
        print("-" * 60)
        print(legenda)
        print("-" * 60)
        return 0

    urls = [url_publica(arquivo) for arquivo in arquivos]
    post_id = publicar_na_meta(urls, legenda)
    registro["publicado"] = True
    registro["post_id"] = post_id
    registro["urls"] = urls
    (pasta / "log.json").write_text(
        json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    marcar_publicado(dia, post_id)
    print(f"{dia}: publicado. id {post_id}")
    return 0


def main() -> int:
    analisador = argparse.ArgumentParser(description="Publica o post do dia no Instagram.")
    analisador.add_argument("--data", default=date.today().isoformat(), help="AAAA-MM-DD")
    analisador.add_argument("--dry-run", action="store_true", help="monta o pacote e não publica")
    analisador.add_argument("--conferir", action="store_true", help="só valida a pauta inteira")
    analisador.add_argument("--forcar", action="store_true", help="republica um dia já publicado")
    argumentos = analisador.parse_args()

    if argumentos.conferir:
        return _conferir_pauta_inteira()
    return executar(argumentos.data, argumentos.dry_run, argumentos.forcar)


if __name__ == "__main__":
    sys.exit(main())
