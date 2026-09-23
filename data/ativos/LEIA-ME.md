# data/ativos/

Suas fotos e vídeos reais de vistoria, obra e campo. É o material que separa este perfil de
qualquer página genérica de engenharia.

**Nada aqui vai para o repositório** (`.gitignore`): é material de cliente. O que vai a público é a
arte final composta em `data/saida/<data>/`, que é exatamente o que seria publicado de qualquer
forma.

## Como usar

1. Jogue o arquivo aqui, com nome descritivo: `2026-09-30-fissura-diagonal.jpg`.
2. Na entrada do dia em `data/pauta/calendario.yaml`, aponte o campo `ativo` para esse nome:

```yaml
ativo: 2026-09-30-fissura-diagonal.jpg
```

3. O motor usa a foto como fundo da arte, com o título por cima.

Sem arquivo declarado, o dia cai para arte de template — nunca se inventa uma foto de obra que não
existe.

## Antes de subir uma foto

- Foto de imóvel, obra ou ambiente de cliente exige **autorização escrita de uso**, guardada fora
  daqui. Vale também para foto "sem identificar" que a cidade reconhece.
- Enquadre o detalhe técnico (a fissura, o equipamento, a medição), não o contexto identificável
  (fachada, número, placa, rosto).
- Foto de celular serve. Luz do dia e foco no detalhe valem mais que câmera boa.
