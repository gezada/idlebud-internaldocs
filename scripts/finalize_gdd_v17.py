#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html as html_lib
import re
import sys


SECTION_PATTERN = re.compile(
    r'<section\b(?P<attrs>[^>]*)>(?P<body>.*?)</section>', re.I | re.S
)
CLICKABLE_PATTERN = re.compile(
    r'<(?P<tag>a|button)\b(?P<attrs>[^>]*)>(?P<body>.*?)</(?P=tag)>',
    re.I | re.S,
)
POINT_REFERENCE = re.compile(r'\b(Ponto|Point)\s+(1[1-9]|2[0-5])\b', re.I)
LEGACY_TARGET = re.compile(
    r'(?:href|data-target|data-section)\s*=\s*["\']#?formacao["\']', re.I
)
PVP_BLOCK = r'''<div class="statement" data-canonical="pvp-formation-role"><strong>Não existe formação defensiva separada.</strong> A formação ativa do jogador é simultaneamente sua formação de ataque e de defesa.</div>
<ul data-canonical="pvp-asynchronous-scope">
<li>o PvP assíncrono existe para farm e teste de composição;</li>
<li>o PvP assíncrono não gera ranking;</li>
<li>o PvP com ranking não pode ser assíncrono;</li>
<li>o formato do PvP ranqueado será definido na revisão específica do sistema.</li>
</ul>'''


def visible_text(fragment: str) -> str:
    return " ".join(html_lib.unescape(re.sub(r"<[^>]+>", " ", fragment)).split())


def top_level_point(fragment: str) -> int | None:
    match = re.match(
        r"^(?:Ponto\s+)?0*(\d+)(?:\.(?!\d)|\s*[—–:-]\s*|\s+|$)",
        visible_text(fragment),
        re.I,
    )
    return int(match.group(1)) if match else None


def section_heading(body: str) -> tuple[int, str] | None:
    heading = re.search(r'<h2\b[^>]*>(?P<body>.*?)</h2>', body, re.I | re.S)
    if not heading:
        return None
    text = visible_text(heading.group("body"))
    number = re.match(r'(\d+)\.', text)
    return (int(number.group(1)), text) if number else None


def renumber_nav_body(body: str, old: int, new: int) -> str:
    replacements = [
        (rf"(?P<a>>\s*){old}(?P<b>\s*<)", rf"\g<a>{new}\g<b>"),
        (rf"\bPonto\s+{old}\b", f"Ponto {new}"),
        (rf"(?<!\d){old}\.(?!\d)", f"{new}."),
        (rf"(?<!\d){old}(?!\d)", str(new)),
    ]
    for pattern, replacement in replacements:
        result, count = re.subn(pattern, replacement, body, count=1, flags=re.I)
        if count:
            return result
    raise RuntimeError(f"Não foi possível renumerar a navegação {old}→{new}.")


def protected_sections(gdd: str) -> dict[int, str]:
    result: dict[int, str] = {}
    for match in SECTION_PATTERN.finditer(gdd):
        heading = section_heading(match.group("body"))
        if heading and heading[0] <= 9:
            result[heading[0]] = match.group(0)
    return result


def shift_references(fragment: str, mapping: dict[int, int]) -> str:
    return POINT_REFERENCE.sub(
        lambda match: f"{match.group(1)} {mapping[int(match.group(2))]}",
        fragment,
    )


def remove_legacy_formation_section(gdd: str) -> str:
    removed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal removed
        attrs = match.group("attrs")
        heading = section_heading(match.group("body"))
        legacy_id = bool(re.search(r'\bid=["\']formacao["\']', attrs, re.I))
        legacy_title = bool(heading and "Formação de sete plantas" in heading[1])
        if not legacy_id and not legacy_title:
            return match.group(0)
        if not legacy_title:
            raise RuntimeError("#formacao não corresponde à seção legada esperada.")
        removed += 1
        return ""

    gdd = SECTION_PATTERN.sub(repl, gdd)
    if removed != 1:
        raise RuntimeError(f"Esperada uma seção legada de formação; encontradas {removed}.")
    return gdd


def remove_legacy_navigation(gdd: str) -> str:
    removed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal removed
        body = visible_text(match.group("body"))
        if LEGACY_TARGET.search(match.group("attrs")) or "Formação de sete" in body:
            removed += 1
            return ""
        return match.group(0)

    gdd = CLICKABLE_PATTERN.sub(repl, gdd)
    if removed == 0:
        raise RuntimeError("Nenhuma entrada de navegação da formação legada foi encontrada.")
    if LEGACY_TARGET.search(gdd):
        raise RuntimeError("A navegação ainda aponta para #formacao.")
    return gdd


def renumber_later_points(gdd: str) -> str:
    mapping = {old: old - 1 for old in range(11, 26)}

    def section_repl(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        body = shift_references(match.group("body"), mapping)
        heading = section_heading(body)
        if not heading or heading[0] not in mapping:
            return f'<section{attrs}>{body}</section>'
        old = heading[0]
        new = mapping[old]
        body, count = re.subn(
            rf'(<h2\b[^>]*>\s*){old}\.', rf'\g<1>{new}.', body,
            count=1, flags=re.I,
        )
        if count != 1:
            raise RuntimeError(f"Cabeçalho {old}→{new} não pôde ser renumerado.")
        body = re.sub(
            rf'(<h3\b[^>]*>\s*){old}\.(\d+)', rf'\g<1>{new}.\2',
            body, flags=re.I,
        )
        return f'<section{attrs}>{body}</section>'

    gdd = SECTION_PATTERN.sub(section_repl, gdd)

    def nav_repl(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        body = match.group("body")
        point = top_level_point(body)
        if point not in mapping or not re.search(
            r'\b(?:href|data-target|data-section)\s*=', attrs, re.I
        ):
            return match.group(0)
        body = renumber_nav_body(body, point, mapping[point])
        return f'<{match.group("tag")}{attrs}>{body}</{match.group("tag")}>'

    return CLICKABLE_PATTERN.sub(nav_repl, gdd)


def insert_pvp_decision(gdd: str) -> str:
    count = gdd.count('data-canonical="pvp-formation-role"')
    if count == 1:
        return gdd
    if count > 1:
        raise RuntimeError("Bloco canônico de PvP duplicado.")

    inserted = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal inserted
        body = match.group("body")
        heading = section_heading(body)
        if not heading or "PvP assíncrono" not in heading[1]:
            return match.group(0)
        body, replacements = re.subn(
            r'(<h2\b[^>]*>.*?</h2>)', rf'\1\n{PVP_BLOCK}', body,
            count=1, flags=re.I | re.S,
        )
        if replacements != 1:
            raise RuntimeError("Cabeçalho da seção de PvP não encontrado.")
        inserted += 1
        return f'<section{match.group("attrs")}>{body}</section>'

    gdd = SECTION_PATTERN.sub(repl, gdd)
    if inserted != 1:
        raise RuntimeError(f"Esperada uma seção de PvP assíncrono; encontradas {inserted}.")
    return gdd


def headings(gdd: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for match in SECTION_PATTERN.finditer(gdd):
        heading = section_heading(match.group("body"))
        if heading:
            result.append(heading)
    return result


def navigation_points(gdd: str) -> set[int]:
    result: set[int] = set()
    for match in CLICKABLE_PATTERN.finditer(gdd):
        if not re.search(
            r'\b(?:href|data-target|data-section)\s*=', match.group("attrs"), re.I
        ):
            continue
        point = top_level_point(match.group("body"))
        if point is not None:
            result.add(point)
    return result


def validate(gdd: str, portal: str) -> None:
    if "Game Design Document · v17" not in gdd:
        raise AssertionError("Cabeçalho v17 ausente.")
    if "Available · v17" not in portal:
        raise AssertionError("Portal não indica v17.")
    if re.search(r'\bid=["\']formacao["\']', gdd, re.I):
        raise AssertionError("A seção #formacao ainda existe.")
    if "Formação de sete plantas" in gdd or "Formação de sete" in gdd:
        raise AssertionError("Texto da formação legada ainda existe.")
    if LEGACY_TARGET.search(gdd):
        raise AssertionError("A navegação ainda aponta para #formacao.")
    for stale in [
        "targeting, adjacência, alcance, vanguarda, centro, retaguarda e áreas serão prototipadas",
        "serão prototipadas separadamente",
    ]:
        if stale in gdd:
            raise AssertionError(f"Texto provisório obsoleto presente: {stale}")

    expected = list(range(1, 25))
    actual = headings(gdd)
    if [number for number, _ in actual] != expected:
        raise AssertionError(f"Numeração superior inválida: {actual}")
    if (8, "8. Campo de Batalha, Formação e Posicionamento") not in actual:
        raise AssertionError("Ponto 8 canônico ausente.")
    if (9, "9. Carry, Treinamento e Progressão PvE") not in actual:
        raise AssertionError("Ponto 9 canônico ausente.")
    if navigation_points(gdd) != set(expected):
        raise AssertionError(f"Navegação inválida: {sorted(navigation_points(gdd))}")

    if gdd.count('id="battlefield-formation"') != 1:
        raise AssertionError("A seção autoritativa de formação está ausente ou duplicada.")
    if gdd.count('data-canonical="pvp-formation-role"') != 1:
        raise AssertionError("Decisão de formação do PvP ausente ou duplicada.")
    for required in [
        "Não existe formação defensiva separada.",
        "A formação ativa do jogador é simultaneamente sua formação de ataque e de defesa.",
        "o PvP assíncrono existe para farm e teste de composição",
        "o PvP assíncrono não gera ranking",
        "o PvP com ranking não pode ser assíncrono",
    ]:
        if required not in gdd:
            raise AssertionError(f"Decisão aprovada de PvP ausente: {required}")


def finalize(gdd_path: Path, portal_path: Path) -> None:
    gdd = gdd_path.read_text(encoding="utf-8")
    portal = portal_path.read_text(encoding="utf-8")

    if "Game Design Document · v16" in gdd:
        before = protected_sections(gdd)
        gdd = remove_legacy_formation_section(gdd)
        gdd = remove_legacy_navigation(gdd)
        gdd = renumber_later_points(gdd)
        after = protected_sections(gdd)
        mapping = {old: old - 1 for old in range(11, 26)}
        expected_after = {
            number: shift_references(section, mapping)
            for number, section in before.items()
        }
        if after != expected_after:
            raise RuntimeError("A remoção alterou indevidamente os Pontos 1–9.")
        gdd = gdd.replace("Game Design Document · v16", "Game Design Document · v17", 1)
        portal = portal.replace("Available · v16", "Available · v17", 1)
    elif "Game Design Document · v17" not in gdd:
        raise RuntimeError("Versão-base esperada (v16 ou v17) não encontrada.")

    gdd = insert_pvp_decision(gdd)
    validate(gdd, portal)
    gdd_path.write_text(gdd, encoding="utf-8")
    portal_path.write_text(portal, encoding="utf-8")
    print("Finalized GDD v17: removed legacy Point 10 and recorded PvP scope.")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: finalize_gdd_v17.py <gdd_html> <portal_html>")
    finalize(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
