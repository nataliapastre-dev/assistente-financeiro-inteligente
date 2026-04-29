import pandas as pd
import json

# =========================
# 📂 Carregar dados
# =========================
def carregar_dados():
    try:
        transacoes = pd.read_csv("data/transacoes.csv")

        with open("data/perfil_investidor.json", "r", encoding="utf-8") as f:
            perfil = json.load(f)

        return transacoes, perfil

    except FileNotFoundError:
        return None, None


# =========================
# 📊 Análise de gastos
# =========================
def analisar_gastos(transacoes):
    if transacoes is None or transacoes.empty:
        return 0, {}

    total = transacoes["valor"].sum()
    por_categoria = transacoes.groupby("categoria")["valor"].sum()

    return total, por_categoria


# =========================
# 💡 Insights inteligentes
# =========================
def gerar_insights(total, por_categoria):
    insights = []

    if len(por_categoria) > 0:
        maior_categoria = por_categoria.idxmax()
        valor_maior = por_categoria.max()

        percentual = (valor_maior / total) * 100 if total > 0 else 0

        insights.append(f"📊 Seu maior gasto foi com {maior_categoria}: R$ {valor_maior:.2f} ({percentual:.1f}% do total)")

        if percentual > 40:
            insights.append("⚠️ Esse gasto está alto e pode impactar seu orçamento.")

        economia = valor_maior * 0.2
        insights.append(f"💡 Se reduzir 20% em {maior_categoria}, você pode economizar cerca de R$ {economia:.2f}")

        insights.append("📌 Dica: tente definir um limite mensal por categoria.")

    return insights


# =========================
# 🤖 Resposta padrão (fallback)
# =========================
def responder_regra(pergunta, total, por_categoria, perfil):
    pergunta = pergunta.lower()

    if "gastei" in pergunta:
        return f"Você gastou R$ {total:.2f} no período analisado."

    elif "categoria" in pergunta or "onde" in pergunta:
        resposta = "Seus gastos por categoria:\n"
        for cat, val in por_categoria.items():
            resposta += f"- {cat}: R$ {val:.2f}\n"
        return resposta

    elif "insight" in pergunta or "analise" in pergunta:
        insights = gerar_insights(total, por_categoria)
        return "\n".join(insights)

    elif "investir" in pergunta:
        return f"Seu perfil é {perfil['perfil']}. Busque investimentos compatíveis com esse perfil."

    else:
        return "Posso te ajudar com gastos, categorias, insights ou investimentos."


# =========================
# 🤖 IA (opcional)
# =========================
def responder_com_ia(pergunta, total, por_categoria, perfil):
    try:
        from openai import OpenAI
        client = OpenAI()

        resumo = f"""
        Total gasto: R$ {total:.2f}
        Gastos por categoria: {por_categoria.to_dict()}
        Perfil: {perfil['perfil']}
        """

        prompt = f"""
        Você é um assistente financeiro inteligente.

        Dados do usuário:
        {resumo}

        Pergunta:
        {pergunta}

        Responda de forma clara, prática e útil.
        """

        resposta = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return resposta.choices[0].message.content

    except Exception:
        # fallback se não tiver API
        return responder_regra(pergunta, total, por_categoria, perfil)


# =========================
# 🤖 Função principal
# =========================
def responder(pergunta, transacoes, perfil):
    if transacoes is None or perfil is None:
        return "Erro ao carregar dados. Verifique a pasta 'data'."

    total, por_categoria = analisar_gastos(transacoes)

    # tenta usar IA, senão usa regra
    return responder_com_ia(pergunta, total, por_categoria, perfil)