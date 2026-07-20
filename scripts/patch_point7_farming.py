#!/usr/bin/env python3
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
html = path.read_text(encoding='utf-8')

if 'Game Design Document · v11' in html:
    html = html.replace('Game Design Document · v11', 'Game Design Document · v12', 1)
elif 'Game Design Document · v12' not in html:
    raise RuntimeError('Versão-base esperada (v11) não encontrada no HTML.')

section = '''<section id="farm-level">
<span class="tag blue">Farm Level</span>
<span class="review-state rs-validation">Em validação</span>
<h2>7. Farm Level, Cultivo e Processos do Plot</h2>
<p>O Farm Level é individual, possui cap 100 na primeira temporada e avança por produção no plot e recuperação legítima de Stamina. Ele não compartilha experiência com o Battle Level. Raridade e Vigor não aumentam Farm Level, produção, qualidade, Stamina ou velocidade de cultivo.</p>
<div class="statement"><strong>Simples de operar, difícil de otimizar.</strong> O jogador vê tempo, quantidade esperada, qualidade, afinidade e ações claras; fórmulas e curvas permanecem ocultas em detalhes avançados.</div>

<h3>7.1 Pontos, experiência e identidade de Cultivo</h3>
<ul>
<li>todo Bud nasce no <strong>Farm Level 1</strong>;</li>
<li>cada level concede um Ponto de Cultivo, totalizando <strong>100 pontos distribuíveis</strong> no cap 100;</li>
<li>cada Bud nasce também com <strong>24 Pontos Inatos de Cultivo</strong>, distribuídos entre REC, COL, QLD, EFI, ADA e SUS;</li>
<li>cada atributo recebe entre 1 e 10 pontos inatos, mantendo total fixo de 24;</li>
<li>Pontos Inatos são permanentes, visíveis e não são devolvidos por reset;</li>
<li>Farm XP vem de produção no plot e, em ritmo menor, de recuperação legítima de Stamina;</li>
<li>recuperação precisa de validação por ciclo para impedir geração artificial de Farm XP;</li>
<li>cultivar não consome Stamina.</li>
</ul>

<h3>7.2 Função dos seis Atributos de Cultivo</h3>
<div class="grid three">
<div class="card attribute"><div class="abbr">REC</div><div><h4>Recuperação</h4><p>Aumenta a velocidade de recuperação da Stamina utilizada em batalha.</p></div></div>
<div class="card attribute"><div class="abbr">COL</div><div><h4>Colheita</h4><p>Aumenta a quantidade produzida por Ciclo de Cultivo, sem alterar qualidade, velocidade ou pool de itens.</p></div></div>
<div class="card attribute"><div class="abbr">QLD</div><div><h4>Qualidade</h4><p>Aumenta a chance de resultados de qualidade superior dentro da pool válida do Plano de Cultivo.</p></div></div>
<div class="card attribute"><div class="abbr">EFI</div><div><h4>Eficiência</h4><p>Reduz o tempo dos ciclos e o consumo ou desperdício de insumos quando aplicável.</p></div></div>
<div class="card attribute"><div class="abbr">ADA</div><div><h4>Adaptação</h4><p>Reduz penalidades de incompatibilidade e amplifica de forma controlada as bonificações positivas de afinidade do plot.</p></div></div>
<div class="card attribute"><div class="abbr">SUS</div><div><h4>Sustentação</h4><p>Aumenta a Stamina máxima e a autonomia de batalha antes do retorno ao plot.</p></div></div>
</div>
<ul>
<li>ADA atua de forma assimétrica: corrige penalidades com mais força do que amplia bônus positivos;</li>
<li>ADA nunca transforma uma penalidade em bônus nem deve duplicar novamente uma afinidade já muito forte;</li>
<li>SUS não aumenta duração de cultivo, intervalo de cuidados ou limite de progresso offline;</li>
<li>REC não recupera HP, Mana ou cooldowns: esses recursos reiniciam após cada batalha;</li>
<li>doenças, ferimentos persistentes e condições negativas fora do combate não fazem parte do escopo atual.</li>
</ul>

<h3>7.3 Ficha de Cultivo e influência dos attachments</h3>
<p>Cada Bud possui duas leituras separadas: uma <strong>Ficha de Batalha</strong> e uma <strong>Ficha de Cultivo</strong>. Os Atributos de Batalha alimentam apenas a ficha de combate; os Atributos de Cultivo alimentam apenas a ficha de farm.</p>
<p>Núcleo Arcano e Totem podem fornecer modificadores numéricos para ambas as fichas. No Alpha, suas <strong>passivas condicionais</strong> atuam somente em batalha; o cultivo utiliza bônus claros e previsíveis.</p>
<div class="card warn"><strong>Não existem equipamentos adicionais.</strong><p>Núcleo Arcano e Totem continuam sendo os únicos attachments do Bud.</p></div>
<table>
<thead><tr><th>Status derivados da Ficha de Cultivo</th><th>Leitura</th></tr></thead>
<tbody>
<tr><td><strong>Stamina Máxima</strong></td><td>Reserva disponível para atividades de batalha.</td></tr>
<tr><td><strong>Recuperação de Stamina</strong></td><td>Stamina recuperada por unidade de tempo no plot.</td></tr>
<tr><td><strong>Bônus de Colheita</strong></td><td>Quantidade adicional esperada por ciclo.</td></tr>
<tr><td><strong>Chance de Qualidade</strong></td><td>Probabilidade de resultados superiores dentro da pool válida.</td></tr>
<tr><td><strong>Velocidade de Cultivo</strong></td><td>Redução efetiva do tempo do ciclo.</td></tr>
<tr><td><strong>Economia de Insumos</strong></td><td>Redução prevista de consumo ou desperdício.</td></tr>
<tr><td><strong>Adaptação</strong></td><td>Mitigação de penalidades e amplificação controlada de bônus do plot.</td></tr>
<tr><td><strong>Autonomia Estimada</strong></td><td>Quantidade aproximada de atividades de batalha antes da recuperação.</td></tr>
</tbody>
</table>
<p>Ao selecionar um plot e um Plano de Cultivo, a interface também apresenta quantidade esperada, tempo efetivo, pool possível e demais resultados contextuais.</p>

<h3>7.4 Três Processos do Plot</h3>
<p>Cada Plot comporta apenas <strong>um processo ativo por vez</strong>:</p>
<div class="grid three">
<div class="card"><h4>Germinação</h4><p>Transforma uma semente em um novo Bud.</p></div>
<div class="card"><h4>Ciclo de Cultivo</h4><p>Produz materiais por meio de um Bud já nascido.</p></div>
<div class="card"><h4>Recuperação de Stamina</h4><p>Prepara o Bud para retornar às batalhas.</p></div>
</div>
<ul>
<li>um Bud não pode batalhar, cultivar ou recuperar-se simultaneamente;</li>
<li>cada processo utiliza três etapas, com dois checkpoints de cuidado;</li>
<li>quando um checkpoint termina, o processo aguarda interação sem destruir ou perder o resultado;</li>
<li>a ação básica de cuidado é a rega; fertilizantes são opcionais.</li>
</ul>

<h3>7.5 Germinação em três etapas</h3>
<div class="formula">Plantar semente → Germinação 1/3: Enraizamento → Germinação 2/3: Bloom → Germinação 3/3: Nascimento e Revelação do Bud</div>
<table>
<thead><tr><th>Etapa</th><th>Função</th></tr></thead>
<tbody>
<tr><td><strong>Enraizamento — 1/3</strong></td><td>Inicia o desenvolvimento da semente e termina no primeiro checkpoint de cuidado.</td></tr>
<tr><td><strong>Bloom — 2/3</strong></td><td>Etapa intermediária da Germinação; termina no segundo checkpoint de cuidado e pode receber fertilizantes direcionados.</td></tr>
<tr><td><strong>Nascimento e Revelação — 3/3</strong></td><td>Somente aqui o servidor calcula, cria e registra o novo Bud.</td></tr>
</tbody>
</table>
<p>No Nascimento e Revelação são definidos espécie, raridade, Vigor, Pontos Inatos de Batalha, Pontos Inatos de Cultivo e demais valores individuais. Nada fica pré-gerado ou escondido dentro da semente.</p>
<p>Regas e fertilizantes alteram probabilidades, mas não garantem resultados específicos. O cálculo final é autoritativo, atômico, idempotente e auditável pelo servidor.</p>

<h3>7.6 Plano e Ciclo de Cultivo</h3>
<p>Depois de nascer, o Bud pode ser alocado em um Plot e executar um <strong>Plano de Cultivo</strong>. Cada execução completa desse plano é um <strong>Ciclo de Cultivo</strong>.</p>
<p>O Plano de Cultivo define:</p>
<ul>
<li>duração-base e três etapas do ciclo;</li>
<li>pool de materiais possível;</li>
<li>quantidade-base e qualidade-base;</li>
<li>insumos opcionais;</li>
<li>requisitos de região, mapa ou progresso PvE.</li>
</ul>
<p>A pool pode combinar materiais comuns, materiais exclusivos do elemento do Bud e materiais regionais liberados pelo avanço no PvE. O jogador escolhe entre os Planos de Cultivo já desbloqueados.</p>
<div class="formula">Iniciar cultivo → Etapa 1 → Cuidado → Etapa 2 → Cuidado → Etapa 3 → Colheita</div>
<ul>
<li>Ciclo de Cultivo não consome Stamina;</li>
<li>o jogador gratuito coleta e reinicia manualmente;</li>
<li>o VIP pode coletar e repetir automaticamente o mesmo Plano de Cultivo.</li>
</ul>

<h3>7.7 Stamina e Recuperação</h3>
<ul>
<li>somente batalhas consomem Stamina;</li>
<li>cada atividade PvE ou PvP possui custo previsível; bosses e conteúdos mais exigentes podem custar mais;</li>
<li>Stamina não depende de dano causado, dano recebido, cura ou duração da luta;</li>
<li>um Bud não inicia uma atividade sem Stamina suficiente;</li>
<li>HP, Mana e cooldowns reiniciam após cada batalha;</li>
<li>SUS aumenta a Stamina máxima;</li>
<li>REC reduz o tempo da recuperação;</li>
<li>Recuperação não consome Stamina e utiliza as mesmas três etapas e dois cuidados do Processo de Plot.</li>
</ul>

<h3>7.8 Operação manual e automação VIP</h3>
<div class="grid">
<div class="card"><h4>Jogador gratuito</h4><ul><li>inicia cada processo;</li><li>realiza os dois cuidados;</li><li>conclui nascimento, colheita ou recuperação;</li><li>inicia manualmente o próximo processo.</li></ul></div>
<div class="card good"><h4>Jogador VIP</h4><ul><li>cuidados automáticos;</li><li>nascimento e revelação automáticos, quando habilitados;</li><li>colheita automática;</li><li>repetição automática do Plano de Cultivo;</li><li>conclusão automática da recuperação;</li><li>uso automático de fertilizantes previamente autorizados;</li><li>pequena aceleração controlada dos processos, com percentual a definir.</li></ul></div>
</div>
<p>O uso automático de fertilizantes nunca vem ativado por padrão e depende de autorização específica e estoque disponível.</p>

<h3>7.9 Rotação automática Batalha → Recuperação → Batalha</h3>
<p>O VIP pode reservar um Plot para um Bud e automatizar sua rotação operacional:</p>
<div class="formula">Batalhar → Stamina insuficiente → Finalizar a atividade atual → Retornar ao Plot reservado → Recuperar → Voltar à atividade compatível</div>
<ul>
<li>o Plot precisa estar reservado, livre e vinculado ao Bud;</li>
<li>um Plot reservado não pode germinar, cultivar ou receber outro Bud;</li>
<li>o Bud não abandona uma batalha em andamento;</li>
<li>se o Plot estiver indisponível, a automação pausa;</li>
<li>o jogador pode desativar o retorno e deixar o Bud no Plot após a recuperação;</li>
<li>depois de recuperar, o Bud volta à batalha; ele não inicia Bloom nem Ciclo de Cultivo automaticamente, salvo configuração futura específica.</li>
</ul>
<p>A interface deve resumir essa lógica em poucas escolhas: recuperação automática, Plot reservado e retorno à atividade.</p>

<h3>7.10 Fertilizantes</h3>
<p>Fertilizantes são consumíveis opcionais aplicáveis nos checkpoints de cuidado. A rega básica sempre permite continuar o processo sem consumir fertilizante.</p>
<p>Tipos, raridades, receitas, valores e disponibilidade serão definidos posteriormente. Exemplos conceituais:</p>
<ul>
<li><strong>Fertilizante Simples:</strong> pequeno aumento geral distribuído entre os efeitos válidos do processo;</li>
<li><strong>Fertilizante de Raridade:</strong> utilizado durante o Bloom para aumentar apenas a probabilidade de raridades superiores, sem bônus nos demais resultados;</li>
<li><strong>Fertilizante de Vigor:</strong> desloca a distribuição probabilística de Vigor no nascimento, sem garantir um valor específico;</li>
<li><strong>Fertilizante de Colheita:</strong> aumenta quantidade no Ciclo de Cultivo;</li>
<li><strong>Fertilizante de Qualidade:</strong> melhora resultados de qualidade dentro da pool válida;</li>
<li><strong>Fertilizante de Recuperação:</strong> reduz o tempo da Recuperação de Stamina.</li>
</ul>
<div class="card blue"><strong>Quantidade ainda não definida</strong><p>A quantidade máxima de Fertilizantes permitida por processo, por etapa ou por checkpoint será decidida durante o balanceamento. O sistema deve suportar essa configuração sem assumir previamente um único uso.</p></div>

<h3>7.11 Princípio de interface</h3>
<p>O jogador não precisa compreender raízes, curvas ou fórmulas para utilizar o sistema. A tela principal apresenta apenas:</p>
<ul>
<li>processo selecionado;</li>
<li>tempo restante;</li>
<li>quantidade e qualidade esperadas;</li>
<li>afinidade do Plot;</li>
<li>próximo cuidado necessário;</li>
<li>botão principal de ação.</li>
</ul>
<p>Detalhes avançados, fontes dos bônus e probabilidades ficam em tooltips ou expansão da ficha.</p>
<div class="statement"><strong>Fácil de entender, difícil de masterizar.</strong> A profundidade pertence às decisões de alocação, atributos, afinidades, fertilizantes e automações — não à quantidade de botões.</div>

<h3>7.12 O que ainda permanece em validação</h3>
<ul>
<li>Matriz de Afinidade de Cultivo e multiplicadores de cada relação elemental;</li>
<li>fórmula de ADA para mitigação de penalidades e amplificação controlada de bônus;</li>
<li>fórmulas, caps e retornos decrescentes de COL, QLD, EFI, REC e SUS;</li>
<li>tipos, quantidade e progressão dos Planos de Cultivo;</li>
<li>custos de Stamina por atividade e tempos-base de recuperação;</li>
<li>quantidade permitida de Fertilizantes, catálogo, receitas, raridades e valores;</li>
<li>percentual de aceleração VIP;</li>
<li>nome e fórmula do indicador geral de cultivo, com <strong>FP — Farm Power / Poder de Cultivo</strong> como proposta em validação.</li>
</ul>
</section>'''

html, replacements = re.subn(r'<section id="farm-level">.*?</section>', section, html, count=1, flags=re.S)
if replacements != 1:
    raise RuntimeError(f'Esperava substituir uma seção farm-level; substituições realizadas: {replacements}')

marker = '<div class="decision"><div><strong>CP e Poder de Confronto</strong><p>CP resume a ficha permanente; Poder de Confronto adiciona matchup, elementos, posição e composição para estimar a vitória.</p></div><span class="status s-defined">Definido</span></div>'
addition = marker + '''
<div class="decision"><div><strong>Atributos de Cultivo</strong><p>REC, COL, QLD, EFI, ADA e SUS possuem funções separadas; raridade e Vigor não interferem no Farm.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Fichas separadas</strong><p>Cada Bud possui Ficha de Batalha e Ficha de Cultivo; Núcleo e Totem podem modificar ambas, mas suas passivas condicionais ficam restritas à batalha no Alpha.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Processos do Plot</strong><p>Germinação, Ciclo de Cultivo e Recuperação utilizam três etapas, dois cuidados e apenas um processo ativo por Plot.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Etapas da Germinação</strong><p>Enraizamento 1/3, Bloom 2/3 e Nascimento e Revelação 3/3; o Bud é calculado somente na etapa final.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Stamina</strong><p>Somente batalhas consomem Stamina; SUS aumenta a reserva, REC acelera a recuperação e cultivo não gera custo de Stamina.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Automação VIP do Plot</strong><p>VIP pode automatizar cuidados, conclusão, repetição e a rotação batalha–recuperação–batalha mediante Plot reservado.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Fertilizantes</strong><p>Consumíveis opcionais aplicáveis nos cuidados; catálogo e quantidade por processo ainda serão balanceados.</p></div><span class="status s-rule">Estrutura definida</span></div>'''
if marker in html:
    html = html.replace(marker, addition, 1)
else:
    raise RuntimeError('Marcador de decisões consolidadas do Ponto 6 não encontrado.')

html = re.sub(
    r'<li><strong>Germinação:</strong>.*?</li>',
    '<li><strong>Germinação e Fertilizantes:</strong> tempos-base, quantidade permitida por etapa ou processo, catálogo, receitas, raridades, valores e impacto probabilístico de cada Fertilizante.</li>',
    html,
    count=1,
    flags=re.S,
)
html = re.sub(
    r'<li><strong>Farm XP:</strong>.*?</li>',
    '<li><strong>Farm XP e Stamina:</strong> curvas, validação por ciclo, custos por atividade, tempos de recuperação, proteções contra abuso e percentual de aceleração VIP.</li>',
    html,
    count=1,
    flags=re.S,
)
html = re.sub(
    r'<li><strong>Plots:</strong>.*?</li>',
    '<li><strong>Plots e Cultivo:</strong> Matriz de Afinidade de Cultivo, multiplicadores, fórmula de ADA, Planos de Cultivo, pools, tempos, caps, retornos decrescentes e indicador FP.</li>',
    html,
    count=1,
    flags=re.S,
)

required = [
    'Game Design Document · v12',
    '7. Farm Level, Cultivo e Processos do Plot',
    '24 Pontos Inatos de Cultivo',
    '7.5 Germinação em três etapas',
    'Germinação 1/3: Enraizamento',
    'Germinação 2/3: Bloom',
    'Germinação 3/3: Nascimento e Revelação do Bud',
    'cultivar não consome Stamina',
    'Não existem equipamentos adicionais',
    '7.9 Rotação automática Batalha → Recuperação → Batalha',
    'Fertilizante de Raridade',
    'Fertilizante de Vigor',
    'Quantidade ainda não definida',
    'Fácil de entender, difícil de masterizar.',
]
for item in required:
    assert item in html, f'Conteúdo obrigatório ausente: {item}'

farm_match = re.search(r'<section id="farm-level">.*?</section>', html, re.S)
assert farm_match, 'Seção farm-level não encontrada após substituição.'
farm = farm_match.group(0)
for stale in [
    'vida, energia, fadiga e condições negativas',
    '7.1 Arquétipos possíveis',
    'Colhedora',
    'Operária',
    'Curadora',
    'Nômade',
    'Experimental',
    'Sprays de Cuidado',
    'cultivo consome Stamina',
]:
    assert stale not in farm, f'Texto obsoleto no Ponto 7: {stale}'

assert farm.count('<h3>7.') == 12, 'Quantidade inesperada de subseções no Ponto 7.'
assert html.count('<section id="farm-level">') == 1, 'Seção farm-level duplicada.'

path.write_text(html, encoding='utf-8')
print(f'Patched {path} ({path.stat().st_size} bytes)')
