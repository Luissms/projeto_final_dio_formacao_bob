"""
Fixture: dados esperados para a trilha Java Moderno com Spring Boot
Usado pelos testes como referência de ground truth.
"""

TRILHA_JAVA_FIXTURE = {
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
    "vitalicio": True,
    "live_ao_vivo": True
}

DESAFIO_JAVA_FIXTURE = {
    "nivel": "Intermediário",
    "tecnologia": "Java / Spring Boot",
    "xp_esperado": 300,
    "tempo_esperado": "30 min",
    "secoes_obrigatorias": [
        "## 📋 Contexto",
        "## 🎯 Objetivo",
        "## 📐 Requisitos",
        "## 💡 Dica",
        "## 🚀 Bônus",
    ]
}

CERTIFICADO_JAVA_FIXTURE = {
    "nome_aluno": "Luis Silva",
    "iniciais": "LS",
    "trilha_nome": "Java Moderno com Spring Boot",
    "tecnologia": "Java / Spring Boot / Hibernate / Maven",
    "nivel": "Intermediário",
    "modulos": 13,
    "xp": 10200,
    "badges": ["Java Developer", "Spring Expert", "Backend Engineer"],
    "id_pattern": r"DIO-\d{4}-0012-LS"
}
