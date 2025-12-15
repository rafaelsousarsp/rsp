import streamlit as st

def br(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(page_title="Simulador de DRE do Agronegócio", layout="centered")

st.title("🌾 Simulador de DRE do Agronegócio 🌾")

st.markdown("""
Preencha os campos abaixo com os valores da sua operação agrícola.
O sistema calculará automaticamente os indicadores em **Reais/ha** e **Reais/saca**, além do DRE completo.
""")

st.sidebar.header("🎯 Simulador")

# Entradas do usuário
produtividade = st.sidebar.slider ("Produtividade (sacas/ha):", 0.0, 200.0, 0.0, step =0.1 )
area = st.sidebar.slider ("Área Plantada (ha):", 0.0, 20000.0, 0.0, step=0.1)
preco = st.sidebar.slider("Preço Médio de Venda (R$):", 0.0, 200.0, 0.0, step=0.1)
custo_producao = st.sidebar.slider("Custo de Produção Total (R$):", 0.0, 100000000.0, 0.0, step=100.0)
desp_nao_op = st.sidebar.slider("Despesas Não Operacionais (R$):", 0.0, 100000000.0, 0.0, step=100.0)
desp_fin = st.sidebar.slider("Despesas Financeiras (R$):", 0.0, 10000000.0, 0.0, step=100.0)
juros = st.sidebar.slider("Juros Totais (R$):", 0.0, 10000000.0, 0.0, step=100.0)

# Botão para calcular
if st.button("Calcular DRE"):
    if area == 0 or produtividade == 0:
        st.error("Área plantada e produtividade devem ser maiores que zero.")
    else:
        # Cálculos básicos
        producao_total = produtividade * area
        receita_total = producao_total * preco
        deducoes = receita_total * 0.03
        receita_liquida = receita_total - deducoes

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
        margem_contribuicao = (lucro_bruto / receita_liquida) * 100
        ebitda = lucro_bruto - desp_nao_op
        ebitda_perc = (ebitda / receita_liquida) * 100

        st.success("Cálculo realizado com sucesso!")

        # Resultados
        st.header("📊 Resultados do DRE 📊")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("R$/ha")
            st.write(f"**Receita/ha:** R$ {br(receita_ha)}")
            st.write(f"**Custo de Produção/ha:** R$ {br(custo_ha)}")
            st.write(f"**Despesas Não Operacionais/ha:** R$ {br(desp_no_ha)}")
            st.write(f"**Despesas Financeiras/ha:** R$ {br(desp_fin_ha)}")
            st.write(f"**Juros/ha:** R$ {br(juros_ha)}")

        with col2:
            st.subheader("R$/saca")
            st.write(f"**Receita/saca:** R$ {br(receita_saca)}")
            st.write(f"**Custo/saca:** R$ {br(custo_saca)}")
            st.write(f"**Despesas Não Operacionais/saca:** R$ {br(desp_no_saca)}")
            st.write(f"**Despesas Financeiras/saca:** R$ {br(desp_fin_saca)}")
            st.write(f"**Juros/saca:** R$ {br(juros_saca)}")

        st.header("📘 DRE Completo 📘")

        st.write(f"**Produção Total:** {br(producao_total)} sacas")
        st.write(f"**Receita Bruta:** R$ {br(receita_total)}")
        st.write(f"**Deduções de Impostos:** R$ {br(deducoes)}")
        st.write(f"**Receita Líquida:** R$ {br(receita_liquida)}")
        st.write(f"**Custo de Produção:** R$ {br(custo_producao)}")
        st.write(f"**Lucro Bruto:** R$ {br(lucro_bruto)}")
        st.write(f"**Margem de Contribuição:** {br(margem_contribuicao)} %")
        st.write(f"**Lucro Operacional:** R$ {br(lucro_operacional)}")
        st.write(f"**EBITDA %:** {br(ebitda_perc)} %")
        st.write(f"**Lucro Antes dos Juros:** R$ {br(lucro_antes_juros)}")
        st.write(f"**Lucro Líquido:** R$ {br(lucro_liquido)}")

        st.markdown("---")
        st.caption("Simulador desenvolvido por RSP · Agronegócio & Finanças")
