# Idle Lovers — matriz interna de rastreabilidade tecnológica

Atualizado em 28 de julho de 2026.

Este arquivo é material interno de revisão. A página pública canônica é
`technology-source/index.html`.

## Hierarquia de autoridade

1. `gdd-source/index.html` e o GDD publicado definem produto, gameplay, estados,
   resultados e limites que a tecnologia precisa preservar.
2. `economy-source/index.html` operacionaliza os invariantes financeiros
   aprovados pelo GDD.
3. `D:\_Idle Lovers\idle_lovers_technology_guidelines.html` define a direção
   técnica proposta pelos fundadores onde ela não conflita com as duas fontes
   anteriores.
4. Documentação oficial de tecnologias e padrões atuais é usada para verificar
   viabilidade e formular controles, sem transformar versão, fornecedor ou
   serviço ainda não escolhido em decisão aprovada.

## Matriz de decisões

| Decisão ou obrigação | Evidência | Seção pública |
|---|---|---|
| GDD e Economia vencem conflitos técnicos | GDD P1–24; Economia 1 e 16 | 1. Autoridade |
| Simplicidade, servidor autoritativo, multi-game e tecnologia por necessidade | Fonte técnica §§2 e 11 | 2. Princípios |
| Monólito modular antes de microserviços | Inferência operacional conservadora da fonte técnica §§3–4 e 11 | 3. Arquitetura |
| TypeScript como linguagem padrão | Fonte técnica §§3, 5 e 12 | 4. Stack |
| Node.js apenas em linha LTS suportada | Fonte técnica §3 + política oficial do Node.js | 4. Stack |
| Phaser como padrão recomendado para o cliente 2D web | Fonte técnica §§3 e 12; Phaser oficial | 4 e 12 |
| PostgreSQL como banco transacional recomendado | Fonte técnica §§3 e 12 | 4 e 8 |
| `game-core` puro, determinístico e sem dependência de UI/banco | Fonte técnica §4.2; GDD P8, P9 e P19 | 5 e 7 |
| Isolamento por `game_id`, ambiente, temporada e ruleset | Fonte técnica §§2 e 7; GDD P19 e P22 | 5, 8 e 11 |
| Cliente envia intenção; servidor valida, calcula e persiste | Fonte técnica §6; GDD P4–P22 | 6 |
| Seeds oficiais nascem no servidor e resultados são reproduzíveis | Fonte técnica §6.1; GDD P8, P14, P19 | 7 |
| Resultados de gameplay independem de duração de animação | GDD P8 e P19 | 7 e 12 |
| Dinheiro usa inteiro na menor unidade ou decimal exato | Fonte técnica §5.2; Economia 3–4 | 8 e 9 |
| Saldo, item e propriedade protegidos também por constraints/transações | Fonte técnica §§7 e 10; Economia 4–6 | 8–10 |
| Ledger é append-only; correção é compensatória | Fonte técnica §§9.3 e 10; Economia 4 e 12 | 9 |
| Marketplace e Trade liquidam de forma atômica e idempotente | GDD P21; Economia 5–6 | 9 e 10 |
| Comandos mutáveis usam autenticação, autorização e chave idempotente | Fonte técnica §10; Economia 4 e 12 | 10 |
| Configuração crítica é versionada, revisada, publicada e reversível | Fonte técnica §7; GDD P24; Economia 13 | 11 |
| Pixel art segue constituição visual e proveniência de asset | Fonte técnica §8 | 12 e 17 |
| Segredos não entram no cliente, repositório ou artefato | Fonte técnica §10; OWASP ASVS 5.0 | 13 e 16 |
| Telemetria de servidor prova resultado; cliente explica UX | GDD P22; Economia 13 | 15 |
| Privacidade por desenho, finalidade, minimização e retenção | GDD P22; Economia 13–14 | 13 e 15 |
| Testes de domínio, integração, contrato, concorrência e replay | Fonte técnica §10; GDD P19; Economia 12 | 14 |
| Logs estruturados, métricas, traces, alertas e auditoria | Fonte técnica §10; GDD P19/P22; Economia 12–13 | 15 |
| Build reprodutível, dependências fixadas, SBOM e proveniência | Extensão operacional baseada em GitHub, SPDX e SLSA oficiais | 16–17 |
| Open source acelera componentes, mas não terceiriza invariantes | Fonte técnica §9 | 17 |
| Nova linguagem, cache, fila ou serviço exige problema medido e ADR | Fonte técnica §11 | 18 |
| Detalhes de fornecedor, versões, SLOs e operação ficam abertos | Ausência de aprovação na fonte técnica/GDD/Economia | 19 |

## Correções e exclusões da fonte técnica original

| Texto ou ideia histórica | Tratamento |
|---|---|
| “Ganhos” como saldo financeiro | Substituído por `Saldo`, termo aprovado pelo GDD P21 e pela Economia. |
| Guildas na interface e no módulo web | Removidas do escopo; o GDD não aprovou guildas. |
| “Todos os jogos serão 2D em pixel art” | Mantido como direção da plataforma apresentada pela fonte técnica, sem alterar gameplay do GDD nem prometer catálogo futuro. |
| PixelLab.ai como ferramenta central | Mantido como padrão recomendado de produção, sujeito a contrato, licença, segurança, custo e qualidade; não como dependência de runtime. |
| Phaser como framework definido | Classificado como padrão recomendado, condicionado a spike de desempenho, pipeline de assets e replays; a direção 2D web continua aceita. |
| PostgreSQL como fonte central | Classificado como padrão recomendado; a obrigação é um armazenamento transacional que preserve constraints, histórico e auditoria. |
| Ledger e marketplace “próprios” | Interpretado como domínio e invariantes controlados pela Idle Lovers. Bibliotecas e provedores auditados podem ser usados sem entregar a autoridade econômica a uma caixa-preta. |
| GPL/AGPL/MPL por regra simples | Mantido apenas como sinal de revisão. Compatibilidade e obrigações precisam de análise caso a caso; este documento não dá parecer jurídico. |
| `Math.random()` permitido no cliente | Restrito a efeitos puramente visuais. Nunca decide estado oficial ou valor. |
| Electron/Tauri posteriormente | Mantido como rota ainda não aprovada; depende de necessidade de distribuição e operação. |

## Referências técnicas primárias verificadas

- TypeScript `strict`: <https://www.typescriptlang.org/tsconfig/strict.html>
- Ciclo de suporte do Node.js:
  <https://nodejs.org/en/about/previous-releases>
- Mudança do calendário Node.js a partir da linha 27:
  <https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule>
- Phaser oficial: <https://docs.phaser.io/>
- PostgreSQL — tipos numéricos:
  <https://www.postgresql.org/docs/current/datatype-numeric.html>
- PostgreSQL — constraints:
  <https://www.postgresql.org/docs/current/ddl-constraints.html>
- PostgreSQL — isolamento:
  <https://www.postgresql.org/docs/current/transaction-iso.html>
- OWASP ASVS 5.0:
  <https://owasp.org/www-project-application-security-verification-standard/>
- OpenTelemetry JavaScript:
  <https://opentelemetry.io/docs/languages/js/>
- SPDX: <https://spdx.dev/>
- SLSA 1.2: <https://slsa.dev/spec/v1.2/>
- GitHub Actions — proteção contra ameaças:
  <https://docs.github.com/en/code-security/tutorials/secure-your-organization/protect-against-threats>
- GitHub Actions — OIDC:
  <https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers>

## Dupla revisão por capítulo

| Capítulo | Autoridade | Operação |
|---|---|---|
| 1 | GDD/Economia acima da tecnologia | Critério de conflito e mudança explícito |
| 2 | Preserva os quatro princípios da fonte | Guardrails testáveis e sem tecnologia por moda |
| 3 | Não inventa fornecedor ou microserviço | Fronteiras, transações e extração gradual claras |
| 4 | TypeScript definido; Phaser/PostgreSQL recomendados | Política LTS, pin e spike explícitos |
| 5 | Módulos seguem domínios aprovados | Dependências e contratos evitam acoplamento |
| 6 | Replica autoridade do GDD | Trust boundaries e autorização implementáveis |
| 7 | Preserva seeds, snapshots e replays | Determinismo, relógio e precisão auditáveis |
| 8 | Não cria novo saldo ou ativo | Constraints, migração e backup previstos |
| 9 | Replica Economia sem reinterpretar fee | Ledger, atomicidade e compensação executáveis |
| 10 | Não altera fluxos de produto | Idempotência e concorrência com estados finais |
| 11 | Configura somente parâmetros permitidos | Publicação, diff, aprovação e rollback |
| 12 | Não adiciona mecânica cliente | Phaser isolado da verdade do domínio |
| 13 | Não promete conformidade | Threat model, segredos e privacidade previstos |
| 14 | Testa regras existentes | Pirâmide de testes, concorrência e replay |
| 15 | Respeita telemetria do P22 | Sinais, correlação, alertas e retenção |
| 16 | Não escolhe cloud | Pipeline com mínimo privilégio e proveniência |
| 17 | Não dá parecer de licença | Inventário, revisão e remoção operacional |
| 18 | Mantém evolução sob demanda | Métrica, ADR, ownership e rollback exigidos |
| 19 | Só inclui decisões realmente ausentes | Cada item traz motivo, impacto e fechamento |
| 20 | Liga obrigações às fontes | Matriz pública suficiente para auditoria |
| 21 | Termos não criam decisões | Vocabulário consistente com GDD/Economia |
