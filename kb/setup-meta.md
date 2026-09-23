# Configuração da publicação automática

Passos únicos, feitos uma vez, com login nas suas contas. Só você consegue fazer — eu não tenho (e
não devo ter) acesso ao seu Instagram nem ao seu Facebook.

Leva de 30 a 60 minutos na primeira vez. Onde estiver `[CONFERIR]`, o nome do botão pode ter mudado:
a Meta renomeia essas telas com frequência, e eu prefiro dizer isso a te mandar procurar um botão
que não existe mais.

## 0. Git nesta máquina

Esta máquina ainda não tem Git instalado (conferido em 23.09.2026), e ele é necessário para enviar
o projeto ao GitHub. O `winget` está disponível, então a instalação é um comando:

```
winget install --id Git.Git -e
```

Depois, feche e reabra o terminal e confirme com `git --version`.

## 1. Instagram em conta Comercial

No app: **Configurações → Tipo de conta e ferramentas → Mudar para conta profissional →
Empresa/Comercial**.

Conta pessoal e conta de Criador de Conteúdo **não publicam pela API de conteúdo**. Precisa ser
Comercial (Business).

## 2. Página do Facebook vinculada

A API exige que o Instagram esteja vinculado a uma Página do Facebook. Se você não tem, crie uma —
ela pode ficar praticamente vazia, serve de ponte.

Vincular: no Instagram, **Configurações → Central de Contas** (ou, pelo computador, no Meta Business
Suite) **→ adicionar a Página** `[CONFERIR — o caminho muda entre versões do app]`.

Confirme que deu certo: no Meta Business Suite a conta do Instagram aparece listada junto da Página.

## 3. App no Meta for Developers

1. Entre em `developers.facebook.com` com a mesma conta do Facebook e aceite os termos de
   desenvolvedor.
2. **Meus Apps → Criar app**. Tipo: **Empresa/Business**.
3. Dentro do app, **Adicionar produto → Instagram** (o produto de publicação de conteúdo;
   `[CONFERIR — pode aparecer como "Instagram Graph API" ou "Instagram API setup with Facebook
   Login"]`).
4. Vincule ali a Página e a conta do Instagram do passo 2.

Enquanto o app estiver em **modo de desenvolvimento**, ele publica na sua própria conta — que é
exatamente o que a gente precisa. Colocar o app em modo Live e pedir Advanced Access só seria
necessário para publicar em contas de terceiros `[CONFERIR — política de App Review vigente]`.

## 4. Token de acesso

No **Graph API Explorer** (dentro do painel do app):

1. Selecione o seu app e clique em **Gerar token de acesso**.
2. Marque as permissões: `instagram_basic`, `instagram_content_publish`, `pages_show_list`,
   `pages_read_engagement`.
3. Esse token dura poucas horas. Troque-o por um de **longa duração** (~60 dias) chamando, no
   navegador:

```
https://graph.facebook.com/v21.0/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id=<ID DO APP>
  &client_secret=<CHAVE SECRETA DO APP>
  &fb_exchange_token=<O TOKEN CURTO>
```

Guarde o `access_token` devolvido. **Esse é o `IG_TOKEN`.**

## 5. Descobrir o `IG_USER_ID`

Não é o `@`, é um número. No Graph API Explorer, com o token de longa duração:

```
GET /me/accounts                                  → pega o id da Página
GET /<ID DA PÁGINA>?fields=instagram_business_account   → devolve o IG_USER_ID
```

## 6. Repositório no GitHub

1. Crie uma conta no `github.com`, se ainda não tiver.
2. Crie um repositório para este projeto.
3. **Decisão pendente:** a Meta busca a imagem por URL pública, sem token. A rota gratuita mais
   simples é o repositório ser **público** (a arte fica em `raw.githubusercontent.com`). O que ficaria
   público é a arte e a legenda — que vão ao ar de qualquer jeito — mais o código. Suas fotos de
   vistoria **não** vão (estão no `.gitignore`). Se preferir repositório privado, a hospedagem da
   imagem precisa ser outra, e isso a gente resolve junto.
4. Em **Settings → Secrets and variables → Actions**, crie os secrets:

| Secret | Valor |
| --- | --- |
| `IG_TOKEN` | o token de longa duração do passo 4 |
| `IG_USER_ID` | o número do passo 5 |
| `HOSPEDAGEM_BASE` | `https://raw.githubusercontent.com/<usuário>/<repositório>/main` |

## 7. Teste antes de ligar o automático

Local, sem publicar nada:

```
python -m engenharia.publicar --dry-run
```

No GitHub: aba **Actions → publicar-diario → Run workflow**, com `dry_run` marcado. Confira a arte
e a legenda no artefato que o próprio workflow guarda.

Só depois disso, rode uma vez com `dry_run` desmarcado, de preferência num horário de baixo alcance,
e confira o post no perfil.

## 8. A cada ~60 dias

O token vence. Refazer o passo 4 (leva dois minutos) e atualizar o secret `IG_TOKEN`.

A renovação é manual de propósito: automatizá-la exigiria guardar no repositório uma segunda
credencial com poder de trocar segredos — uma credencial a mais para vazar, para economizar dois
minutos a cada dois meses. Coloque um lembrete no calendário.
