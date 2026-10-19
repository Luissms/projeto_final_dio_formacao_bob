#!/usr/bin/env node
/**
 * DIO Explorer MCP Server
 *
 * Expõe as funcionalidades do projeto DIO Explorer via protocolo MCP:
 *   - Ferramenta: buscar_trilha       → /trilha
 *   - Ferramenta: gerar_desafio       → /desafio
 *   - Ferramenta: gerar_certificado   → /certificado
 *   - Ferramenta: listar_trilhas      → lista todas as trilhas disponíveis
 *   - Recurso:    trilhas://catalogo  → JSON completo das trilhas
 *   - Prompt:     plano_de_estudos    → prompt formatado para trilha específica
 *
 * Transporte: stdio (local) — extensível para HTTP/SSE ou SSO futuramente.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, resolve, join } from "path";

// ─────────────────────────────────────────────────────────────────────────────
// Resolução de caminhos
// ─────────────────────────────────────────────────────────────────────────────

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Sobe dois níveis: build/ → mcp/ → dio_explorer/  →  data/trilhas_dio.json
const DATA_PATH = resolve(__dirname, "..", "..", "data", "trilhas_dio.json");

// ─────────────────────────────────────────────────────────────────────────────
// Tipos
// ─────────────────────────────────────────────────────────────────────────────

interface Promocao {
  desconto_percentual: number;
  validade: string;
  cupom: string;
}

interface Trilha {
  id: number;
  nome: string;
  tecnologia: string;
  nivel: "Básico" | "Intermediário" | "Avançado";
  numero_de_modulos: number;
  xp_total: number;
  badges_disponiveis: string[];
  promocoes: Promocao | null;
  vitalicio: boolean;
  live_ao_vivo: boolean;
}

// ─────────────────────────────────────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────────────────────────────────────

function carregarTrilhas(): Trilha[] {
  const raw = readFileSync(DATA_PATH, "utf-8");
  return (JSON.parse(raw) as { trilhas: Trilha[] }).trilhas;
}

function buscarPorTecnologia(termo: string): Trilha[] {
  const t = termo.toLowerCase();
  const trilhas = carregarTrilhas();
  const porTec = trilhas.filter((x) => x.tecnologia.toLowerCase().includes(t));
  if (porTec.length > 0) return porTec;
  return trilhas.filter((x) => x.nome.toLowerCase().includes(t));
}

function formatarTrilha(t: Trilha): string {
  const vitalicio = t.vitalicio ? "Sim" : "Não";
  const live = t.live_ao_vivo ? "Sim" : "Não";
  const badges = t.badges_disponiveis.map((b) => `  🏷️ ${b}`).join("\n");
  const promo = t.promocoes
    ? `  Desconto: ${t.promocoes.desconto_percentual}% | Cupom: ${t.promocoes.cupom} | Válido até: ${t.promocoes.validade}`
    : "  Nenhuma promoção ativa.";

  return [
    `# 🎓 ${t.nome}`,
    ``,
    `🛠  Tecnologias   : ${t.tecnologia}`,
    `📊 Nível          : ${t.nivel}`,
    `📦 Módulos        : ${t.numero_de_modulos}`,
    `⭐ XP Total        : ${t.xp_total} XP`,
    `♾️  Acesso Vitalício: ${vitalicio}`,
    `📡 Lives ao Vivo   : ${live}`,
    ``,
    `## 🏅 Badges`,
    badges,
    ``,
    `## 🎟️ Promoção`,
    promo,
  ].join("\n");
}

function dataHoje(): string {
  return new Date().toLocaleDateString("pt-BR");
}

function anoAtual(): number {
  return new Date().getFullYear();
}

function iniciais(nome: string): string {
  return nome
    .split(/\s+/)
    .filter(Boolean)
    .map((p) => p[0].toUpperCase())
    .join("");
}

// ─────────────────────────────────────────────────────────────────────────────
// Servidor MCP
// ─────────────────────────────────────────────────────────────────────────────

const server = new McpServer({
  name: "dio-explorer-mcp",
  version: "1.0.0",
});

// ─────────────────────────────────────────────────────────────────────────────
// FERRAMENTA 1 — listar_trilhas
// ─────────────────────────────────────────────────────────────────────────────

server.registerTool(
  "listar_trilhas",
  {
    description:
      "Lista todas as trilhas de aprendizado disponíveis no catálogo DIO Explorer, com id, nome, tecnologia e nível.",
    inputSchema: z.object({
      nivel: z
        .enum(["Básico", "Intermediário", "Avançado", "Todos"])
        .optional()
        .describe("Filtrar por nível. Use 'Todos' ou omita para ver todas."),
    }),
  },
  async ({ nivel }) => {
    try {
      const trilhas = carregarTrilhas();
      const filtradas =
        !nivel || nivel === "Todos"
          ? trilhas
          : trilhas.filter((t) => t.nivel === nivel);

      const linhas = filtradas.map(
        (t) =>
          `[${String(t.id).padStart(2, "0")}] ${t.nome.padEnd(48)} | ${t.nivel.padEnd(14)} | ${t.tecnologia}`
      );

      const cabecalho = `${"ID".padEnd(4)} ${"Nome".padEnd(48)} | ${"Nível".padEnd(14)} | Tecnologia`;
      const separador = "─".repeat(120);

      return {
        content: [
          {
            type: "text",
            text: [
              `📚 Catálogo DIO Explorer — ${filtradas.length} trilha(s)`,
              separador,
              cabecalho,
              separador,
              ...linhas,
              separador,
            ].join("\n"),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Erro ao carregar trilhas: ${error instanceof Error ? error.message : String(error)}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────────────────────
// FERRAMENTA 2 — buscar_trilha
// ─────────────────────────────────────────────────────────────────────────────

server.registerTool(
  "buscar_trilha",
  {
    description:
      "Busca trilhas DIO pela tecnologia ou nome e retorna o plano de estudos formatado. Equivale ao slash command /trilha.",
    inputSchema: z.object({
      tecnologia: z
        .string()
        .min(1)
        .describe(
          "Nome da tecnologia ou parte do nome da trilha. Ex: 'Java', 'Python', 'React', 'AWS'."
        ),
    }),
  },
  async ({ tecnologia }) => {
    try {
      const encontradas = buscarPorTecnologia(tecnologia);

      if (encontradas.length === 0) {
        const todas = carregarTrilhas();
        const nomes = todas.map((t) => `  • ${t.nome}`).join("\n");
        return {
          content: [
            {
              type: "text",
              text: `Nenhuma trilha encontrada para "${tecnologia}".\n\nTrilhas disponíveis:\n${nomes}`,
            },
          ],
        };
      }

      const resultado = encontradas.map(formatarTrilha).join("\n\n---\n\n");
      return {
        content: [{ type: "text", text: resultado }],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Erro na busca: ${error instanceof Error ? error.message : String(error)}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────────────────────
// FERRAMENTA 3 — gerar_desafio
// ─────────────────────────────────────────────────────────────────────────────

server.registerTool(
  "gerar_desafio",
  {
    description:
      "Gera a estrutura de um desafio de código para o aluno baseado no nível e tecnologia escolhidos. Equivale ao slash command /desafio.",
    inputSchema: z.object({
      nivel: z
        .enum(["Básico", "Intermediário", "Avançado"])
        .describe("Nível do desafio."),
      tecnologia: z
        .string()
        .min(1)
        .describe("Tecnologia do desafio. Ex: 'Java', 'Python', 'React'."),
    }),
  },
  async ({ nivel, tecnologia }) => {
    const xpMap: Record<string, number> = {
      Básico: 150,
      Intermediário: 300,
      Avançado: 500,
    };
    const tempoMap: Record<string, string> = {
      Básico: "15 min",
      Intermediário: "30 min",
      Avançado: "60 min",
    };

    const xp = xpMap[nivel];
    const tempo = tempoMap[nivel];

    const template = [
      `# ⚡ Desafio DIO`,
      ``,
      `**🎯 Nível:** ${nivel}`,
      `**🛠 Tecnologia:** ${tecnologia}`,
      `**⏱ Tempo estimado:** ${tempo}`,
      `**⭐ XP ao concluir:** ${xp} XP`,
      ``,
      `---`,
      ``,
      `## 📋 Contexto`,
      ``,
      `[Bob irá gerar o contexto narrativo do desafio aqui]`,
      ``,
      `## 🎯 Objetivo`,
      ``,
      `[Bob irá descrever o objetivo do desafio aqui]`,
      ``,
      `## 📐 Requisitos`,
      ``,
      `- [ ] Requisito 1`,
      `- [ ] Requisito 2`,
      `- [ ] Requisito 3`,
      ``,
      `## 💡 Dica`,
      ``,
      `[Dica calibrada para o nível ${nivel}]`,
      ``,
      `## 🧪 Exemplo de Entrada e Saída`,
      ``,
      `\`\`\``,
      `Entrada: [exemplo]`,
      `Saída esperada: [exemplo]`,
      `\`\`\``,
      ``,
      `## 🚀 Bônus (opcional)`,
      ``,
      `[Desafio extra para quem quiser ir além]`,
      ``,
      `---`,
      ``,
      `> 💬 Use \`/certificado <seu-nome> ${tecnologia}\` ao concluir!`,
    ].join("\n");

    return {
      content: [{ type: "text", text: template }],
    };
  }
);

// ─────────────────────────────────────────────────────────────────────────────
// FERRAMENTA 4 — gerar_certificado
// ─────────────────────────────────────────────────────────────────────────────

server.registerTool(
  "gerar_certificado",
  {
    description:
      "Gera um certificado fictício de conclusão de trilha DIO para o aluno. Equivale ao slash command /certificado.",
    inputSchema: z.object({
      nome_aluno: z
        .string()
        .min(1)
        .describe("Nome completo do aluno. Ex: 'Luis Silva'."),
      trilha: z
        .string()
        .min(1)
        .describe(
          "Nome ou tecnologia da trilha concluída. Ex: 'Java', 'Python para IA'."
        ),
    }),
  },
  async ({ nome_aluno, trilha }) => {
    try {
      const encontradas = buscarPorTecnologia(trilha);
      const t = encontradas[0] ?? null;

      const ini = iniciais(nome_aluno);
      const ano = anoAtual();
      const data = dataHoje();
      const certId = t
        ? `DIO-${ano}-${String(t.id).padStart(4, "0")}-${ini}`
        : `DIO-${ano}-${Math.floor(1000 + Math.random() * 9000)}-${ini}`;

      const nomeTrilha = t ? t.nome : trilha;
      const tecnologiaTrilha = t ? t.tecnologia : "—";
      const nivelTrilha = t ? t.nivel : "—";
      const modulos = t ? `${t.numero_de_modulos} de ${t.numero_de_modulos}` : "—";
      const xp = t ? `${t.xp_total} XP` : "N/A";
      const badges = t
        ? t.badges_disponiveis.map((b) => `🏷️ **${b}**`).join("  |  ")
        : "_Nenhuma badge registrada._";

      const cert = [
        `\`\`\``,
        `╔══════════════════════════════════════════════════════════════════╗`,
        `║                                                                  ║`,
        `║               🏆  CERTIFICADO DE CONCLUSÃO  🏆                  ║`,
        `║                                                                  ║`,
        `║                   dio_explorer · DIO Platform                    ║`,
        `╚══════════════════════════════════════════════════════════════════╝`,
        `\`\`\``,
        ``,
        `## 🎓 Este certificado é conferido a`,
        ``,
        `# ${nome_aluno}`,
        ``,
        `---`,
        ``,
        `### ✅ Pela conclusão com êxito da trilha:`,
        ``,
        `## ${nomeTrilha}`,
        ``,
        `---`,
        ``,
        `| Campo                  | Detalhe                                      |`,
        `|------------------------|----------------------------------------------|`,
        `| 🛠 Tecnologias          | ${tecnologiaTrilha}                          |`,
        `| 📊 Nível               | ${nivelTrilha}                               |`,
        `| 📦 Módulos Concluídos  | ${modulos}                                   |`,
        `| ⭐ XP Conquistado       | ${xp}                                        |`,
        `| 📅 Data de Emissão     | ${data}                                      |`,
        `| 🔖 ID do Certificado   | ${certId}                                    |`,
        ``,
        `---`,
        ``,
        `### 🏅 Badges Conquistadas`,
        ``,
        badges,
        ``,
        `---`,
        ``,
        `> _"A jornada de mil milhas começa com um único passo."_`,
        `> — Lao Tsé`,
        ``,
        `---`,
        ``,
        `**dio_explorer** · Plataforma de Educação em Tecnologia`,
        `_Certificado fictício gerado para fins educacionais · Projeto DIO + IBM Bob_`,
      ].join("\n");

      return {
        content: [{ type: "text", text: cert }],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Erro ao gerar certificado: ${error instanceof Error ? error.message : String(error)}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────────────────────
// RECURSO — trilhas://catalogo
// ─────────────────────────────────────────────────────────────────────────────

server.registerResource(
  "catalogo-trilhas",
  "trilhas://catalogo",
  {
    title: "Catálogo de Trilhas DIO",
    description:
      "JSON completo com todas as trilhas disponíveis no DIO Explorer, incluindo módulos, XP, badges e promoções.",
    mimeType: "application/json",
  },
  async () => {
    try {
      const trilhas = carregarTrilhas();
      return {
        contents: [
          {
            uri: "trilhas://catalogo",
            mimeType: "application/json",
            text: JSON.stringify({ total: trilhas.length, trilhas }, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        contents: [
          {
            uri: "trilhas://catalogo",
            mimeType: "text/plain",
            text: `Erro ao carregar catálogo: ${error instanceof Error ? error.message : String(error)}`,
          },
        ],
      };
    }
  }
);

// ─────────────────────────────────────────────────────────────────────────────
// PROMPT — plano_de_estudos
// ─────────────────────────────────────────────────────────────────────────────

server.registerPrompt(
  "plano_de_estudos",
  {
    description:
      "Gera um prompt estruturado pedindo ao modelo que elabore um plano de estudos detalhado para uma trilha DIO.",
    argsSchema: {
      tecnologia: z.string().describe("Tecnologia ou nome da trilha."),
      nome_aluno: z
        .string()
        .optional()
        .describe("Nome do aluno (opcional, personaliza o plano)."),
    },
  },
  async ({ tecnologia, nome_aluno }) => {
    const encontradas = buscarPorTecnologia(tecnologia);
    const t = encontradas[0];

    const contextoTrilha = t
      ? `Trilha encontrada: "${t.nome}" | Nível: ${t.nivel} | ${t.numero_de_modulos} módulos | ${t.xp_total} XP`
      : `Nenhuma trilha específica encontrada para "${tecnologia}". Use seu conhecimento para criar um plano coerente.`;

    const saudacao = nome_aluno ? `para ${nome_aluno} ` : "";

    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: [
              `Crie um plano de estudos detalhado ${saudacao}para a tecnologia: **${tecnologia}**.`,
              ``,
              `Contexto da trilha DIO: ${contextoTrilha}`,
              ``,
              `O plano deve conter:`,
              `1. Lista numerada de módulos com títulos e descrições de 1 linha cada`,
              `2. Progressão lógica do básico ao avançado`,
              `3. Recursos recomendados por módulo (docs, ferramentas, práticas)`,
              `4. Estimativa de horas por módulo`,
              `5. Projeto final sugerido para consolidar o aprendizado`,
              ``,
              `Responda em português brasileiro com formatação Markdown.`,
            ].join("\n"),
          },
        },
      ],
    };
  }
);

// ─────────────────────────────────────────────────────────────────────────────
// Inicialização
// ─────────────────────────────────────────────────────────────────────────────

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("✅ dio-explorer-mcp rodando em stdio");
  console.error(`📂 Dados: ${DATA_PATH}`);
}

main().catch((error) => {
  console.error("❌ Erro fatal no servidor MCP:", error);
  process.exit(1);
});
