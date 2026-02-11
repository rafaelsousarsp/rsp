import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Simulador de Custo de Insumos - Safra",
    layout="wide"
)

st.title("🌾 Simulador de Custo de Insumos – Safra")
st.caption("Conversão automática Real + Dólar com PTAX")

# ==========================================================
# ENTRADAS PRINCIPAIS
# ==========================================================

st.subheader("📌 Dados Gerais")

col1, col2, col3 = st.columns(3)

with col1:
    preco_saca = st.number_input("Preço da Saca (R$)", min_value=0.0, step=1.0)

with col2:
    area = st.number_input("Área Plantada (ha)", min_value=0.0, step=1.0)

with col3:
    ptax = st.number_input("PTAX (R$/US$)", min_value=0.0, step=0.01)

# ==========================================================
# INSUMOS
# ==========================================================

st.subheader("📦 Insumos")

insumos = [
    "Corretivos",
    "Fertilizantes",
    "Nitrogênio",
    "Fósforo",
    "Potássio",
    "Fungicidas",
    "Herbicidas",
    "Inseticidas",
    "Sementes Soja",
    "Sementes Milho"
]

dados = []

for insumo in insumos:
    col1, col2 = st.columns(2)
    
    with col1:
        valor_real = st.number_input(f"{insumo} - Valor em R$", min_value=0.0, step=100.0, key=f"real_{insumo}")
    
    with col2:
        valor_dolar = st.number_input(f"{insumo} - Valor em US$", min_value=0.0, step=100.0, key=f"dolar_{insumo}")
    
    total_convertido = valor_real + (valor_dolar * ptax)
    
    dados.append({
        "Insumo": insumo,
        "Real (R$)": valor_real,
        "Dólar (US$)": valor_dolar,
        "Total (R$)": total_convertido
    })

# ==========================================================
# CÁLCULOS
# ==========================================================

if st.button("📊 Calcular Custos"):

    if area == 0 or preco_saca == 0:
        st.error("Preço da saca e área devem ser maiores que zero.")
    else:

        df = pd.DataFrame(dados)

        total_geral = df["Total (R$)"].sum()
        custo_por_ha = total_geral / area
        sacas_por_ha = custo_por_ha / preco_saca
        total_sacas = total_geral / preco_saca

        df["R$/ha"] = df["Total (R$)"] / area
        df["Sacas/ha"] = df["R$/ha"] / preco_saca

        # ======================================================
        # KPIs
        # ======================================================
        st.markdown("## 📌 Indicadores Consolidados")

        k1, k2, k3, k4 = st.columns(4)

        k1.metric("Custo Total", f"R$ {total_geral:,.0f}")
        k2.metric("Custo por ha", f"R$ {custo_por_ha:,.2f}")
        k3.metric("Sacas por ha", f"{sacas_por_ha:,.2f}")
        k4.metric("Total em Sacas", f"{total_sacas:,.0f}")

        st.markdown("## 📋 Detalhamento por Insumo")
        st.dataframe(df, use_container_width=True)

        # ======================================================
        # EXPORTAÇÃO EXCEL
        # ======================================================

        resumo_df = pd.DataFrame({
            "Indicador": [
                "Custo Total",
                "Custo por ha",
                "Sacas por ha",
                "Total em Sacas"
            ],
            "Valor": [
                total_geral,
                custo_por_ha,
                sacas_por_ha,
                total_sacas
            ]
        })

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Insumos")
            resumo_df.to_excel(writer, index=False, sheet_name="Resumo")

        st.download_button(
            "📥 Baixar Planilha do Simulador",
            buffer.getvalue(),
            file_name="simulador_custo_insumos_safra.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.caption("Simulador Estratégico • RSP | Finanças & Agronegócio")
