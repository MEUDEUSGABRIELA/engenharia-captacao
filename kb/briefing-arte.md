# Como se faz a arte de um post

Registrado em 23.09.2026, depois de quatro tentativas reprovadas. O que **não** funciona e o que
funciona estão aqui para ninguém repetir o caminho errado.

## O que não funciona

**Posicionar caixa de texto à mão.** Foi o que eu fiz nas primeiras tentativas: pegar um molde,
trocar o texto, ajustar posição e tamanho. Isso é diagramação, não design, e o resultado é sempre o
mesmo — bloco de texto sobre cor chapada, com cara de planilha. A responsável técnica chamou de
"computadorizado", e estava certa.

**Inventar paleta.** Usei azul-marinho com âmbar, cores que não existem na identidade dela. Parecia
outra empresa.

**Foto de enfeite.** Selfie com capacete num post sobre a diferença entre PGR e PCMSO não diz nada.
Foto entra quando a foto *é* o assunto: bastidor, campo, equipamento.

## O que funciona

O motor de geração da Canva (`generate-design`, tipo `instagram_post`), com um briefing detalhado.
Ele devolve quatro opções; escolhe-se a melhor e converte com `create-design-from-candidate`.

### O briefing, em cinco partes

1. **Quem é a marca.** "GABRIELA LIMA — Engenharia Ambiental, Civil e Segurança".
2. **A paleta, com os códigos.** Verde `#00BF63` como principal, cinza-esverdeado `#53727C`,
   grafite `#415157`, bege claro `#F2EDE4`.
3. **O estilo, dito pelo que é e pelo que não é.** "Orgânico e moderno: formas curvas e
   arredondadas, camadas suaves, ícones ilustrados, cantos arredondados, profundidade — **nada de
   caixas retangulares duras nem blocos de texto corrido**." A negativa importa tanto quanto a
   afirmativa.
4. **O conteúdo estruturado**, não corrido: o título; os dois ou três blocos com rótulo, ícone
   sugerido e texto curto; a frase de fechamento.
5. **O rodapé e o idioma.** Telefone, `@`, e "texto em português do Brasil, curto e legível no
   celular" — sem isso ele às vezes devolve em inglês.

### Sugerir o ícone de cada bloco

É o que transforma diagrama em design. No post de PGR e PCMSO: fábrica para o PGR (o ambiente),
estetoscópio para o PCMSO (a pessoa). O leitor entende antes de ler.

### O que o rodapé da arte pode dizer

Telefone, `@` e, se couber, **"Presidente Prudente e região"**. Nunca "atuação nacional": a
captação é regional (ver `kb/identidade.yaml`), e dizer nacional dilui justamente o que faz um
perfil deste porte ser encontrado por quem pode contratar.

### Conferir antes de aceitar

Das quatro opções da primeira geração, uma veio **com subtítulo em inglês**. Sempre olhar as quatro
antes de escolher.

## Referência aprovada

O post de 24/09 (`data/artes/2026-09-24/`) é o padrão: fundo creme, dois círculos orgânicos com os
ícones, frase de fechamento em cartão arredondado, contato no rodapé.
Design: https://www.canva.com/d/7UO0FCyA6IZXI9t
