from engenharia import qa
from engenharia.copy import montar, sortear_hashtags
from engenharia.pauta.calendario import carregar, do_dia


def test_pauta_integra():
    assert qa.conferir_pauta(carregar()) == []


def test_todo_post_tem_o_telefone_no_cta():
    for post in carregar():
        if post.get("status") == "feriado":
            continue
        assert "18996418959" in post["legenda"].replace(" ", "").replace("(", "").replace(")", "").replace("-", ""), (
            f"{post['data']} sem o WhatsApp no CTA"
        )


def test_hashtags_sao_deterministicas():
    primeira = sortear_hashtags("civil", "2026-09-25")
    segunda = sortear_hashtags("civil", "2026-09-25")
    assert primeira == segunda
    assert 12 <= len(primeira) <= 18
    assert "presidenteprudente" in primeira


def test_legenda_do_dia_cabe_no_instagram():
    post = do_dia("2026-09-24")
    legenda = montar(post)
    assert len(legenda) <= qa.LIMITE_LEGENDA
    assert legenda.count("#") >= 12


def test_qa_pega_promessa_de_resultado():
    achados = qa.conferir_legenda("Garanto a aprovação do seu projeto na prefeitura.")
    assert any("termo proibido" in achado for achado in achados)


def test_qa_pega_marcador_de_conferencia():
    achados = qa.conferir_legenda("A NR-1 exige X [CONFERIR — NR-1 item 1.2].")
    assert any("CONFERIR" in achado for achado in achados)
