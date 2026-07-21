#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

import patch_point8_battlefield_impl as impl


NAV_LABELS = {
    "battlefield-formation": "Campo de batalha e formação",
    "pve-training": "Carry, treinamento e PvE",
}


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


def replace_once_or_confirm(text: str, old: str, new: str, context: str) -> str:
    """Apply one deterministic replacement, while remaining idempotent on rebuilt output."""
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Texto-base não encontrado para microajuste: {context}")
    return text.replace(old, new, 1)


def replace_regex_once_or_confirm(
    text: str,
    pattern: str,
    replacement: str,
    confirmation: str,
    context: str,
) -> str:
    """Apply one regex replacement, or accept an already-adjusted confirmation marker."""
    if confirmation in text:
        return text
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.I | re.S)
    if count != 1:
        raise RuntimeError(f"Texto-base não encontrado para microajuste: {context}")
    return text


def rewrite_navigation_label(text: str, target: str, label: str) -> str:
    expected_point = 8 if target == "battlefield-formation" else 9
    pattern = re.compile(
        rf'<(?P<tag>a|button)\b(?P<attrs>[^>]*(?:href|data-target|data-section)\s*=\s*["\']#?{re.escape(target)}["\'][^>]*)>'
        rf'(?P<body>.*?)</(?P=tag)>',
        re.I | re.S,
    )
    candidates = [
        "Carry e formação de elenco",
        "Carry, Treinamento e Progressão PvE",
        "Carry, treinamento e PvE",
        "Carry e PvE",
        "Campo de Batalha, Formação e Posicionamento",
        "Campo de batalha e formação",
    ]
    matched = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal matched
        body = match.group("body")
        if impl.top_level_point(body) != expected_point:
            return match.group(0)
        matched += 1
        visible = impl.visible_text(body)
        if label not in visible:
            for candidate in candidates:
                body, count = re.subn(
                    re.escape(candidate),
                    label,
                    body,
                    count=1,
                    flags=re.I,
                )
                if count:
                    break
        if label not in impl.visible_text(body):
            raise RuntimeError(
                f"Não foi possível ajustar o texto do menu para #{target}: {visible!r}"
            )
        return f'<{match.group("tag")}{match.group("attrs")}>{body}</{match.group("tag")}>'

    text = pattern.sub(repl, text)
    if matched == 0:
        raise RuntimeError(f"Nenhum botão de navegação encontrado para #{target}.")
    return text


def apply_approved_microadjustments(gdd: str) -> str:
    """Apply the independently reviewed and explicitly approved Point 8/9 refinements."""
    for target, label in NAV_LABELS.items():
        gdd = rewrite_navigation_label(gdd, target, label)

    gdd = replace_once_or_confirm(
        gdd,
        "<div class=\"statement\"><strong>Quando uma posição-alvo está vazia ou derrotada, 33% do peso dela atravessa para a próxima camada viva do mesmo corredor. Os 67% restantes são redistribuídos proporcionalmente entre os demais alvos vivos já acessíveis.</strong></div>",
        "<div class=\"statement\"><strong>Quando uma posição-alvo está vazia ou derrotada, 33% de seu peso passa para a próxima camada do mesmo corredor. Caso essa camada também esteja vazia, o coeficiente de 33% é aplicado novamente antes de alcançar a camada seguinte. Os 67% restantes de cada passagem são redistribuídos proporcionalmente entre os demais alvos vivos já acessíveis.</strong></div>",
        "8.6 — exposição por camadas",
    )

    eligibility_anchor = """<li>o usuário não está sob um efeito que bloqueie Power Moves.</li>
</ul>
<p>Se estiver inelegível, o Bud executa obrigatoriamente um Basic Attack."""
    eligibility_expanded = """<li>o usuário não está sob um efeito que bloqueie Power Moves.</li>
</ul>
<div class="card"><strong>Exemplos objetivos de elegibilidade</strong><ul>
<li>um Power Move de cura fica inelegível quando todos os aliados válidos estão com HP cheio e volta a ser elegível quando ao menos um deles está ferido;</li>
<li>um Power Move que apenas remove debuffs fica inelegível quando não existe debuff removível em nenhum alvo válido;</li>
<li>um Power Move que causa dano e também aplica debuff permanece elegível enquanto houver alvo válido para o dano, mesmo quando esse alvo for imune ao efeito secundário;</li>
<li>um buff no próprio usuário pode ficar inelegível quando o movimento proíbe renovação ou acúmulo e o buff já está ativo;</li>
<li>um Power Move direcionado a uma posição específica vazia fica inelegível quando não declara fallback, exposição ou outra regra alternativa de targeting.</li>
</ul></div>
<p>Se estiver inelegível, o Bud executa obrigatoriamente um Basic Attack."""
    gdd = replace_once_or_confirm(
        gdd,
        eligibility_anchor,
        eligibility_expanded,
        "8.7 — exemplos objetivos de elegibilidade",
    )

    gdd = replace_once_or_confirm(
        gdd,
        "<h3>8.19 Limite de invocações e reforços</h3>",
        "<h3>8.19 Ausência de invocações para Buds e reforços roteirizados no PvE</h3>",
        "8.19 — título sem ambiguidade",
    )

    gdd = replace_once_or_confirm(
        gdd,
        "<li>se o último Bud e o último inimigo forem derrotados no mesmo tick, a tentativa é derrota do jogador;</li>\n<li>essa eliminação simultânea não concede conclusão da fase, avanço de mapa nem drops de conclusão;</li>",
        "<li>se o último Bud e o último inimigo forem derrotados no mesmo tick, a tentativa é derrota do jogador;</li>\n<li>XP e drops normais dos inimigos definitivamente derrotados são preservados conforme as regras do Ponto 9;</li>\n<li>recompensas de conclusão não são concedidas e a fase não avança o mapa;</li>",
        "8.20 — preservação de XP e drops normais",
    )

    gdd = replace_once_or_confirm(
        gdd,
        "<div class=\"statement\"><strong>O Ponto 8 está estruturalmente definido.</strong> Números de dano, fórmulas exatas de ganho de prontidão, curva interna do pseudo-RNG e kits individuais serão calibrados e documentados sem alterar estas invariantes.</div>",
        "<div class=\"statement\"><strong>O Ponto 8 está estruturalmente definido.</strong> Números de dano, fórmulas exatas de ganho de prontidão, valor da SOR de referência da temporada, curva interna do pseudo-RNG e kits individuais serão calibrados e documentados sem alterar estas invariantes.</div>",
        "8.21 — parâmetros pendentes de balanceamento",
    )

    gdd = replace_once_or_confirm(
        gdd,
        "<li>retorna com HP e recursos de combate completamente restaurados;</li>",
        "<li>retorna com o HP completamente restaurado;</li>",
        "9.11 — retorno sem recurso universal inexistente",
    )

    gdd = replace_once_or_confirm(
        gdd,
        "<div class=\"statement\"><strong>Eliminação simultânea completa é derrota do jogador.</strong> Se o último Bud e o último inimigo forem derrotados no mesmo tick, todas as ações são concluídas, mas a fase não é vencida, não avança o mapa e não concede drops de conclusão.</div>",
        "<div class=\"statement\"><strong>Eliminação simultânea completa é derrota do jogador.</strong> Se o último Bud e o último inimigo forem derrotados no mesmo tick, todas as ações são concluídas. XP e drops normais dos inimigos definitivamente derrotados são preservados, mas a fase não é vencida, não avança o mapa e não concede recompensas de conclusão.</div>",
        "9.12 — resultado da eliminação simultânea",
    )

    new_tick_order = r"""\1
<ol>
<li>no início do tick, processa os retornos cujo contador já terminou;</li>
<li>constrói o snapshot com esses Buds já presentes em suas posições originais;</li>
<li>fixa e resolve as ações autorizadas para aquele snapshot;</li>
<li>consolida as mortes e demais mudanças no fechamento do tick;</li>
<li>verifica se existe ao menos um Bud ativo;</li>
<li>declara derrota somente depois dessa verificação.</li>
</ol>"""
    gdd = replace_regex_once_or_confirm(
        gdd,
        r'(<h3\b[^>]*>\s*9\.12\b.*?</h3>.*?<p>Em cada tick, o servidor processa nesta ordem:</p>)\s*<(?:ol|ul)>.*?</(?:ol|ul)>',
        new_tick_order,
        "constrói o snapshot com esses Buds já presentes em suas posições originais",
        "9.12 — retornos alinhados ao snapshot",
    )

    gdd = replace_once_or_confirm(
        gdd,
        "<li>após o Frenesi, todos os inimigos recebem cumulativamente +15% de dano e +10% de Penetração a cada 30 segundos;</li>",
        "<li>ao iniciar o Frenesi, todos os inimigos recebem imediatamente o primeiro acúmulo de +15% de dano e +10% de Penetração;</li>\n<li>a partir daí, recebem um novo acúmulo cumulativo a cada 30 ticks — equivalentes a 30 segundos lógicos;</li>",
        "9.16 — primeiro acúmulo imediato do Frenesi",
    )
    gdd = replace_once_or_confirm(
        gdd,
        "<li>o relógio nunca pausa: ataques, transformações, transições, invocações, retornos, efeitos e animações contam no tempo;</li>",
        "<li>o relógio lógico nunca pausa durante ataques, transformações, transições, reforços, retornos ou efeitos; animações não adicionam ticks nem interrompem a simulação;</li>",
        "9.16 — relógio lógico e animações",
    )

    gdd = replace_once_or_confirm(
        gdd,
        "<li>o VIP pode reproduzir visualmente o PvE em <strong>2×</strong>, apresentando cada tick em aproximadamente <strong>0,5 segundo</strong>;</li>\n<li>a aceleração é de apresentação e não modifica prontidão, chance de Power Move, targeting, dano, XP, drops ou resultado;</li>",
        "<li>em 1×, cada tick lógico é apresentado em aproximadamente <strong>1 segundo real</strong>;</li>\n<li>o VIP pode reproduzir visualmente o PvE em <strong>2×</strong>, apresentando cada tick lógico em aproximadamente <strong>0,5 segundo real</strong>;</li>\n<li>o número de ticks, as fórmulas, as decisões pseudoaleatórias autoritativas e o resultado final permanecem idênticos em 1× e 2×;</li>\n<li>a aceleração reduz apenas o tempo real de apresentação e não modifica prontidão, chance de Power Move, targeting, dano, XP ou drops;</li>",
        "8.18 — distinção entre tempo lógico e tempo real",
    )

    gdd = replace_once_or_confirm(
        gdd,
        "<li>1× é a apresentação padrão;</li>\n<li>2× é um recurso exclusivo do VIP e começa desativado;</li>\n<li>o jogador VIP pode alternar entre 1× e 2× durante a própria tentativa;</li>\n<li>em 2×, cada tick já autoritativo é apresentado visualmente em aproximadamente 0,5 segundo;</li>\n<li><code>timeScale</code> afeta somente animações, transições e apresentação;</li>\n<li>não altera prontidão, probabilidades, quantidade de ticks, XP, drops ou resultado calculado;</li>",
        "<li>1× é a apresentação padrão e exibe cada tick lógico em aproximadamente 1 segundo real;</li>\n<li>2× é um recurso exclusivo do VIP e começa desativado;</li>\n<li>o jogador VIP pode alternar entre 1× e 2× durante a própria tentativa;</li>\n<li>em 2×, cada tick lógico já autoritativo é apresentado em aproximadamente 0,5 segundo real;</li>\n<li><code>timeScale</code> altera somente a velocidade de animações, transições e apresentação de resultados já calculados;</li>\n<li>o número de ticks, as fórmulas, as decisões pseudoaleatórias autoritativas, a XP, os drops e o resultado final permanecem idênticos em 1× e 2×;</li>",
        "9.17 — velocidade visual sem alteração da simulação",
    )

    return gdd


def navigation_visible_texts(gdd: str, target: str) -> list[str]:
    expected_point = 8 if target == "battlefield-formation" else 9
    pattern = re.compile(
        rf'<(?:a|button)\b[^>]*(?:href|data-target|data-section)\s*=\s*["\']#?{re.escape(target)}["\'][^>]*>(?P<body>.*?)</(?:a|button)>',
        re.I | re.S,
    )
    return [
        impl.visible_text(match.group("body"))
        for match in pattern.finditer(gdd)
        if impl.top_level_point(match.group("body")) == expected_point
    ]


def validate(gdd: str, portal: str) -> None:
    """Validate the generated v16 by stable structure and all approved microadjustments."""
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
            "33% de seu peso passa para a próxima camada do mesmo corredor",
            "Exemplos objetivos de elegibilidade",
            "Chance natural efetiva = mínimo entre Chance natural e 35%",
            "Bônus de SOR = 14x ÷ (1 + x)",
            "Vigor possível vai de <strong>50 a 500</strong>",
            "persistem por toda a tentativa, inclusive entre ondas, derrota temporária e retorno",
            "após oito Basic Attacks consecutivos",
            "até três Power Moves consecutivos",
            "Tick lógico de um segundo",
            "1 segundo real",
            "0,5 segundo real",
            "8.19 Ausência de invocações para Buds e reforços roteirizados no PvE",
            "XP e drops normais dos inimigos definitivamente derrotados são preservados",
            "valor da SOR de referência da temporada",
            "O Ponto 8 está estruturalmente definido.",
        ],
        "Ponto 8",
    )
    require_all(
        pve,
        [
            "9.8 Formação canônica, posições e bloqueio durante a tentativa",
            "retorna com o HP completamente restaurado",
            "constrói o snapshot com esses Buds já presentes em suas posições originais",
            "XP e drops normais dos inimigos definitivamente derrotados são preservados",
            "9.15 Reforços roteirizados e bosses com múltiplas fases",
            "ao iniciar o Frenesi, todos os inimigos recebem imediatamente o primeiro acúmulo",
            "a cada 30 ticks — equivalentes a 30 segundos lógicos",
            "animações não adicionam ticks nem interrompem a simulação",
            "9.17 VIP e velocidade visual 1× / 2×",
            "1 segundo real",
            "0,5 segundo real",
            "240 ticks (4 minutos lógicos)",
            "360 ticks (6 minutos lógicos)",
            "480 ticks (8 minutos lógicos)",
            "600 ticks (10 minutos lógicos)",
            "O Ponto 9 está estruturalmente definido.",
        ],
        "Ponto 9",
    )

    forbidden = [
        "próxima camada viva do mesmo corredor",
        "HP e recursos de combate completamente restaurados",
        "a cada 30 segundos",
        "invocações, retornos, efeitos e animações contam no tempo",
    ]
    leftovers = [item for item in forbidden if item in gdd]
    if leftovers:
        raise AssertionError(f"Textos substituídos ainda presentes no GDD: {leftovers}")

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

    for target, expected_label in NAV_LABELS.items():
        labels = navigation_visible_texts(gdd, target)
        if not labels or not all(expected_label in label for label in labels):
            raise AssertionError(
                f"Texto de menu incorreto para #{target}: {labels}; esperado {expected_label!r}."
            )

    print(
        "Validated GDD v16 with approved review adjustments:",
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
        adjusted = apply_approved_microadjustments(gdd)
        validate(adjusted, portal)
        if adjusted != gdd:
            gdd_path.write_text(adjusted, encoding="utf-8")
            print("Applied approved review adjustments to existing GDD v16.")
        else:
            print("Point 8/9 consolidation and approved review adjustments already present and valid.")
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
    gdd = apply_approved_microadjustments(gdd)

    validate(gdd, portal)
    gdd_path.write_text(gdd, encoding="utf-8")
    portal_path.write_text(portal, encoding="utf-8")
    print(f"Consolidated Point 8, renumbered PvE to Point 9 and applied approved review adjustments in {gdd_path}.")


if __name__ == "__main__":
    main()
