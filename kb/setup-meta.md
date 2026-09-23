# Configuração da publicação automática

Três blocos: **Meta** (o que autoriza publicar), **GitHub** (onde o robô roda) e **o teste**. O que
exige o seu login está marcado com 🔑 — o resto eu executo.

Git 2.55 e GitHub CLI 2.101 já foram instalados nesta máquina em 23.09.2026.

Onde estiver `[CONFERIR]`, o nome do botão pode ter mudado: a Meta renomeia essas telas com
frequência.

---

## Bloco 1 — Meta

### 🔑 1. Instagram em conta Comercial

No app: **Configurações → Tipo de conta e ferramentas → Mudar para conta profissional →
Empresa/Comercial**.

Conta pessoal e conta de Criador **não publicam pela API de conteúdo**. Precisa ser Comercial.

### 🔑 2. Página do Facebook vinculada

A API exige o vínculo. Se você não tem Página, crie uma — ela pode ficar praticamente vazia, serve
de ponte.

Vincular pelo Instagram: **Configurações → Central de Contas → adicionar a Página**
`[CONFERIR — o caminho muda entre versões do app]`. Ou, pelo computador, dentro do Meta Business
Suite.

Confirme: no Meta Business Suite, a conta do Instagram aparece listada junto da Página.

### 🔑 3. App no Meta for Developers

1. `developers.facebook.com`, com a mesma conta do Facebook, aceitando os termos de desenvolvedor.
2. **Meus Apps → Criar app**, tipo **Empresa/Business**.
3. **Adicionar produto → Instagram**, o de publicação de conteúdo
   `[CONFERIR — aparece como "Instagram Graph API" ou "Instagram API setup with Facebook Login"]`.
4. Vincule ali a Página e a conta do Instagram.

Em **modo de desenvolvimento** o app já publica na sua própria conta — que é tudo que precisamos.
Modo Live e Advanced Access só seriam necessários para publicar em contas de terceiros
`[CONFERIR — política de App Review vigente]`.

### 🔑 4. Gerar o token curto

No **Graph API Explorer**, dentro do painel do app:

1. Selecione o seu app e clique em **Gerar token de acesso**.
2. Marque as permissões: `instagram_basic`, `instagram_content_publish`, `pages_show_list`,
   `pages_read_engagement`.
3. Copie o token. Ele dura poucas horas — e não tem problema, porque o próximo passo já o troca.

Anote também, na página inicial do app (**Configurações → Básico**): o **ID do app** e a **chave
secreta do app**.

### 5. Um comando resolve o resto

```
python -m engenharia.configurar --app-id <ID> --app-secret <CHAVE> --token-curto <TOKEN>
```

O que ele faz sozinho: troca o token curto pelo de longa duração (~60 dias), encontra a Página,
descobre o `IG_USER_ID` da conta do Instagram e escreve o `.env`.

**A chave secreta não é guardada.** Ela serve só para a troca e é descartada quando o comando
termina — por isso não vai para o `.env` nem para o GitHub.

Conferir depois, a qualquer momento:

```
python -m engenharia.configurar --conferir
```

Ele mostra qual conta está conectada, quantos seguidores tem e quantos dias faltam para o token
vencer.

---

## Bloco 2 — GitHub

### 🔑 6. Conta e login do CLI

Crie a conta em `github.com`, se ainda não tiver. Depois, **no seu terminal** (este passo pede
interação, então não dá para eu rodar por você):

```
gh auth login
```

Responda: **GitHub.com** → **HTTPS** → **Yes** (autenticar o Git) → **Login with a web browser**.
Ele mostra um código de 8 caracteres, abre o navegador, você cola o código e autoriza.

Terminou? Me avise. Daí em diante eu executo.

### 7. Repositório, push e secrets

Com o `gh` autenticado, isto é meu:

```
gh repo create engenharia-captacao --public --source=. --remote=origin --push
gh secret set IG_TOKEN --body "<token>"
gh secret set IG_USER_ID --body "<id>"
gh secret set HOSPEDAGEM_BASE --body "https://raw.githubusercontent.com/<usuário>/engenharia-captacao/main"
```

**Repositório público — decidido em 23.09.2026.** A Meta busca a imagem por URL, sem token, e
`raw.githubusercontent.com` não serve arquivo de repositório privado. O que fica visível é a arte,
as legendas e o código: conteúdo que vai ao ar de qualquer forma. As fotos de vistoria **não** vão —
`data/ativos/` está no `.gitignore`.

O que isso obriga a lembrar, para sempre: **nada de dado de cliente neste repositório.** Foto,
planta, nome, endereço, número de processo. Se um dia entrar por engano, não basta apagar no commit
seguinte — o histórico guarda.

---

## Bloco 3 — O teste

### 8. Sem publicar nada

```
python -m engenharia.publicar --dry-run
```

E no GitHub: aba **Actions → publicar-diario → Run workflow**, com `dry_run` marcado. Confira a arte
e a legenda no artefato que o próprio workflow guarda.

### 9. Publicando de verdade, uma vez

```
python -m engenharia.publicar
```

De preferência num horário de baixo alcance. Confira o post no perfil e o `post_id` em
`data/saida/<data>/log.json`. Deu certo? O automático já está ligado: o workflow roda de segunda a
sexta às 11h de Brasília.

---

## A cada ~60 dias

O token vence. Refazer os passos 4 e 5 (dois minutos) e atualizar o secret:

```
gh secret set IG_TOKEN --body "<novo token>"
```

A renovação é manual de propósito: automatizá-la exigiria guardar no repositório uma segunda
credencial com poder de trocar segredos — mais risco do que os dois minutos economizados. Vale um
lembrete no calendário.
