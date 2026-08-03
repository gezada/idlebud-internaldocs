# Idle Bud — Internal Documentation

Este repositório mantém a documentação interna viva e oficial de **Idle Bud**.

## Portal

O conteúdo é publicado pelo GitHub Pages a partir do workflow em `.github/workflows/pages.yml`.

Endereço permanente:

`https://gezada.github.io/idlebud-internaldocs/`

O portal centraliza:

- **Game Design Document** — documento vivo disponível em `/gdd/`;
- **Economy** — referência econômica oficial disponível em `/economy/`;
- **Enemies, Drops, Itemization & Forge** — Bíblia oficial de conteúdo da
  Temporada 1 disponível em `/enemies-drops-craft/`;
- **Technology Guidelines** — referência oficial de tecnologia e engenharia
  disponível em `/technology-guidelines/`.

## Publicação

O GitHub Pages usa **GitHub Actions**. O workflow publica o GDD a partir de
`gdd-source/index.html`, publica Economia a partir de
`economy-source/index.html`, publica Tecnologia a partir de
`technology-source/index.html`, publica Inimigos e Forja a partir de
`enemies-drops-craft-source/index.html` e gera a página inicial.

## Estrutura publicada

- `/` — portal de documentação;
- `/gdd/` — Game Design Document;
- `/economy/` — Economia oficial v1.0;
- `/enemies-drops-craft/` — Inimigos, Drops, Itemização e Forja v1.0;
- `/technology-guidelines/` — Diretrizes de Tecnologia e Engenharia v1.1.

## Fontes canônicas

- `gdd-source/index.html` — Game Design Document v17;
- `economy-source/index.html` — Economia v1.0;
- `economy-source/TRACEABILITY.md` — matriz interna de evidências e propostas
  históricas descartadas;
- `technology-source/index.html` — Diretrizes de Tecnologia e Engenharia v1.1;
- `technology-source/TRACEABILITY.md` — matriz interna de decisões, correções da
  fonte original e referências técnicas verificadas.
- `enemies-drops-craft-source/index.html` — Bíblia de conteúdo da Temporada 1;
- `enemies-drops-craft-source/TRACEABILITY.md` — matriz de autoridade,
  decisões de conteúdo e pendências reais.
