# projeto_final_dio_formacao_bob

Projeto final da Formação IBM Bob na DIO — **DIO Explorer**.

Plataforma educacional que permite explorar trilhas de aprendizagem, gerar desafios de código e emitir certificados fictícios — tudo via slash commands do IBM Bob e um servidor MCP customizado.

## Funcionalidades

| Comando | Descrição |
|---|---|
| `/trilha <tecnologia>` | Plano de estudos formatado de qualquer trilha do catálogo |
| `/desafio <nivel> <tecnologia>` | Desafio de código original, calibrado por nível |
| `/certificado <nome> <trilha>` | Certificado fictício com ID único e badges |

Além dos slash commands, o projeto expõe um **servidor MCP** (`dio-explorer-mcp`) que integra as mesmas funcionalidades diretamente como ferramentas de IA no Bob.

## Documentação completa

📄 **[dio_explorer/docs/PROJETO_DOCUMENTACAO_COMPLETA.md](dio_explorer/docs/PROJETO_DOCUMENTACAO_COMPLETA.md)**

Contém:
- Arquitetura e estrutura de arquivos
- Modos de uso do IBM Bob (Agent, Plan, Ask)
- Histórico completo de todos os prompts utilizados
- Slash commands com sintaxe e exemplos
- Documentação do servidor MCP (ferramentas, recursos, prompt)
- Resultados dos testes unitários (73 testes · 100% aprovados · 98% cobertura)
- Dicas de uso
- Insights para futuros profissionais

## Quick start

```bash
# Build do servidor MCP
cd dio_explorer/mcp
npm install && npm run build

# Testes unitários
cd ../..
pytest dio_explorer/tests/ -v
```

## Stack

- **IBM Bob** — copiloto de IA principal
- **TypeScript / Node.js 18+** — servidor MCP
- **@modelcontextprotocol/sdk** — protocolo MCP
- **Python 3 / pytest** — testes unitários
- **JSON** — catálogo de 32 trilhas DIO
