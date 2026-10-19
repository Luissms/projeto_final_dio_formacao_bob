---
description: Gera um certificado fictício de conclusão de trilha DIO em Markdown
argument-hint: <seu-nome> <nome-da-trilha>
---
O usuário quer gerar um certificado fictício de conclusão com os seguintes dados:
- **Nome do aluno:** $1
- **Trilha concluída:** $2

Siga exatamente estes passos:

1. Leia o arquivo `dio_explorer/data/trilhas_dio.json`.
2. Procure a trilha cujo campo `nome` ou `tecnologia` corresponda mais ao texto "$2" (ignorando maiúsculas/minúsculas). Use correspondência parcial se necessário.
3. Se não encontrar a trilha no JSON, use os dados fornecidos pelo usuário diretamente e preencha os campos extras com "—".
4. Calcule a data atual real no formato DD/MM/AAAA.
5. Gere o ID do certificado no padrão: `DIO-{ano atual}-{id da trilha ou 4 dígitos aleatórios}-{iniciais de $1 em maiúsculas}`.
6. Exiba **somente** o certificado abaixo, sem nenhum texto antes ou depois dele.

---

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║               🏆  CERTIFICADO DE CONCLUSÃO  🏆                  ║
║                                                                  ║
║                   dio_explorer · DIO Platform                    ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🎓 Este certificado é conferido a

# $1

---

### ✅ Pela conclusão com êxito da trilha:

## {nome da trilha encontrada no JSON, ou "$2" se não encontrada}

---

| Campo                  | Detalhe                                                            |
|------------------------|--------------------------------------------------------------------|
| 🛠 Tecnologias          | {tecnologia da trilha ou "—"}                                      |
| 📊 Nível               | {nivel da trilha ou "—"}                                           |
| 📦 Módulos Concluídos  | {numero_de_modulos} de {numero_de_modulos} ou "—/—"               |
| ⭐ XP Conquistado       | {xp_total} XP ou "N/A"                                             |
| 📅 Data de Emissão     | {data atual no formato DD/MM/AAAA}                                 |
| 🔖 ID do Certificado   | {DIO-{ano}-{id ou 4 dígitos aleatórios}-{iniciais de $1 maiúsculas}} |

---

### 🏅 Badges Conquistadas

{Liste cada badge de `badges_disponiveis` no formato: 🏷️ **{badge}**}

{Se trilha não encontrada, escreva: _Nenhuma badge registrada._}

---

> _"A jornada de mil milhas começa com um único passo."_
> — Lao Tsé

---

**dio_explorer** · Plataforma de Educação em Tecnologia
_Certificado fictício gerado para fins educacionais · Projeto DIO + IBM Bob_

---

Regras:
- Exiba **apenas** o certificado — sem introdução, sem explicação, sem texto adicional.
- Preencha a data de emissão com a data atual real.
- Se a trilha for encontrada no JSON, use todos os campos reais dela.
- Se não for encontrada, preencha tecnologia, nível e módulos com "—" e XP com "N/A".
- O ID deve seguir exatamente o padrão `DIO-{ano}-{id ou 4 dígitos aleatórios}-{iniciais em maiúsculas}`.
- Responda sempre em **português brasileiro**.
