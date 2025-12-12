import streamlit as st

st.set_page_config(page_title="Simulador de DRE do Agronegócio", layout="centered")

st.title("🌾 Simulador de DRE do Agronegócio 🌾")

st.markdown("""
Preencha os campos abaixo com os valores da sua operação agrícola.
O sistema calculará automaticamente os indicadores em **Reais/ha** e **Reais/saca**, além do DRE completo.
""")

# Entradas do usuário
produtividade = st.number_input("Produtividade (sacas/ha):", min_value=0.0, step=0.1)
area = st.number_input("Área Plantada (ha):", min_value=0.0, step=0.1)
preco = st.number_input("Preço Médio de Venda (R$):", min_value=0.0, step=0.1)
custo_producao = st.number_input("Custo de Produção Total (R$):", min_value=0.0, step=100.0)
desp_nao_op = st.number_input("Despesas Não Operacionais (R$):", min_value=0.0, step=100.0)
desp_fin = st.number_input("Despesas Financeiras (R$):", min_value=0.0, step=100.0)
juros = st.number_input("Juros Totais (R$):", min_value=0.0, step=100.0)

# Botão para calcular
if st.button("Calcular DRE"):
    if area == 0 or produtividade == 0:
        st.error("Área plantada e produtividade devem ser maiores que zero.")
    else:
        # Cálculos básicos
        producao_total = produtividade * area
        receita_total = producao_total * preco
        deducoes = receita_total * 0.3

        # R$/ha
        receita_ha = receita_total / area
        custo_ha = custo_producao / area
        desp_no_ha = desp_nao_op / area
        desp_fin_ha = desp_fin / area
        juros_ha = juros / area

        # R$/saca
        receita_saca = receita_total / producao_total
        custo_saca = custo_producao / producao_total
        desp_no_saca = desp_nao_op / producao_total
        desp_fin_saca = desp_fin / producao_total
        juros_saca = juros / producao_total

        # DRE Final
        lucro_bruto = receita_total - custo_producao
        lucro_operacional = lucro_bruto - desp_nao_op
        lucro_antes_juros = lucro_operacional - desp_fin
        lucro_liquido = lucro_antes_juros - juros

        st.success("Cálculo realizado com sucesso!")

        # Resultados
        st.header("📊 Resultados do DRE")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("R$/ha")
            st.write(f"**Receita/ha:** R$ {receita_ha:,.2f}")
            st.write(f"**Custo de Produção/ha:** R$ {custo_ha:,.2f}")
            st.write(f"**Despesas Não Operacionais/ha:** R$ {desp_no_ha:,.2f}")
            st.write(f"**Despesas Financeiras/ha:** R$ {desp_fin_ha:,.2f}")
            st.write(f"**Juros/ha:** R$ {juros_ha:,.2f}")

        with col2:
            st.subheader("R$/saca")
            st.write(f"**Receita/saca:** R$ {receita_saca:,.2f}")
            st.write(f"**Custo/saca:** R$ {custo_saca:,.2f}")
            st.write(f"**Despesas Não Operacionais/saca:** R$ {desp_no_saca:,.2f}")
            st.write(f"**Despesas Financeiras/saca:** R$ {desp_fin_saca:,.2f}")
            st.write(f"**Juros/saca:** R$ {juros_saca:,.2f}")

        st.header("📘 DRE Completo")

        st.write(f"**Produção Total:** {producao_total:,.2f} sacas")
        st.write(f"**Receita Bruta:** R$ {receita_total:,.2f}")
        st.write(f"**Deduções de Impostos:** R$ {deducoes:,.2f}")
        st.write(f"**Lucro Bruto:** R$ {lucro_bruto:,.2f}")
        st.write(f"**Lucro Operacional:** R$ {lucro_operacional:,.2f}")
        st.write(f"**Lucro Antes dos Juros:** R$ {lucro_antes_juros:,.2f}")
        st.write(f"**Lucro Líquido:** R$ {lucro_liquido:,.2f}")

        st.markdown("---")
        st.caption("Simulador desenvolvido por RSP · Agronegócio & Finanças")
