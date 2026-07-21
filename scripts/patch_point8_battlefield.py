#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

import patch_point8_battlefield_impl as impl


def shift_later_sections(text: str) -> str:
    """Shift pre-existing top-level Point 9+ sections before inserting the new Point 8."""
    section_pattern = re.compile(
        r'<section\b(?P<attrs>[^>]*)>(?P<body>.*?)</section>',
        re.I | re.S,
    )
    shifted: list[tuple[int, int]] = []

    def repl(match: re.Match[str]) -> str:
        body = match.group("body")
        heading = re.search(r'<h2\b[^>]*>\s*(\d+)\.', body, re.I)
        if not heading:
            return match.group(0)

        old = int(heading.group(1))
        if old < 9:
            return match.group(0)
        new = old + 1

        body, count = re.subn(
            rf'(<h2\b[^>]*>\s*){old}\.',
            rf'\g<1>{new}.',
            body,
            count=1,
            flags=re.I,
        )
        if count != 1:
            raise RuntimeError(f"Não foi possível deslocar o cabeçalho do Ponto {old}.")

        body = re.sub(
            rf'(<h3\b[^>]*>\s*){old}\.(\d+)',
            rf'\g<1>{new}.\2',
            body,
            flags=re.I,
        )
        body = body.replace(
            f'O Ponto {old} está estruturalmente definido.',
            f'O Ponto {new} está estruturalmente definido.',
        )
        shifted.append((old, new))
        return f'<section{match.group("attrs")}>{body}</section>'

    result = section_pattern.sub(repl, text)
    if shifted:
        print("Shifted later GDD points:", ", ".join(f"{old}→{new}" for old, new in shifted))
    return result


def patch_navigation(text: str) -> str:
    """Shift pre-existing Point 9+ navigation, then create the Point 8 and Point 9 entries."""
    clickable = re.compile(
        r"<(?P<tag>a|button)\b(?P<attrs>[^>]*)>(?P<body>.*?)</(?P=tag)>",
        re.I | re.S,
    )

    def shift_existing_clickable(match: re.Match[str]) -> str:
        point = impl.top_level_point(match.group("body"))
        if point is None or point < 9:
            return match.group(0)
        attrs = match.group("attrs")
        if not re.search(r"\b(?:href|data-target|data-section)\s*=", attrs, re.I):
            return match.group(0)
        body = impl.renumber_nav_body(match.group("body"), point, point + 1)
        return f'<{match.group("tag")}{attrs}>{body}</{match.group("tag")}>'

    text = clickable.sub(shift_existing_clickable, text)
    return impl.patch_navigation(text)


def extract_section(gdd: str, section_id: str) -> str:
    matches = re.findall(
        rf'<section\b[^>]*\bid=["\']{re.escape(section_id)}["\'][^>]*>.*?</section>',
        gdd,
        re.I | re.S,
    )
    if len(matches) != 1:
        raise AssertionError(
            f"Esperada exatamente uma seção #{section_id}; encontradas {len(matches)}."
        )
    return matches[0]


def require_all(haystack: str, items: list[str], context: str) -> None:
    missing = [item for item in items if item not in haystack]
    if missing:
        raise AssertionError(f"Conteúdo ausente em {context}: {missing}")


def validate(gdd: str, portal: str) -> None:
    """Validate the generated v16 by stable structure, not brittle literal tag shapes."""
    if "Game Design Document · v16" not in gdd:
        raise AssertionError("Cabeçalho da versão v16 ausente no GDD.")
    if "Available · v16" not in portal:
        raise AssertionError("Portal não foi atualizado para Available · v16.")
    if re.search(r'\bSpecial Moves?\b', gdd, re.I):
        raise AssertionError("Ainda existe ocorrência de Special Move no GDD.")

    battlefield = extract_section(gdd, "battlefield-formation")
    pve = extract_section(gdd, "pve-training")

    if not re.search(
        r'<h2\b[^>]*>\s*8\.\s*Campo de Batalha, Formação e Posicionamento\s*</h2>',
        battlefield,
        re.I,
    ):
        raise AssertionError("Cabeçalho estrutural do novo Ponto 8 não encontrado.")
    if not re.search(
        r'<h2\b[^>]*>\s*9\.\s*Carry, Treinamento e Progressão PvE\s*</h2>',
        pve,
        re.I,
    ):
        raise AssertionError("Cabeçalho estrutural do Ponto 9 não encontrado.")

    battlefield_subsections = re.findall(r'<h3\b[^>]*>\s*8\.(\d+)\b', battlefield, re.I)
    pve_subsections = re.findall(r'<h3\b[^>]*>\s*9\.(\d+)\b', pve, re.I)
    expected_battlefield = [str(number) for number in range(1, 22)]
    expected_pve = [str(number) for number in range(1, 21)]
    if battlefield_subsections != expected_battlefield:
        raise AssertionError(
            f"Subseções inesperadas no Ponto 8: {battlefield_subsections}; "
            f"esperado {expected_battlefield}."
        )
    if pve_subsections != expected_pve:
        raise AssertionError(
            f"Subseções inesperadas no Ponto 9: {pve_subsections}; esperado {expected_pve}."
        )

    require_all(
        battlefield,
        [
            "70% → P1; 15% → P2; 15% → P3",
            "33% do peso dela atravessa",
            "Chance natural efetiva = mínimo entre Chance natural e 35%",
            "Bônus de SOR = 14x ÷ (1 + x)",
            "Vigor possível vai de <strong>50 a 500</strong>",
            "após oito Basic Attacks consecutivos",
            "até três Power Moves consecutivos",
            "Tick lógico de um segundo",
            "0,5 segundo",
            "O Ponto 8 está estruturalmente definido.",
        ],
        "Ponto 8",
    )
    require_all(
        pve,
        [
            "9.8 Formação canônica, posições e bloqueio durante a tentativa",
            "9.15 Reforços roteirizados e bosses com múltiplas fases",
            "9.17 VIP e velocidade visual 1× / 2×",
            "240 ticks (4 minutos lógicos)",
            "360 ticks (6 minutos lógicos)",
            "480 ticks (8 minutos lógicos)",
            "600 ticks (10 minutos lógicos)",
            "O Ponto 9 está estruturalmente definido.",
        ],
        "Ponto 9",
    )

    formation_match = re.search(
        r'<h3\b[^>]*>\s*9\.8\b.*?</h3>.*?(?=<h3\b[^>]*>\s*9\.9\b)',
        pve,
        re.I | re.S,
    )
    if not formation_match:
        raise AssertionError("Não foi possível isolar a subseção 9.8 de formação.")
    if "7 → 5 → 6 → 4 → 2 → 3 → 1" in formation_match.group(0):
        raise AssertionError("A antiga prioridade fixa de targeting permaneceu na subseção 9.8.")

    link_pattern = r'(?:href|data-target|data-section)\s*=\s*["\']#?{target}["\']'
    if not re.search(link_pattern.format(target="battlefield-formation"), gdd, re.I):
        raise AssertionError("Navegação para #battlefield-formation ausente.")
    if not re.search(link_pattern.format(target="pve-training"), gdd, re.I):
        raise AssertionError("Navegação para #pve-training ausente.")

    print(
        "Validated GDD v16:",
        f"Point 8 subsections={len(battlefield_subsections)};",
        f"Point 9 subsections={len(pve_subsections)}.",
    )


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: patch_point8_battlefield.py <gdd_html> <portal_html>")

    gdd_path = Path(sys.argv[1])
    portal_path = Path(sys.argv[2])
    gdd = gdd_path.read_text(encoding="utf-8")
    portal = portal_path.read_text(encoding="utf-8")

    if "Game Design Document · v16" in gdd and '<section id="battlefield-formation">' in gdd:
        validate(gdd, portal)
        print("Point 8 battlefield consolidation already present and valid.")
        return

    if "Game Design Document · v15" not in gdd:
        raise RuntimeError("Versão-base esperada (v15) não encontrada.")

    gdd = re.sub(r"\bSpecial Moves\b", "Power Moves", gdd, flags=re.I)
    gdd = re.sub(r"\bSpecial Move\b", "Power Move", gdd, flags=re.I)
    gdd = shift_later_sections(gdd)

    pve_pattern = re.compile(r'<section id="pve-training">.*?</section>', re.S)
    match = pve_pattern.search(gdd)
    if not match:
        raise RuntimeError("Seção atual de Carry/PvE não encontrada.")

    pve = impl.renumber_and_align_pve(match.group(0))
    gdd = gdd[:match.start()] + impl.BATTLEFIELD_SECTION + "\n" + pve + gdd[match.end():]
    gdd = impl.insert_decisions(gdd)
    gdd = patch_navigation(gdd)
    gdd = gdd.replace("Game Design Document · v15", "Game Design Document · v16")
    portal = portal.replace("Available · v15", "Available · v16")

    validate(gdd, portal)
    gdd_path.write_text(gdd, encoding="utf-8")
    portal_path.write_text(portal, encoding="utf-8")
    print(f"Consolidated Point 8 and renumbered PvE to Point 9 in {gdd_path}.")


if __name__ == "__main__":
    main()
