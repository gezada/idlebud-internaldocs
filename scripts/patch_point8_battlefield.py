#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html as html_lib
import re
import sys

import patch_point8_battlefield_impl as impl


def shift_later_sections(text: str) -> str:
    """Shift every pre-existing top-level Point 9+ by one before inserting the new Point 8."""
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
    """Shift pre-existing Point 9+ navigation, then let the original patch create Points 8 and 9."""
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


def top_level_headings(gdd: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    for match in re.finditer(r'<section\b[^>]*>(?P<body>.*?)</section>', gdd, re.I | re.S):
        h2 = re.search(r'<h2\b[^>]*>(?P<body>.*?)</h2>', match.group('body'), re.I | re.S)
        if not h2:
            continue
        visible = re.sub(r'<[^>]+>', ' ', h2.group('body'))
        visible = ' '.join(html_lib.unescape(visible).split())
        number = re.match(r'(\d+)\.', visible)
        if number:
            headings.append((int(number.group(1)), visible))
    return headings


def validate(gdd: str, portal: str) -> None:
    required = [
        "Game Design Document · v16",
        "8. Campo de Batalha, Formação e Posicionamento",
        "8.1 Campo canônico e identidade das sete posições",
        "8.2 Corredores canônicos",
        "8.3 Ocupação livre, posições vazias e ausência de movimento",
        "8.4 Adjacência canônica",
        "8.5 Targeting canônico dos Basic Attacks",
        "8.6 Exposição e penetração por posições vazias",
        "8.7 Elegibilidade e escolha entre Basic Attack e Power Move",
        "8.8 Chance natural de Power Move",
        "8.9 SOR efetiva e curva de até +7 pontos percentuais",
        "8.10 Distribuição pseudoaleatória e contadores de sequência",
        "8.11 Snapshot de Power Moves multi-alvo e multi-hit",
        "8.12 Manipulação de targeting exclusivamente por Power Moves",
        "8.13 Linha do tempo contínua com ticks sincronizados",
        "8.14 AGI, prontidão e limite de uma ação por tick",
        "8.15 Ação garantida para quem estava pronto no snapshot",
        "8.16 Ordem simultânea de defesa, suporte, ataque e fechamento",
        "8.17 Stun, Silence e prontidão armazenada",
        "8.18 Tick lógico de um segundo e apresentação VIP em 2×",
        "8.19 Limite de invocações e reforços",
        "8.20 Eliminação simultânea completa no PvE",
        "8.21 Ordem autoritativa completa",
        "70% → P1; 15% → P2; 15% → P3",
        "33% do peso dela atravessa",
        "Vigor possível vai de <strong>50 a 500</strong>",
        "Chance natural efetiva = mínimo entre Chance natural e 35%",
        "Bônus de SOR = 14x ÷ (1 + x)",
        "após oito Basic Attacks consecutivos",
        "até três Power Moves consecutivos",
        "1 segundo",
        "0,5 segundo",
        "9. Carry, Treinamento e Progressão PvE",
        "9.8 Formação canônica, posições e bloqueio durante a tentativa",
        "9.15 Reforços roteirizados e bosses com múltiplas fases",
        "9.17 VIP e velocidade visual 1× / 2×",
        "240 ticks (4 minutos lógicos)",
        "360 ticks (6 minutos lógicos)",
        "480 ticks (8 minutos lógicos)",
        "600 ticks (10 minutos lógicos)",
        "O Ponto 8 está estruturalmente definido.",
        "O Ponto 9 está estruturalmente definido.",
    ]
    for item in required:
        assert item in gdd, f"Conteúdo consolidado ausente: {item}"

    assert "Special Move" not in gdd and "Special Moves" not in gdd
    assert gdd.count('<section id="battlefield-formation">') == 1
    assert gdd.count('<section id="pve-training">') == 1

    battlefield_match = re.search(r'<section id="battlefield-formation">.*?</section>', gdd, re.S)
    pve_match = re.search(r'<section id="pve-training">.*?</section>', gdd, re.S)
    assert battlefield_match, "Seção battlefield-formation ausente."
    assert pve_match, "Seção pve-training ausente."
    battlefield = battlefield_match.group(0)
    pve = pve_match.group(0)

    assert battlefield.count("<h3>8.") == 21
    assert pve.count("<h3>9.") == 20
    assert re.search(r'<h2>\s*8\. Campo de Batalha, Formação e Posicionamento</h2>', battlefield)
    assert re.search(r'<h2>\s*9\. Carry, Treinamento e Progressão PvE</h2>', pve)
    assert "7 → 5 → 6 → 4 → 2 → 3 → 1" not in pve
    assert re.search(r'(?:href|data-target|data-section)=["\']#?battlefield-formation["\']', gdd)
    assert re.search(r'(?:href|data-target|data-section)=["\']#?pve-training["\']', gdd)
    assert "Available · v16" in portal

    headings = top_level_headings(gdd)
    numbers = [number for number, _ in headings]
    assert len(numbers) == len(set(numbers)), f"Numeração duplicada nos pontos: {headings}"
    assert (8, "8. Campo de Batalha, Formação e Posicionamento") in headings
    assert (9, "9. Carry, Treinamento e Progressão PvE") in headings
    print("Validated top-level GDD headings:", headings)


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
