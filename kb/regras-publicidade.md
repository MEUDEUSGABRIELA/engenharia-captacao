# O que a copy pode afirmar

Perfil de engenharia tem um risco que perfil de loja não tem: legenda é manifestação de
profissional habilitada. Estas regras são conferidas pelo `--final` antes de publicar.

## Proibido

A base está transcrita em `kb/normas-conferidas.md`. Em resumo, o Código de Ética Profissional
(Resolução Confea nº 1.002/2002) impõe **fornecer informação certa, precisa e objetiva em
publicidade e propaganda pessoal** (art. 9º, III, c) e veda **artifício ou expediente enganoso para
conquista de contratos** (art. 10, III, c).

| Nunca | Por quê | No lugar |
| --- | --- | --- |
| Prometer resultado ("aprovo na prefeitura", "livre de multa", "ganho de causa") | Informação em publicidade tem que ser certa, precisa e objetiva (art. 9º, III, c) — resultado que não depende só da profissional não é informação certa | Descrever o serviço e o que ele destrava |
| Foto, planta, endereço ou nome de cliente sem autorização escrita | Dever de resguardar o sigilo profissional (art. 9º, III, b) e LGPD; vale para foto "anônima" que a cidade reconhece | Detalhe técnico enquadrado, com autorização guardada |
| Depoimento, número ou resultado fabricado | É artifício enganoso para conquista de contrato (art. 10, III, c), e prova social falsa é descoberta numa cidade desse porte | Só número comprovável, ou nenhum |
| Diagnóstico técnico fechado sobre o caso de quem perguntou | Opinião sem vistoria e sem ART é responsabilidade assumida de graça | "O que costuma causar isso é...; afirmar sobre a sua exige ver no local" |
| Citar NR, artigo ou resolução sem conferir na fonte | Norma errada em post público é pior que norma não citada | Citar só o que está em `kb/normas-conferidas.md`; o resto entra com `[CONFERIR]` |
| Desqualificar colega ou concorrente | Referir-se preconceituosamente a outro profissional é vedado (art. 10, IV, b) e, na prática, corta a indicação de colegas | Criticar a prática: "documento genérico não protege" |
| Tabela de preço no feed, ou "o mais barato" | Proposta de honorários com valor vil ou desrespeitando tabela mínima é vedada (art. 10, III, b); preço público ainda vira comparação por número | "Depende do escopo — te passo o orçamento no WhatsApp" |

## Marcadores que bloqueiam a publicação

O `--final` **recusa publicar** um post cuja legenda contenha:

- `[CONFERIR` — dispositivo normativo não conferido na fonte oficial
- `⟨PENDENTE` — campo que depende de decisão humana
- qualquer termo da lista `termos_proibidos` abaixo

```yaml
termos_proibidos:
  - "garanto"
  - "garantido"
  - "100% aprovado"
  - "livre de multa"
  - "sem risco de multa"
  - "aprovação garantida"
  - "resultado garantido"
  - "o melhor da região"
  - "o mais barato"
```

A lista existe para pegar o deslize de redação, não para substituir leitura. Frase nova que promete
resultado com outras palavras continua proibida mesmo passando no filtro.

## Respostas prontas para DM e comentário

- **Preço nos comentários:** "Depende do que precisa ser feito — te chamo no WhatsApp para entender
  e já te passo o orçamento."
- **Diagnóstico por foto:** "Consigo te dizer o que normalmente causa isso, mas afirmar sobre a sua
  exige ver no local. Quer que eu te explique como funciona a vistoria?"
- **"Você faz de graça uma olhadinha?":** "A visita técnica é o serviço — é nela que eu consigo te
  dar resposta com responsabilidade. Te passo o valor da visita?"

## LGPD

Nome, telefone e empresa de quem chega ficam só pelo tempo necessário para atender e orçar. Contato
que não virou trabalho não fica guardado indefinidamente. Nenhum dado de lead entra em arquivo
versionado deste projeto.
