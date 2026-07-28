# Idle Bud — Internal Documentation

Este repositório mantém a documentação interna viva e oficial de **Idle Bud**.

## Portal

O conteúdo é publicado pelo GitHub Pages a partir do workflow em `.github/workflows/pages.yml`.

Endereço permanente:

`https://gezada.github.io/idlebud-internaldocs/`

O portal centraliza:

- **Game Design Document** — documento vivo disponível em `/gdd/`;
- **Economy** — referência econômica oficial disponível em `/economy/`;
- **Enemies, Drops, Itemization & Forge** — TBD;
- **Technology Guidelines** — TBD.

## Publicação

O GitHub Pages usa **GitHub Actions**. O workflow publica o GDD a partir de
`gdd-source/index.html`, publica Economia a partir de
`economy-source/index.html`, gera a página inicial e mantém placeholders apenas
para os documentos ainda não disponíveis.

## Estrutura publicada

- `/` — portal de documentação;
- `/gdd/` — Game Design Document;
- `/economy/` — Economia oficial v1.0;
- `/enemies-drops-craft/` — TBD;
- `/technology-guidelines/` — TBD.

## Fontes canônicas

- `gdd-source/index.html` — Game Design Document v17;
- `economy-source/index.html` — Economia v1.0;
- `economy-source/TRACEABILITY.md` — matriz interna de evidências e propostas
  históricas descartadas.
