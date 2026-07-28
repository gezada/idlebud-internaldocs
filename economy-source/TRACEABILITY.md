# Idle Bud — matriz interna de rastreabilidade econômica

Documento de trabalho para auditoria da página `economy-source/index.html`.

## Ordem de autoridade

1. GDD publicado em `https://gezada.github.io/idlebud-internaldocs/gdd/`;
2. fonte local canônica `gdd-source/index.html`;
3. `idle_lovers_foundign_doc.html`, usado somente para riscos, contexto e perguntas.

O GDD publicado e a fonte local foram comparados por estrutura: ambos apresentam o
GDD v17, com os mesmos 24 capítulos e o mesmo capítulo econômico. Nenhuma proposta
do Founding Doc é tratada como aprovação.

## Decisão econômica → origem → seção Economia

| Decisão ou limite | Autoridade no GDD | Seção em Economia |
|---|---|---|
| O Bud é indivíduo persistente e transfere identidade, progressão, build, proveniência e consumo de resets | 2; 4.1; 4.5–4.7; 23 | 8. Ativos |
| Apelido é privado e não integra anúncio nem valor público | 4.3; 23 | 8. Ativos |
| Reset gratuito de Batalha/Cultivo pertence ao Bud e deve aparecer antes da compra | 4.7; 6.3; 23 | 5. Marketplace; 8. Ativos |
| Nível do Jardineiro libera funções e limites-base do mercado | 5.7.1–5.7.2 | 9. Oferta, escassez e limites |
| VIP amplia eficiência, capacidade e conforto sem conceder atributos ou conteúdo principal exclusivo | 5.7.3–5.7.5; 23 | 10. Sistemas conectados |
| Desmontagem VIP 40% versus 20% é exceção econômica deliberada e provisória | 5.7.5; 16.6; 23 | 9. Sinks; 10. Sistemas conectados |
| Cap 100 sem XP excedente limita emissão de progressão vertical | 5.6; 6.1; 7.1; 23 | 9. Oferta, escassez e limites |
| Raridade e Vigor não aumentam drop, produção ou velocidade de progressão | 6.8; 7; 23 | 9. Oferta, escassez e limites |
| Germinação consome semente/insumos, é autoritativa, atômica, idempotente e auditável | 7.4–7.5; 14.1–14.7; 23 | 9. Sinks; 12. Integridade |
| Sementes guardadas usam a pool vigente no plantio; isso é estratégia legítima, não exploit | 5.5; 14.2; 23 | 8. Ativos; 12. Integridade |
| Proteção de Raridade pertence à conta, não à semente | 14.6–14.7; 21.5; 23 | 8. Ativos |
| Plots iniciais e vagas são vinculados; Plots não iniciais vazios podem circular em Gold | 13.1–13.4; 21.5; 23 | 8. Ativos |
| Infraestrutura de Cultivo permanece com a conta e não acompanha o Plot | 13.4; 21.5; 23 | 8. Ativos |
| Núcleo e Totem são os únicos attachments; listar Bud não inclui attachments | 6.6; 15.1; 15.5; 18.5; 23 | 8. Ativos |
| Attachments completos só nascem por Síntese; Forja consome materiais e pode destruir valor | 15; 16.1–16.6; 23 | 9. Sinks; 10. Sistemas conectados |
| Calibração sempre exige recursos de gameplay; ferramenta premium não substitui custo normal | 15.4; 21.6–21.7 | 9. Sinks; 10. Sistemas conectados |
| Estados e bloqueios impedem uso, produção e venda simultâneos | 18.1–18.5; 23 | 5. Marketplace; 8. Ativos; 12. Integridade |
| PvP ranqueado emite Gold e Battle XP; derrota emite menos; amistoso não emite nada | 19.4–19.5 | 9. Fontes; 10. Sistemas conectados |
| PvP não consome Stamina e VIP não altera luta | 19.1–19.2 | 10. Sistemas conectados |
| Resultados, recompensas e replays de PvP são autoritativos e auditáveis | 19.2; 19.6 | 12. Integridade |
| Interface e wiki devem revelar custos, chances, fontes e regras ativas antes do gasto | 20.3–20.4 | 5. Marketplace; 12. Transparência |
| Gold é local do Idle Bud; Cash e Saldo são globais da conta Idol Lovers | 21.1; 23 | 2. Arquitetura; 3. Saldos |
| Não há conversão automática entre Gold, Cash e Saldo | 21.1 | 2. Arquitetura; 3. Saldos |
| Marketplace aceita Gold, Cash ou anúncio duplo; primeira liquidação válida encerra tudo | 21.2; 23 | 5. Marketplace |
| Taxa-base de Marketplace é 10%, configurável | 21.2; 23 | 5. Marketplace; 13. Governança |
| Venda em Gold credita 90% em Gold; venda em Cash credita 90% em Saldo | 21.2; 23 | 5. Marketplace |
| Operação de mercado deve ser atômica, autoritativa e idempotente | 21.2; 23 | 4. Ledger; 5. Marketplace; 12. Integridade |
| Saldo não é transferível e pode virar Cash com taxa de 5% | 21.1; 21.3; 23 | 3. Saldos; 7. Conversão e saque |
| Saque inicial usa Saldo e somente cripto/stablecoin; primeiro saque exige identidade | 21.1; 21.3; 23 | 7. Conversão e saque; 14. Risco regulatório |
| Taxa de rede é separada da taxa de Marketplace | 21.3 | 7. Conversão e saque |
| Venda direcionada usa as mesmas moedas, fee e liquidação do Marketplace | 21.4; 23 | 6. Trade |
| Venda direcionada respeita máximo entre piso administrativo e 50% da referência | 21.4 | 6. Trade; 15. Backlog |
| Referência é mediana das últimas 10 vendas públicas válidas em 14 dias | 21.4 | 6. Trade; 15. Backlog |
| Sem histórico suficiente, vale somente o piso administrativo | 21.4 | 6. Trade; 15. Backlog |
| Escambo exige sete dias de amizade, custódia atômica e fee em Cash | 21.4; 23 | 6. Trade |
| Fee de escambo é o máximo entre taxa mínima e 10% da referência Cash do item mais valioso | 21.4 | 6. Trade; 15. Backlog |
| Partes dividem livremente o fee; Cash nunca é transferido entre elas | 21.4; 23 | 6. Trade |
| Não existem presentes nem transferências diretas de Cash ou Saldo | 21.3–21.4; 23 | 3. Saldos; 6. Trade |
| Plots não iniciais estão aprovados por Gold; demais categorias têm liberação gradual | 21.5; 21.7; 24.5 | 8. Ativos; 15. Backlog |
| Ferramentas premium de Calibração podem ser vendidas por Cash e negociadas por Gold | 21.7 | 8. Ativos; 10. Sistemas conectados |
| Expedição mostra resultados recentes, sem multiplicador econômico oculto | 10.2; 21.8 | 10. Sistemas conectados; 12. Transparência |
| Alpha e Beta vendem VIP e validam economia, pagamentos e abuso | 22; 22.3 | 10. Sistemas conectados; 11. Testes |
| Alpha→Beta e Beta→S1 resetam jogo, mas preservam conta, Cash e ledger elegível | 22.1 | 11. Testes |
| Gasto Cash válido no Alpha volta como 130%; no Beta, 120% | 22.2; 23 | 11. Testes |
| Cash não gasto não recebe crédito duplicado | 22.2 | 11. Testes |
| Estorno, chargeback, concessão administrativa, Cash de teste e fraude não geram crédito | 22.2 | 11. Testes |
| Elegibilidade do Crédito no Marketplace/Trade ainda é financeira | 22.2 | 11. Testes; 15. Backlog |
| Eventos de servidor são verdade econômica; telemetria mede fontes, gastos, fees e anomalias | 22.3 | 12. Integridade; 13. Governança |
| Dados têm finalidade, versão, retenção e minimização; telemetria não essencial exige consentimento | 22.4 | 12. Integridade; 14. Risco regulatório |
| Cotação, conversões não aprovadas, pisos, limites, cooldowns, saque e cronograma ficam no documento financeiro | 21.1; 21.3–21.7; 24.5 | 15. Backlog |

## Propostas históricas descartadas ou não aprovadas

| Proposta do Founding Doc | Tratamento | Motivo |
|---|---|---|
| Saldo visível chamado “Ganhos” e originado também de prêmio, creator e bug bounty | Descartada como regra | O GDD define **Saldo** como crédito de venda quitada em Cash. Outras origens não foram aprovadas. |
| Fee agregado de Marketplace entre 8% e 15%, dividido entre listagem/comprador/vendedor | Superada | O GDD fixa taxa-base configurável de 10% sobre a liquidação. |
| Stablecoin como preço-base obrigatório e Pix 5%–10% mais caro | Não aprovada | O GDD permite compra de Cash por PIX ou cripto, mas reserva cotação e operação ao financeiro. |
| Saque depois de “período de liquidação” obrigatório e modelo de reserva específico | Hipótese operacional | O GDD exige liquidação atômica da venda e deixa disponibilidade, limites e operação de saque em aberto. Holds só podem ser definidos sem desfazer a venda. |
| Prize pool de 10%–25% do lucro distribuível | Não aprovada | O GDD não aprova percentual, fórmula contábil nem promessa de prêmio financeiro. |
| Planos VIP de 7/30 dias por 30/100 Cash | Não aprovada | O GDD vende VIP no Alpha/Beta e define benefícios, mas não fixa duração, preço ou rota financeira. |
| VIP com filas de crafting, auto-desmonte e inteligência de mercado | Parcialmente superada | O GDD define benefícios concretos; a Forja é instantânea e não tem filas. Benefícios não listados não entram. |
| Guildas, economia de guilda e premiação financeira coletiva | Não aprovada | Guildas não integram as regras centrais dos Pontos 1–22. |
| “FOMO como principal arma”, especulação e produto desenhado para ciclo curto | Descartada como princípio oficial | Contraria o tom e os limites de transparência exigidos; não é decisão econômica do GDD. |
| Mercado real somente na Season 1 e VIP gratuito no Alpha | Superada | O GDD vende VIP no Alpha e Beta e aplica os sistemas aprovados tão cedo quanto viável. |
| Market Balance como saldo/moeda | Descartada | O GDD define somente Gold, Cash e Saldo. |
| Referral e creators pagos em Cash | Não aprovada | Ausente do GDD. Pode voltar apenas por decisão posterior explícita. |
| Venda direta de moeda local ou ponte Cash↔Gold | Não aprovada | O GDD proíbe conversão automática e reserva qualquer rota futura ao documento financeiro. |
| Itens genéricos “negociáveis por valor real” | Não aprovada por categoria | O GDD exige liberação gradual e regras específicas de elegibilidade. |

## Registro da dupla revisão por capítulo

| Capítulo público | Revisão de autoridade | Revisão de operação |
|---|---|---|
| 1. Autoridade | Aprovado: hierarquia explícita; nenhuma proposta histórica tratada como decisão. | Aprovado: legenda diferencia regra, parâmetro, hipótese e pendência. |
| 2. Arquitetura | Aprovado: Gold local; Cash/Saldo globais; sem inventário cross-game. | Aprovado: fronteiras de ledger e contabilidade por `game_id` são explícitas. |
| 3. Saldos | Aprovado: origens/destinos não ampliam os Pontos 21–22. | Aprovado: buckets preservam direitos, reservas e proveniência. |
| 4. Ledger | Aprovado: atomicidade/idempotência derivam dos Pontos 7, 9, 14, 18, 19 e 21. | Aprovado: invariantes, envelope de evento e compensações são implementáveis. |
| 5. Marketplace | Aprovado: Gold/Cash/duplo, 10%, 90% e Saldo fiéis ao Ponto 21.2. | Aprovado: lock, concorrência, recibo e rollback sem efeito parcial descritos. |
| 6. Trade | Aprovado: sete dias, mediana 10/14, 50%, custódia e fee em Cash preservados. | Aprovado: fallback, comparabilidade e contribuição de fee tratados como pendências. |
| 7. Conversão/saque | Aprovado: 5%, KYC inicial, cripto/stablecoin e fee de rede separada. | Aprovado: fluxo é hipótese identificada; sem promessa, prazo ou conclusão jurídica. |
| 8. Ativos | Aprovado: estados, vínculos e liberações por categoria não são ampliados. | Aprovado: cada ativo informa dados transferidos, bloqueio e estado de liberação. |
| 9. Equilíbrio | Aprovado: fontes/sinks não recebem moedas que o GDD não atribui. | Aprovado: indicadores distinguem recurso, moeda, estoque, liquidez e concentração. |
| 10. Sistemas | Aprovado: Cultivo, Forja, PvE, PvP, temporada e VIP seguem seus pontos. | Aprovado: efeitos econômicos e parâmetros em aberto ficam separados. |
| 11. Alpha/Beta | Aprovado: resets, 130%/120% e todas as exclusões foram preservados. | Aprovado: buckets, replay e não duplicação tornam o crédito auditável. |
| 12. Integridade | Aprovado: controles adicionais são hipóteses, não novas regras de gameplay. | Aprovado: duplicação, multiaccount, wash trading, chargeback e abuso têm resposta. |
| 13. Governança | Aprovado: telemetria de servidor/cliente e limites de privacidade seguem o Ponto 22. | Aprovado: eventos, painéis, publicação versionada e rollback foram definidos. |
| 14. Risco | Aprovado: fontes externas aparecem como sensores, nunca como aprovação. | Aprovado: gate jurídico/tributário/contábil/privacidade impede ativação prematura. |
| 15. Backlog | Aprovado: pendências correspondem ao Ponto 24.5 ou números reservados. | Aprovado: cada item declara motivo, impacto e decisão que o fecha. |
| 16. Rastreabilidade | Aprovado: mapa cobre os Pontos 1–22 economicamente relevantes. | Aprovado: ligação tema→ponto facilita auditoria editorial. |
| 17. Glossário | Aprovado: definições não criam direitos nem alteram fórmulas. | Aprovado: termos técnicos são legíveis para produto, engenharia e operação. |

## Fontes regulatórias consultadas

Estas fontes são sensores de risco, não parecer jurídico nem aprovação de operação:

- Lei nº 14.478/2022 e Decreto nº 11.563/2023;
- Resoluções BCB nº 520 e nº 521, de 2025, em vigor desde 2 de fevereiro de 2026;
- IN RFB nº 2.291/2025 e materiais DeCripto;
- atualização FATF de 2025 sobre ativos virtuais e VASPs;
- LGPD e guias da ANPD.
