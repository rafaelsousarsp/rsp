import streamlit as st
import pandas as pd
from io import BytesIO

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Simulador Profissional de DRE - Agronegócio",
    layout="wide"
)

st.title("🌾 Simulador Profissional de DRE – Agronegócio")
st.caption("Análise financeira, cenários e indicadores estratégicos")

# SIDEBAR — SIMULADOR DE CENÁRIOS
st.sidebar.header("🎯 Indicadores")

produtividade = st.sidebar.number_input("Produtividade (sc/ha)", 0.0, step=1.0)
area = st.sidebar.number_input("Área Plantada (ha)", 0.0, step=1.0)
preco = st.sidebar.number_input("Preço Médio (R$/sc)", 0.0, step=1.0)

ajuste_preco = st.sidebar.slider("Variação de Preço (%)", -30, 30, 0)
ajuste_prod = st.sidebar.slider("Variação de Produtividade (%)", -30, 30, 0)
ajuste_custo = st.sidebar.slider("Variação de Custos (%)", -30, 30, 0)

# APLICAÇÃO DOS CENÁRIOS
preco_aj = preco * (1 + ajuste_preco / 100)
prod_aj = produtividade * (1 + ajuste_prod / 100)

# CUSTOS DE PRODUÇÃO
st.subheader("📉 Custos de Produção")

col1, col2, col3 = st.columns(3)

with col1:
    custo_insumos_def = st.number_input("Insumos: Defensivos (R$)", 0.0, step=100.0)
    custo_insumos_fert = st.number_input("Insumos: Fertilizantes (R$)", 0.0, step=100.0)
    custo_insumos_sem = st.number_input("Insumos: Sementes (R$)", 0.0, step=100.0)
    custo_insumos_out = st.number_input("Insumos: Outros Insumos (R$)", 0.0, step=100.0)

with col2:
    custo_comb = st.number_input("Combustíveis (R$)", 0.0, step=100.0)
    custo_frete = st.number_input("Fretes (R$)", 0.0, step=100.0)
    custo_analises = st.number_input("Análises de Materiais (R$)", 0.0, step=100.0)
    custo_arrendamento = st.number_input("Arrendamento (R$)", 0.0, step=100.0)

with col3:
    custo_mao_obra = st.number_input("Mão de Obra (R$)", 0.0, step=100.0)
    custo_manutencao = st.number_input("Manutenção (R$)", 0.0, step=100.0)
    custo_comissoes = st.number_input("Comissões (R$)", 0.0, step=100.0)
    custo_outros = st.number_input("Outros Custos de Produção (R$)", 0.0, step=100.0)

# DESPESAS NÃO OPERACIONAIS
st.subheader("📉 Despesas Não Operacionais")

col1, col2, col3 = st.columns(3)

with col1:
    desp_comb = st.number_input("Combustíveis Indiretos (R$):", 0.0, step=100.0)
    desp_adm = st.number_input("Despesas Administrativas (R$):",0.0, step=100.0)
    desp_frete = st.number_input("Fretes Indiretos (R$):", 0.0, step=100.0)
    desp_impostos = st.number_input("Impostos (R$):", 0.0, step=100.0)

with col2:
    desp_seguros = st.number_input("Seguros (R$):", 0.0, step=100.0)
    desp_terceiros = st.number_input("Serviços Terceiros (R$):", 0.0, step=100.0)
    desp_man = st.number_input("Manutenção Indireta (R$):", 0.0, step=100.0)
    desp_outros = st.number_input("Outras Despesas Indiretas (R$):", 0.0, step=100.0)

with col3:
    desp_fin = st.number_input("Despesas Financeiras (R$)", 0.0, step=100.0)
    juros = st.number_input("Juros Totais (R$)", 0.0, step=100.0)

# BOTÃO DE CÁLCULO
if st.button("📊 Calcular Cenário"):
    if area == 0 or produtividade == 0:
        st.error("Área e produtividade devem ser maiores que zero.")
    else:
        # --------------------------------------------------
        # CÁLCULOS PRINCIPAIS
        # --------------------------------------------------
        producao_total = prod_aj * area
        receita_total = producao_total * preco_aj
        deducoes = receita_total * 0.03
        receita_liquida = receita_total - deducoes

        custo_base = (
            custo_insumos_def + custo_insumos_fert + custo_insumos_out + custo_insumos_sem + custo_mao_obra + custo_manutencao +
            custo_frete + custo_comb + custo_arrendamento
        )

        custo_producao = custo_base * (1 + ajuste_custo / 100)
        desp_nao_op = desp_adm + desp_comb + desp_fin + desp_frete + desp_impostos + desp_man + desp_outros + desp_seguros + desp_terceiros
        lucro_bruto = receita_total - custo_producao
        lucro_operacional = lucro_bruto - desp_nao_op
        lucro_antes_juros = lucro_operacional - desp_fin
        lucro_liquido = lucro_antes_juros - juros

        margem = (lucro_liquido / receita_liquida) * 100 if receita_liquida > 0 else 0
        ebitda = lucro_operacional
        ebitda_perc = (ebitda / receita_liquida) * 100 if receita_liquida > 0 else 0

        # ==================================================
        # CARDS DE MÉTRICAS (KPIs)
        # ==================================================
        st.markdown("## 📌 Indicadores-Chave")

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        kpi1.metric("Receita Líquida", f"R$ {receita_liquida:,.0f}")
        kpi2.metric("Lucro Líquido", f"R$ {lucro_liquido:,.0f}")
        kpi3.metric("Margem Líquida", f"{margem:,.1f}%")
        kpi4.metric("EBITDA", f"R$ {ebitda:,.0f}")

        # ==================================================
        # TABELAS ANALÍTICAS
        # ==================================================
        dre_df = pd.DataFrame({
            "Descrição": [
                "Produção Total (sc)",
                "Receita Bruta",
                "Deduções",
                "Receita Líquida",
                "Custo de Produção",
                "Lucro Bruto",
                "Despesas Administrativas",
                "Lucro Operacional",
                "Despesas Financeiras",
                "Juros",
                "Lucro Líquido"
            ],
            "Valor (R$)": [
                producao_total,
                receita_total,
                deducoes,
                receita_liquida,
                custo_producao,
                lucro_bruto,
                desp_nao_op,
                lucro_operacional,
                desp_fin,
                juros,
                lucro_liquido
            ]
        })

        por_ha_df = pd.DataFrame({
            "Indicador": ["Receita", "Custo", "Lucro"],
            "R$/ha": [
                receita_total / area,
                custo_producao / area,
                lucro_liquido / area
            ]
        })

        por_saca_df = pd.DataFrame({
            "Indicador": ["Receita", "Custo", "Lucro"],
            "R$/sc": [
                receita_total / producao_total,
                custo_producao / producao_total,
                lucro_liquido / producao_total
            ]
        })

        st.markdown("## 📘 Demonstrativo de Resultado")
        st.dataframe(dre_df, use_container_width=True)

        # ==================================================
        # EXPORTAÇÃO PROFISSIONAL PARA EXCEL
        # ==================================================
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            dre_df.to_excel(writer, index=False, sheet_name="DRE")
            por_ha_df.to_excel(writer, index=False, sheet_name="Indicadores_ha")
            por_saca_df.to_excel(writer, index=False, sheet_name="Indicadores_saca")

        st.download_button(
            "📥 Exportar Análise Completa (Excel)",
            buffer.getvalue(),
            file_name="simulador_dre_profissional_rsp.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.caption("Simulador Profissional • RSP | Finanças & Agronegócio")
