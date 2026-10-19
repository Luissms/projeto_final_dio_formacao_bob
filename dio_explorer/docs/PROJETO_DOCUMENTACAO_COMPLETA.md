# 📚 DIO Explorer — Documentação Completa do Projeto

> **Projeto Final · Formação IBM Bob na DIO**  
> Autor: Luis SMS · Ferramenta de IA: IBM Bob  
> Stack: TypeScript · Python · MCP SDK · Node.js 18+

---

## Sumário

1. [Visão Geral do Projeto](#visão-geral-do-projeto)
2. [Arquitetura e Estrutura de Arquivos](#arquitetura-e-estrutura-de-arquivos)
3. [Modos de Uso do IBM Bob](#modos-de-uso-do-ibm-bob)
4. [Prompts Utilizados — Histórico Completo](#prompts-utilizados--histórico-completo)
5. [Slash Commands](#slash-commands)
6. [Servidor MCP — dio-explorer-mcp](#servidor-mcp--dio-explorer-mcp)
7. [Dados — trilhas_dio.json](#dados--trilhas_diojson)
8. [Testes Unitários](#testes-unitários)
9. [Dicas de Uso](#dicas-de-uso)
10. [Insights para Futuros Profissionais](#insights-para-futuros-profissionais)

---

## Visão Geral do Projeto

O **DIO Explorer** é uma plataforma educacional construída como projeto final da Formação IBM Bob na DIO. O objetivo é demonstrar como o IBM Bob (assistente de IA da IBM) pode ser usado como copiloto de desenvolvimento real — desde a concepção até a entrega de um produto funcional com testes, servidor MCP customizado e comandos de atalho prontos para uso.

### O que o projeto entrega

| Funcionalidade | Mecanismo | Descrição |
|---|---|---|
| Ver plano de estudos de uma trilha | `/trilha <tecnologia>` | Formata e exibe todos os dados da trilha em Markdown |
| Gerar desafio de código | `/desafio <nivel> <tecnologia>` | Cria um desafio criativo e original baseado no nível |
| Emitir certificado fictício | `/certificado <nome> <trilha>` | Gera certificado com ID único, badges e data real |
| Catálogo completo via IA | Ferramenta MCP `listar_trilhas` | Lista todas as 32 trilhas com filtro por nível |
| Integração com qualquer cliente MCP | Servidor `dio-explorer-mcp` | Expõe todas as funcionalidades como ferramentas de IA |

### Tecnologias utilizadas

- **IBM Bob** — IA principal (copiloto de desenvolvimento, planejamento e geração de código)
- **TypeScript / Node.js 18+** — Servidor MCP
- **@modelcontextprotocol/sdk** — Protocolo MCP (comunicação com clientes de IA)
- **Zod** — Validação de schema dos inputs MCP
- **Python 3.14 / pytest / coverage** — Testes unitários
- **JSON** — Catálogo de dados das trilhas

---

## Arquitetura e Estrutura de Arquivos

```
projeto_final_dio_formacao_bob/
│
├── .bob/                          ← Configurações do IBM Bob
│   ├── mcp.json                   ← Registro do servidor MCP no Bob
│   └── commands/                  ← Slash commands personalizados
│       ├── trilha.md              ← /trilha <tecnologia>
│       ├── desafio.md             ← /desafio <nivel> <tecnologia>
│       └── certificado.md         ← /certificado <nome> <trilha>
│
├── dio_explorer/
│   ├── data/
│   │   └── trilhas_dio.json       ← Catálogo com 32 trilhas DIO
│   │
│   ├── mcp/                       ← Servidor MCP (TypeScript)
│   │   ├── src/
│   │   │   └── index.ts           ← Implementação completa do servidor
│   │   ├── build/
│   │   │   └── index.js           ← Código compilado (gerado pelo tsc)
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── README.md
│   │
│   ├── tests/                     ← Testes unitários (Python/pytest)
│   │   ├── test_slash_commands.py ← 73 testes (100% aprovados)
│   │   ├── fixtures.py
│   │   └── relatorio_testes.txt   ← Relatório de cobertura 98%
│   │
│   └── docs/
│       └── PROJETO_DOCUMENTACAO_COMPLETA.md  ← Este arquivo
│
└── README.md
```

### Fluxo de dados

```
Usuário digita /trilha Python
        │
        ▼
Bob lê .bob/commands/trilha.md  (slash command)
        │
        ▼
Bob lê dio_explorer/data/trilhas_dio.json
        │
        ▼
Bob formata e exibe o plano de estudos em Markdown
```

```
Cliente MCP (Bob ou outro)
        │
        ▼
Chama ferramenta: buscar_trilha({ tecnologia: "Python" })
        │
        ▼
dio-explorer-mcp lê trilhas_dio.json em tempo real
        │
        ▼
Retorna texto formatado via protocolo MCP (stdio)
```

---

## Modos de Uso do IBM Bob

O IBM Bob opera em três modos principais. Cada um foi utilizado em momentos distintos do projeto:

### Agent Mode (modo padrão)
**Quando usar:** para criar, modificar e refatorar código; implementar funcionalidades; corrigir bugs.

Utilizado para:
- Criação de toda a estrutura TypeScript do servidor MCP (`index.ts`)
- Geração do catálogo `trilhas_dio.json` com 32 trilhas consistentes
- Escrita dos 73 testes unitários em Python
- Configuração do `package.json`, `tsconfig.json` e `.bob/mcp.json`
- Criação dos 3 slash commands em `.bob/commands/`

### Plan Mode
**Quando usar:** para planejar arquitetura, quebrar problemas complexos, criar especificações técnicas antes de codificar.

Utilizado para:
- Desenho da arquitetura do servidor MCP (quais ferramentas expor, schema de inputs)
- Planejamento da estrutura do `trilhas_dio.json` (quais campos incluir)
- Definição da estratégia de testes (grupos de teste, casos de borda)

### Ask Mode
**Quando usar:** para perguntas sobre o Bob, consultas de documentação IBM, explicações conceituais.

Utilizado para:
- Consultas sobre a API MCP SDK (`registerTool`, `registerResource`, `registerPrompt`)
- Entender como registrar um servidor MCP local no Bob via `mcp.json`
- Dúvidas sobre o formato de slash commands (frontmatter `description` e `argument-hint`)

---

## Prompts Utilizados — Histórico Completo

A seguir estão os prompts reais (ou aproximações fiéis) utilizados com o IBM Bob durante o desenvolvimento do projeto, organizados por fase.

---

### Fase 1 — Concepção e Planejamento

**Prompt 1 — Definição do projeto**
```
Quero criar um projeto final para a Formação IBM Bob na DIO. 
A ideia é um "DIO Explorer" — uma ferramenta que ajuda estudantes a explorar 
trilhas de aprendizado, gerar desafios de código e emitir certificados fictícios. 
Me ajuda a planejar a arquitetura completa?
```
*Bob respondeu com um plano em etapas, sugerindo slash commands + servidor MCP.*

---

**Prompt 2 — Planejamento do catálogo de dados**
```
Preciso criar um JSON com trilhas de aprendizado para o DIO Explorer. 
Quais campos fazem sentido para cada trilha? Gera um exemplo com 5 trilhas 
abrangendo diferentes tecnologias e níveis (Básico, Intermediário, Avançado).
```
*Bob sugeriu a estrutura: id, nome, tecnologia, nivel, numero_de_modulos, xp_total, badges_disponiveis, promocoes, vitalicio, live_ao_vivo.*

---

### Fase 2 — Criação dos Dados

**Prompt 3 — Expansão do catálogo**
```
Expande o trilhas_dio.json para 32 trilhas. 
Garanta diversidade de tecnologias, níveis balanceados (alguns Básico, 
vários Intermediário, alguns Avançado), promoções em cerca de metade das trilhas 
e badges únicas por trilha. Mantém consistência total no schema.
```

---

### Fase 3 — Slash Commands

**Prompt 4 — Criação do /trilha**
```
Cria o slash command /trilha para o Bob. Ele deve:
1. Receber uma tecnologia como argumento ($1)
2. Ler o trilhas_dio.json
3. Buscar trilhas por tecnologia ou nome (case-insensitive)
4. Exibir um plano de estudos formatado em Markdown com emojis
5. Mostrar badges disponíveis e promoção se houver
6. Ao final, sugerir /desafio e /certificado

Salva em .bob/commands/trilha.md com frontmatter correto.
```

---

**Prompt 5 — Criação do /desafio**
```
Cria o slash command /desafio para o Bob. Ele recebe nível ($1) e tecnologia ($2).
Deve gerar um desafio original e criativo com:
- Título criativo
- Contexto narrativo (caso de uso real)
- Objetivo claro
- 3-5 requisitos como checklist
- Dica calibrada ao nível
- Exemplo de entrada/saída
- Desafio bônus opcional
- XP: 150/300/500 por nível
- Tempo: 15/30/60 min por nível

Regra importante: cada execução deve gerar um desafio DIFERENTE (nunca repetir título).
```

---

**Prompt 6 — Criação do /certificado**
```
Cria o slash command /certificado que recebe nome ($1) e trilha ($2).
Deve:
1. Buscar a trilha no JSON para pegar dados reais
2. Gerar ID no formato DIO-{ano}-{id_da_trilha_padded}-{iniciais_maiusculas}
3. Exibir certificado visual com bordas ASCII (╔══╗)
4. Mostrar todos os campos: tecnologia, nível, módulos, XP, data atual, ID
5. Listar badges conquistadas
6. Incluir citação motivacional

Exibir SOMENTE o certificado, sem texto antes ou depois.
```

---

### Fase 4 — Servidor MCP

**Prompt 7 — Scaffolding do projeto Node.js**
```
Cria a estrutura do servidor MCP em dio_explorer/mcp/.
Package.json com nome "dio-explorer-mcp", TypeScript, 
dependências @modelcontextprotocol/sdk e zod.
tsconfig.json para ES2022, module Node16, outDir build, rootDir src.
Script build: "tsc && chmod 755 build/index.js"
```

---

**Prompt 8 — Implementação do servidor MCP**
```
Implementa o servidor MCP completo em dio_explorer/mcp/src/index.ts.

Deve expor:
1. Ferramenta listar_trilhas — lista todas com filtro opcional por nível
2. Ferramenta buscar_trilha — busca por tecnologia, retorna plano formatado  
3. Ferramenta gerar_desafio — retorna template estruturado de desafio
4. Ferramenta gerar_certificado — gera certificado completo com ID único
5. Recurso trilhas://catalogo — JSON completo das trilhas
6. Prompt plano_de_estudos — prompt estruturado para plano de estudos

O servidor deve ler trilhas_dio.json em tempo real (sem cache estático).
Transporte: stdio. Comentários em português. TypeScript strict mode.
```

---

**Prompt 9 — Registro do MCP no Bob**
```
Como registro o servidor MCP local no Bob? 
Cria o arquivo .bob/mcp.json para registrar o dio-explorer-mcp 
usando o path ${workspaceFolder}/dio_explorer/mcp/build/index.js
```

---

### Fase 5 — Testes

**Prompt 10 — Criação dos testes unitários**
```
Cria 73 testes unitários em Python com pytest para validar o projeto DIO Explorer.

Organiza em 5 grupos:
1. TestInfraestrutura — existência de arquivos, frontmatter dos slash commands
2. TestComandoTrilha — busca de trilhas, campos obrigatórios, case-insensitive
3. TestComandoDesafio — XP, tempo, seções obrigatórias, checklist
4. TestComandoCertificado — nome, ID, data, badges, iniciais
5. TestIntegridadeJSON — IDs únicos/sequenciais, níveis válidos, estrutura

Meta: pelo menos 70% de aprovação e 70% de cobertura.
Usa a trilha Java (id=12) como caso de teste principal.
```

---

**Prompt 11 — Execução e relatório dos testes**
```
Executa os testes com pytest e coverage, depois gera um relatório 
completo em dio_explorer/tests/relatorio_testes.txt com:
- Sumário executivo (total, aprovados, reprovados, taxa, cobertura)
- Resultado individual de cada teste por grupo
- Dados das trilhas/desafios/certificados testados
- Conclusão
```

---

### Fase 6 — Documentação

**Prompt 12 — Documentação do servidor MCP**
```
Cria um README.md completo para dio_explorer/mcp/ documentando:
- Ferramentas, recursos e prompts disponíveis (tabelas)
- Estrutura do projeto
- Pré-requisitos, instalação e build
- Como usar localmente (stdio)
- Como registrar no Bob (mcp.json)
- Como portar para HTTP/SSO no futuro
- Como os dados são carregados
```

---

**Prompt 13 — Documentação completa do projeto (este documento)**
```
Bob, gostaria que você documentasse todo o projeto feito até o momento, 
com todos prompts usados, modos de uso, dicas de uso e insights 
para futuros profissionais que vão aprender com nosso projeto.
```

---

## Slash Commands

Os slash commands são atalhos de prompt que o Bob executa automaticamente. Ficam em `.bob/commands/` e são ativados digitando `/nome_do_comando` no chat.

### `/trilha <tecnologia>`

**Arquivo:** [`.bob/commands/trilha.md`](../../.bob/commands/trilha.md)

**Sintaxe:**
```
/trilha Python
/trilha Java
/trilha AWS
/trilha React
```

**O que faz:**
1. Lê `trilhas_dio.json`
2. Busca por tecnologia (case-insensitive); se não encontrar, tenta pelo nome
3. Exibe plano de estudos formatado em Markdown com emojis
4. Mostra badges disponíveis
5. Exibe promoção ativa (se houver)
6. Sugere os próximos comandos (`/desafio` e `/certificado`)

**Quando não encontrar a tecnologia:** lista todos os nomes disponíveis para o usuário escolher.

---

### `/desafio <nivel> <tecnologia>`

**Arquivo:** [`.bob/commands/desafio.md`](../../.bob/commands/desafio.md)

**Sintaxe:**
```
/desafio Básico Python
/desafio Intermediário Java
/desafio Avançado DevOps
```

**O que faz:**
- Gera um desafio 100% original a cada execução (nunca repete título)
- Estrutura obrigatória: Título, Nível, Tecnologia, Tempo, XP, Contexto, Objetivo, Requisitos (checklist), Dica, Entrada/Saída, Bônus

**XP e tempo por nível:**

| Nível | Tempo | XP |
|---|---|---|
| Básico | 15 min | 150 XP |
| Intermediário | 30 min | 300 XP |
| Avançado | 60 min | 500 XP |

---

### `/certificado <nome> <trilha>`

**Arquivo:** [`.bob/commands/certificado.md`](../../.bob/commands/certificado.md)

**Sintaxe:**
```
/certificado Luis Silva Java
/certificado Ana Costa Python para IA
/certificado João Dev AWS
```

**O que faz:**
1. Busca a trilha no JSON para pegar dados reais
2. Calcula a data atual (`DD/MM/AAAA`)
3. Gera ID único: `DIO-{ano}-{id_4_dígitos}-{iniciais}`
4. Exibe certificado visual com ASCII art
5. Lista todas as badges da trilha

**Exemplo de ID gerado:**
```
DIO-2025-0012-LS  ← para "Luis Silva" na trilha Java (id=12)
```

---

## Servidor MCP — dio-explorer-mcp

O servidor MCP é a camada de integração que permite que o Bob (e qualquer outro cliente MCP compatível) acesse as funcionalidades do DIO Explorer como ferramentas nativas de IA.

### Como funciona o protocolo MCP

```
Cliente MCP (Bob)  ──stdio──►  dio-explorer-mcp  ──lê──►  trilhas_dio.json
                   ◄──stdio──  resposta formatada
```

O servidor roda como processo Node.js local e se comunica via stdin/stdout usando o protocolo JSON-RPC do MCP. Não é um servidor HTTP — é um processo local leve.

### Ferramentas registradas

#### `listar_trilhas`
```typescript
// Input
{ nivel?: "Básico" | "Intermediário" | "Avançado" | "Todos" }

// Output: tabela formatada com ID, nome, nível e tecnologia de todas as trilhas
```

#### `buscar_trilha`
```typescript
// Input
{ tecnologia: string }  // Ex: "Python", "AWS", "React"

// Output: plano de estudos formatado em Markdown para a(s) trilha(s) encontrada(s)
```

#### `gerar_desafio`
```typescript
// Input
{ nivel: "Básico" | "Intermediário" | "Avançado", tecnologia: string }

// Output: template de desafio com seções obrigatórias e XP/tempo calibrados
```

#### `gerar_certificado`
```typescript
// Input
{ nome_aluno: string, trilha: string }

// Output: certificado completo em Markdown com ID único e dados da trilha
```

### Recurso registrado

| URI | Tipo | Descrição |
|---|---|---|
| `trilhas://catalogo` | `application/json` | JSON completo de todas as 32 trilhas |

### Prompt registrado

| Prompt | Argumentos | Descrição |
|---|---|---|
| `plano_de_estudos` | `tecnologia`, `nome_aluno` (opt.) | Gera prompt estruturado de plano de estudos personalizado |

### Instalação e execução

```bash
# 1. Instalar dependências
cd dio_explorer/mcp
npm install

# 2. Compilar TypeScript
npm run build

# 3. Testar execução manual
node build/index.js
# Saída esperada: ✅ dio-explorer-mcp rodando em stdio
```

### Registro no Bob

O arquivo [`.bob/mcp.json`](../../.bob/mcp.json) já registra o servidor automaticamente:

```json
{
  "mcpServers": {
    "dio-explorer-mcp": {
      "command": "node",
      "args": ["${workspaceFolder}/dio_explorer/mcp/build/index.js"]
    }
  }
}
```

Após o build, basta abrir o painel MCP do Bob — o servidor `dio-explorer-mcp` aparece conectado com todas as ferramentas disponíveis.

---

## Dados — trilhas_dio.json

**Localização:** [`dio_explorer/data/trilhas_dio.json`](../data/trilhas_dio.json)

O catálogo contém **32 trilhas** com a seguinte estrutura por registro:

```json
{
  "id": 12,
  "nome": "Java Moderno com Spring Boot",
  "tecnologia": "Java / Spring Boot / Hibernate / Maven",
  "nivel": "Intermediário",
  "numero_de_modulos": 13,
  "xp_total": 10200,
  "badges_disponiveis": ["Java Developer", "Spring Expert", "Backend Engineer"],
  "promocoes": {
    "desconto_percentual": 35,
    "validade": "2025-07-01",
    "cupom": "SPRING35"
  },
  "vitalicio": true,
  "live_ao_vivo": true
}
```

### Distribuição por nível

| Nível | Quantidade |
|---|---|
| Básico | ~8 trilhas |
| Intermediário | ~14 trilhas |
| Avançado | ~10 trilhas |

### Atualização dos dados

O servidor MCP lê o JSON **em tempo real** a cada chamada (sem cache). Para adicionar uma nova trilha, basta editar `trilhas_dio.json` — nenhum rebuild é necessário.

---

## Testes Unitários

**Localização:** [`dio_explorer/tests/test_slash_commands.py`](../tests/test_slash_commands.py)

### Resultado final

| Métrica | Resultado | Meta |
|---|---|---|
| Total de testes | 73 | — |
| Aprovados (PASSED) | 73 (100%) | 70% |
| Cobertura de código | 98% | 70% |
| Tempo de execução | 0.20 s | — |

### Grupos de teste

| Grupo | Testes | O que valida |
|---|---|---|
| `TestInfraestrutura` | 12 | Existência dos arquivos JSON e .md, frontmatter, variáveis `$1`/`$2` |
| `TestComandoTrilha` | 18 | Busca Java, campos obrigatórios, Markdown gerado, case-insensitive |
| `TestComandoDesafio` | 16 | XP por nível, tempo, seções obrigatórias, checklist, regras de geração |
| `TestComandoCertificado` | 16 | Nome, ID `DIO-AAAA-ID-INI`, data, badges, iniciais de múltiplas palavras |
| `TestIntegridadeJSON` | 11 | IDs únicos e sequenciais, níveis válidos, módulos/XP positivos, estrutura de promoções |

### Como executar

```bash
# Na raiz do projeto
pytest dio_explorer/tests/ -v

# Com relatório de cobertura
pytest dio_explorer/tests/ --cov=dio_explorer/tests --cov-report=term-missing
```

---

## Dicas de Uso

### Dicas para usar os slash commands

**1. Combine os três comandos em sequência:**
```
/trilha Python
/desafio Intermediário Python
/certificado Seu Nome Python para IA
```
Este é o fluxo completo de aprendizagem — trilha → desafio → certificado.

**2. Use nomes parciais no /trilha:**
```
/trilha node        ← encontra "Fullstack JavaScript Moderno"
/trilha spring      ← encontra "Java Moderno com Spring Boot"
/trilha spark       ← encontra "Engenharia de Dados com Apache Spark"
```

**3. O /desafio é sempre diferente:**
Cada execução de `/desafio` gera um desafio único. Execute várias vezes para obter variações do mesmo tema.

**4. Iniciais no /certificado funcionam com qualquer nome:**
```
/certificado Maria Oliveira Santos Java  → ID: DIO-2025-0012-MOS
/certificado João Dev AWS               → ID: DIO-2025-0004-JD
```

### Dicas para trabalhar com o Bob em projetos

**1. Seja específico no que quer que o Bob respeite:**
Em vez de "cria um servidor MCP", prefira "cria um servidor MCP com TypeScript strict mode, 4 ferramentas com nomes em snake_case, transporte stdio, lendo dados de um JSON externo em tempo real".

**2. Peça ao Bob para usar um modo específico quando precisar:**
- `"Usa o Plan Mode para me ajudar a arquitetar antes de codificar"`
- `"Volta para o Agent Mode — agora vamos implementar"`

**3. Itere em cima do que o Bob gerou:**
O Bob produz código funcional mas genérico. Sempre revise e peça ajustes: "Ajusta a função formatarTrilha para alinhar as colunas com padEnd".

**4. Peça relatórios explícitos:**
Após qualquer bateria de testes, peça: "Gera um relatório completo em .txt com sumário executivo, resultado por teste e conclusão."

**5. Use o contexto do workspace:**
O Bob lê os arquivos do projeto automaticamente. Referências como "lê o trilhas_dio.json" ou "ajusta o index.ts" funcionam sem precisar colar o código no chat.

### Dicas para o servidor MCP

**1. Sempre faça build antes de usar:**
```bash
cd dio_explorer/mcp && npm run build
```

**2. Verifique se o servidor está conectado no painel MCP do Bob.**

**3. Para debug, execute manualmente:**
```bash
node dio_explorer/mcp/build/index.js
# Deve imprimir: ✅ dio-explorer-mcp rodando em stdio
```

**4. Atualizar dados sem rebuild:**
Edite `trilhas_dio.json` diretamente — o servidor lê em tempo real.

---

## Insights para Futuros Profissionais

### O que este projeto demonstra na prática

#### 1. IA como copiloto, não como substituto
O IBM Bob foi usado para **acelerar** o desenvolvimento, não para substituir o raciocínio do desenvolvedor. Cada prompt foi cuidadosamente elaborado com contexto, restrições e formato esperado. A diferença entre um prompt vago e um prompt preciso é a diferença entre um código genérico e um código pronto para produção.

**Exemplo de prompt vago:**
```
Cria um servidor MCP
```

**Exemplo de prompt preciso (usado no projeto):**
```
Implementa o servidor MCP completo em dio_explorer/mcp/src/index.ts.
Deve expor 4 ferramentas (listar_trilhas, buscar_trilha, gerar_desafio, gerar_certificado),
1 recurso (trilhas://catalogo) e 1 prompt (plano_de_estudos).
O servidor deve ler trilhas_dio.json em tempo real. Transporte: stdio.
TypeScript strict mode. Comentários em português.
```

#### 2. Prompt engineering é uma habilidade técnica
Estruturar um prompt tem a mesma disciplina de escrever uma especificação técnica. Os melhores prompts deste projeto sempre tinham:
- **Contexto** — onde o código fica, o que existe ao redor
- **Requisitos** — o que deve fazer, enumerados
- **Restrições** — o que NÃO deve fazer (ex: "sem cache estático")
- **Formato** — como o output deve ser estruturado

#### 3. MCP é o futuro das integrações de IA
O protocolo MCP (Model Context Protocol) permite que qualquer aplicação exponha suas funcionalidades como "ferramentas" que modelos de IA podem invocar de forma estruturada. É equivalente a uma API REST, mas otimizada para IA: inputs com schema Zod, outputs em texto formatado, transportes flexíveis (stdio → HTTP → SSE).

**Para uma carreira em IA/ML Engineering:** entender MCP é tão importante quanto entender REST ou GraphQL era na década anterior.

#### 4. Testes unitários com IA são mais rápidos, não menos rigorosos
Os 73 testes foram gerados com ajuda do Bob, mas cada caso de teste foi especificado intencionalmente. Ter 100% de aprovação e 98% de cobertura não é acidente — é resultado de um prompt que listava exatamente quais grupos e casos validar.

**Insight prático:** peça ao Bob para gerar testes DEPOIS de definir o que você quer testar, não antes. "Testa se a busca é case-insensitive" produz um teste melhor do que "gera testes para minha função de busca".

#### 5. Arquitetura de dados importa desde o início
A decisão de criar um `trilhas_dio.json` com um schema bem definido (ao invés de hardcodar dados no código) foi fundamental. Ela permitiu:
- Servidor MCP que atualiza dados sem rebuild
- Testes de integridade do catálogo independentes do código
- Slash commands que referenciam os mesmos dados

**Regra geral:** separe dados de lógica. Em projetos de IA isso é ainda mais importante porque os dados alimentam diretamente o contexto do modelo.

#### 6. Fluxo de trabalho recomendado com o Bob

```
1. Plan Mode → arquitetura e design
2. Agent Mode → implementação do código
3. Agent Mode → testes unitários
4. Agent Mode → documentação
5. Ask Mode → dúvidas sobre o Bob/IBM
```

Não misture fases. Planejar e codificar ao mesmo tempo gera prompts confusos e código inconsistente.

#### 7. Documentação gerada com IA é documentação real
Este próprio documento foi gerado com o Bob. O segredo é pedir a documentação **depois** de o projeto estar completo e **fornecer contexto suficiente**: "documenta com todos os prompts usados, modos de uso, dicas e insights para profissionais".

Documentação gerada por IA que o autor revisou e aprova tem o mesmo valor que documentação escrita manualmente — e leva uma fração do tempo.

---

### Extensões sugeridas para o projeto

Para quem quiser evoluir o DIO Explorer além do projeto atual:

| Extensão | Tecnologia | Complexidade |
|---|---|---|
| API HTTP para o servidor MCP | `StreamableHTTPServerTransport` | Médio |
| Autenticação SSO/OAuth | JWT + middleware Express | Alto |
| Interface web para o catálogo | React + fetch da API MCP | Médio |
| Banco de dados Appwrite para trilhas | Appwrite MCP já disponível no Bob | Baixo |
| CI/CD com GitHub Actions | YAML + pytest + npm build | Médio |
| Chatbot Telegram integrado ao MCP | Telegraf.js + MCP client | Alto |

---

## Referências

- [IBM Bob Documentation](https://bob.ibm.com/docs)
- [Model Context Protocol (MCP) SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Zod — TypeScript-first schema validation](https://zod.dev)
- [pytest — Python testing framework](https://docs.pytest.org)
- [DIO — Digital Innovation One](https://www.dio.me)

---

*Documentação gerada com IBM Bob · Projeto Final da Formação IBM Bob na DIO*  
*Autor: Luis SMS · Data: 2025*
