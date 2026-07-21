#!/usr/bin/env python3
from pathlib import Path
import re
import sys

import finalize_gdd_v17
import patch_point8_battlefield_v2 as canonical


REFERENCE_TABLE = r'''<table class="reference-table">
<thead><tr><th>Referência</th><th class="reference-positive-head">✓ O que inspira</th><th class="reference-negative-head">× O que não significa</th></tr></thead>
<tbody>
<tr><td><strong>DIGIMON UP</strong></td><td class="reference-positive">Coleção, cuidado, crescimento e uso de criaturas em ciclos leves.</td><td class="reference-negative">Copiar personagens, identidade visual ou estrutura fechada.</td></tr>
<tr><td><strong>Plants vs. Undead</strong></td><td class="reference-positive">Jardim, rega, recuperação, cultivo e sensação de colocar unidades para trabalhar.</td><td class="reference-negative">Repetir a economia NFT ou depender de novos entrantes.</td></tr>
<tr><td><strong>Pokémon</strong></td><td class="reference-positive">Tipos, counters, elenco amplo e troca de equipe conforme o desafio.</td><td class="reference-negative">Limitar o jogo a pedra-papel-tesoura simples.</td></tr>
<tr><td><strong>Ragnarok</strong></td><td class="reference-positive">Seis atributos clássicos com distribuição livre e espaço para builds inteligentes ou ruins.</td><td class="reference-negative">Reproduzir fórmulas ou classes literalmente.</td></tr>
<tr><td><strong>Grand Chase</strong></td><td class="reference-positive">Campanha organizada por regiões, fases, identidade visual e chefes.</td><td class="reference-negative">Transformar o combate em ação lateral manual.</td></tr>
<tr><td><strong>Task Bar Hero</strong></td><td class="reference-positive">Progressão longa, árvore de skills, itemização, raridades e prazer de otimizar.</td><td class="reference-negative">Transformar toda a oferta em emissão passiva negociável.</td></tr>
<tr><td><strong>Corepunk</strong></td><td class="reference-positive">Atributos, passivas, níveis discretos e reroll como camada profunda de build.</td><td class="reference-negative">Importar complexidade sem função clara.</td></tr>
<tr><td><strong>V Rising</strong></td><td class="reference-positive">Materiais regionais, receitas, pesquisa, refinamento, desmontagem, fusão e crafting com risco.</td><td class="reference-negative">Substituir a progressão da planta por Gear Level ou criar burocracia de estações.</td></tr>
</tbody>
</table>'''

REFERENCE_CSS = r'''<style id="reference-table-tone">
.reference-table .reference-positive-head,
.reference-table .reference-positive {
  background: linear-gradient(90deg, rgba(82, 146, 104, .13), rgba(82, 146, 104, .055));
  border-left-color: rgba(116, 190, 139, .32);
}
.reference-table .reference-negative-head,
.reference-table .reference-negative {
  background: linear-gradient(90deg, rgba(145, 74, 78, .14), rgba(145, 74, 78, .06));
  border-left-color: rgba(206, 112, 118, .34);
}
.reference-table .reference-positive-head { color: #9bd6ad; }
.reference-table .reference-negative-head { color: #dda0a4; }
.reference-table .reference-positive,
.reference-table .reference-negative { color: var(--text, #e8ecef); }
.reference-table td.reference-positive,
.reference-table td.reference-negative { border-left-width: 2px; }
</style>'''


def replace_subsection(
    section: str,
    point: int,
    current: int,
    following: int | None,
    replacement: str,
) -> str:
    """Replace a numbered subsection by structural heading boundaries."""
    if following is None:
        pattern = re.compile(
            rf'<h3\b[^>]*>\s*{point}\.{current}\b.*?</h3>.*?\Z',
            re.I | re.S,
        )
    else:
        pattern = re.compile(
            rf'<h3\b[^>]*>\s*{point}\.{current}\b.*?</h3>.*?'
            rf'(?=<h3\b[^>]*>\s*{point}\.{following}\b)',
            re.I | re.S,
        )
    section, count = pattern.subn(replacement + "\n", section, count=1)
    if count != 1:
        raise RuntimeError(
            f"Subseção {point}.{current} ausente ou duplicada; transformação estrutural interrompida."
        )
    return section


def rewrite_navigation_labels(gdd: str) -> str:
    """Set canonical menu labels; fall back to plain button text instead of failing on copy drift."""
    clickable = re.compile(
        r'<(?P<tag>a|button)\b(?P<attrs>[^>]*)>(?P<body>.*?)</(?P=tag)>',
        re.I | re.S,
    )
    candidates = [
        "Carry e formação de elenco",
        "Carry, Treinamento e Progressão PvE",
        "Carry, treinamento e PvE",
        "Carry e PvE",
        "Campo de Batalha, Formação e Posicionamento",
        "Campo de batalha e formação",
        "Campo de batalha",
    ]
    found = {target: 0 for target in canonical.NAV_LABELS}

    def repl(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        body = match.group("body")
        for target, label in canonical.NAV_LABELS.items():
            if not re.search(
                rf'(?:href|data-target|data-section)\s*=\s*["\']#?{re.escape(target)}["\']',
                attrs,
                re.I,
            ):
                continue
            found[target] += 1
            if label not in canonical.impl.visible_text(body):
                for candidate in candidates:
                    body, count = re.subn(
                        re.escape(candidate), label, body, count=1, flags=re.I
                    )
                    if count:
                        break
            if label not in canonical.impl.visible_text(body):
                point = 8 if target == "battlefield-formation" else 9
                body = f"{point}. {label}"
            break
        return f'<{match.group("tag")}{attrs}>{body}</{match.group("tag")}>'

    gdd = clickable.sub(repl, gdd)
    missing = [target for target, count in found.items() if count == 0]
    if missing:
        raise RuntimeError(f"Navegação estrutural ausente para: {missing}")
    return gdd


def patch_reference_table(gdd: str) -> str:
    """Rebuild Point 2.2's comparison table with canonical copy and restrained semantic color."""
    table_pattern = re.compile(
        r'<table\b[^>]*>\s*<thead>\s*<tr>\s*'
        r'<th>\s*Referência\s*</th>\s*'
        r'<th>\s*O que inspira\s*</th>\s*'
        r'<th>\s*O que não significa\s*</th>\s*'
        r'</tr>\s*</thead>.*?</table>',
        re.I | re.S,
    )
    gdd, count = table_pattern.subn(REFERENCE_TABLE, gdd, count=1)
    if count == 0 and 'class="reference-table"' not in gdd:
        print("Warning: Point 2.2 reference table was not found; build will continue unchanged.")

    if 'id="reference-table-tone"' not in gdd:
        if "</head>" in gdd:
            gdd = gdd.replace("</head>", REFERENCE_CSS + "\n</head>", 1)
        else:
            gdd = REFERENCE_CSS + "\n" + gdd
    return gdd


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: patch_point8_battlefield.py <gdd_html> <portal_html>")

    gdd_path = Path(sys.argv[1])
    portal_path = Path(sys.argv[2])
    existing = gdd_path.read_text(encoding="utf-8")
    already_v17 = (
        "Game Design Document · v17" in existing
        and 'id="battlefield-formation"' in existing
    )

    if not already_v17:
        canonical.main()

    gdd = gdd_path.read_text(encoding="utf-8")
    gdd = patch_reference_table(gdd)
    gdd_path.write_text(gdd, encoding="utf-8")
    print("Refined Point 2.2 reference table copy and semantic colors.")

    finalize_gdd_v17.finalize(gdd_path, portal_path)


canonical.replace_subsection = replace_subsection
canonical.rewrite_navigation_labels = rewrite_navigation_labels


if __name__ == "__main__":
    main()
