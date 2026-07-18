#!/usr/bin/env python3
from pathlib import Path
import sys

path = Path(sys.argv[1])
html = path.read_text(encoding="utf-8")

old_points = '<li>o backend registra o resultado de forma autoritativa e auditável.</li>\n</ul>\n<div class="statement"><strong>Exemplo:</strong>'
new_points = '<li>o backend registra o resultado de forma autoritativa e auditável.</li>\n<li>no cap, cada grupo soma <strong>124 pontos-base</strong>: 24 inatos e 100 distribuíveis.</li>\n</ul>\n<div class="statement"><strong>Exemplo:</strong>'

old_odds = 'Essa vantagem é relevante, mas não produz sozinha o extremo competitivo de 96% contra 4%.</p>'
new_odds = 'Essa vantagem é relevante, mas não produz sozinha o extremo competitivo de 96% contra 4%. Como alvo inicial de balanceamento, o extremo de raridade e Vigor com todo o restante idêntico deve ficar próximo de <strong>59% contra 41%</strong>; o simulador definirá a curva final.</p>'

if old_points not in html:
    raise RuntimeError('Ponto de inserção dos 124 pontos-base não encontrado.')
if old_odds not in html:
    raise RuntimeError('Ponto de inserção do alvo 59% contra 41% não encontrado.')

html = html.replace(old_points, new_points, 1)
html = html.replace(old_odds, new_odds, 1)

assert '124 pontos-base' in html
assert '59% contra 41%' in html
path.write_text(html, encoding='utf-8')
print(f'Finalized {path} ({path.stat().st_size} bytes)')
