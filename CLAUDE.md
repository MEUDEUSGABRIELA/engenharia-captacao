# engenharia-captacao — captação de clientes de engenharia via Instagram

Motor de conteúdo e publicação automática do Instagram **@meudeusgabrielaengenharia**, que capta
clientes de **engenharia civil**, **engenharia de segurança do trabalho** e **engenharia ambiental**
em Presidente Prudente/SP e região.

Responsável técnica: ver `kb/dados-empresa.md` (fonte única de nome, CREA, telefone e handle).

O perfil atende dois públicos com o mesmo feed: **empresa** (indústria, comércio, construtora,
condomínio — compra conformidade: PGR, PCMSO, laudos, NRs) e **pessoa física** (dono de obra ou
imóvel — compra regularização, laudo e projeto). O CTA é sempre o mesmo WhatsApp.

Este projeto é independente de `projects/laudos/`, `projects/pericias-judiciais/`,
`projects/calculos-estruturais/` e `projects/desenhos-tecnicos/` — aqui o produto é **publicação**,
não documento técnico assinado. Nenhum dado de caso real desses projetos entra aqui.

## Regras invioláveis

Valem para **toda** interação neste projeto e prevalecem sobre conveniência, estética ou velocidade.
O risco aqui não é estético: o que o perfil publica é manifestação de profissional habilitada e
pode ser cobrada como tal.

1. **Nenhuma promessa de resultado.** "Aprovo na prefeitura", "sua empresa fica livre de multa",
   "garanto o laudo em X dias" não são copy — são obrigação assumida em público. O que pode ser
   dito é o que o serviço é e o que ele destrava. Ver `kb/regras-publicidade.md`.
2. **Nenhuma citação normativa sem conferência.** Número de NR, artigo da CLT, item de resolução só
   entram na legenda se o trecho estiver transcrito em `kb/normas-conferidas.md`, com fonte e data.
   Fora disso, o texto carrega `[CONFERIR — <norma> §?]` **visível**, e o `--final` se recusa a
   publicar com ele.
3. **Nenhum dado de cliente sem autorização escrita.** Foto de obra, planta, endereço, nome ou
   detalhe que identifique um caso só entra com autorização de uso guardada. Vale também para foto
   "sem identificar" que a cidade reconhece. Sigilo profissional e LGPD.
4. **Nenhum depoimento, número ou resultado fabricado.** "+500 laudos", print de conversa montado,
   depoimento escrito por nós: não existem. Número só com lastro verificável, ou nenhum número.
5. **Nenhum diagnóstico técnico fechado em post, DM ou comentário.** Opinião técnica sem vistoria e
   sem ART é responsabilidade assumida de graça. A copy fala do que costuma causar, nunca do caso
   de quem perguntou.
6. **Nenhuma credencial em arquivo versionado.** Token da Meta em `.env` (fora do Git) e em GitHub
   Actions secret. A senha do Instagram nunca é usada por código — a API usa token.
7. **Publicação é auditada.** Data, arte, legenda, hashtags e o id devolvido pela Meta ficam em
   `data/saida/<AAAA-MM-DD>/log.json`. Publicação sem log é bug, não detalhe.
8. **O motor publica; ele não inventa conteúdo técnico.** Todo tema vem de `data/pauta/calendario.yaml`
   e todo bloco de texto reusável vem de `kb/`. O código monta e publica — ele não escreve
   afirmação técnica nova por conta própria.
9. **Pendência fica à mostra.** O que depende de decisão humana é marcado `⟨PENDENTE: o que falta⟩`
   no arquivo — nunca preenchido com valor plausível.

## Estrutura

- `kb/` — acervo operacional: `dados-empresa.md` (fonte única de identidade e contato),
  `pilares-conteudo.md` (os cinco pilares e o dia de cada um), `regras-publicidade.md` (o que a copy
  pode afirmar), `normas-conferidas.md` (trechos normativos transcritos da fonte oficial, com data —
  é o lastro de toda citação), `hashtags.yaml` (blocos local/SST/civil/ambiental), `setup-meta.md`
  (passo a passo da configuração que só a responsável faz).
- `data/pauta/calendario.yaml` — a pauta. Fonte da verdade do que é publicado em cada dia.
- `data/ativos/` — fotos reais de vistoria e obra, por pilar. Fora do versionamento.
- `data/saida/<AAAA-MM-DD>/` — pacote do dia: arte final, legenda e `log.json`.
- `src/engenharia/` — Python: `pauta/` (lê o calendário), `copy/` (legenda e hashtags),
  `arte/` (composição da imagem), `publicacao/` (hospedagem, Graph API, token).
- `.github/workflows/publicar-diario.yml` — agendamento diário no GitHub Actions.

## Fluxo de um dia

```
calendario.yaml → copy/legenda → arte/compor → publicacao/hospedagem → publicacao/graph → log.json
```

### Instalação

```
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -e .
```

### Configurar as credenciais da Meta

```
python -m engenharia.configurar --app-id <ID> --app-secret <CHAVE> --token-curto <TOKEN>
python -m engenharia.configurar --conferir
```

Troca o token curto pelo de longa duração, descobre o `IG_USER_ID` e escreve o `.env`. A chave
secreta do app é usada na troca e descartada — ela não é guardada em lugar nenhum. Passo a passo
completo em `kb/setup-meta.md`.

### Rodar

```
python -m engenharia.publicar --dry-run              # monta o pacote do dia, não publica
python -m engenharia.publicar --data 2026-09-24 --dry-run
python -m engenharia.publicar                        # publica de verdade (exige token)
python -m engenharia.publicar --conferir             # só valida a pauta e o kb, não monta nada
```

`--dry-run` escreve em `data/saida/<data>/` e imprime a legenda exata que iria ao ar. É o modo de
conferência antes de ligar o automático — e é o que roda quando não há token configurado.

## Custo

O projeto é desenhado para **R$ 0/mês**: GitHub Actions (agendamento), Instagram Graph API
(publicação) e a hospedagem de imagem escolhida em `kb/setup-meta.md`, todas em camada gratuita.
Se qualquer item passar a cobrar, isso é uma decisão a tomar, não um fato a aceitar.

## Convenções

- Tudo em português do Brasil, inclusive nomes de campo e de módulo.
- Datas em ISO (`AAAA-MM-DD`) nos dados; por extenso apenas em texto publicado.
- **Texto nunca é gerado dentro da imagem por IA.** A arte compõe tipografia em código, para ser
  exata, editável e idêntica todo dia.
- Um dia nunca escreve fora de `data/saida/<data>/`.
