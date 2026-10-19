---
description: Exibe o plano de estudos formatado de uma trilha DIO pela tecnologia informada
argument-hint: <tecnologia>
---
O usuário quer ver o plano de estudos da trilha relacionada à tecnologia: **$1**

Siga exatamente estes passos:

1. Leia o arquivo `dio_explorer/data/trilhas_dio.json`.
2. Procure todas as trilhas cujo campo `tecnologia` contenha (ignorando maiúsculas/minúsculas) o termo **$1**. Se não encontrar, tente pelo campo `nome`.
3. Se nenhuma trilha for encontrada, informe o usuário e liste os nomes de todas as trilhas disponíveis no JSON para ele escolher.
4. Se encontrar uma ou mais trilhas, exiba **cada uma** no seguinte formato Markdown:

---

# 🎓 Trilha: {nome}

**🛠 Tecnologias:** {tecnologia}
**📊 Nível:** {nivel}
**📦 Total de Módulos:** {numero_de_modulos}
**⭐ XP Total:** {xp_total} XP
**♾️ Acesso Vitalício:** {Sim se vitalicio=true, Não se false}
**📡 Lives ao Vivo:** {Sim se live_ao_vivo=true, Não se false}

## 📚 Plano de Estudos

Gere uma lista numerada com exatamente {numero_de_modulos} módulos coerentes com a tecnologia e o nível da trilha, seguindo progressão lógica do básico ao avançado dentro do nível:

**Módulo 1 — {título do módulo}**
> {breve descrição de 1 linha do que será aprendido}

Repita para todos os {numero_de_modulos} módulos.

## 🏅 Badges Disponíveis

Liste as badges do campo `badges_disponiveis` em formato de lista com ícone 🏷️.

## 🎟️ Promoção Ativa

Se `promocoes` não for null, exiba:
- Desconto: {desconto_percentual}%
- Cupom: `{cupom}`
- Válido até: {validade}

Se `promocoes` for null, escreva: _Nenhuma promoção ativa no momento._

---

> 💡 Use `/desafio <nivel> $1` para praticar ou `/certificado <seu-nome> {nome da trilha}` ao concluir!

Responda sempre em **português brasileiro**.
