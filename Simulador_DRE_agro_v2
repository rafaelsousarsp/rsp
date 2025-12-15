import streamlit as st
import pandas as pd
from io import BytesIO

# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------
st.set_page_config(
    page_title="Simulador de DRE do Agronegócio",
    layout="centered"
)

st.title("🌾 Simulador de DRE – Agronegócio")
st.markdown("""
Preencha os campos abaixo com os dados da sua operação agrícola.
O sistema calculará automaticamente o **DRE completo**, indicadores em **R$/ha** e **R$/saca**.
""")

# --------------------------------------------------
# ENTRADAS PRINCIPAIS
# --------------------------------------------------
produtividade = st.number_input("Produtividade (sacas/ha)", min_value=0.0, step=0.1)
area = st.number_input("Área Plantada (ha)", min_value=0.0, step=0.1)
preco = st.number_input("Preço Médio de Venda (R$)", min_value=0.0, step=0.1)

st.markdown("---")

# --------------------------------------------------
# CUSTOS DE PRODUÇÃO
# --------------------------------------------------
st.subheader("📉 Custos de Produção")

custo_insumos_def = st.number_input("Defensivos Agrícolas (R$)", 0.0, step=100.0)
custo_insumos_fert = st.number_input("Fertilizantes (R$)", 0.0, step=100.0)
custo_insumos_sem = st.number_input("Sementes (R$)", 0.0, step=100.0)
custo_insumos_out = st.number_input("Outros Insumos (R$)", 0.0, step=100.0)
custo_comb = st.number_input("Combustíveis Diretos (R$)", 0.0, step=100.0)
custo_frete = st.number_input("Fretes Diretos (R$)", 0.0, step=100.0)
custo_analises = st.number_input("Análises (R$)", 0.0, step=100.0)
custo_arrendamento = st.number_input("Arrendamento (R$)", 0.0, step=100.0)
custo_comissao = st.number_input("Comissões (R$)", 0.0, step=100.0)
custo_manutencao = st.number_input("Manutenção Direta (R$)", 0.0, step=100.0)
custo_mao_obra = st.number_input("Mão de Obra Direta (R$)", 0.0, step=100.0)
custo_outros = st.number_input("Outros Custos (R$)", 0.0, step=100.0)

st.markdown("---")

# --------------------------------------------------
# DESPESAS
# --------------------------------------------------
st.subheader("📉 Despesas Não Operacionais")

desp_comb = st.number_input("Combustíveis Indiretos (R$)", 0.0, step=100.0)
desp_adm = st.number_input("Despesas Administrativas (R$)", 0.0, step=100.0)
desp_frete = st.number_input("Fretes Indiretos (R$)", 0.0, step=100.0)
desp_impostos = st.number_input("Impostos (R$)", 0.0, step=100.0)
desp_seguros = st.number_input("Seguros (R$)", 0.0, step=100.0)
desp_terceiros = st.number_input("Serviços Terceiros (R$)", 0.0, step=100.0)
desp_man = st.number_input("Manutenção Indireta (R$)", 0.0, step=100.0)
desp_outros = st.number_input("Outras Despesas (R$)", 0.0, step=100.0)

desp_fin = st.number_input("Despesas Financeiras (R$)", 0.0, step=100.0)
juros = st.number_input("Juros Totais (R$)", 0.0, step=100.0)

# --------------------------------------------------
# BOTÃO DE CÁLCULO
# --------------------------------------------------
if st.button("📊 Calcular DRE"):
    if area == 0 or produtividade == 0:
        st.error("Área plantada e produtividade devem ser maiores que zero.")
    else:
        # PRODUÇÃO E RECEITA
        producao_total = produtividade * area
        receita_total = producao_total * preco
        deducoes = receita_total * 0.03
        receita_liquida = receita_total - deducoes

        # CUSTOS E DESPESAS
        custo_producao = (
            custo_insumos_def + custo_insumos_fert + custo_insumos_sem +
            custo_insumos_out + custo_comb + custo_frete + custo_analises +
            custo_arrendamento + custo_comissao + custo_manutencao +
            custo_mao_obra + custo_outros
        )

        desp_nao_op = (
            desp_comb + desp_adm + desp_frete + desp_impostos +
            desp_seguros + desp_terceiros + desp_man + desp_outros
        )

        # DRE
        lucro_bruto = receita_total - custo_producao
        lucro_operacional = lucro_bruto - desp_nao_op
        lucro_antes_juros = lucro_operacional - desp_fin
        lucro_liquido = lucro_antes_juros - juros

        margem_contribuicao = (lucro_bruto / receita_liquida) * 100
        ebitda = lucro_operacional
        ebitda_perc = (ebitda / receita_liquida) * 100

        # --------------------------------------------------
        # DATAFRAME DRE
        # --------------------------------------------------
        dre_df = pd.DataFrame({
            "Descrição": [
                "Produção Total (sacas)",
                "Receita Bruta",
                "Deduções",
                "Receita Líquida",
                "Custo de Produção",
                "Lucro Bruto",
                "Despesas Não Operacionais",
                "Lucro Operacional",
                "Despesas Financeiras",
                "Lucro Antes dos Juros",
                "Juros",
                "Lucro Líquido",
                "Margem de Contribuição (%)",
                "EBITDA (%)"
            ],
            "Valor": [
                producao_total,
                receita_total,
                deducoes,
                receita_liquida,
                custo_producao,
                lucro_bruto,
                desp_nao_op,
                lucro_operacional,
                desp_fin,
                lucro_antes_juros,
                juros,
                lucro_liquido,
                margem_contribuicao,
                ebitda_perc
            ]
        })

        st.success("Cálculo realizado com sucesso!")

        st.subheader("📘 DRE Completo")
        st.dataframe(dre_df, use_container_width=True)

        # --------------------------------------------------
        # EXPORTAÇÃO PARA EXCEL
        # --------------------------------------------------
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            dre_df.to_excel(writer, index=False, sheet_name="DRE")

        st.download_button(
            label="📥 Exportar DRE para Excel",
            data=buffer.getvalue(),
            file_name="dre_agro_rsp.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.markdown("---")
        st.caption("Simulador desenvolvido por RSP · Agronegócio & Finanças")
