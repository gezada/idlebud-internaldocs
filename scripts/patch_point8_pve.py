#!/usr/bin/env python3
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
html = path.read_text(encoding='utf-8')

if 'Game Design Document · v13' in html:
    html = html.replace('Game Design Document · v13', 'Game Design Document · v14', 1)
elif 'Game Design Document · v14' not in html:
    raise RuntimeError('Versão-base esperada (v13) não encontrada no HTML.')

section = '''<section id="pve-training">
<span class="tag blue">Carry, treinamento e PvE</span>
<span class="review-state rs-validation">Em validação</span>
<h2>8. Carry, Treinamento e Progressão PvE</h2>
<p>O PvE permite desenvolver Buds individualmente, repetir fases já vencidas e utilizar veteranos para carregar integrantes mais novos. A primeira leva deste ponto consolida elegibilidade, distribuição de Battle XP, Stamina de entrada e retorno após derrota. Farm XP permanece completamente separado.</p>
<div class="statement"><strong>O carry acelera o desenvolvimento de um Bud, mas nunca compartilha níveis com o elenco inteiro.</strong></div>

<h3>8.1 Quem recebe Battle XP</h3>
<ul>
<li>somente Buds efetivamente escalados na formação que iniciou a tentativa podem receber Battle XP;</li>
<li>Buds no inventário, na reserva ou fora da formação não recebem XP;</li>
<li>não existe XP global ou compartilhamento automático entre todo o elenco;</li>
<li>um Bud em treinamento precisa ocupar uma posição real na formação;</li>
<li>veteranos podem carregar Buds iniciantes em conteúdos PvE já acessíveis pela conta;</li>
<li>Farm XP não é carregada, transferida ou compartilhada: cada Bud precisa cultivar ou recuperar Stamina por conta própria.</li>
</ul>

<h3>8.2 XP fixa por inimigo</h3>
<p>Cada inimigo possui <strong>nível próprio</strong> e um <strong>valor fixo de Battle XP</strong>. Quando ele é derrotado, seu valor cria uma única pool de XP, distribuída entre os Buds elegíveis.</p>
<div class="formula">XP-base da fase = soma da XP fixa de todos os inimigos efetivamente derrotados</div>
<ul>
<li>a XP de um inimigo não é multiplicada pela quantidade de Buds;</li>
<li>como a composição de uma fase é fixa, uma conclusão equivalente gera sempre a mesma pool-base;</li>
<li>cada inimigo é resolvido individualmente, permitindo que a distribuição use o nível específico daquele inimigo.</li>
</ul>

<h3>8.3 Peso de XP por diferença de nível</h3>
<div class="formula">Diferença = Nível do Bud na entrada − Nível do inimigo</div>
<table>
<thead><tr><th>Diferença</th><th>Peso na distribuição</th></tr></thead>
<tbody>
<tr><td>De −5 até +5</td><td><strong>100%</strong></td></tr>
<tr><td>−6</td><td>110%</td></tr>
<tr><td>−7</td><td>120%</td></tr>
<tr><td>−8</td><td>130%</td></tr>
<tr><td>−9</td><td>140%</td></tr>
<tr><td>−10</td><td>150%</td></tr>
<tr><td>−11</td><td>160%</td></tr>
<tr><td>−12</td><td>170%</td></tr>
<tr><td>−13</td><td>180%</td></tr>
<tr><td>−14</td><td>190%</td></tr>
<tr><td>−15</td><td><strong>200%</strong></td></tr>
<tr><td>Menor que −15</td><td><strong>0%</strong></td></tr>
<tr><td>+6</td><td>90%</td></tr>
<tr><td>+7</td><td>80%</td></tr>
<tr><td>+8</td><td>70%</td></tr>
<tr><td>+9</td><td>60%</td></tr>
<tr><td>+10</td><td>50%</td></tr>
<tr><td>+11</td><td>40%</td></tr>
<tr><td>+12</td><td>30%</td></tr>
<tr><td>+13</td><td>20%</td></tr>
<tr><td>+14</td><td>10%</td></tr>
<tr><td>+15 ou mais</td><td><strong>0%</strong></td></tr>
</tbody>
</table>
<p>Buds moderadamente abaixo do inimigo recebem peso maior, enquanto Buds muito abaixo não podem saltar diretamente para conteúdo desproporcional. Buds muito acima podem realizar o carry, mas deixam de participar da XP.</p>

<h3>8.4 Distribuição dinâmica da pool</h3>
<div class="formula">XP do Bud = XP do inimigo × Peso do Bud ÷ Soma dos pesos positivos elegíveis</div>
<ul>
<li>a pool é dividida somente entre Buds com peso positivo;</li>
<li>a soma distribuída conserva exatamente a XP original do inimigo;</li>
<li>dois Buds de peso 100% e um Bud de peso 0% dividem a pool em 50%, 50% e 0%;</li>
<li>um Bud de peso 150% ao lado de outro com 100% recebe 60% da pool, enquanto o segundo recebe 40%;</li>
<li>caso nenhum participante possua peso positivo, a pool daquele inimigo não é distribuída.</li>
</ul>

<h3>8.5 Snapshot de entrada e level up no encerramento</h3>
<p>O nível usado para XP, status e regras da tentativa é congelado quando a fase começa. Ganhos acumulados durante a batalha não modificam o combate em andamento.</p>
<ul>
<li>nenhum Bud sobe de nível no meio da fase;</li>
<li>o servidor acumula a XP de cada inimigo, preservando valores fracionados internamente;</li>
<li>o arredondamento ocorre somente no encerramento válido da tentativa;</li>
<li>a XP efetivamente concedida é aplicada em lote ao final;</li>
<li>um Bud pode subir múltiplos níveis caso a XP seja suficiente;</li>
<li>XP excedente permanece no nível seguinte: se faltavam 200 e o Bud recebeu 300, ele termina um nível acima com 100 XP;</li>
<li>animações de level up, atualização de status e novos pontos são apresentados apenas depois da fase.</li>
</ul>

<h3>8.6 Repetição, treinamento e carry</h3>
<ul>
<li>fases já vencidas podem ser repetidas para treinamento;</li>
<li>cada repetição paga Stamina normalmente, já considerando o desconto individual de nível;</li>
<li>o veterano pode carregar Buds novos mesmo quando ele próprio já não recebe XP;</li>
<li>fases antigas podem se tornar farms quase gratuitos para Buds muito acima do nível;</li>
<li>isso é intencional porque o veterano não evolui por XP nesse conteúdo, embora materiais antigos continuem sujeitos às regras da fase;</li>
<li>carry não concede XP a Buds fora da formação, não compartilha níveis e não transfere Farm XP.</li>
</ul>

<h3>8.7 Desconto individual de Stamina no PvE</h3>
<p>A Stamina é calculada por Bud em relação ao nível recomendado da fase. Estar abaixo do conteúdo nunca aumenta o custo: o maior risco de derrota já é a desvantagem.</p>
<table>
<thead><tr><th>Diferença do Bud acima da fase</th><th>Stamina cobrada</th></tr></thead>
<tbody>
<tr><td>Até +5 ou qualquer nível abaixo</td><td><strong>100%</strong></td></tr>
<tr><td>+6</td><td>95%</td></tr>
<tr><td>+7</td><td>90%</td></tr>
<tr><td>+8</td><td>85%</td></tr>
<tr><td>+9</td><td>80%</td></tr>
<tr><td>+10</td><td>75%</td></tr>
<tr><td>+11</td><td>70%</td></tr>
<tr><td>+12</td><td>65%</td></tr>
<tr><td>+13</td><td>60%</td></tr>
<tr><td>+14</td><td>55%</td></tr>
<tr><td>+15</td><td>50%</td></tr>
<tr><td>+16</td><td>45%</td></tr>
<tr><td>+17</td><td>40%</td></tr>
<tr><td>+18</td><td>35%</td></tr>
<tr><td>+19</td><td>30%</td></tr>
<tr><td>+20</td><td>25%</td></tr>
<tr><td>+21</td><td>20%</td></tr>
<tr><td>+22</td><td>15%</td></tr>
<tr><td>+23 ou mais</td><td><strong>10%</strong></td></tr>
</tbody>
</table>
<ul>
<li>o custo final é arredondado para cima;</li>
<li>o custo mínimo é 1 Stamina;</li>
<li>dificuldade maior pode aumentar o peso de XP, mas nunca aumenta a Stamina;</li>
<li>uma fase de custo-base 10 pode chegar a 1 Stamina para um veterano muito acima.</li>
</ul>

<h3>8.8 Stamina paga na entrada</h3>
<p>A Stamina funciona como uma taxa individual e fixa de entrada na tentativa.</p>
<ul>
<li>o custo é calculado separadamente para cada Bud escalado;</li>
<li>todos precisam possuir Stamina suficiente antes do início;</li>
<li>o débito é atômico e acontece antes da criação válida da batalha;</li>
<li>depois de iniciada a tentativa, morrer, retornar, abandonar, perder ou completar apenas parte da fase não devolve Stamina;</li>
<li>um retorno após derrota não cria uma nova cobrança;</li>
<li>somente falha técnica do servidor ou execução invalidada pelo próprio sistema pode gerar reembolso.</li>
</ul>

<h3>8.9 Derrota temporária e retorno no PvE</h3>
<p>Chegar a zero de vida no PvE remove o Bud temporariamente do campo, mas não encerra sua participação na tentativa.</p>
<ol>
<li>o Bud sai do campo e inicia seu Tempo de Retorno;</li>
<li>continua elegível para receber sua parte da XP dos inimigos derrotados;</li>
<li>não paga Stamina adicional;</li>
<li>ao terminar a contagem, retorna à posição original da formação;</li>
<li>retorna com HP e recursos de combate completamente restaurados;</li>
<li>buffs, debuffs, controles e demais efeitos temporários anteriores são removidos.</li>
</ol>
<p>Um mesmo Bud pode ser derrotado e retornar novamente durante uma fase longa.</p>

<h3>8.10 Condição de derrota da fase</h3>
<div class="statement"><strong>A fase é perdida somente quando todos os Buds estiverem derrotados simultaneamente.</strong></div>
<p>Para impedir derrota no mesmo instante em que um retorno deveria acontecer, o servidor processa:</p>
<ol>
<li>retornos cujo tempo já terminou;</li>
<li>mortes e demais eventos daquele instante;</li>
<li>verificação de Buds vivos;</li>
<li>declaração de derrota apenas após essa ordem.</li>
</ol>

<h3>8.11 Tempo de Retorno</h3>
<ul>
<li>valor inicial de protótipo: <strong>60 segundos</strong>;</li>
<li>o valor poderá ser ajustado após testes de duração e dificuldade sem alterar a estrutura;</li>
<li>o Tempo de Retorno não é reduzido diretamente por VIT ou por outro Atributo de Batalha;</li>
<li>VIT já oferece HP, DEF e resistência a controle, portanto acumular retorno rápido tornaria o atributo dominante no PvE.</li>
</ul>

<h3>8.12 Passivas de Núcleo e Totem</h3>
<p>Núcleo Arcano e Totem podem possuir passivas específicas para reduzir o Tempo de Retorno.</p>
<div class="card good"><strong>Rebrota — exemplo conceitual</strong><p>Reduz o Tempo de Retorno do próprio Bud exclusivamente no PvE.</p></div>
<ul>
<li>a passiva pode possuir níveis e receber contribuição de Núcleo e Totem;</li>
<li>redução máxima acumulada: <strong>50%</strong>;</li>
<li>com base de 60 segundos, o retorno mínimo é <strong>30 segundos</strong>;</li>
<li>a redução não devolve Stamina e não interfere na participação de XP;</li>
<li>Rebrota e efeitos equivalentes ficam completamente desativados no PvP.</li>
</ul>

<h3>8.13 Fronteira entre PvE e PvP</h3>
<div class="grid">
<div class="card good"><h4>PvE</h4><p>O Bud derrotado entra em contagem e pode retornar completamente restaurado. A tentativa só termina quando todos estiverem derrotados juntos.</p></div>
<div class="card danger"><h4>PvP</h4><p>Bud derrotado permanece derrotado até o fim do confronto. Não existe retorno, Rebrota ou contagem regressiva.</p></div>
</div>
<p>XP, recompensas e demais regras específicas do PvP serão tratados posteriormente, sem misturar sua estrutura com esta definição de PvE.</p>

<div class="statement"><strong>Primeira leva do Ponto 8 registrada.</strong> Estas regras estão definidas; as bordas ainda não decididas serão tratadas em uma segunda leva antes de marcar o ponto inteiro como concluído.</div>
</section>'''

# Replace an existing single section whose H2 is Point 8, without crossing a section boundary.
point8_pattern = re.compile(
    r'<section\b[^>]*>(?:(?!</section>).)*?<h2>\s*8\..*?</section>',
    re.S,
)
html, replacements = point8_pattern.subn(section, html, count=1)

if replacements == 0:
    farm_match = re.search(r'<section id="farm-level">.*?</section>', html, re.S)
    if not farm_match:
        raise RuntimeError('Seção farm-level não encontrada para inserir o Ponto 8.')
    html = html[:farm_match.end()] + '\n' + section + html[farm_match.end():]

# Add consolidated decisions after the final Point 7 decision, avoiding duplicates.
if '<strong>XP por inimigo e carry PvE</strong>' not in html:
    marker = '<div class="decision"><div><strong>FP — Farming Power</strong><p>Poder de Cultivo resume produção, qualidade, velocidade, economia, adaptação, recuperação e Stamina sem considerar VIP ou efeitos temporários.</p></div><span class="status s-defined">Definido</span></div>'
    decisions = marker + '''
<div class="decision"><div><strong>XP por inimigo e carry PvE</strong><p>Cada inimigo cria uma pool fixa dividida dinamicamente entre os Buds elegíveis da formação conforme diferença de nível.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Level up no fim da fase</strong><p>Níveis e pesos ficam congelados durante a tentativa; XP, excedente e múltiplos level ups são processados somente no encerramento.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Stamina de entrada PvE</strong><p>Cada Bud paga antecipadamente; veteranos recebem desconto progressivo até 10%, com arredondamento para cima e mínimo de 1.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Retorno no PvE</strong><p>Bud derrotado continua na XP e retorna restaurado após 60 segundos; a fase só termina se todos estiverem mortos simultaneamente.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Rebrota e fronteira PvP</strong><p>Núcleo e Totem podem reduzir o retorno PvE até 50%; no PvP, morreu permanece derrotado até o fim.</p></div><span class="status s-defined">Definido</span></div>'''
    if marker in html:
        html = html.replace(marker, decisions, 1)
    else:
        raise RuntimeError('Marcador de decisões consolidadas do Ponto 7 não encontrado.')

required = [
    'Game Design Document · v14',
    '8. Carry, Treinamento e Progressão PvE',
    '8.1 Quem recebe Battle XP',
    '8.2 XP fixa por inimigo',
    '8.3 Peso de XP por diferença de nível',
    '8.4 Distribuição dinâmica da pool',
    '8.5 Snapshot de entrada e level up no encerramento',
    '8.6 Repetição, treinamento e carry',
    '8.7 Desconto individual de Stamina no PvE',
    '8.8 Stamina paga na entrada',
    '8.9 Derrota temporária e retorno no PvE',
    '8.10 Condição de derrota da fase',
    '8.11 Tempo de Retorno',
    '8.12 Passivas de Núcleo e Totem',
    '8.13 Fronteira entre PvE e PvP',
    'XP do Bud = XP do inimigo × Peso do Bud ÷ Soma dos pesos positivos elegíveis',
    '+23 ou mais</td><td><strong>10%',
    'custo mínimo é 1 Stamina',
    'débito é atômico',
    'continua elegível para receber sua parte da XP',
    'todos os Buds estiverem derrotados simultaneamente',
    '60 segundos',
    'redução máxima acumulada: <strong>50%</strong>',
    'retorno mínimo é <strong>30 segundos</strong>',
    'Primeira leva do Ponto 8 registrada.',
]
for item in required:
    assert item in html, f'Conteúdo obrigatório do Ponto 8 ausente: {item}'

point8_match = re.search(r'<section id="pve-training">.*?</section>', html, re.S)
assert point8_match, 'Seção pve-training não encontrada.'
point8 = point8_match.group(0)
assert point8.count('<h3>8.') == 13, 'Quantidade inesperada de subseções no Ponto 8.'
assert html.count('<h2>8.') == 1, 'Mais de uma seção numerada como Ponto 8.'
assert html.count('<section id="pve-training">') == 1, 'Seção pve-training duplicada.'

for premature in [
    'XP somente na vitória',
    'XP parcial na derrota',
    'Enrage',
    'inimigos invocados',
    'substituição manual durante a fase',
]:
    assert premature not in point8, f'Decisão ainda não aprovada apareceu no Ponto 8: {premature}'

path.write_text(html, encoding='utf-8')
print(f'Patched Point 8 first batch in {path} ({path.stat().st_size} bytes)')
