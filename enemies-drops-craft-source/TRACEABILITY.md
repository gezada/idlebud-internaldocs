# Idle Bud — matriz de autoridade de Inimigos, Drops, Itemização e Forja

## Hierarquia

1. `https://gezada.github.io/idlebud-internaldocs/gdd/`
2. `gdd-source/index.html`
3. Este documento de conteúdo.

O GDD publicado e a fonte local v17 foram lidos integralmente. A comparação
semântica das 24 seções resultou em equivalência exata. Não existe fonte
histórica ou documento auxiliar nesta entrega.

## Matriz de rastreabilidade

| Decisão obrigatória | Autoridade no GDD | Destino no documento |
|---|---|---|
| Conteúdo detalha; GDD define estrutura | 1; 9.20; 16.1; 17.5; 24 | 01–02, 26 |
| Nove elementos e matriz simétrica | 12.1–12.3 | 02, 05–09 |
| Neutro não é décimo elemento | 12.2; 17.3 | 02, 05 |
| Um elemento ativo por inimigo | 12.2; 17.3 | 05–09 |
| Somente Comum, Elite e Boss | 17.1 | 02, 05–09 |
| Comum: Basic Attack e um papel | 17.1–17.2 | 05–09 |
| Elite: exatamente dois papéis; Power Move só quando declarado | 17.1–17.2 | 05–09 |
| Boss: Basic, Power Move e dois ou três papéis | 17.1–17.2 | 05–09 |
| Gatilhos somente por tempo, HP, morte, reforço ou fase | 17.2 | 05–09 |
| Sem afixos, status ou multiplicadores ocultos | 10.2; 17.2; 20.3 | 03–12, 25 |
| Formação P1–P7, 1–2–1–2–1 | 8.1–8.6 | 03–09 |
| Basic Attack usa targeting canônico | 8.5 | 05–09 |
| Reforços roteirizados, posição reservada, sem XP/drop | 8.19; 9.15; 17.4 | 04, 09–11 |
| 14 mapas e 139 fases | 11 | 03–04 |
| Regular: fases 1–8, fase 9 normal/Elite, fase 10 Boss | 11.1 | 03–04 |
| Inicial Neutro, 9 específicos, 3 mistos, Convergência | 11 | 03–09 |
| Cinco Comuns por mapa regular | 17.4 | 04–08 |
| Mistos reutilizam seis Comuns e três Bosses associados | 17.4 | 04, 09 |
| Convergência: nove Bosses fortalecidos em sequência | 11.2; 17.4 | 04, 09 |
| XP fixa por inimigo derrotado | 9.2 | 04, 10 |
| Drops normais pertencem ao inimigo derrotado | 9.14 | 10–11 |
| Vitória preserva drops e dá conclusão; outros finais preservam só o conquistado | 9.12; 9.14; 10.2 | 10–11 |
| Elite dá componente próprio por vitória | 17.1; 17.5 | 05–11 |
| Boss dá Conhecimento na primeira vitória e componente nas repetições | 11.1; 17.1; 17.5 | 05–11 |
| Primeiro abate revela ficha no Codex | 17.5; 20.2 | 05–09, 25 |
| Semente tem elemento/pool, não Bud pré-gerado | 5.5; 14 | 12–14 |
| Água obrigatória; Fertilizante opcional e só na Germinação | 7.4; 7.11; 14 | 12–14 |
| Três perfis de Fertilizante 80/20, 20/80 e 50/50 | 7.11 | 14 |
| Proteção de Raridade do nascimento | 14.6 | 14 |
| Planos Básico, Elemental e Regional | 7.6 | 12–14 |
| Só Núcleo e Totem são equipáveis | 6.6; 15 | 16–18 |
| Attachment completo nunca cai; nasce por Síntese | 15; 16 | 10–12, 19–20 |
| Tipo e elemento fixos; 18 pools separados | 15.1 | 16, 18 |
| Linhas/passivas/níveis por raridade | 15.2 | 16–18 |
| Orçamento: até 80% Combate e 20% Cultivo; débito amplia até 25% | 15.3 | 17 |
| Attachment não cria skill, ataque ou movimento | 15; 15.6 | 16–18 |
| Pesquisa e refinamento instantâneos | 16.1 | 19 |
| Síntese escolhe tipo/elemento e toda raridade pode nascer | 16.2 | 20 |
| Distribuições Básica/Superior/Máxima | 16.2 | 20 |
| Proteção de Forja por conta/tipo/elemento/tier | 16.2 | 20 |
| Calibração preserva tipo, elemento e raridade | 15.4; 16.4; 21.6 | 21 |
| Apenas três ferramentas premium; máximo uma | 21.7 | 15, 21 |
| Fusão: três de mesma raridade/tipo/elemento; garantida; sem Lendário | 16.4 | 22 |
| Ascensão só Raro→Épico e Épico→Lendário | 16.5 | 23 |
| Três falhas seguras e risco crescente | 16.5 | 23 |
| Quebra destrói item e investimento; sem resíduo | 16.5–16.6 | 23 |
| Desmontagem: retorno parcial, normal/VIP, nunca 100% | 16.6 | 24 |
| Mercado não é redefinido; categoria precisa estar liberada | 21; Economia 08 | 15, 25 |
| Ferramentas premium: Cash store e mercado em Gold aprovados | 21.7; Economia 08 | 15, 21, 25 |
| Materiais/moldes/componentes sem negociabilidade aprovada | Economia 08 | 12–15, 25 |
| Autoridade, atomicidade, idempotência e auditoria | 8, 9, 14, 18, 21, 22 | 10, 19–25 |

## Decisões de conteúdo consolidadas aqui

- nomes, biomas e trios dos mapas;
- cinco Comuns, Elite quando aplicável e Boss de cada mapa;
- composição das 139 fases por templates versionados;
- papéis, ataques, gatilhos, reforços e apresentação no Codex;
- valores fixos de XP derivados no build de conteúdo;
- pools, pesos, garantias e Proteção de Semente;
- catálogo de Água, Seeds, Fertilizantes, materiais, moldes e reagentes;
- receitas e custos de Pesquisa, refinamento, Síntese, Calibração, Fusão,
  Ascensão e Desmontagem;
- orçamento de attachments, linhas, 18 pools de passivas e pesos;
- matriz completa de fonte → uso → sink → próximo objetivo.

## Decisões que continuam abertas

| Pendência | Por que permanece aberta | Decisão que fecha |
|---|---|---|
| Coeficientes finais de HP, dano, cura, escudo e prontidão por inimigo | O GDD reserva esses números ao simulador e ao Alpha. | Pacote versionado do simulador com duração, win rate, CP e testes de regressão. |
| Curva final de Battle XP e economia de Gold | Gold fora do PvP e curva de level ainda não foram aprovados. | Documento de balanceamento/economia com fontes, sinks e metas por coorte. |
| Gates numéricos do Nível do Jardineiro | O GDD define a responsabilidade do nível, não seus thresholds. | Tabela de progressão do Jardineiro aprovada sem alterar os gates territoriais deste catálogo. |
| Cronograma e moedas de mercado por categoria | A Economia mantém sementes, attachments e materiais em liberação controlada. | Política financeira versionada por categoria, moeda, fase e controles. |
| Produção final de arte, animação e áudio | O catálogo fixa função e leitura, mas não substitui direção de arte nem performance. | Art bible, atlas/rig, VFX, áudio e teste de silhueta aprovados. |
| Recalibração pós-Alpha | Pesos são completos para T1, mas continuam parâmetros públicos. | Relatório estatístico com mudança versionada, justificativa e patch note. |

## Dupla revisão

Cada capítulo passou por duas perguntas:

1. **Autoridade:** preserva categoria, elemento, formação, drops, estados,
   itemização, Forja e economia definidos pelo GDD?
2. **Jogo/operação:** possui fonte, uso, sink, leitura prévia, parâmetros
   versionados, atomicidade e proteção contra abuso?

Nenhuma decisão deste catálogo aprova moeda, saque, liquidez, negociabilidade
ou sistema paralelo.
