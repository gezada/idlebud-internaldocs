#!/usr/bin/env python3
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
html = path.read_text(encoding='utf-8')

if 'Game Design Document · v12' in html:
    html = html.replace('Game Design Document · v12', 'Game Design Document · v13', 1)
elif 'Game Design Document · v13' not in html:
    raise RuntimeError('Versão-base esperada (v12) não encontrada no HTML.')

section = '''<section id="farm-level">
<span class="tag blue">Farm Level</span>
<span class="review-state rs-defined">Definido</span>
<h2>7. Farm Level, Cultivo, Stamina e Processos do Plot</h2>
<p>O Farm Level é individual, possui cap 100 na primeira temporada e avança por produção no Plot e, em ritmo menor, pela recuperação legítima de Stamina. Ele não compartilha experiência com o Battle Level. Raridade e Vigor não aumentam Farm Level, produção, qualidade, Stamina, recuperação ou velocidade de cultivo.</p>
<div class="statement"><strong>Fácil de entender, difícil de masterizar.</strong> O jogador opera tempo, afinidade, quantidade, qualidade e cuidados claros; a profundidade matemática permanece por trás da interface.</div>

<h3>7.1 Farm Level, pontos e identidade de Cultivo</h3>
<ul>
<li>todo Bud nasce no <strong>Farm Level 1</strong>;</li>
<li>cada level concede um Ponto de Cultivo, totalizando <strong>100 pontos distribuíveis</strong> no cap 100;</li>
<li>cada Bud nasce também com <strong>24 Pontos Inatos de Cultivo</strong>, distribuídos aleatoriamente entre REC, COL, QLD, EFI, ADA e SUS;</li>
<li>cada atributo recebe no mínimo 1 e no máximo 10 pontos inatos, mantendo total fixo de 24;</li>
<li>Pontos Inatos são permanentes, visíveis, não rerroláveis e não são devolvidos por reset;</li>
<li>o reset de Cultivo devolve somente os pontos conquistados por Farm Level;</li>
<li>Farm XP vem de Ciclos de Cultivo concluídos e, em ritmo menor, da Stamina realmente recuperada;</li>
<li>recuperação possui validação por ciclo e proteções contra geração artificial de Farm XP;</li>
<li>Ciclo de Cultivo e Germinação não consomem Stamina.</li>
</ul>

<h3>7.2 Função dos seis Atributos de Cultivo</h3>
<div class="grid three">
<div class="card attribute"><div class="abbr">REC</div><div><h4>Recuperação</h4><p>Aumenta a velocidade de recuperação da Stamina consumida em batalha.</p></div></div>
<div class="card attribute"><div class="abbr">COL</div><div><h4>Colheita</h4><p>Aumenta a quantidade produzida por Ciclo de Cultivo, sem alterar qualidade, velocidade ou pool de itens.</p></div></div>
<div class="card attribute"><div class="abbr">QLD</div><div><h4>Qualidade</h4><p>Aumenta a chance de resultados superiores dentro da pool válida do Plano de Cultivo.</p></div></div>
<div class="card attribute"><div class="abbr">EFI</div><div><h4>Eficiência</h4><p>Aumenta a velocidade dos ciclos e reduz consumo ou desperdício de insumos quando aplicável.</p></div></div>
<div class="card attribute"><div class="abbr">ADA</div><div><h4>Adaptação</h4><p>Reduz penalidades de incompatibilidade e amplifica de forma controlada bonificações positivas de afinidade do Plot.</p></div></div>
<div class="card attribute"><div class="abbr">SUS</div><div><h4>Sustentação</h4><p>Aumenta a Stamina máxima e a autonomia de batalha antes do retorno ao Plot.</p></div></div>
</div>
<ul>
<li>ADA corrige penalidades com mais força do que amplia bônus positivos;</li>
<li>ADA nunca transforma penalidade em bônus e não altera o Plot Simples;</li>
<li>SUS não aumenta duração do cultivo, intervalo de cuidados ou limite offline;</li>
<li>REC não recupera HP, Mana ou cooldowns: esses recursos reiniciam após cada batalha;</li>
<li>doenças, ferimentos persistentes e condições negativas fora do combate não fazem parte do escopo atual;</li>
<li>não existem arquétipos nomeados, árvores ou skills de Cultivo; a especialização surge dos pontos, attachments, Plot e Plano de Cultivo.</li>
</ul>

<h3>7.3 Fichas separadas e influência dos attachments</h3>
<p>Cada Bud possui uma <strong>Ficha de Batalha</strong> e uma <strong>Ficha de Cultivo</strong>. Atributos de Batalha alimentam a primeira; Atributos de Cultivo alimentam a segunda.</p>
<p>Núcleo Arcano e Totem podem fornecer bônus planos ou percentuais para ambas as fichas. No Alpha, suas <strong>passivas condicionais</strong> atuam somente em batalha; no Cultivo, seus efeitos são numéricos, claros e previsíveis.</p>
<div class="card warn"><strong>Não existem equipamentos adicionais.</strong><p>Núcleo Arcano e Totem são os únicos attachments do Bud.</p></div>
<table>
<thead><tr><th>Status derivados da Ficha de Cultivo</th><th>Leitura</th></tr></thead>
<tbody>
<tr><td><strong>Stamina Máxima</strong></td><td>Reserva disponível para atividades de batalha.</td></tr>
<tr><td><strong>Recuperação de Stamina</strong></td><td>Stamina recuperada por unidade de tempo no Plot.</td></tr>
<tr><td><strong>Bônus de Colheita</strong></td><td>Quantidade adicional esperada por ciclo.</td></tr>
<tr><td><strong>Chance de Qualidade</strong></td><td>Probabilidade de resultados superiores dentro da pool válida.</td></tr>
<tr><td><strong>Velocidade de Cultivo</strong></td><td>Aumento da velocidade efetiva do ciclo.</td></tr>
<tr><td><strong>Economia de Insumos</strong></td><td>Redução prevista de consumo ou desperdício.</td></tr>
<tr><td><strong>Adaptação</strong></td><td>Mitigação de penalidades e amplificação controlada de bônus do Plot.</td></tr>
<tr><td><strong>Autonomia Estimada</strong></td><td>Quantidade aproximada de atividades de batalha antes da recuperação.</td></tr>
</tbody>
</table>

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
<li>quando um checkpoint termina, o processo aguarda interação sem destruir a semente, o Bud ou o resultado;</li>
<li>a ação básica é regar; Fertilizantes são opcionais;</li>
<li>antes da Germinação, o jogador seleciona semente e Plot, garante a água básica do processo e pode preparar insumos opcionais, como Fertilizantes ou tratamentos de solo futuramente suportados.</li>
</ul>

<h3>7.5 Germinação em três etapas</h3>
<div class="formula">Plantar semente → Germinação 1/3: Enraizamento → Germinação 2/3: Bloom → Germinação 3/3: Nascimento e Revelação do Bud</div>
<table>
<thead><tr><th>Etapa</th><th>Função</th></tr></thead>
<tbody>
<tr><td><strong>Enraizamento — 1/3</strong></td><td>Inicia o desenvolvimento da semente e termina no primeiro checkpoint de cuidado.</td></tr>
<tr><td><strong>Bloom — 2/3</strong></td><td>Etapa intermediária da Germinação; termina no segundo checkpoint e aceita Fertilizantes compatíveis.</td></tr>
<tr><td><strong>Nascimento e Revelação — 3/3</strong></td><td>Somente aqui o servidor calcula, cria, registra e revela o novo Bud.</td></tr>
</tbody>
</table>
<p>No Nascimento e Revelação são definidos espécie, raridade, Vigor, Pontos Inatos de Batalha, Pontos Inatos de Cultivo e demais valores individuais. Nada fica pré-gerado ou escondido dentro da semente.</p>
<p>Regas, Fertilizantes e demais insumos válidos deslocam probabilidades, mas nunca garantem um resultado específico. O cálculo final é autoritativo, atômico, idempotente e auditável pelo servidor.</p>

<h3>7.6 Planos e Ciclos de Cultivo</h3>
<p>Depois de nascer, o Bud pode executar um <strong>Plano de Cultivo</strong>. Cada execução completa é um <strong>Ciclo de Cultivo</strong>.</p>
<div class="formula">Iniciar cultivo → Etapa 1 → Cuidado → Etapa 2 → Cuidado → Etapa 3 → Colheita</div>
<table>
<thead><tr><th>Plano inicial</th><th>Duração-base</th><th>Função</th></tr></thead>
<tbody>
<tr><td><strong>Cultivo Básico</strong></td><td>1h30 — três etapas de 30 min</td><td>Disponível desde o início; foca volume de materiais comuns e qualidade simples.</td></tr>
<tr><td><strong>Cultivo Elemental</strong></td><td>6h — três etapas de 2h</td><td>Liberado pelo progresso inicial no PvE; combina materiais comuns e exclusivos do elemento do Bud, com melhor potencial de qualidade.</td></tr>
<tr><td><strong>Cultivo Regional</strong></td><td>12h — três etapas de 4h</td><td>Liberado por região, mapa ou boss; adiciona materiais regionais, ingredientes avançados e maior teto de qualidade.</td></tr>
</tbody>
</table>
<ul>
<li>cada Plano define duração, pool de materiais, quantidade-base, qualidade-base, insumos opcionais e requisitos de progresso;</li>
<li>as pools podem combinar materiais comuns, exclusivos do elemento do Bud e regionais liberados pelo PvE;</li>
<li>Ciclo de Cultivo não consome Stamina;</li>
<li>novos Planos podem ser adicionados sem alterar a estrutura central;</li>
<li>o jogador escolhe um objetivo compreensível, sem configurar dezenas de parâmetros.</li>
</ul>

<h3>7.7 Afinidade dos Plots</h3>
<p>Existem nove categorias elementais de Plot e um <strong>Plot Simples</strong>, sempre neutro. A Matriz de Afinidade de Cultivo utiliza a roda elemental como referência estrutural, mas é configurada separadamente da matriz de combate.</p>
<table>
<thead><tr><th>Relação do Bud com o Plot</th><th>Produtividade total</th></tr></thead>
<tbody>
<tr><td>Mesmo elemento</td><td><strong>2,00×</strong></td></tr>
<tr><td>Muito Forte</td><td><strong>1,60×</strong></td></tr>
<tr><td>Forte</td><td><strong>1,30×</strong></td></tr>
<tr><td>Neutro</td><td><strong>1,00×</strong></td></tr>
<tr><td>Fraco</td><td><strong>0,75×</strong></td></tr>
<tr><td>Muito Fraco</td><td><strong>0,50×</strong></td></tr>
<tr><td>Plot Simples</td><td><strong>1,00×</strong> com qualquer elemento</td></tr>
</tbody>
</table>
<div class="formula">Multiplicador de quantidade = √Afinidade efetiva &nbsp;|&nbsp; Multiplicador de velocidade = √Afinidade efetiva</div>
<p>Dividir a afinidade pela raiz quadrada impede que um bônus de 2,00× em quantidade e velocidade resulte em 4,00× por hora. Em 2,00×, quantidade e velocidade recebem aproximadamente 1,414×, preservando produtividade total de 2,00×.</p>
<p>Na interface principal, o jogador vê apenas a produtividade total esperada; a decomposição fica nos detalhes.</p>

<h3>7.8 Matemática de ADA</h3>
<div class="formula">Score de ADA = Pontos Inatos + pontos distribuídos + bônus planos de Núcleo Arcano e Totem</div>
<div class="formula">Curva de ADA = Score ÷ (Score + 100)</div>
<div class="grid">
<div class="card"><h4>Afinidade abaixo de 1,00×</h4><p><strong>Mitigação = 60% × Curva de ADA</strong></p><p>Afinidade efetiva = Afinidade original + (1 − Afinidade original) × Mitigação.</p></div>
<div class="card"><h4>Afinidade acima de 1,00×</h4><p><strong>Amplificação = 20% × Curva de ADA</strong></p><p>Afinidade efetiva = Afinidade original + (Afinidade original − 1) × Amplificação.</p></div>
</div>
<ul>
<li>com 100 ADA, 0,50× passa aproximadamente a 0,65×;</li>
<li>com 100 ADA, 2,00× passa aproximadamente a 2,10×;</li>
<li>ADA nunca transforma penalidade em bônus, não reduz afinidades positivas e não altera relações neutras ou o Plot Simples;</li>
<li>os limites de 60% e 20% são hard caps estruturais da contribuição de ADA.</li>
</ul>

<h3>7.9 Fórmulas dos Atributos de Cultivo</h3>
<p>Para REC, COL, QLD, EFI e SUS, o Score considera Pontos Inatos, pontos distribuídos e bônus planos dos attachments. Bônus percentuais diretos de Núcleo e Totem entram depois da curva e não podem contornar hard caps globais.</p>
<div class="formula">Curva padrão = Score ÷ (Score + 100)</div>
<table>
<thead><tr><th>Atributo</th><th>Conversão</th><th>Hard cap da curva</th></tr></thead>
<tbody>
<tr><td><strong>REC</strong></td><td>Velocidade de recuperação = 1 + 100% × Curva</td><td>2,00× velocidade</td></tr>
<tr><td><strong>COL</strong></td><td>Quantidade = Quantidade-base × (1 + 100% × Curva)</td><td>2,00× quantidade antes de afinidade e efeitos contextuais</td></tr>
<tr><td><strong>QLD</strong></td><td>Bônus de Qualidade = 40 pontos percentuais × Curva</td><td>+40 p.p. dentro da pool válida</td></tr>
<tr><td><strong>EFI — velocidade</strong></td><td>Velocidade de Cultivo = 1 + 50% × Curva</td><td>1,50× velocidade</td></tr>
<tr><td><strong>EFI — economia</strong></td><td>Redução de insumos = 30% × Curva</td><td>30% de redução</td></tr>
<tr><td><strong>SUS</strong></td><td>Stamina máxima = Stamina-base × (1 + 100% × Curva)</td><td>2,00× Stamina-base</td></tr>
</tbody>
</table>
<ul>
<li>QLD desloca probabilidades para faixas superiores, mas não cria materiais fora da pool;</li>
<li>Raridade e Vigor não entram em nenhuma fórmula de Cultivo;</li>
<li>coeficientes podem ser refinados no Alpha sem alterar as responsabilidades de cada atributo.</li>
</ul>

<h3>7.10 Economia de Stamina e Recuperação</h3>
<p>Somente batalhas consomem Stamina. O custo é previsível e independente de dano causado, dano recebido, cura ou duração da luta.</p>
<table>
<thead><tr><th>Atividade</th><th>Custo inicial de protótipo por Bud participante</th></tr></thead>
<tbody>
<tr><td>PvE normal</td><td>10</td></tr>
<tr><td>PvE elite</td><td>15</td></tr>
<tr><td>Boss</td><td>25</td></tr>
<tr><td>Ataque PvP</td><td>12</td></tr>
<tr><td>Defesa PvP assíncrona</td><td>0</td></tr>
</tbody>
</table>
<ul>
<li>Stamina-base: <strong>100</strong>;</li>
<li>cada Bud participante paga o custo completo da atividade;</li>
<li>a derrota consome o custo normalmente;</li>
<li>cancelamentos técnicos ou falhas do servidor devem reembolsar o custo;</li>
<li>um Bud não inicia nova atividade sem Stamina suficiente;</li>
<li>defesa PvP assíncrona não consome Stamina para impedir que terceiros esgotem o elenco;</li>
<li>HP, Mana e cooldowns reiniciam depois de cada batalha.</li>
</ul>
<h4>Recuperação</h4>
<div class="formula">Tempo para recuperar = 60 min × (Stamina ausente ÷ 100) ÷ Velocidade de REC ÷ Multiplicador VIP</div>
<ul>
<li>recuperar de 0 a 100 leva no máximo <strong>60 minutos</strong> sem bônus;</li>
<li>a recuperação completa utiliza três etapas-base de aproximadamente 20 minutos e dois checkpoints;</li>
<li>Stamina retorna continuamente; o jogador pode interromper e utilizar o valor já recuperado;</li>
<li>o processo pausa nos checkpoints do jogador gratuito até o cuidado;</li>
<li>afinidade elemental do Plot não altera a Recuperação;</li>
<li>com REC no limite, a recuperação completa chega a aproximadamente 30 minutos;</li>
<li>com REC no limite e VIP, chega a aproximadamente 27 minutos;</li>
<li>Farm XP considera somente Stamina realmente restaurada: não existe XP por excesso, início e cancelamento sem recuperação ou loops artificiais.</li>
</ul>

<h3>7.11 Fertilizantes</h3>
<p>Fertilizantes são consumíveis opcionais aplicáveis nos dois checkpoints de cuidado. A rega básica sempre permite continuar sem consumir Fertilizante.</p>
<ul>
<li>limite inicial: <strong>um Fertilizante por checkpoint</strong> e <strong>dois por processo completo</strong>;</li>
<li>cada tipo declara em quais processos e etapas pode ser usado;</li>
<li>o mesmo tipo pode ser utilizado duas vezes quando permitido, respeitando os caps;</li>
<li>o item é consumido na aplicação;</li>
<li>Fertilizantes alteram probabilidades ou valores esperados, mas não garantem resultados;</li>
<li>Fertilizantes especializados são fortes em um objetivo e não concedem bônus aos demais;</li>
<li>VIP não recebe Fertilizantes exclusivos, potência adicional ou limite maior; apenas pode automatizar o uso autorizado.</li>
</ul>
<table>
<thead><tr><th>Exemplo conceitual</th><th>Função</th></tr></thead>
<tbody>
<tr><td><strong>Fertilizante Simples</strong></td><td>Pequeno aumento geral entre os efeitos válidos do processo.</td></tr>
<tr><td><strong>Fertilizante de Raridade</strong></td><td>Aplicável ao Bloom; aumenta apenas a probabilidade de raridades superiores.</td></tr>
<tr><td><strong>Fertilizante de Vigor</strong></td><td>Desloca a distribuição de Vigor no nascimento, sem garantir valor específico.</td></tr>
<tr><td><strong>Fertilizante de Colheita</strong></td><td>Aumenta quantidade no Ciclo de Cultivo.</td></tr>
<tr><td><strong>Fertilizante de Qualidade</strong></td><td>Melhora resultados dentro da pool válida.</td></tr>
<tr><td><strong>Fertilizante de Recuperação</strong></td><td>Reduz o tempo de Recuperação de Stamina.</td></tr>
</tbody>
</table>
<p>Catálogo definitivo, receitas, raridades, valores e potência de cada Fertilizante permanecem como conteúdo de balanceamento.</p>

<h3>7.12 Operação manual e benefícios VIP</h3>
<div class="grid">
<div class="card"><h4>Jogador gratuito</h4><ul><li>inicia cada processo;</li><li>realiza os dois cuidados;</li><li>conclui nascimento, colheita ou recuperação;</li><li>inicia manualmente o próximo processo;</li><li>se não retornar, o processo apenas aguarda e nada é perdido.</li></ul></div>
<div class="card good"><h4>Jogador VIP</h4><ul><li>cuidados automáticos, inclusive offline;</li><li>nascimento e revelação automáticos, quando habilitados;</li><li>colheita automática e repetição do mesmo Plano;</li><li>conclusão automática da Recuperação;</li><li>uso automático de Fertilizantes previamente autorizados e disponíveis;</li><li>rotação Batalha → Recuperação → Batalha com Plot reservado;</li><li><strong>10% de velocidade adicional</strong> em Germinação, Cultivo e Recuperação.</li></ul></div>
</div>
<div class="formula">Tempo VIP = Tempo final ÷ 1,10</div>
<ul>
<li>o bônus VIP é aplicado depois das demais velocidades válidas;</li>
<li>uso automático de Fertilizantes nunca vem ativado por padrão;</li>
<li>VIP não aumenta diretamente raridade, Vigor, qualidade ou potência dos Fertilizantes;</li>
<li>VIP não concede materiais exclusivos, não aumenta o limite de Fertilizantes e não cria Plot gratuito;</li>
<li>VIP continua dependente de sementes, materiais, Planos, regiões e requisitos já desbloqueados;</li>
<li>a combinação foi desenhada para um VIP de baixo preço, com teto comercial atualmente desejado de <strong>R$ 9,99</strong>.</li>
</ul>

<h3>7.13 Rotação automática Batalha → Recuperação → Batalha</h3>
<div class="formula">Batalhar → Stamina insuficiente → Finalizar a atividade atual → Retornar ao Plot reservado → Recuperar → Voltar à atividade compatível</div>
<ul>
<li>o Plot precisa estar reservado, livre e vinculado ao Bud;</li>
<li>um Plot reservado não pode germinar, cultivar ou receber outro Bud;</li>
<li>o Bud não abandona batalha em andamento;</li>
<li>se o Plot ficar indisponível, a automação pausa;</li>
<li>o jogador pode desativar o retorno e deixar o Bud no Plot;</li>
<li>depois de recuperar, o Bud retorna à batalha configurada; ele não inicia Bloom ou Ciclo de Cultivo;</li>
<li>a interface resume o sistema em três escolhas: recuperação automática, Plot reservado e retorno à atividade.</li>
</ul>

<h3>7.14 FP — Farming Power / Poder de Cultivo</h3>
<p>Cada Bud possui um indicador geral chamado <strong>FP — Farming Power</strong>, apresentado em português como <strong>Poder de Cultivo</strong>. Ele resume a Ficha de Cultivo permanente para comparação, organização e marketplace.</p>
<div class="formula">FP = C × (25% Produção + 20% Qualidade + 20% Velocidade + 10% Economia + 10% Adaptação + 7,5% Recuperação + 7,5% Stamina)</div>
<ul>
<li>cada componente é normalizado em relação a um Bud-base;</li>
<li>Produção considera COL; Qualidade considera QLD; Velocidade e Economia consideram EFI; Adaptação considera ADA; Recuperação considera REC; Stamina considera SUS;</li>
<li>ADA é avaliada por desempenho médio na Matriz de Afinidade, não por Plot Simples;</li>
<li>FP não considera VIP, Fertilizantes ou efeitos temporários;</li>
<li>a ficha expandida apresenta os subindicadores <strong>Produção</strong> e <strong>Autonomia</strong>;</li>
<li>FP não determina drops, não desbloqueia conteúdo e não substitui a estimativa específica de um Plano em determinado Plot;</li>
<li><strong>C</strong> é um coeficiente de normalização para manter números legíveis.</li>
</ul>

<h3>7.15 Ordem de cálculo contextual</h3>
<ol>
<li>valores-base do Plano de Cultivo ou da Recuperação;</li>
<li>Score formado por Pontos Inatos, pontos distribuídos e bônus planos de Núcleo e Totem;</li>
<li>conversão do Score pelas curvas e hard caps de REC, COL, QLD, EFI, ADA e SUS;</li>
<li>bônus percentuais numéricos de Núcleo e Totem, sem ultrapassar caps globais;</li>
<li>Afinidade efetiva do Plot, já ajustada por ADA;</li>
<li>Fertilizantes e outros insumos válidos do processo;</li>
<li>multiplicador VIP de velocidade, quando ativo;</li>
<li>arredondamento somente no ponto definido pelo servidor e apresentação do resultado.</li>
</ol>
<p>Todos os cálculos de produção, qualidade, Stamina, FP e probabilidades de nascimento são autoritativos e auditáveis pelo servidor.</p>

<h3>7.16 Princípio de interface e estado do sistema</h3>
<p>A tela principal mostra somente processo, tempo restante, quantidade e qualidade esperadas, afinidade do Plot, próximo cuidado e botão principal. Fórmulas, curvas e fontes dos bônus ficam em tooltips ou detalhes avançados.</p>
<div class="statement"><strong>O Ponto 7 está estruturalmente definido.</strong> Permanecem ajustáveis no simulador, Alpha e patches apenas curvas de XP, coeficientes K, custos de Stamina, pools e quantidades de materiais, receitas, valores dos Fertilizantes e normalização visual do FP. Esses ajustes não alteram as regras centrais descritas acima.</div>
</section>'''

html, replacements = re.subn(r'<section id="farm-level">.*?</section>', section, html, count=1, flags=re.S)
if replacements != 1:
    raise RuntimeError(f'Esperava substituir uma seção farm-level; substituições realizadas: {replacements}')

decisions = '''<div class="decision"><div><strong>Atributos de Cultivo</strong><p>REC, COL, QLD, EFI, ADA e SUS possuem funções, curvas e hard caps próprios; raridade e Vigor não interferem no Farm.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Fichas separadas</strong><p>Cada Bud possui Ficha de Batalha e Ficha de Cultivo; Núcleo e Totem modificam ambas numericamente, mas passivas condicionais ficam na batalha no Alpha.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Processos do Plot</strong><p>Germinação, Ciclo de Cultivo e Recuperação usam três etapas, dois cuidados e apenas um processo ativo por Plot.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Germinação</strong><p>Enraizamento 1/3, Bloom 2/3 e Nascimento e Revelação 3/3; o Bud é calculado somente na etapa final.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Afinidade de Cultivo</strong><p>Plot Simples é 1,00×; Plots elementais variam de 0,50× a 2,00× e dividem o efeito por raiz quadrada entre quantidade e velocidade.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>ADA</strong><p>Mitiga até 60% das penalidades e amplia até 20% do bônus positivo, sempre com retorno decrescente e sem alterar o Plot Simples.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Planos de Cultivo</strong><p>Alpha parte de Cultivo Básico, Elemental e Regional, com durações de 1h30, 6h e 12h e pools progressivas ligadas ao PvE.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Stamina</strong><p>Somente batalhas consomem Stamina; base 100, custos previsíveis por atividade e recuperação total em até 60 minutos antes de REC e VIP.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>Fertilizantes</strong><p>Um por checkpoint e dois por processo; são opcionais, especializados, não garantem resultados e podem ter uso automatizado pelo VIP.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>VIP de Cultivo</strong><p>Automatiza etapas offline, Fertilizantes autorizados e rotação de recuperação, além de acelerar os processos em 10%.</p></div><span class="status s-defined">Definido</span></div>
<div class="decision"><div><strong>FP — Farming Power</strong><p>Poder de Cultivo resume produção, qualidade, velocidade, economia, adaptação, recuperação e Stamina sem considerar VIP ou efeitos temporários.</p></div><span class="status s-defined">Definido</span></div>'''

v12_block = re.compile(
    r'<div class="decision"><div><strong>Atributos de Cultivo</strong>.*?'
    r'<div class="decision"><div><strong>Fertilizantes</strong>.*?</div><span class="status [^"]+">.*?</span></div>',
    re.S,
)
html, replaced_decisions = v12_block.subn(decisions, html, count=1)
if replaced_decisions == 0:
    marker = '<div class="decision"><div><strong>CP e Poder de Confronto</strong><p>CP resume a ficha permanente; Poder de Confronto adiciona matchup, elementos, posição e composição para estimar a vitória.</p></div><span class="status s-defined">Definido</span></div>'
    if marker not in html:
        raise RuntimeError('Marcador para decisões consolidadas não encontrado.')
    html = html.replace(marker, marker + '\n' + decisions, 1)

replacements_open = [
    (
        r'<li><strong>(?:Germinação e Fertilizantes|Germinação):</strong>.*?</li>',
        '<li><strong>Conteúdo de Germinação e Fertilizantes:</strong> tempos finais por semente, catálogo, receitas, raridades, valores e potência probabilística de cada insumo.</li>',
    ),
    (
        r'<li><strong>(?:Farm XP e Stamina|Farm XP):</strong>.*?</li>',
        '<li><strong>Calibração de Farm XP e Stamina:</strong> curvas de XP, limites antiabuso, custos finais por atividade e ajustes de recuperação após testes.</li>',
    ),
    (
        r'<li><strong>(?:Plots e Cultivo|Plots):</strong>.*?</li>',
        '<li><strong>Conteúdo de Plots e Cultivo:</strong> mapeamento final da Matriz de Afinidade, pools, quantidades, receitas, requisitos regionais, coeficientes K e normalização visual do FP.</li>',
    ),
]
for pattern, replacement in replacements_open:
    html, count = re.subn(pattern, replacement, html, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f'Não foi possível atualizar pendência: {pattern}')

required = [
    'Game Design Document · v13',
    '7. Farm Level, Cultivo, Stamina e Processos do Plot',
    'review-state rs-defined">Definido',
    '24 Pontos Inatos de Cultivo',
    'Germinação 1/3: Enraizamento',
    'Germinação 2/3: Bloom',
    'Germinação 3/3: Nascimento e Revelação do Bud',
    'Cultivo Básico',
    'Cultivo Elemental',
    'Cultivo Regional',
    'Mesmo elemento</td><td><strong>2,00×',
    'Plot Simples',
    'Mitigação = 60% × Curva de ADA',
    'Amplificação = 20% × Curva de ADA',
    'Bônus de Qualidade = 40 pontos percentuais × Curva',
    'Stamina-base: <strong>100</strong>',
    'recuperar de 0 a 100 leva no máximo <strong>60 minutos</strong>',
    'um Fertilizante por checkpoint',
    'dois por processo completo',
    '10% de velocidade adicional',
    'R$ 9,99',
    'FP — Farming Power',
    '25% Produção + 20% Qualidade + 20% Velocidade',
    'O Ponto 7 está estruturalmente definido.',
]
for item in required:
    assert item in html, f'Conteúdo obrigatório do Ponto 7 ausente: {item}'

farm_match = re.search(r'<section id="farm-level">.*?</section>', html, re.S)
assert farm_match, 'Seção farm-level não encontrada.'
farm = farm_match.group(0)
for stale in [
    'review-state rs-validation',
    'review-state rs-provisional',
    'Quantidade ainda não definida',
    'percentual a definir',
    'proposta em validação',
    'Sprays de Cuidado',
    'cultivo consome Stamina',
    '7.1 Arquétipos possíveis',
    'Bloom nem Ciclo de Cultivo automaticamente, salvo configuração futura específica',
]:
    assert stale not in farm, f'Texto obsoleto no Ponto 7: {stale}'

assert farm.count('<h3>7.') == 16, 'Quantidade inesperada de subseções no Ponto 7.'
assert html.count('<section id="farm-level">') == 1, 'Seção farm-level duplicada.'

path.write_text(html, encoding='utf-8')
print(f'Finalized Point 7 in {path} ({path.stat().st_size} bytes)')