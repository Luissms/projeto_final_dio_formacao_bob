# dio-explorer-mcp

Servidor MCP local para o projeto **DIO Explorer**, parte do Projeto Final da Formação IBM Bob na DIO.

Expõe trilhas de aprendizado, geração de desafios e emissão de certificados via protocolo MCP — permitindo que o Bob (e qualquer cliente MCP compatível) consuma as funcionalidades do projeto diretamente como ferramentas de IA.

---

## Ferramentas disponíveis

| Ferramenta           | Equivalente slash | Descrição                                                          |
|----------------------|-------------------|--------------------------------------------------------------------|
| `listar_trilhas`     | —                 | Lista todas as trilhas do catálogo com filtro opcional por nível   |
| `buscar_trilha`      | `/trilha`         | Busca trilhas por tecnologia ou nome e retorna o plano formatado   |
| `gerar_desafio`      | `/desafio`        | Gera a estrutura de um desafio de código por nível e tecnologia    |
| `gerar_certificado`  | `/certificado`    | Emite um certificado fictício de conclusão de trilha               |

## Recursos disponíveis

| URI                  | Tipo             | Descrição                                            |
|----------------------|------------------|------------------------------------------------------|
| `trilhas://catalogo` | application/json | JSON completo com as 32 trilhas do DIO Explorer      |

## Prompts disponíveis

| Prompt               | Argumentos                         | Descrição                                         |
|----------------------|------------------------------------|---------------------------------------------------|
| `plano_de_estudos`   | `tecnologia`, `nome_aluno` (opt.)  | Gera um prompt estruturado de plano de estudos    |

---

## Estrutura do projeto

```
dio_explorer/mcp/
├── src/
│   └── index.ts        ← implementação do servidor
├── build/              ← gerado após npm run build
│   └── index.js
├── package.json
├── tsconfig.json
└── README.md
```

---

## Pré-requisitos

- Node.js >= 18
- npm >= 9

---

## Instalação e build

```bash
cd dio_explorer/mcp
npm install
npm run build
```

---

## Uso local (stdio)

Após o build, execute diretamente:

```bash
node build/index.js
```

O servidor aguarda mensagens MCP no stdin e responde no stdout.

---

## Registro no Bob (mcp.json)

O servidor já está registrado em `.bob/mcp.json` (escopo do projeto).  
Para verificar, abra o painel MCP do Bob — o servidor `dio-explorer-mcp` deve aparecer como conectado.

Para registrar manualmente ou em outro ambiente, adicione ao `mcp.json`:

```json
{
  "mcpServers": {
    "dio-explorer-mcp": {
      "command": "node",
      "args": ["/caminho/absoluto/para/dio_explorer/mcp/build/index.js"]
    }
  }
}
```

---

## Extensão futura — HTTP / SSO / API

O servidor foi projetado para ser facilmente portado para transporte HTTP:

1. Substitua `StdioServerTransport` por `StreamableHTTPServerTransport` (pacote `@modelcontextprotocol/sdk`)
2. Configure um endpoint HTTPS com seu certificado TLS
3. Para SSO, adicione um middleware de validação de token (OAuth 2.0 / OIDC) antes de repassar a requisição ao servidor MCP
4. Registre no Bob usando `url` em vez de `command`:

```json
{
  "mcpServers": {
    "dio-explorer-mcp": {
      "url": "https://seu-servidor.exemplo.com/mcp"
    }
  }
}
```

---

## Dados

O servidor lê em tempo real o arquivo `dio_explorer/data/trilhas_dio.json` — qualquer atualização no catálogo é refletida imediatamente, sem necessidade de rebuild.
