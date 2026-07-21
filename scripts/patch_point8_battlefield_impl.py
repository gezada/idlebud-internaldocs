#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html as html_lib
import re
import sys


BATTLEFIELD_SECTION = r'''<section id="battlefield-formation">
<span class="tag blue">Campo de batalha, formação e resolução</span>
<span class="review-state rs-defined">Definido</span>
<h2>8. Campo de Batalha, Formação e Posicionamento</h2>
<p>Este ponto define a geometria canônica do combate, o targeting dos Basic Attacks, a ativação dos Power Moves, a prontidão baseada em AGI e a resolução simultânea por ticks. As mesmas regras lógicas sustentam PvE e PvP, salvo quando um encontro ou Power Move declarar uma exceção explícita.</p>
<div class="statement"><strong>O servidor decide primeiro; o cliente apenas apresenta.</strong> Posições, alvos, probabilidades, resultados e estados finais são autoritativos e não dependem da duração das animações.</div>

<h3>8.1 Campo canônico e identidade das sete posições</h3>
<p>Cada equipe possui até sete posições lógicas próprias, organizadas da frente para a retaguarda na formação fixa <strong>1–2–1–2–1</strong>.</p>
<div class="formula">Frente → P1 → P2/P3 → P4 → P5/P6 → P7 → Retaguarda</div>
<table>
<thead><tr><th>Posição</th><th>Identidade lógica</th></tr></thead>
<tbody>
<tr><td><strong>P1</strong></td><td>posição frontal central;</td></tr>
<tr><td><strong>P2 e P3</strong></td><td>alas da segunda camada;</td></tr>
<tr><td><strong>P4</strong></td><td>posição central do campo;</td></tr>
<tr><td><strong>P5 e P6</strong></td><td>alas da retaguarda;</td></tr>
<tr><td><strong>P7</strong></td><td>posição mais profunda.</td></tr>
</tbody>
</table>
<ul>
<li>cada equipe possui sua própria P1 até P7;</li>
<li>no desktop, as duas formações podem aparecer horizontalmente espelhadas;</li>
<li>no mobile, o inimigo pode aparecer acima e o jogador abaixo;</li>
<li>rotação, espelhamento ou adaptação visual nunca alteram a identidade lógica das posições;</li>
<li>todas as regras usam os números canônicos, independentemente da orientação da câmera.</li>
</ul>

<h3>8.2 Corredores canônicos</h3>
<table>
<thead><tr><th>Corredor</th><th>Sequência da frente para trás</th></tr></thead>
<tbody>
<tr><td><strong>Superior</strong></td><td>P2 → P5</td></tr>
<tr><td><strong>Central</strong></td><td>P1 → P4 → P7</td></tr>
<tr><td><strong>Inferior</strong></td><td>P3 → P6</td></tr>
</tbody>
</table>
<p>Corredores são usados por exposição, penetração de targeting, ataques em linha e efeitos que declarem relação de profundidade. Eles não representam distância física em metros.</p>

<h3>8.3 Ocupação livre, posições vazias e ausência de movimento</h3>
<ul>
<li>uma equipe pode iniciar com apenas <strong>um Bud</strong> ou com qualquer quantidade até sete;</li>
<li>o jogador pode ocupar livremente qualquer combinação das sete posições;</li>
<li>uma posição pode começar vazia e permanece logicamente vazia;</li>
<li>para targeting e exposição, uma posição vazia é tratada como uma posição cujo Bud já foi derrotado;</li>
<li>não existe reposicionamento automático quando uma posição fica vazia;</li>
<li>cada Bud permanece na mesma posição lógica durante toda a batalha;</li>
<li>não há alcance físico, deslocamento lógico, pathfinding, colisão, velocidade de movimento, tempo de viagem ou bloqueio corporal;</li>
<li>conceitos como frente, centro e retaguarda são regras de proteção e targeting, não medidas espaciais;</li>
<li>animações podem avançar, saltar, disparar projéteis ou atravessar o campo, mas o Bud retorna visualmente e nunca muda de slot lógico;</li>
<li>diferenças de duração ou estilo de animação não concedem qualquer vantagem mecânica.</li>
</ul>

<h3>8.4 Adjacência canônica</h3>
<p>Adjacência e corredor são geometrias diferentes. A adjacência serve para efeitos como “alvo e vizinhos”, enquanto o corredor serve para profundidade e ataques em linha.</p>
<table>
<thead><tr><th>Posição</th><th>Vizinhos diretamente adjacentes</th></tr></thead>
<tbody>
<tr><td><strong>P1</strong></td><td>P2 e P3</td></tr>
<tr><td><strong>P2</strong></td><td>P1, P4 e P5</td></tr>
<tr><td><strong>P3</strong></td><td>P1, P4 e P6</td></tr>
<tr><td><strong>P4</strong></td><td>P2, P3, P5 e P6</td></tr>
<tr><td><strong>P5</strong></td><td>P2, P4 e P7</td></tr>
<tr><td><strong>P6</strong></td><td>P3, P4 e P7</td></tr>
<tr><td><strong>P7</strong></td><td>P5 e P6</td></tr>
</tbody>
</table>
<ul>
<li>uma posição vazia continua existindo geometricamente, mas não recebe efeitos;</li>
<li>posições vazias não criam novas conexões entre slots que antes não eram adjacentes;</li>
<li>um efeito em P2 que atinja adjacentes alcança P1, P4 e P5, quando ocupadas;</li>
<li>um efeito usado por P4 sobre aliados adjacentes alcança P2, P3, P5 e P6, quando ocupadas.</li>
</ul>

<h3>8.5 Targeting canônico dos Basic Attacks</h3>
<p>Cada posição atacante possui uma tabela fixa de pesos contra as posições inimigas. Antes de cada Basic Attack, o servidor recalcula quais alvos estão vivos, aplica exposição e normaliza os pesos válidos para exatamente 100%.</p>
<table>
<thead><tr><th>Posição atacante</th><th>Pesos canônicos iniciais</th></tr></thead>
<tbody>
<tr><td><strong>P1</strong></td><td>70% → P1; 15% → P2; 15% → P3</td></tr>
<tr><td><strong>P2</strong></td><td>50% → P1; 40% → P2; 10% → P3</td></tr>
<tr><td><strong>P3</strong></td><td>50% → P1; 40% → P3; 10% → P2</td></tr>
<tr><td><strong>P4</strong></td><td>40% → P1; 20% → P2; 20% → P3; 20% → P4</td></tr>
<tr><td><strong>P5</strong></td><td>35% → P2; 25% → P1; 10% → P3; 15% → P4; 15% → P5</td></tr>
<tr><td><strong>P6</strong></td><td>35% → P3; 25% → P1; 10% → P2; 15% → P4; 15% → P6</td></tr>
<tr><td><strong>P7</strong></td><td>25% → P1; 15% → P2; 15% → P3; 20% → P4; 10% → P5; 10% → P6; 5% → P7</td></tr>
</tbody>
</table>
<ul>
<li>posições vazias ou derrotadas nunca são o alvo final;</li>
<li>Basic Attacks sempre usam esta matriz, salvo uma exceção futura explicitamente registrada no GDD;</li>
<li>inimigos PvE também ocupam P1–P7 e usam as mesmas regras, salvo exceção declarada pelo encontro ou pelo movimento;</li>
<li>designers de fase podem distribuir inimigos, espaços vazios, elites e bosses nas posições canônicas para criar padrões distintos de exposição.</li>
</ul>

<h3>8.6 Exposição e penetração por posições vazias</h3>
<div class="statement"><strong>Quando uma posição-alvo está vazia ou derrotada, 33% do peso dela atravessa para a próxima camada viva do mesmo corredor. Os 67% restantes são redistribuídos proporcionalmente entre os demais alvos vivos já acessíveis.</strong></div>
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
<p>Esse cálculo é refeito antes de cada Basic Attack com base no snapshot válido para aquela ação ou tick.</p>

<h3>8.7 Elegibilidade e escolha entre Basic Attack e Power Move</h3>
<p>Quando um Bud fica pronto, o servidor verifica primeiro se seu Power Move pode produzir uma ação válida naquele instante.</p>
<p>Um Power Move é elegível quando:</p>
<ul>
<li>existe ao menos um alvo válido;</li>
<li>suas condições próprias estão satisfeitas;</li>
<li>existe algum efeito aplicável e não completamente inútil;</li>
<li>o usuário não está sob um efeito que bloqueie Power Moves.</li>
</ul>
<p>Se estiver inelegível, o Bud executa obrigatoriamente um Basic Attack. Não há sorteio desperdiçado nem animação sem efeito. Esse Basic Attack conta normalmente para os contadores de sequência.</p>
<p>Se estiver elegível, o servidor decide primeiro entre Basic Attack e Power Move. Somente depois escolhe os alvos:</p>
<ul>
<li>Basic Attack sempre usa o targeting canônico;</li>
<li>Power Move pode usar o targeting canônico ou declarar uma regra própria;</li>
<li>regras próprias podem selecionar alvo único, múltiplos alvos, área, aliado, menor HP, posição, corredor ou todos os participantes elegíveis.</li>
</ul>

<h3>8.8 Chance natural de Power Move</h3>
<table>
<thead><tr><th>Raridade</th><th>Chance-base</th></tr></thead>
<tbody>
<tr><td>Comum</td><td><strong>14%</strong></td></tr>
<tr><td>Incomum</td><td><strong>17%</strong></td></tr>
<tr><td>Raro</td><td><strong>20%</strong></td></tr>
<tr><td>Épico</td><td><strong>23%</strong></td></tr>
<tr><td>Lendário</td><td><strong>26%</strong></td></tr>
</tbody>
</table>
<div class="formula">Chance natural = Base da raridade + (Vigor ÷ 100) + Bônus de SOR</div>
<div class="formula">Chance natural efetiva = mínimo entre Chance natural e 35%</div>
<ul>
<li>o Vigor possível vai de <strong>50 a 500</strong>;</li>
<li>Vigor 50 concede +0,50 ponto percentual;</li>
<li>Vigor 356 concede +3,56 pontos percentuais;</li>
<li>Vigor 500 concede +5 pontos percentuais;</li>
<li>a menor chance natural possível é <strong>14,5%</strong>;</li>
<li>Lendário com Vigor 500 e bônus máximo de SOR alcança 38% brutos, mas permanece em <strong>35%</strong> pela hard cap;</li>
<li>a sobreposição entre faixas de raridade é intencional.</li>
</ul>

<h3>8.9 SOR efetiva e curva de até +7 pontos percentuais</h3>
<p>O bônus usa a <strong>SOR efetiva atual</strong> do Bud no momento da decisão, e não uma SOR-base escondida.</p>
<p>Entram no cálculo todas as fontes legítimas que alterem SOR:</p>
<ul>
<li>valor inato e pontos distribuídos;</li>
<li>modificadores e multiplicadores aplicáveis ao atributo;</li>
<li>Núcleo Arcano e Totem;</li>
<li>passivas;</li>
<li>buffs e debuffs temporários;</li>
<li>demais efeitos válidos que modifiquem a SOR exibida e autoritativa.</li>
</ul>
<div class="formula">x = SOR efetiva ÷ SOR de referência da temporada, limitado entre 0 e 1</div>
<div class="formula">Bônus de SOR = 14x ÷ (1 + x)</div>
<table>
<thead><tr><th>SOR efetiva em relação à referência</th><th>Bônus de Power Move</th></tr></thead>
<tbody>
<tr><td>0%</td><td>0 pp</td></tr>
<tr><td>25%</td><td>+2,8 pp</td></tr>
<tr><td>50%</td><td>+4,67 pp</td></tr>
<tr><td>75%</td><td>+6 pp</td></tr>
<tr><td>100% ou mais</td><td><strong>+7 pp</strong></td></tr>
</tbody>
</table>
<ul>
<li>attachments e passivas não adicionam porcentagem direta de Power Move na Temporada 1; eles podem alterar SOR e, por consequência, a chance;</li>
<li>Vigor pode influenciar diretamente pela parcela Vigor ÷ 100 e indiretamente caso participe do cálculo final de SOR;</li>
<li>a decisão usa um snapshot da SOR efetiva; alterações causadas pela própria ação só afetam ações futuras.</li>
</ul>

<h3>8.10 Distribuição pseudoaleatória e contadores de sequência</h3>
<p>Cada Bud possui dois contadores individuais: <code>basicStreak</code> e <code>powerStreak</code>.</p>
<ul>
<li>os contadores começam zerados em uma nova batalha;</li>
<li>Basic Attack incrementa <code>basicStreak</code> e zera <code>powerStreak</code>;</li>
<li>Power Move incrementa <code>powerStreak</code> e zera <code>basicStreak</code>;</li>
<li>persistem por toda a tentativa, inclusive entre ondas, derrota temporária e retorno;</li>
<li>não são apagados por buffs, controles, transformações ou mudança de fase de boss;</li>
<li>só zeram quando uma nova batalha começa;</li>
<li>multi-hit, ricochete ou vários impactos do mesmo movimento contam como uma única ação.</li>
</ul>
<p>A chance natural exibida representa a frequência-alvo de longo prazo. O servidor usa uma distribuição pseudoaleatória calibrada para reduzir secas sem inflar essa frequência:</p>
<ul>
<li>os três primeiros Basic Attacks consecutivos não recebem proteção especial;</li>
<li>após o terceiro Basic consecutivo, a chance interna da próxima oportunidade elegível cresce progressivamente;</li>
<li>após oito Basic Attacks consecutivos, o próximo Power Move elegível é obrigatório;</li>
<li>um Power Move zera a sequência de Basics;</li>
<li>a hard cap de 35% limita a chance natural; a correção oculta de sequência pode elevar a chance pontual necessária ao pity;</li>
<li>a curva interna exata será calibrada em protótipo para preservar a frequência média indicada na ficha.</li>
</ul>
<p>Também existe um limite de sequência ofensiva:</p>
<ul>
<li>são permitidos até três Power Moves consecutivos;</li>
<li>depois do terceiro, a próxima ação é obrigatoriamente um Basic Attack;</li>
<li>não existe penalidade progressiva antes desse limite;</li>
<li>o Basic forçado zera <code>powerStreak</code>, passa a ser o primeiro Basic da nova sequência e permite sorteio normal na ação seguinte.</li>
</ul>
<p>Todos os Power Moves devem ser balanceados dentro de uma faixa comparável de impacto esperado, considerando dano, cura, proteção, controle, quantidade de alvos, frequência e condições de uso.</p>

<h3>8.11 Snapshot de Power Moves multi-alvo e multi-hit</h3>
<ul>
<li>todos os alvos de uma mesma ação são definidos a partir de um único snapshot;</li>
<li>a lista de alvos é fixada antes da resolução;</li>
<li>mortes causadas pela ação não criam exposição, adjacência ou novos alvos dentro dela;</li>
<li>dano em área é logicamente simultâneo, mesmo quando a animação mostra impactos em sequência;</li>
<li>não existe retarget no meio da ação, salvo quando o próprio Power Move declarar ricochete ou regra equivalente;</li>
<li>um multi-hit contra o mesmo alvo mantém esse alvo; dano excedente vira overkill;</li>
<li>crítico, proc e aplicação por hit só são testados separadamente quando a definição do Power Move disser isso;</li>
<li>todos os hits continuam compondo uma única ação para prontidão e contadores.</li>
</ul>

<h3>8.12 Manipulação de targeting exclusivamente por Power Moves</h3>
<p>Provocar, Marcação, Inalvejável, Proteção e efeitos equivalentes não formam, por enquanto, uma camada genérica do combate. Eles só existem quando um Power Move específico os declarar completamente.</p>
<p>Um Power Move pode implementar uma ou mais destas operações:</p>
<ol>
<li><strong>modificação de peso:</strong> aumenta ou reduz o peso de alvos antes da normalização;</li>
<li><strong>restrição de elegibilidade:</strong> limita temporariamente o conjunto de alvos válidos;</li>
<li><strong>redirecionamento:</strong> troca o destinatário final depois da escolha, sem realizar um novo sorteio.</li>
</ol>
<ul>
<li>Basic Attacks não criam essas manipulações por conta própria;</li>
<li>não haverá agora um sistema universal de taunt, marca ou interceptação;</li>
<li>cada Power Move excepcional deve definir alvo, duração, ações afetadas, condições, prioridade e fallback;</li>
<li>nenhum desses efeitos altera a posição lógica dos Buds.</li>
</ul>

<h3>8.13 Linha do tempo contínua com ticks sincronizados</h3>
<p>O combate não usa rodadas globais tradicionais. Cada unidade acumula prontidão individualmente, mas o servidor agrupa em um mesmo tick todas as unidades que estiverem prontas.</p>
<ol>
<li>o servidor abre o tick com um snapshot único do campo;</li>
<li>identifica todos os Buds e inimigos vivos, aptos e prontos;</li>
<li>cada unidade fixa o tipo de ação e seus alvos usando o mesmo snapshot;</li>
<li>todas as ações daquele tick são calculadas;</li>
<li>os resultados são consolidados simultaneamente;</li>
<li>mortes, exposição, controles e mudanças de estado passam a afetar o tick seguinte.</li>
</ol>
<p>Como não existe prioridade sequencial entre ações do mesmo tick, empates de prontidão não concedem vantagem permanente a nenhuma equipe.</p>

<h3>8.14 AGI, prontidão e limite de uma ação por tick</h3>
<ul>
<li>AGI determina o ganho de prontidão, e não a duração do tick;</li>
<li>todas as unidades presentes no início da batalha começam com <strong>0% de prontidão</strong>;</li>
<li>ao alcançar 100, a unidade fica elegível para agir no tick;</li>
<li>ao agir, consome 100 pontos de prontidão;</li>
<li>o excedente normal é preservado para o ciclo seguinte;</li>
<li>cada unidade pode executar no máximo <strong>uma ação por tick</strong>;</li>
<li>o dimensionamento da fórmula de AGI e do tick não permite descarregar múltiplas ações no mesmo snapshot.</li>
</ul>
<div class="formula">Prontidão 94 + ganho 14 = 108; o Bud age, consome 100 e preserva 8.</div>

<h3>8.15 Ação garantida para quem estava pronto no snapshot</h3>
<div class="statement"><strong>Toda unidade viva, apta e pronta no início do tick conclui sua ação, mesmo que receba dano letal naquele mesmo tick.</strong></div>
<ul>
<li>dois oponentes podem atacar e derrotar um ao outro simultaneamente;</li>
<li>uma morte dentro do tick não cancela retroativamente uma ação já fixada;</li>
<li>a ação só não ocorre quando a unidade já começou o tick derrotada, impedida de agir ou sem qualquer ação possível;</li>
<li>animações podem ser encadeadas para legibilidade, mas não criam uma ordem lógica.</li>
</ul>

<h3>8.16 Ordem simultânea de defesa, suporte, ataque e fechamento</h3>
<ol>
<li>o servidor registra HP, escudos, status, prontidão, ações e alvos no snapshot inicial;</li>
<li>efeitos defensivos e de suporte do tick estabelecem escudos, barreiras, reduções e créditos de cura;</li>
<li>ataques e danos são calculados contra as proteções válidas daquele tick;</li>
<li>escudos antigos e concedidos no tick absorvem o dano aplicável;</li>
<li>cura e dano restante são consolidados no HP;</li>
<li>o HP final é limitado entre zero e o máximo;</li>
<li>somente então são declaradas sobrevivência, derrota e mudanças para o próximo tick.</li>
</ol>
<div class="formula">HP final = HP inicial + cura do tick − dano que ultrapassou os escudos</div>
<p>Exemplo: 100 HP, 30 de escudo recebido, 20 de cura e 130 de dano resultam em 20 HP. A cura do mesmo tick pode salvar de dano letal; overheal não ultrapassa o HP máximo.</p>
<p>Buffs, debuffs e controles aplicados durante o tick não recalculam ações já fixadas. Eles entram em vigor após o fechamento, salvo o efeito defensivo ou de cura imediato explicitamente resolvido nesta etapa.</p>

<h3>8.17 Stun, Silence e prontidão armazenada</h3>
<ul>
<li>Stun impede a ação, mas a prontidão continua acumulando até o limite de 100%;</li>
<li>uma unidade atordoada em 100% permanece pronta e age no primeiro tick elegível após o controle terminar;</li>
<li>Stun não zera <code>basicStreak</code> nem <code>powerStreak</code>;</li>
<li>uma ação impedida por Stun não conta como Basic Attack nem Power Move;</li>
<li>Silence não impede a ação: ele torna o Power Move inelegível e força Basic Attack;</li>
<li>o Basic forçado por Silence conta normalmente para os dois contadores;</li>
<li>controles aplicados dentro de um tick só valem depois do fechamento e nunca cancelam ações já fixadas.</li>
</ul>

<h3>8.18 Tick lógico de um segundo e apresentação VIP em 2×</h3>
<ul>
<li>o tick lógico inicial é fixado em <strong>1 segundo</strong>;</li>
<li>o valor permanece configurável para testes e balanceamento futuros;</li>
<li>todos os participantes compartilham o mesmo relógio global;</li>
<li>o VIP pode reproduzir visualmente o PvE em <strong>2×</strong>, apresentando cada tick em aproximadamente <strong>0,5 segundo</strong>;</li>
<li>a aceleração é de apresentação e não modifica prontidão, chance de Power Move, targeting, dano, XP, drops ou resultado;</li>
<li>não concede vantagem em PvP;</li>
<li>o cliente nunca antecipa nem recalcula um resultado autoritativo;</li>
<li>animações podem durar mais de um tick e ser agrupadas, aceleradas ou levemente encadeadas sem bloquear a simulação lógica.</li>
</ul>

<h3>8.19 Limite de invocações e reforços</h3>
<div class="card danger"><strong>Buds jogáveis não possuem sistema de invocação ou reforço.</strong><p>Não entram novos Buds, não há substituição de aliados derrotados e uma posição vazia do jogador permanece vazia durante a batalha.</p></div>
<p>Monstros PvE podem receber reforços somente como comportamento roteirizado de uma fase, elite ou boss. Esses encontros serão desenhados manualmente com posições fixas reservadas, local de entrada, quantidade, condição e momento próprios. Isso não cria um sistema genérico disponível aos Buds.</p>

<h3>8.20 Eliminação simultânea completa no PvE</h3>
<ul>
<li>a batalha nunca termina no meio de um tick;</li>
<li>todas as ações já fixadas são concluídas;</li>
<li>o resultado é verificado somente após o fechamento completo;</li>
<li>para vencer uma fase PvE, ao menos um Bud precisa permanecer ativo;</li>
<li>se o último Bud e o último inimigo forem derrotados no mesmo tick, a tentativa é derrota do jogador;</li>
<li>essa eliminação simultânea não concede conclusão da fase, avanço de mapa nem drops de conclusão;</li>
<li>regras de empate do PvP serão definidas no ponto próprio de PvP.</li>
</ul>

<h3>8.21 Ordem autoritativa completa</h3>
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
<div class="statement"><strong>O Ponto 8 está estruturalmente definido.</strong> Números de dano, fórmulas exatas de ganho de prontidão, curva interna do pseudo-RNG e kits individuais serão calibrados e documentados sem alterar estas invariantes.</div>
</section>'''


PVE_FORMATION_SUBSECTION = r'''<h3>9.8 Formação canônica, posições e bloqueio durante a tentativa</h3>
<p>A formação PvE segue integralmente o Ponto 8 — Campo de Batalha, Formação e Posicionamento.</p>
<ul>
<li>o jogador escolhe entre um e sete Buds e pode deixar quaisquer posições vazias;</li>
<li>cada Bud ocupa uma posição canônica P1–P7;</li>
<li>a formação é congelada quando a tentativa começa;</li>
<li>não existe substituição manual, troca de slot ou reposicionamento automático durante a fase;</li>
<li>posições vazias e Buds temporariamente derrotados participam das regras de exposição definidas no Ponto 8;</li>
<li>targeting probabilístico, corredores, adjacência, prontidão e ticks seguem a especificação autoritativa do Ponto 8.</li>
</ul>'''

PVE_INVOCATION_SUBSECTION = r'''<h3>9.15 Reforços roteirizados e bosses com múltiplas fases</h3>
<ul>
<li>Buds jogáveis não invocam unidades, não recebem reforços e não substituem aliados derrotados;</li>
<li>não existe respawn genérico de inimigos comuns;</li>
<li>fases, elites e bosses podem possuir reforços roteirizados manualmente;</li>
<li>cada reforço PvE deve ter posição fixa reservada, condição, momento, quantidade e comportamento definidos no encontro;</li>
<li>bosses podem trocar de fase, forma ou conjunto de ações sem apagar os contadores individuais já existentes, salvo encerramento real da batalha;</li>
<li>qualquer entrada roteirizada só participa de targeting e resolução a partir de um snapshot válido posterior à sua criação.</li>
</ul>'''

PVE_VIP_SUBSECTION = r'''<h3>9.17 VIP e velocidade visual 1× / 2×</h3>
<ul>
<li>o PvE usa ticks lógicos de 1 segundo;</li>
<li>1× é a apresentação padrão;</li>
<li>2× é um recurso exclusivo do VIP e começa desativado;</li>
<li>o jogador VIP pode alternar entre 1× e 2× durante a própria tentativa;</li>
<li>em 2×, cada tick já autoritativo é apresentado visualmente em aproximadamente 0,5 segundo;</li>
<li><code>timeScale</code> afeta somente animações, transições e apresentação;</li>
<li>não altera prontidão, probabilidades, quantidade de ticks, XP, drops ou resultado calculado;</li>
<li>não se aplica como vantagem mecânica no PvP;</li>
<li>ao perder o benefício, a apresentação retorna imediatamente e suavemente para 1×.</li>
</ul>'''

DECISIONS = r'''
<div class="decision"><div><strong>Campo canônico e formação</strong><p>Sete posições em 1–2–1–2–1, ocupação livre, corredores e adjacência fixos, sem movimento ou reposicionamento lógico.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Targeting e exposição</strong><p>Basic Attacks usam pesos por posição; slots vazios transferem 33% por camada no corredor e redistribuem o restante.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Power Move</strong><p>Raridade, Vigor 50–500 e SOR efetiva definem chance natural entre 14,5% e 35%, com pseudo-RNG, pity e limite de sequência.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Ticks sincronizados</strong><p>Tick lógico de 1 segundo, prontidão por AGI, no máximo uma ação por unidade e resolução simultânea pelo mesmo snapshot.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Resolução simultânea</strong><p>Defesa e suporte imediatos precedem ataques; cura, escudos, dano, controles e mortes são consolidados apenas no fechamento.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Invocações e reforços</strong><p>Buds não invocam unidades; reforços existem apenas em encontros PvE roteirizados manualmente e com posições reservadas.</p></div><span class="status s-defined">Definido</span></div>'''


def visible_text(fragment: str) -> str:
    return " ".join(html_lib.unescape(re.sub(r"<[^>]+>", " ", fragment)).split())


def top_level_point(fragment: str) -> int | None:
    text = visible_text(fragment)
    match = re.match(r"^(?:Ponto\s+)?0*(\d+)(?:\.(?!\d)|\s*[—–:-]\s*|\s+|$)", text, flags=re.I)
    return int(match.group(1)) if match else None


def set_target(attrs: str, target: str) -> str:
    patterns = [
        re.compile(r"(?P<prefix>\bhref\s*=\s*)(?P<quote>['\"])#(?P<target>[^'\"]*)(?P=quote)", re.I),
        re.compile(r"(?P<prefix>\b(?:data-target|data-section)\s*=\s*)(?P<quote>['\"])(?P<hash>#?)(?P<target>[^'\"]*)(?P=quote)", re.I),
    ]
    for pattern in patterns:
        match = pattern.search(attrs)
        if not match:
            continue
        start, end = match.span("target")
        return attrs[:start] + target + attrs[end:]
    return attrs


def renumber_nav_body(body: str, old: int, new: int) -> str:
    replacements = [
        (rf"(?P<a>>\s*){old}(?P<b>\s*<)", rf"\g<a>{new}\g<b>"),
        (rf"\bPonto\s+{old}\b", f"Ponto {new}"),
        (rf"(?<!\d){old}\.(?!\d)", f"{new}."),
        (rf"(?<!\d){old}(?!\d)", str(new)),
    ]
    result = body
    for pattern, replacement in replacements:
        result, count = re.subn(pattern, replacement, result, count=1, flags=re.I)
        if count:
            return result
    raise RuntimeError("Não foi possível renumerar o corpo do botão do Ponto 8 para o Ponto 9.")


def relabel_point8_body(body: str) -> str:
    result = body
    for old, new in [
        ("Carry, Treinamento e Progressão PvE", "Campo de Batalha, Formação e Posicionamento"),
        ("Carry, treinamento e PvE", "Campo de batalha e formação"),
        ("Carry e PvE", "Campo de batalha"),
    ]:
        result = result.replace(old, new)
    return result


def patch_navigation(text: str) -> str:
    clickable = re.compile(r"<(?P<tag>a|button)\b(?P<attrs>[^>]*)>(?P<body>.*?)</(?P=tag)>", re.I | re.S)
    inserted = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal inserted
        if top_level_point(match.group("body")) != 8:
            return match.group(0)
        attrs = match.group("attrs")
        if not re.search(r"\b(?:href|data-target|data-section)\s*=", attrs, re.I):
            return match.group(0)

        tag = match.group("tag")
        old_body = match.group("body")
        point8_attrs = set_target(attrs, "battlefield-formation")
        point9_attrs = set_target(attrs, "pve-training")
        point8_body = relabel_point8_body(old_body)
        point9_body = renumber_nav_body(old_body, 8, 9)
        inserted += 1
        return (
            f"<{tag}{point8_attrs}>{point8_body}</{tag}>"
            f"<{tag}{point9_attrs}>{point9_body}</{tag}>"
        )

    text = clickable.sub(repl, text)
    if inserted == 0:
        raise RuntimeError("Nenhum botão ou link superior do Ponto 8 foi encontrado para criar o Ponto 9.")
    return text


def replace_subsection(section: str, current: str, following: str, replacement: str) -> str:
    pattern = re.compile(
        rf"<h3>\s*{re.escape(current)}\b.*?</h3>.*?(?=<h3>\s*{re.escape(following)}\b)",
        re.S,
    )
    section, count = pattern.subn(replacement + "\n", section, count=1)
    if count != 1:
        raise RuntimeError(f"Subseção {current} não encontrada ou duplicada.")
    return section


def renumber_and_align_pve(section: str) -> str:
    section = re.sub(r"(<h2>\s*)8\.", r"\g<1>9.", section, count=1)
    section = re.sub(r"(<h3>\s*)8\.(\d+)", r"\g<1>9.\2", section)
    section = section.replace("Ponto 8", "Ponto 9").replace("Point 8", "Point 9")

    section = replace_subsection(section, "9.8", "9.9", PVE_FORMATION_SUBSECTION)
    section = replace_subsection(section, "9.15", "9.16", PVE_INVOCATION_SUBSECTION)
    section = replace_subsection(section, "9.17", "9.18", PVE_VIP_SUBSECTION)

    frenzy_pattern = re.compile(r"(<h3>\s*9\.16\b.*?</h3>.*?)(?=<h3>\s*9\.17\b)", re.S)
    frenzy_match = frenzy_pattern.search(section)
    if not frenzy_match:
        raise RuntimeError("Subseção 9.16 de Frenesi não encontrada.")
    frenzy = frenzy_match.group(1)
    for old, new in [
        ("4 minutos", "240 ticks (4 minutos lógicos)"),
        ("6 minutos", "360 ticks (6 minutos lógicos)"),
        ("8 minutos", "480 ticks (8 minutos lógicos)"),
        ("10 minutos", "600 ticks (10 minutos lógicos)"),
    ]:
        frenzy = frenzy.replace(old, new)
    section = section[:frenzy_match.start(1)] + frenzy + section[frenzy_match.end(1):]

    heading = re.compile(r"(<h3>\s*9\.12\s+Condição de derrota e ordem de eventos\s*</h3>)")
    note = r'''\1
<div class="statement"><strong>Eliminação simultânea completa é derrota do jogador.</strong> Se o último Bud e o último inimigo forem derrotados no mesmo tick, todas as ações são concluídas, mas a fase não é vencida, não avança o mapa e não concede drops de conclusão.</div>'''
    section, count = heading.subn(note, section, count=1)
    if count != 1:
        raise RuntimeError("Cabeçalho 9.12 não encontrado para registrar a derrota simultânea.")

    return section


def insert_decisions(text: str) -> str:
    if "<strong>Campo canônico e formação</strong>" in text:
        return text
    marker = '<div class="decision"><div><strong>XP por inimigo e carry PvE</strong>'
    index = text.find(marker)
    if index < 0:
        raise RuntimeError("Marcador das decisões de carry PvE não encontrado.")
    return text[:index] + DECISIONS + "\n" + text[index:]


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
    assert gdd.count("<h2>8.") == 1
    assert gdd.count("<h2>9.") == 1
    battlefield = re.search(r'<section id="battlefield-formation">.*?</section>', gdd, re.S)
    pve = re.search(r'<section id="pve-training">.*?</section>', gdd, re.S)
    assert battlefield and battlefield.group(0).count("<h3>8.") == 21
    assert pve and pve.group(0).count("<h3>9.") == 20
    assert "7 → 5 → 6 → 4 → 2 → 3 → 1" not in pve.group(0)
    assert re.search(r'(?:href|data-target|data-section)=["\']#?battlefield-formation["\']', gdd)
    assert re.search(r'(?:href|data-target|data-section)=["\']#?pve-training["\']', gdd)
    assert "Available · v16" in portal


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

    pve_pattern = re.compile(r'<section id="pve-training">.*?</section>', re.S)
    match = pve_pattern.search(gdd)
    if not match:
        raise RuntimeError("Seção atual de Carry/PvE não encontrada.")
    pve = renumber_and_align_pve(match.group(0))
    gdd = gdd[:match.start()] + BATTLEFIELD_SECTION + "\n" + pve + gdd[match.end():]

    gdd = insert_decisions(gdd)
    gdd = patch_navigation(gdd)
    gdd = gdd.replace("Game Design Document · v15", "Game Design Document · v16")
    portal = portal.replace("Available · v15", "Available · v16")

    validate(gdd, portal)
    gdd_path.write_text(gdd, encoding="utf-8")
    portal_path.write_text(portal, encoding="utf-8")
    print(f"Consolidated Point 8 and renumbered PvE to Point 9 in {gdd_path}.")


if __name__ == "__main__":
    main()
