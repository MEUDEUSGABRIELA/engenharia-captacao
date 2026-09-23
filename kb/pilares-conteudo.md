# Pilares de conteúdo

Cinco pilares, um por dia útil. Cada post pertence a **exatamente um**. O dia da semana fixa o
pilar — é isso que torna a pauta automatizável e impede o perfil de virar mural de frases soltas.

| Dia | Pilar (`pilar` no calendário) | O que é | Formato que melhor funciona |
| --- | --- | --- | --- |
| Segunda | `alerta-legal` | Prazo, mudança de norma, exigência nova, o que o fiscal pede primeiro | Carrossel ou Reels curto |
| Terça | `erro-caro` | O erro comum em obra, reforma ou gestão de SST e o que ele cobra depois | Carrossel |
| Quarta | `bastidor` | Vistoria, medição, obra, campo — foto ou vídeo real | Reels ou foto única |
| Quinta | `pergunta` | Uma dúvida real de cliente, respondida direto | Estático ou Reels falado |
| Sexta | `servico` | O que é entregue, para quem serve, o que destrava | Carrossel |

## Como cada pilar abre

A primeira linha da legenda é o post. Ela nomeia o problema antes de nomear o serviço.

- `alerta-legal` — abre pela consequência datada: "Multa de NR chega antes do aviso."
- `erro-caro` — abre pelo erro, não pela solução: "Derrubaram a parede errada."
- `bastidor` — abre pelo que está sendo feito: "Antes de dizer se a fissura é grave, eu meço três coisas."
- `pergunta` — abre repetindo a pergunta como o cliente faz: "PGR e PCMSO são a mesma coisa?"
- `servico` — abre pelo que trava sem o serviço: "Imóvel irregular não financia."

Nunca abrir com "Você sabia que...", "Dica de engenharia" ou saudação. São as três aberturas que
mais custam alcance.

## Proporção por segmento

Os pesos vivem em `kb/segmentos.yaml`: SST 30% · civil 30% · perícia 15% · avaliação 15% ·
ambiental 10%. O ambiental entra quando houver gancho (licenciamento, outorga, estiagem, exigência
de órgão), não por rodízio automático.

**Perícia e avaliação falam com outro público** — advogado, banco, corretor, inventariante — dentro
do mesmo feed. Isso é de propósito: quem contrata laudo de avaliação muitas vezes é o mesmo
escritório que precisa de assistente técnico, e quem vê um post de vistoria entende que a mesma
engenheira faz as duas coisas. O que muda é o vocabulário, não a identidade.

Duas travas para esses segmentos, detalhadas em `kb/regras-publicidade.md`: perícia judicial vem por
nomeação do juízo e **não se oferece** (o que se oferece é assistência técnica), e nenhuma legenda
estima valor de imóvel.

## CTA

Um por post, sempre para o WhatsApp de `kb/dados-empresa.md`. Varia a frase, nunca o destino:

- "Quer saber o que falta na sua? Chama no WhatsApp (18) 99641-8959."
- "Me manda uma mensagem que eu te digo o que se aplica ao seu caso: (18) 99641-8959."
- "Vai começar? Me chama antes: (18) 99641-8959."
- "Quer a situação real da sua empresa? WhatsApp (18) 99641-8959."

## Formatos

| `formato` | O que o motor monta | Observação |
| --- | --- | --- |
| `estatico` | Uma imagem: título grande + assinatura | Sempre possível, não depende de foto |
| `carrossel` | Capa + telas de conteúdo a partir do campo `telas` | A Graph API publica carrossel em duas etapas |
| `reels` | Vídeo do `data/ativos/` + legenda | ⟨PENDENTE: Reels exige vídeo gravado por você — o motor não gera vídeo⟩ |

Dia de `bastidor` sem foto real disponível cai para `estatico` do mesmo pilar. **Nunca se pula o
dia**, e nunca se inventa uma foto de obra que não existe (regra inviolável 4 do `CLAUDE.md`).
