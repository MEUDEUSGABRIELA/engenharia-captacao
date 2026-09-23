# A operação: segmentos, público e serviços

Quem assina, registro, contato e handle estão em `kb/identidade.yaml` — é lá que a arte e a copy vão
buscar. Este arquivo trata do resto: para quem o perfil fala e o que ele pode oferecer.

## Praça

Atuação **regional**: Presidente Prudente/SP e região, com presença diária na cidade — confirmado
pela responsável técnica em 23.09.2026. O endereço profissional registrado fica em São Paulo
capital, que é onde os laudos são elaborados; a praça de captação é o oeste paulista.

Como a presença é diária, a copy **pode** falar em visita e atendimento presencial na região.

E **não pode** dizer "atuação nacional": dilui exatamente o que faz um perfil deste porte ser
encontrado por quem contrata. Ver `kb/identidade.yaml`.

⟨PENDENTE: até quantos km você se desloca para vistoria? Hoje as hashtags locais cobrem de
Presidente Prudente a Marília, Assis, Dracena e Adamantina. Se o raio real for menor, vale
encolher a lista; se for maior, acrescentar cidades⟩

## Segmentos e prioridade

Os pesos e o público de cada segmento estão em `kb/segmentos.yaml` — é de lá que o motor lê, e é
lá que se muda a prioridade. Hoje: **SST 30% · civil 30% · perícia 15% · avaliação 15% ·
ambiental 10%**.

`python -m engenharia.publicar --conferir` mostra o mix real do que ainda vai ao ar contra esses
pesos.

## Os quatro públicos

| Público | O que tira o sono | Post que converte |
| --- | --- | --- |
| Empresa com empregado | Fiscalização do trabalho, multa de NR, exigência de cliente ou seguradora | PGR/PCMSO, insalubridade, LTCAT, prazos legais |
| Pessoa física | Obra embargada, habite-se, financiamento, prefeitura | Regularização, laudo estrutural, ART, projeto |
| Advogado e escritório | Prova técnica fraca, quesito que volta "prejudicado", laudo que não se sustenta | Assistência técnica, como se formula quesito, como se lê um laudo |
| Banco, corretor, inventariante | Valor errado: imóvel que encalha, partilha injusta, garantia recusada | Avaliação NBR 14653, método, quando o laudo é exigido |

Os dois públicos novos são **menores e valem mais**: um advogado satisfeito indica outros casos, e
banco e imobiliária viram recorrência. Não se mede esse segmento por curtida.

## Serviços que a copy pode oferecer

Lista fechada. Serviço que não está aqui não é anunciado até ser acrescentado aqui.

- **Segurança do trabalho:** PGR, PCMSO (em conjunto com médico do trabalho), laudo de insalubridade,
  laudo de periculosidade, LTCAT, avaliação de agentes (ruído, calor, químicos), ordens de serviço,
  apoio em fiscalização.
- **Civil:** laudo técnico de edificação, vistoria de patologia (fissura, infiltração, recalque),
  vistoria pré-compra, projeto e regularização de imóvel, acompanhamento de obra, ART.
- **Ambiental:** licenciamento ambiental, outorga, gestão de resíduos, estudos e laudos ambientais.
- **Perícia:** assistência técnica contratada pela parte; perícia judicial por nomeação do juízo.
  A distinção entre as duas é regra de copy — ver `kb/regras-publicidade.md`.
- **Avaliação de imóveis:** laudo conforme NBR 14653 — urbano, rural, involutivo, evolutivo.

Cálculo estrutural e desenho técnico entram como serviços do segmento `civil`, não como segmento
próprio: quem contrata é o mesmo público de obra e reforma.
