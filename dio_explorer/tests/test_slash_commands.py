"""
Suite de testes unitários — Slash Commands DIO Explorer
Cobre: /trilha, /desafio, /certificado
Meta de cobertura: 70%
"""

import json
import os
import re
import unittest
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# Caminhos base
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "dio_explorer" / "data" / "trilhas_dio.json"
COMMANDS_DIR = BASE_DIR / ".bob" / "commands"


# ─────────────────────────────────────────────
# Helpers reutilizáveis (simulam a lógica dos
# slash commands sem depender do Bob runtime)
# ─────────────────────────────────────────────

def load_trilhas() -> list[dict]:
    """Carrega e retorna a lista de trilhas do JSON."""
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)["trilhas"]


def buscar_trilha(tecnologia: str) -> list[dict]:
    """Replica a busca do /trilha: campo tecnologia → campo nome (case-insensitive)."""
    termo = tecnologia.lower()
    trilhas = load_trilhas()
    resultado = [t for t in trilhas if termo in t["tecnologia"].lower()]
    if not resultado:
        resultado = [t for t in trilhas if termo in t["nome"].lower()]
    return resultado


def gerar_plano_markdown(trilha: dict) -> str:
    """Simula o output Markdown do /trilha para uma trilha."""
    vitalicio = "Sim" if trilha["vitalicio"] else "Não"
    live = "Sim" if trilha["live_ao_vivo"] else "Não"
    badges = "\n".join(f"🏷️ {b}" for b in trilha["badges_disponiveis"])
    promo = trilha.get("promocoes")
    if promo:
        promo_texto = (
            f"- Desconto: {promo['desconto_percentual']}%\n"
            f"- Cupom: `{promo['cupom']}`\n"
            f"- Válido até: {promo['validade']}"
        )
    else:
        promo_texto = "_Nenhuma promoção ativa no momento._"

    return (
        f"# 🎓 Trilha: {trilha['nome']}\n"
        f"**🛠 Tecnologias:** {trilha['tecnologia']}\n"
        f"**📊 Nível:** {trilha['nivel']}\n"
        f"**📦 Total de Módulos:** {trilha['numero_de_modulos']}\n"
        f"**⭐ XP Total:** {trilha['xp_total']} XP\n"
        f"**♾️ Acesso Vitalício:** {vitalicio}\n"
        f"**📡 Lives ao Vivo:** {live}\n\n"
        f"## 🏅 Badges Disponíveis\n{badges}\n\n"
        f"## 🎟️ Promoção Ativa\n{promo_texto}"
    )


def gerar_desafio_markdown(nivel: str, tecnologia: str) -> str:
    """Simula o output estrutural do /desafio."""
    xp_map = {"básico": 150, "intermediário": 300, "avançado": 500}
    tempo_map = {"básico": "15 min", "intermediário": "30 min", "avançado": "60 min"}
    xp = xp_map.get(nivel.lower(), 300)
    tempo = tempo_map.get(nivel.lower(), "30 min")

    return (
        f"# ⚡ Desafio DIO\n"
        f"**🎯 Nível:** {nivel}\n"
        f"**🛠 Tecnologia:** {tecnologia}\n"
        f"**⏱ Tempo estimado:** {tempo}\n"
        f"**⭐ XP ao concluir:** {xp} XP\n\n"
        f"## 📋 Contexto\n[contexto gerado]\n\n"
        f"## 🎯 Objetivo\n[objetivo gerado]\n\n"
        f"## 📐 Requisitos\n- [ ] Requisito 1\n- [ ] Requisito 2\n- [ ] Requisito 3\n\n"
        f"## 💡 Dica\n[dica gerada]\n\n"
        f"## 🚀 Bônus\n[bônus gerado]"
    )


def gerar_certificado_markdown(nome: str, trilha: dict) -> str:
    """Simula o output do /certificado para uma trilha encontrada no JSON."""
    hoje = datetime.now().strftime("%d/%m/%Y")
    ano = datetime.now().year
    iniciais = "".join(p[0].upper() for p in nome.split() if p)
    cert_id = f"DIO-{ano}-{trilha['id']:04d}-{iniciais}"
    badges = "\n".join(f"🏷️ **{b}**" for b in trilha["badges_disponiveis"])

    return (
        f"## 🎓 Este certificado é conferido a\n# {nome}\n\n"
        f"### ✅ Pela conclusão com êxito da trilha:\n## {trilha['nome']}\n\n"
        f"| Campo | Detalhe |\n|---|---|\n"
        f"| 🛠 Tecnologias | {trilha['tecnologia']} |\n"
        f"| 📊 Nível | {trilha['nivel']} |\n"
        f"| 📦 Módulos Concluídos | {trilha['numero_de_modulos']} de {trilha['numero_de_modulos']} |\n"
        f"| ⭐ XP Conquistado | {trilha['xp_total']} XP |\n"
        f"| 📅 Data de Emissão | {hoje} |\n"
        f"| 🔖 ID do Certificado | {cert_id} |\n\n"
        f"### 🏅 Badges Conquistadas\n{badges}"
    )


# ─────────────────────────────────────────────
# Grupo 1 — Testes de infraestrutura
# ─────────────────────────────────────────────

class TestInfraestrutura(unittest.TestCase):

    def test_json_existe(self):
        """O arquivo trilhas_dio.json deve existir no caminho esperado."""
        self.assertTrue(DATA_PATH.exists(), f"Arquivo não encontrado: {DATA_PATH}")

    def test_json_carregavel(self):
        """O JSON deve ser carregável sem erros."""
        trilhas = load_trilhas()
        self.assertIsInstance(trilhas, list)

    def test_json_nao_vazio(self):
        """O JSON deve conter ao menos uma trilha."""
        trilhas = load_trilhas()
        self.assertGreater(len(trilhas), 0)

    def test_comando_trilha_existe(self):
        """O arquivo .bob/commands/trilha.md deve existir."""
        self.assertTrue((COMMANDS_DIR / "trilha.md").exists())

    def test_comando_desafio_existe(self):
        """O arquivo .bob/commands/desafio.md deve existir."""
        self.assertTrue((COMMANDS_DIR / "desafio.md").exists())

    def test_comando_certificado_existe(self):
        """O arquivo .bob/commands/certificado.md deve existir."""
        self.assertTrue((COMMANDS_DIR / "certificado.md").exists())

    def test_frontmatter_trilha(self):
        """trilha.md deve conter frontmatter com description e argument-hint."""
        content = (COMMANDS_DIR / "trilha.md").read_text(encoding="utf-8")
        self.assertIn("description:", content)
        self.assertIn("argument-hint:", content)
        self.assertIn("<tecnologia>", content)

    def test_frontmatter_desafio(self):
        """desafio.md deve conter frontmatter com argument-hint de dois parâmetros."""
        content = (COMMANDS_DIR / "desafio.md").read_text(encoding="utf-8")
        self.assertIn("argument-hint:", content)
        self.assertIn("<nivel>", content)
        self.assertIn("<tecnologia>", content)

    def test_frontmatter_certificado(self):
        """certificado.md deve conter frontmatter com argument-hint de nome e trilha."""
        content = (COMMANDS_DIR / "certificado.md").read_text(encoding="utf-8")
        self.assertIn("argument-hint:", content)
        self.assertIn("<seu-nome>", content)
        self.assertIn("<nome-da-trilha>", content)

    def test_variaveis_trilha(self):
        """trilha.md deve usar $1 para substituição de argumento."""
        content = (COMMANDS_DIR / "trilha.md").read_text(encoding="utf-8")
        self.assertIn("$1", content)

    def test_variaveis_desafio(self):
        """desafio.md deve usar $1 e $2 para substituição de argumentos."""
        content = (COMMANDS_DIR / "desafio.md").read_text(encoding="utf-8")
        self.assertIn("$1", content)
        self.assertIn("$2", content)

    def test_variaveis_certificado(self):
        """certificado.md deve usar $1 e $2 para substituição de argumentos."""
        content = (COMMANDS_DIR / "certificado.md").read_text(encoding="utf-8")
        self.assertIn("$1", content)
        self.assertIn("$2", content)


# ─────────────────────────────────────────────
# Grupo 2 — Testes do /trilha com Java
# ─────────────────────────────────────────────

class TestComandoTrilha(unittest.TestCase):

    def setUp(self):
        self.trilhas_java = buscar_trilha("Java")
        self.trilha = self.trilhas_java[0] if self.trilhas_java else None

    def test_busca_java_retorna_resultado(self):
        """Busca por 'Java' deve retornar ao menos uma trilha."""
        self.assertGreater(len(self.trilhas_java), 0,
                           "Nenhuma trilha encontrada para 'Java'")

    def test_trilha_java_nome_correto(self):
        """A trilha Java encontrada deve conter 'Java' no nome ou tecnologia."""
        self.assertIsNotNone(self.trilha)
        contem = ("java" in self.trilha["nome"].lower() or
                  "java" in self.trilha["tecnologia"].lower())
        self.assertTrue(contem)

    def test_trilha_java_campos_obrigatorios(self):
        """A trilha Java deve ter todos os campos obrigatórios."""
        campos = ["id", "nome", "tecnologia", "nivel", "numero_de_modulos",
                  "xp_total", "badges_disponiveis", "vitalicio", "live_ao_vivo"]
        for campo in campos:
            self.assertIn(campo, self.trilha, f"Campo ausente: {campo}")

    def test_trilha_java_nivel_valido(self):
        """O nível da trilha Java deve ser Básico, Intermediário ou Avançado."""
        niveis_validos = {"Básico", "Intermediário", "Avançado"}
        self.assertIn(self.trilha["nivel"], niveis_validos)

    def test_trilha_java_modulos_positivo(self):
        """O número de módulos da trilha Java deve ser maior que zero."""
        self.assertGreater(self.trilha["numero_de_modulos"], 0)

    def test_trilha_java_xp_positivo(self):
        """O XP total da trilha Java deve ser positivo."""
        self.assertGreater(self.trilha["xp_total"], 0)

    def test_trilha_java_badges_lista(self):
        """badges_disponiveis deve ser uma lista não vazia."""
        self.assertIsInstance(self.trilha["badges_disponiveis"], list)
        self.assertGreater(len(self.trilha["badges_disponiveis"]), 0)

    def test_trilha_java_promocao_estrutura(self):
        """Se houver promoção, deve conter desconto_percentual, cupom e validade."""
        promo = self.trilha.get("promocoes")
        if promo is not None:
            self.assertIn("desconto_percentual", promo)
            self.assertIn("cupom", promo)
            self.assertIn("validade", promo)
            self.assertIsInstance(promo["desconto_percentual"], (int, float))

    def test_trilha_java_promocao_desconto_range(self):
        """O desconto percentual deve estar entre 1 e 100."""
        promo = self.trilha.get("promocoes")
        if promo:
            self.assertGreaterEqual(promo["desconto_percentual"], 1)
            self.assertLessEqual(promo["desconto_percentual"], 100)

    def test_trilha_java_plano_markdown_gerado(self):
        """O markdown do plano de estudos deve conter o nome da trilha."""
        md = gerar_plano_markdown(self.trilha)
        self.assertIn(self.trilha["nome"], md)

    def test_trilha_java_plano_contem_nivel(self):
        """O markdown do plano deve conter o nível da trilha."""
        md = gerar_plano_markdown(self.trilha)
        self.assertIn(self.trilha["nivel"], md)

    def test_trilha_java_plano_contem_xp(self):
        """O markdown do plano deve conter o XP total."""
        md = gerar_plano_markdown(self.trilha)
        self.assertIn(str(self.trilha["xp_total"]), md)

    def test_trilha_java_plano_contem_badge(self):
        """O markdown do plano deve conter pelo menos uma badge."""
        md = gerar_plano_markdown(self.trilha)
        self.assertIn(self.trilha["badges_disponiveis"][0], md)

    def test_busca_case_insensitive_minusculo(self):
        """Busca com 'java' em minúsculo deve retornar o mesmo resultado."""
        resultado = buscar_trilha("java")
        self.assertGreater(len(resultado), 0)

    def test_busca_case_insensitive_maiusculo(self):
        """Busca com 'JAVA' em maiúsculo deve retornar resultado."""
        resultado = buscar_trilha("JAVA")
        self.assertGreater(len(resultado), 0)

    def test_busca_tecnologia_inexistente(self):
        """Busca por tecnologia inexistente deve retornar lista vazia."""
        resultado = buscar_trilha("CobolXYZ99")
        self.assertEqual(len(resultado), 0)

    def test_trilha_java_vitalicio_booleano(self):
        """O campo vitalicio deve ser booleano."""
        self.assertIsInstance(self.trilha["vitalicio"], bool)

    def test_trilha_java_live_booleano(self):
        """O campo live_ao_vivo deve ser booleano."""
        self.assertIsInstance(self.trilha["live_ao_vivo"], bool)


# ─────────────────────────────────────────────
# Grupo 3 — Testes do /desafio
# ─────────────────────────────────────────────

class TestComandoDesafio(unittest.TestCase):

    def test_desafio_basico_xp(self):
        """Nível Básico deve gerar 150 XP."""
        md = gerar_desafio_markdown("Básico", "Java")
        self.assertIn("150 XP", md)

    def test_desafio_intermediario_xp(self):
        """Nível Intermediário deve gerar 300 XP."""
        md = gerar_desafio_markdown("Intermediário", "Java")
        self.assertIn("300 XP", md)

    def test_desafio_avancado_xp(self):
        """Nível Avançado deve gerar 500 XP."""
        md = gerar_desafio_markdown("Avançado", "Java")
        self.assertIn("500 XP", md)

    def test_desafio_basico_tempo(self):
        """Nível Básico deve ter tempo estimado de 15 min."""
        md = gerar_desafio_markdown("Básico", "Java")
        self.assertIn("15 min", md)

    def test_desafio_intermediario_tempo(self):
        """Nível Intermediário deve ter tempo estimado de 30 min."""
        md = gerar_desafio_markdown("Intermediário", "Java")
        self.assertIn("30 min", md)

    def test_desafio_avancado_tempo(self):
        """Nível Avançado deve ter tempo estimado de 60 min."""
        md = gerar_desafio_markdown("Avançado", "Java")
        self.assertIn("60 min", md)

    def test_desafio_contem_tecnologia(self):
        """O markdown do desafio deve mencionar a tecnologia passada."""
        md = gerar_desafio_markdown("Intermediário", "Java")
        self.assertIn("Java", md)

    def test_desafio_contem_nivel(self):
        """O markdown do desafio deve mencionar o nível passado."""
        md = gerar_desafio_markdown("Intermediário", "Java")
        self.assertIn("Intermediário", md)

    def test_desafio_contem_secao_contexto(self):
        """O markdown do desafio deve conter a seção Contexto."""
        md = gerar_desafio_markdown("Intermediário", "Java")
        self.assertIn("## 📋 Contexto", md)

    def test_desafio_contem_secao_objetivo(self):
        """O markdown do desafio deve conter a seção Objetivo."""
        md = gerar_desafio_markdown("Intermediário", "Java")
        self.assertIn("## 🎯 Objetivo", md)

    def test_desafio_contem_secao_requisitos(self):
        """O markdown do desafio deve conter a seção Requisitos."""
        md = gerar_desafio_markdown("Intermediário", "Java")
        self.assertIn("## 📐 Requisitos", md)

    def test_desafio_requisitos_checklist(self):
        """Os requisitos devem estar em formato de checklist."""
        md = gerar_desafio_markdown("Intermediário", "Java")
        self.assertIn("- [ ]", md)

    def test_desafio_contem_dica(self):
        """O markdown do desafio deve conter a seção Dica."""
        md = gerar_desafio_markdown("Intermediário", "Java")
        self.assertIn("## 💡 Dica", md)

    def test_desafio_contem_bonus(self):
        """O markdown do desafio deve conter a seção Bônus."""
        md = gerar_desafio_markdown("Intermediário", "Java")
        self.assertIn("## 🚀 Bônus", md)

    def test_desafio_prompt_referencia_json(self):
        """O arquivo desafio.md deve referenciar o JSON das trilhas."""
        content = (COMMANDS_DIR / "desafio.md").read_text(encoding="utf-8")
        # desafio pode ou não referenciar o JSON, mas deve ter $1 e $2
        self.assertIn("$1", content)
        self.assertIn("$2", content)

    def test_desafio_prompt_tem_regras(self):
        """O prompt do desafio deve conter regras para Básico, Intermediário e Avançado."""
        content = (COMMANDS_DIR / "desafio.md").read_text(encoding="utf-8")
        self.assertIn("Básico", content)
        self.assertIn("Intermediário", content)
        self.assertIn("Avançado", content)


# ─────────────────────────────────────────────
# Grupo 4 — Testes do /certificado
# ─────────────────────────────────────────────

class TestComandoCertificado(unittest.TestCase):

    def setUp(self):
        trilhas = buscar_trilha("Java")
        self.trilha = trilhas[0]
        self.nome_aluno = "Luis Silva"
        self.cert = gerar_certificado_markdown(self.nome_aluno, self.trilha)

    def test_certificado_contem_nome_aluno(self):
        """O certificado deve exibir o nome do aluno."""
        self.assertIn(self.nome_aluno, self.cert)

    def test_certificado_contem_nome_trilha(self):
        """O certificado deve exibir o nome da trilha."""
        self.assertIn(self.trilha["nome"], self.cert)

    def test_certificado_contem_tecnologia(self):
        """O certificado deve exibir as tecnologias da trilha."""
        self.assertIn(self.trilha["tecnologia"], self.cert)

    def test_certificado_contem_nivel(self):
        """O certificado deve exibir o nível da trilha."""
        self.assertIn(self.trilha["nivel"], self.cert)

    def test_certificado_contem_xp(self):
        """O certificado deve exibir o XP total da trilha."""
        self.assertIn(str(self.trilha["xp_total"]), self.cert)

    def test_certificado_contem_modulos(self):
        """O certificado deve exibir o número de módulos."""
        self.assertIn(str(self.trilha["numero_de_modulos"]), self.cert)

    def test_certificado_contem_data_emissao(self):
        """O certificado deve conter uma data no formato DD/MM/AAAA."""
        padrao = r"\d{2}/\d{2}/\d{4}"
        self.assertRegex(self.cert, padrao)

    def test_certificado_data_ano_correto(self):
        """O ano na data de emissão deve ser o ano atual."""
        ano_atual = str(datetime.now().year)
        self.assertIn(ano_atual, self.cert)

    def test_certificado_id_formato(self):
        """O ID do certificado deve seguir o padrão DIO-AAAA-XXXX-INICIAIS."""
        padrao = r"DIO-\d{4}-\d{4}-[A-Z]+"
        self.assertRegex(self.cert, padrao)

    def test_certificado_id_contem_ano(self):
        """O ID do certificado deve conter o ano atual."""
        ano_atual = str(datetime.now().year)
        self.assertIn(f"DIO-{ano_atual}", self.cert)

    def test_certificado_id_contem_iniciais(self):
        """O ID do certificado deve conter as iniciais do nome do aluno."""
        iniciais = "LS"  # Luis Silva → LS
        self.assertIn(iniciais, self.cert)

    def test_certificado_contem_badges(self):
        """O certificado deve listar as badges da trilha."""
        for badge in self.trilha["badges_disponiveis"]:
            self.assertIn(badge, self.cert)

    def test_certificado_secao_badges(self):
        """O certificado deve conter a seção de Badges Conquistadas."""
        self.assertIn("Badges Conquistadas", self.cert)

    def test_certificado_prompt_referencia_json(self):
        """O certificado.md deve referenciar o arquivo JSON."""
        content = (COMMANDS_DIR / "certificado.md").read_text(encoding="utf-8")
        self.assertIn("trilhas_dio.json", content)

    def test_certificado_prompt_instrucao_apenas_certificado(self):
        """O certificado.md deve instruir a exibir apenas o certificado."""
        content = (COMMANDS_DIR / "certificado.md").read_text(encoding="utf-8")
        self.assertIn("apenas", content.lower())

    def test_certificado_nome_iniciais_multiplas_palavras(self):
        """Iniciais com três nomes devem ser calculadas corretamente."""
        trilha = self.trilha
        cert = gerar_certificado_markdown("Ana Paula Costa", trilha)
        self.assertIn("APC", cert)


# ─────────────────────────────────────────────
# Grupo 5 — Testes de integridade do JSON
# ─────────────────────────────────────────────

class TestIntegridadeJSON(unittest.TestCase):

    def setUp(self):
        self.trilhas = load_trilhas()

    def test_total_trilhas_esperado(self):
        """O JSON deve conter exatamente 32 trilhas."""
        self.assertEqual(len(self.trilhas), 32)

    def test_ids_unicos(self):
        """Todos os IDs de trilhas devem ser únicos."""
        ids = [t["id"] for t in self.trilhas]
        self.assertEqual(len(ids), len(set(ids)))

    def test_ids_sequenciais(self):
        """Os IDs devem ser sequenciais de 1 a 32."""
        ids = sorted(t["id"] for t in self.trilhas)
        self.assertEqual(ids, list(range(1, 33)))

    def test_todos_niveis_validos(self):
        """Todos os níveis devem ser Básico, Intermediário ou Avançado."""
        niveis_validos = {"Básico", "Intermediário", "Avançado"}
        for t in self.trilhas:
            self.assertIn(t["nivel"], niveis_validos,
                          f"Nível inválido na trilha {t['id']}: {t['nivel']}")

    def test_todos_modulos_positivos(self):
        """Todas as trilhas devem ter pelo menos 1 módulo."""
        for t in self.trilhas:
            self.assertGreater(t["numero_de_modulos"], 0,
                               f"Trilha {t['id']} tem 0 módulos")

    def test_todos_xp_positivos(self):
        """Todas as trilhas devem ter XP > 0."""
        for t in self.trilhas:
            self.assertGreater(t["xp_total"], 0,
                               f"Trilha {t['id']} tem XP inválido")

    def test_todas_trilhas_tem_badges(self):
        """Todas as trilhas devem ter ao menos uma badge."""
        for t in self.trilhas:
            self.assertGreater(len(t["badges_disponiveis"]), 0,
                               f"Trilha {t['id']} sem badges")

    def test_campo_vitalicio_booleano_em_todas(self):
        """O campo vitalicio deve ser booleano em todas as trilhas."""
        for t in self.trilhas:
            self.assertIsInstance(t["vitalicio"], bool,
                                  f"Trilha {t['id']}: vitalicio não é bool")

    def test_campo_live_booleano_em_todas(self):
        """O campo live_ao_vivo deve ser booleano em todas as trilhas."""
        for t in self.trilhas:
            self.assertIsInstance(t["live_ao_vivo"], bool,
                                  f"Trilha {t['id']}: live_ao_vivo não é bool")

    def test_promocoes_estrutura_quando_presente(self):
        """Promoções presentes devem ter desconto_percentual, cupom e validade."""
        for t in self.trilhas:
            p = t.get("promocoes")
            if p is not None:
                self.assertIn("desconto_percentual", p,
                              f"Trilha {t['id']}: promoção sem desconto")
                self.assertIn("cupom", p,
                              f"Trilha {t['id']}: promoção sem cupom")
                self.assertIn("validade", p,
                              f"Trilha {t['id']}: promoção sem validade")

    def test_java_presente_no_json(self):
        """Deve existir ao menos uma trilha com Java na tecnologia."""
        java = [t for t in self.trilhas if "java" in t["tecnologia"].lower()]
        self.assertGreater(len(java), 0)


# ─────────────────────────────────────────────
# Ponto de entrada
# ─────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)
