#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html as html_lib
import re
import sys

import patch_point8_battlefield_impl as impl

NAV_LABELS = {
    "battlefield-formation": "Campo de batalha e formação",
    "pve-training": "Carry, treinamento e PvE",
}

BATTLEFIELD_86 = r'''<h3>8.6 Exposição e penetração por posições vazias</h3>
<div class="statement"><strong>Quando uma posição-alvo está vazia ou derrotada, 33% de seu peso passa para a próxima camada do mesmo corredor. Caso essa camada também esteja vazia, o coeficiente de 33% é aplicado novamente antes de alcançar a camada seguinte. Os 67% restantes de cada passagem são redistribuídos proporcionalmente entre os demais alvos vivos já acessíveis.</strong></div>
<ul>
<li>se não houver ninguém vivo atrás daquela posição no mesmo corredor, todo o peso é redistribuído;</li>
<li>camadas quebradas sucessivas aplicam o coeficiente de 33% multiplicativamente;</li>
<li>pesos naturais e herdados se somam;</li>
<li>depois de toda penetração e redistribuição, o servidor soma os pesos vivos e normaliza o total para 100%;</li>
<li>nenhum peso é perdido enquanto existir ao menos um inimigo vivo;</li>
<li>quando resta somente um inimigo, ele se torna alvo com 100%, independentemente de sua posição.</li>
</ul>
<div class="formula">P1 com peso 70 e P1 inimiga vazia: 70 × 33% = 23,1 passam para P4; 46,9 são redistribuídos.</div>
<div class="formula">P1 e P4 vazias, P7 viva: 70 × 33% × 33% = 7,623 chegam a P7; 62,377 são redistribuídos.</div>
<p>Esse cálculo é refeito antes de cada Basic Attack com base no snapshot válido para aquela ação ou tick.</p>'''

BATTLEFIELD_87 = r'''<h3>8.7 Elegibilidade e escolha entre Basic Attack e Power Move</h3>
<p>Quando um Bud fica pronto, o servidor verifica primeiro se seu Power Move pode produzir uma ação válida naquele instante.</p>
<p>Um Power Move é elegível quando:</p>
<ul>
<li>existe ao menos um alvo válido;</li>
<li>suas condições próprias estão satisfeitas;</li>
<li>existe algum efeito aplicável e não completamente inútil;</li>
<li>o usuário não está sob um efeito que bloqueie Power Moves.</li>
</ul>
<div class="card"><strong>Exemplos objetivos de elegibilidade</strong><ul>
<li>um Power Move de cura fica inelegível quando todos os aliados válidos estão com HP cheio e volta a ser elegível quando ao menos um deles está ferido;</li>
<li>um Power Move que apenas remove debuffs fica inelegível quando não existe debuff removível em nenhum alvo válido;</li>
<li>um Power Move que causa dano e também aplica debuff permanece elegível enquanto houver alvo válido para o dano, mesmo quando esse alvo for imune ao efeito secundário;</li>
<li>um buff no próprio usuário pode ficar inelegível quando o movimento proíbe renovação ou acúmulo e o buff já está ativo;</li>
<li>um Power Move direcionado a uma posição específica vazia fica inelegível quando não declara fallback, exposição ou outra regra alternativa de targeting.</li>
</ul></div>
<p>Se estiver inelegível, o Bud executa obrigatoriamente um Basic Attack. Não há sorteio desperdiçado nem animação sem efeito. Esse Basic Attack conta normalmente para os contadores de sequência.</p>
<p>Se estiver elegível, o servidor decide primeiro entre Basic Attack e Power Move. Somente depois escolhe os alvos:</p>
<ul>
<li>Basic Attack sempre usa o targeting canônico;</li>
<li>Power Move pode usar o targeting canônico ou declarar uma regra própria;</li>
<li>regras próprias podem selecionar alvo único, múltiplos alvos, área, aliado, menor HP, posição, corredor ou todos os participantes elegíveis.</li>
</ul>'''

BATTLEFIELD_818 = r'''<h3>8.18 Tick lógico de um segundo e apresentação VIP em 2×</h3>
<ul>
<li>o tick lógico inicial é fixado em <strong>1 segundo</strong>;</li>
<li>o valor permanece configurável para testes e balanceamento futuros;</li>
<li>todos os participantes compartilham o mesmo relógio global;</li>
<li>em 1×, cada tick lógico é apresentado em aproximadamente <strong>1 segundo real</strong>;</li>
<li>o VIP pode reproduzir visualmente o PvE em <strong>2×</strong>, apresentando cada tick lógico em aproximadamente <strong>0,5 segundo real</strong>;</li>
<li>o número de ticks, as fórmulas, as decisões pseudoaleatórias autoritativas e o resultado final permanecem idênticos em 1× e 2×;</li>
<li>a aceleração reduz apenas o tempo real de apresentação e não modifica prontidão, chance de Power Move, targeting, dano, XP ou drops;</li>
<li>não concede vantagem em PvP;</li>
<li>o cliente nunca antecipa nem recalcula um resultado autoritativo;</li>
<li>animações podem ser agrupadas, aceleradas ou levemente encadeadas para legibilidade sem adicionar ticks, pausar ou bloquear a simulação lógica.</li>
</ul>'''

BATTLEFIELD_819 = r'''<h3>8.19 Ausência de invocações para Buds e reforços roteirizados no PvE</h3>
<div class="card danger"><strong>Buds jogáveis não possuem sistema de invocação ou reforço.</strong><p>Não entram novos Buds, não há substituição de aliados derrotados e uma posição vazia do jogador permanece vazia durante a batalha.</p></div>
<p>Monstros PvE podem receber reforços somente como comportamento roteirizado de uma fase, elite ou boss. Esses encontros serão desenhados manualmente com posições fixas reservadas, local de entrada, quantidade, condição e momento próprios. Isso não cria um sistema genérico disponível aos Buds.</p>'''

BATTLEFIELD_820 = r'''<h3>8.20 Eliminação simultânea completa no PvE</h3>
<ul>
<li>a batalha nunca termina no meio de um tick;</li>
<li>todas as ações já fixadas são concluídas;</li>
<li>o resultado é verificado somente após o fechamento completo;</li>
<li>para vencer uma fase PvE, ao menos um Bud precisa permanecer ativo;</li>
<li>se o último Bud e o último inimigo forem derrotados no mesmo tick, a tentativa é derrota do jogador;</li>
<li>XP e drops normais dos inimigos definitivamente derrotados são preservados conforme as regras do Ponto 9;</li>
<li>recompensas de conclusão não são concedidas e a fase não avança o mapa;</li>
<li>regras de empate do PvP serão definidas no ponto próprio de PvP.</li>
</ul>'''

BATTLEFIELD_821 = r'''<h3>8.21 Ordem autoritativa completa</h3>
<ol>
<li>avançar o relógio global e acumular prontidão;</li>
<li>abrir o snapshot do tick;</li>
<li>identificar unidades prontas e aptas;</li>
<li>verificar elegibilidade de Power Move;</li>
<li>decidir Basic Attack ou Power Move, incluindo correções de sequência;</li>
<li>montar alvos elegíveis, aplicar regras próprias do movimento, pesos e redirecionamentos;</li>
<li>fixar todas as ações e alvos;</li>
<li>resolver defesa e suporte imediatos;</li>
<li>resolver ataques, dano e demais efeitos;</li>
<li>consolidar escudos, cura, HP, controles, mortes e estados finais;</li>
<li>atualizar exposição, prontidão e contadores para o tick seguinte;</li>
<li>enviar ao cliente apenas os resultados autoritativos para apresentação.</li>
</ol>
<div class="statement"><strong>O Ponto 8 está estruturalmente definido.</strong> Números de dano, fórmulas exatas de ganho de prontidão, valor da SOR de referência da temporada, curva interna do pseudo-RNG e kits individuais serão calibrados e documentados sem alterar estas invariantes.</div>'''

PVE_911 = r'''<h3>9.11 Derrota temporária e retorno no PvE</h3>
<p>Chegar a zero de vida remove o Bud temporariamente do campo, sem encerrar sua participação.</p>
<ul>
<li>o Bud sai do tabuleiro e inicia seu Tempo de Retorno;</li>
<li>continua elegível para XP dos inimigos derrotados;</li>
<li>não paga Stamina adicional;</li>
<li>ao terminar a contagem, retorna à posição original;</li>
<li>retorna com o HP completamente restaurado;</li>
<li>buffs, debuffs, controles e demais efeitos temporários anteriores são removidos.</li>
</ul>
<p>O mesmo Bud pode morrer e retornar mais de uma vez durante uma tentativa longa.</p>'''

PVE_912 = r'''<h3>9.12 Condição de derrota e ordem de eventos</h3>
<div class="statement"><strong>Eliminação simultânea completa é derrota do jogador.</strong> Se o último Bud e o último inimigo forem derrotados no mesmo tick, todas as ações são concluídas. XP e drops normais dos inimigos definitivamente derrotados são preservados, mas a fase não é vencida, não avança o mapa e não concede recompensas de conclusão.</div>
<p>A fase é perdida somente quando todos os Buds estiverem derrotados simultaneamente ou quando o limite de tempo for atingido.</p>
<p>Em cada tick, o servidor processa nesta ordem:</p>
<ol>
<li>no início do tick, processa os retornos cujo contador já terminou;</li>
<li>constrói o snapshot com esses Buds já presentes em suas posições originais;</li>
<li>fixa e resolve as ações autorizadas para aquele snapshot;</li>
<li>consolida as mortes e demais mudanças no fechamento do tick;</li>
<li>verifica se existe ao menos um Bud ativo;</li>
<li>declara derrota somente depois dessa verificação.</li>
</ol>'''

PVE_916 = r'''<h3>9.16 Frenesi e limites de duração</h3>
<table>
<thead><tr><th>Categoria</th><th>Início máximo do Frenesi</th><th>Limite absoluto</th></tr></thead>
<tbody>
<tr><td>Fase normal</td><td><strong>240 ticks (4 minutos lógicos)</strong></td><td><strong>360 ticks (6 minutos lógicos)</strong></td></tr>
<tr><td>Fase elite</td><td><strong>360 ticks (6 minutos lógicos)</strong></td><td><strong>480 ticks (8 minutos lógicos)</strong></td></tr>
<tr><td>Boss</td><td><strong>480 ticks (8 minutos lógicos)</strong></td><td><strong>600 ticks (10 minutos lógicos)</strong></td></tr>
</tbody>
</table>
<ul>
<li>esses valores são tetos de lançamento; cada fase pode usar Frenesi e limite muito menores;</li>
<li>ao iniciar o Frenesi, todos os inimigos recebem imediatamente o primeiro acúmulo de +15% de dano e +10% de Penetração;</li>
<li>a partir daí, recebem um novo acúmulo cumulativo a cada 30 ticks — equivalentes a 30 segundos lógicos;</li>
<li>inimigos que surgirem depois herdam os acúmulos atuais;</li>
<li>no limite absoluto, o tick final é resolvido integralmente e, se ainda houver inimigos vivos após o fechamento, a tentativa termina como derrota por timeout;</li>
<li>XP e drops já conquistados são preservados; recompensas de conclusão não são entregues;</li>
<li>o relógio lógico nunca pausa durante ataques, transformações, transições, reforços, retornos ou efeitos; animações não adicionam ticks nem interrompem a simulação;</li>
<li>não existem cutscenes separadas; tudo acontece no tabuleiro com animações curtas, impactantes e padronizadas.</li>
</ul>'''

PVE_917 = r'''<h3>9.17 VIP e velocidade visual 1× / 2×</h3>
<ul>
<li>o PvE usa ticks lógicos de 1 segundo;</li>
<li>1× é a apresentação padrão e exibe cada tick lógico em aproximadamente 1 segundo real;</li>
<li>2× é um recurso exclusivo do VIP e começa desativado;</li>
<li>o jogador VIP pode alternar entre 1× e 2× durante a própria tentativa;</li>
<li>em 2×, cada tick lógico já autoritativo é apresentado em aproximadamente 0,5 segundo real;</li>
<li><code>timeScale</code> altera somente a velocidade de animações, transições e apresentação de resultados já calculados;</li>
<li>o número de ticks, as fórmulas, as decisões pseudoaleatórias autoritativas, a XP, os drops e o resultado final permanecem idênticos em 1× e 2×;</li>
<li>não se aplica como vantagem mecânica no PvP;</li>
<li>ao perder o benefício, a apresentação retorna imediatamente e suavemente para 1×.</li>
</ul>'''


def shift_later_sections(text: str) -> str:
    section_pattern = re.compile(r'<section\b(?P<attrs>[^>]*)>(?P<body>.*?)</section>', re.I | re.S)
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
        body, count = re.subn(rf'(<h2\b[^>]*>\s*){old}\.', rf'\g<1>{new}.', body, count=1, flags=re.I)
        if count != 1:
            raise RuntimeError(f"Não foi possível deslocar o cabeçalho do Ponto {old}.")
        body = re.sub(rf'(<h3\b[^>]*>\s*){old}\.(\d+)', rf'\g<1>{new}.\2', body, flags=re.I)
        body = body.replace(f'O Ponto {old} está estruturalmente definido.', f'O Ponto {new} está estruturalmente definido.')
        shifted.append((old, new))
        return f'<section{match.group("attrs")}>{body}</section>'

    result = section_pattern.sub(repl, text)
    if shifted:
        print("Shifted later GDD points:", ", ".join(f"{old}→{new}" for old, new in shifted))
    return result


def patch_navigation(text: str) -> str:
    clickable = re.compile(r"<(?P<tag>a|button)\b(?P<attrs>[^>]*)>(?P<body>.*?)</(?P=tag)>", re.I | re.S)

    def shift_existing(match: re.Match[str]) -> str:
        point = impl.top_level_point(match.group("body"))
        attrs = match.group("attrs")
        if point is None or point < 9 or not re.search(r"\b(?:href|data-target|data-section)\s*=", attrs, re.I):
            return match.group(0)
        body = impl.renumber_nav_body(match.group("body"), point, point + 1)
        return f'<{match.group("tag")}{attrs}>{body}</{match.group("tag")}>'

    return impl.patch_navigation(clickable.sub(shift_existing, text))


def replace_subsection(section: str, point: int, current: int, following: int | None, replacement: str) -> str:
    if following is None:
        pattern = re.compile(rf'<h3\b[^>]*>\s*{point}\.{current}\b.*?</h3>.*?(?=</section>)', re.I | re.S)
    else:
        pattern = re.compile(rf'<h3\b[^>]*>\s*{point}\.{current}\b.*?</h3>.*?(?=<h3\b[^>]*>\s*{point}\.{following}\b)', re.I | re.S)
    section, count = pattern.subn(replacement + "\n", section, count=1)
    if count != 1:
        raise RuntimeError(f"Subseção {point}.{current} ausente ou duplicada; transformação estrutural interrompida.")
    return section


def replace_section(text: str, section_id: str, transform) -> str:
    pattern = re.compile(rf'<section\b(?P<attrs>[^>]*\bid=["\']{re.escape(section_id)}["\'][^>]*)>(?P<body>.*?)</section>', re.I | re.S)
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"Esperada exatamente uma seção #{section_id}; encontradas {len(matches)}.")
    match = matches[0]
    rebuilt = f'<section{match.group("attrs")}>{transform(match.group("body"))}</section>'
    return text[:match.start()] + rebuilt + text[match.end():]


def rewrite_navigation_labels(gdd: str) -> str:
    clickable = re.compile(r'<(?P<tag>a|button)\b(?P<attrs>[^>]*)>(?P<body>.*?)</(?P=tag)>', re.I | re.S)
    candidates = ["Carry e formação de elenco", "Carry, Treinamento e Progressão PvE", "Carry, treinamento e PvE", "Carry e PvE", "Campo de Batalha, Formação e Posicionamento", "Campo de batalha e formação", "Campo de batalha"]
    found = {target: 0 for target in NAV_LABELS}

    def repl(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        body = match.group("body")
        for target, label in NAV_LABELS.items():
            if not re.search(rf'(?:href|data-target|data-section)\s*=\s*["\']#?{re.escape(target)}["\']', attrs, re.I):
                continue
            found[target] += 1
            if label not in impl.visible_text(body):
                for candidate in candidates:
                    body, count = re.subn(re.escape(candidate), label, body, count=1, flags=re.I)
                    if count:
                        break
            if label not in impl.visible_text(body):
                raise RuntimeError(f"Não foi possível definir o rótulo canônico de #{target}.")
            break
        return f'<{match.group("tag")}{attrs}>{body}</{match.group("tag")}>'

    gdd = clickable.sub(repl, gdd)
    missing = [target for target, count in found.items() if count == 0]
    if missing:
        raise RuntimeError(f"Navegação ausente para: {missing}")
    return gdd


def apply_canonical_review(gdd: str) -> str:
    def battlefield(body: str) -> str:
        body = replace_subsection(body, 8, 6, 7, BATTLEFIELD_86)
        body = replace_subsection(body, 8, 7, 8, BATTLEFIELD_87)
        body = replace_subsection(body, 8, 18, 19, BATTLEFIELD_818)
        body = replace_subsection(body, 8, 19, 20, BATTLEFIELD_819)
        body = replace_subsection(body, 8, 20, 21, BATTLEFIELD_820)
        body = replace_subsection(body, 8, 21, None, BATTLEFIELD_821)
        return body

    def pve(body: str) -> str:
        body = replace_subsection(body, 9, 11, 12, PVE_911)
        body = replace_subsection(body, 9, 12, 13, PVE_912)
        body = replace_subsection(body, 9, 16, 17, PVE_916)
        body = replace_subsection(body, 9, 17, 18, PVE_917)
        return body

    gdd = replace_section(gdd, "battlefield-formation", battlefield)
    gdd = replace_section(gdd, "pve-training", pve)
    return rewrite_navigation_labels(gdd)


def extract_section(gdd: str, section_id: str) -> str:
    matches = re.findall(rf'<section\b[^>]*\bid=["\']{re.escape(section_id)}["\'][^>]*>.*?</section>', gdd, re.I | re.S)
    if len(matches) != 1:
        raise AssertionError(f"Esperada exatamente uma seção #{section_id}; encontradas {len(matches)}.")
    return matches[0]


def visible_text(fragment: str) -> str:
    return " ".join(html_lib.unescape(re.sub(r"<[^>]+>", " ", fragment)).split())


def top_level_headings(gdd: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    for match in re.finditer(r'<section\b[^>]*>(?P<body>.*?)</section>', gdd, re.I | re.S):
        h2 = re.search(r'<h2\b[^>]*>(?P<body>.*?)</h2>', match.group("body"), re.I | re.S)
        if not h2:
            continue
        text = visible_text(h2.group("body"))
        number = re.match(r'(\d+)\.', text)
        if number:
            headings.append((int(number.group(1)), text))
    return headings


def validate(gdd: str, portal: str) -> None:
    if "Game Design Document · v16" not in gdd:
        raise AssertionError("Cabeçalho da versão v16 ausente.")
    if "Available · v16" not in portal:
        raise AssertionError("Portal não indica Available · v16.")
    if re.search(r'\bSpecial Moves?\b', gdd, re.I):
        raise AssertionError("Ainda existe ocorrência de Special Move.")

    battlefield = extract_section(gdd, "battlefield-formation")
    pve = extract_section(gdd, "pve-training")
    battle_numbers = re.findall(r'<h3\b[^>]*>\s*8\.(\d+)\b', battlefield, re.I)
    pve_numbers = re.findall(r'<h3\b[^>]*>\s*9\.(\d+)\b', pve, re.I)
    if battle_numbers != [str(n) for n in range(1, 22)]:
        raise AssertionError(f"Subseções do Ponto 8 inválidas: {battle_numbers}")
    if pve_numbers != [str(n) for n in range(1, 21)]:
        raise AssertionError(f"Subseções do Ponto 9 inválidas: {pve_numbers}")

    required = {
        "Ponto 8": ["33% de seu peso passa para a próxima camada do mesmo corredor", "Exemplos objetivos de elegibilidade", "persistem por toda a tentativa, inclusive entre ondas, derrota temporária e retorno", "1 segundo real", "0,5 segundo real", "8.19 Ausência de invocações para Buds e reforços roteirizados no PvE", "XP e drops normais dos inimigos definitivamente derrotados são preservados conforme as regras do Ponto 9", "valor da SOR de referência da temporada"],
        "Ponto 9": ["retorna com o HP completamente restaurado", "constrói o snapshot com esses Buds já presentes em suas posições originais", "recebem imediatamente o primeiro acúmulo", "a cada 30 ticks — equivalentes a 30 segundos lógicos", "animações não adicionam ticks nem interrompem a simulação", "o tick final é resolvido integralmente", "1 segundo real", "0,5 segundo real"],
    }
    for context, items in required.items():
        section = battlefield if context == "Ponto 8" else pve
        missing = [item for item in items if item not in section]
        if missing:
            raise AssertionError(f"Conteúdo canônico ausente em {context}: {missing}")

    for target, label in NAV_LABELS.items():
        pattern = re.compile(rf'<(?:a|button)\b[^>]*(?:href|data-target|data-section)\s*=\s*["\']#?{re.escape(target)}["\'][^>]*>(?P<body>.*?)</(?:a|button)>', re.I | re.S)
        matches = pattern.findall(gdd)
        if not matches or any(label not in visible_text(body) for body in matches):
            raise AssertionError(f"Rótulo de navegação incorreto para #{target}.")

    headings = top_level_headings(gdd)
    numbers = [number for number, _ in headings]
    if len(numbers) != len(set(numbers)):
        raise AssertionError(f"Numeração duplicada nos pontos: {headings}")
    if (8, "8. Campo de Batalha, Formação e Posicionamento") not in headings:
        raise AssertionError("Ponto 8 canônico ausente.")
    if (9, "9. Carry, Treinamento e Progressão PvE") not in headings:
        raise AssertionError("Ponto 9 canônico ausente.")

    print("Validated canonical GDD v16 review: Points 8 and 9 complete, deterministic and idempotent.")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: patch_point8_battlefield.py <gdd_html> <portal_html>")

    gdd_path = Path(sys.argv[1])
    portal_path = Path(sys.argv[2])
    gdd = gdd_path.read_text(encoding="utf-8")
    portal = portal_path.read_text(encoding="utf-8")

    already_v16 = "Game Design Document · v16" in gdd and 'id="battlefield-formation"' in gdd
    if not already_v16:
        if "Game Design Document · v15" not in gdd:
            raise RuntimeError("Versão-base esperada (v15) não encontrada.")

        gdd = re.sub(r"\bSpecial Moves\b", "Power Moves", gdd, flags=re.I)
        gdd = re.sub(r"\bSpecial Move\b", "Power Move", gdd, flags=re.I)
        gdd = shift_later_sections(gdd)

        pve_pattern = re.compile(r'<section\b[^>]*\bid=["\']pve-training["\'][^>]*>.*?</section>', re.I | re.S)
        match = pve_pattern.search(gdd)
        if not match:
            raise RuntimeError("Seção atual de Carry/PvE não encontrada.")
        pve = impl.renumber_and_align_pve(match.group(0))
        gdd = gdd[:match.start()] + impl.BATTLEFIELD_SECTION + "\n" + pve + gdd[match.end():]
        gdd = impl.insert_decisions(gdd)
        gdd = patch_navigation(gdd)
        gdd = gdd.replace("Game Design Document · v15", "Game Design Document · v16", 1)
        portal = portal.replace("Available · v15", "Available · v16", 1)

    gdd = apply_canonical_review(gdd)
    validate(gdd, portal)
    gdd_path.write_text(gdd, encoding="utf-8")
    portal_path.write_text(portal, encoding="utf-8")
    print(f"Canonical Point 8/9 consolidation written to {gdd_path}.")


if __name__ == "__main__":
    main()
