import streamlit as st

st.set_page_config(page_title="Simulador de DRE do Agronegócio", layout="centered")

st.title("🌾 Simulador de DRE do Agronegócio")

st.markdown("""
Preencha os campos abaixo com os valores da sua operação agrícola.
O sistema calculará automaticamente os indicadores em **Reais/ha** e **Reais/saca**, além do DRE completo.
""")

# Entradas do usuário
produtividade = st.number_input("Produtividade (sacas/ha):", min_value=0.0, step=0.1)
area = st.number_input("Área Plantada (ha):", min_value=0.0, step=0.1)
preco = st.number_input("Preço Médio de Venda (R$):", min_value=0.0, step=0.1)

st.markdown("---")

st.title("Custos de Produção")
#Custos de Produção
custo_insumos_def = st.number_input("Insumos: Defensivos Agrícolas (R$):", min_value= 0.0, step = 100.0)
custo_insumos_fert = st.number_input("Insumos: Fertilizantes (R$):", min_value= 0.0, step = 100.0)
custo_insumos_sem = st.number_input("Insumos: Sementes (R$):", min_value= 0.0, step = 100.0)
custo_insumos_out = st.number_input("Insumos: Outros Produtos (R$):", min_value= 0.0, step = 100.0)
custo_comb = st.number_input("Combustíveis Diretos (R$):", min_value= 0.0, step = 100.0)
custo_frete = st.number_input("Fretes (R$):", min_value= 0.0, step = 100.0)
custo_analises = st.number_input("Analises de Materiais (R$):", min_value= 0.0, step = 100.0)
custo_arrendamento = st.number_input("Arrendamentos (R$):", min_value= 0.0, step = 100.0)
custo_comissao = st.number_input("Comissões (R$):", min_value= 0.0, step = 100.0)
custo_manutencao = st.number_input("Manutenção Direta (R$):", min_value= 0.0, step = 100.0)
custo_mao_de_obra = st.number_input("Mão de Obra Direta (R$):", min_value= 0.0, step = 100.0)
custo_outros = st.number_input("Outros Custos De Produção (R$):", min_value= 0.0, step = 100.0)

st.markdown("---")

st.title("Despesas Não Operacionais")
#Despesas Não Operacionais
desp_comb = st.number_input("Combustíveis Indiretos (R$):", min_value=0.0, step=100.0)
desp_adm = st.number_input("Despesas Administrativas (R$):", min_value=0.0, step=100.0)
desp_frete = st.number_input("Fretes Indiretos (R$):", min_value=0.0, step=100.0)
desp_impostos = st.number_input("Impostos (R$):", min_value=0.0, step=100.0)
desp_seguros = st.number_input("Seguros (R$):", min_value=0.0, step=100.0)
desp_terceiros = st.number_input("Serviços Terceiros (R$):", min_value=0.0, step=100.0)
desp_man = st.number_input("Manutenção Indireta (R$):", min_value=0.0, step=100.0)
desp_outros = st.number_input("Outras Despesas Indiretas (R$):", min_value=0.0, step=100.0)

#Despesas Financeiras
desp_fin = st.number_input("Despesas Financeiras (R$):", min_value=0.0, step=100.0)

#Juros
juros = st.number_input("Juros Totais (R$):", min_value=0.0, step=100.0)

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
        custo_producao = custo_analises + custo_arrendamento + custo_comb + custo_comissao + custo_frete + custo_insumos_def + custo_insumos_fert + custo_insumos_sem + custo_insumos_out + custo_manutencao + custo_mao_de_obra + custo_outros
        desp_nao_op = desp_adm + desp_comb + desp_frete + desp_impostos + desp_man + desp_outros + desp_seguros + desp_terceiros


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
        margem_contribuicao = lucro_bruto / receita_liquida
        ebitda = lucro_bruto - desp_nao_op
        ebitda_perc = ebitda / receita_liquida

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
        st.write(f"**Receita Líquida:** R$ {receita_liquida:,.2f}")
        st.write(f"**Lucro Bruto:** R$ {lucro_bruto:,.2f}")
        st.write(f"**Margem de Contribuição:** % {margem_contribuicao:,.2f}")
        st.write(f"**Lucro Operacional:** R$ {lucro_operacional:,.2f}")
        st.write(f"**EBITDA %: {ebitda_perc:,.2f}")
        st.write(f"**Lucro Antes dos Juros:** R$ {lucro_antes_juros:,.2f}")
        st.write(f"**Lucro Líquido:** R$ {lucro_liquido:,.2f}")

        st.markdown("---")
        st.caption("Simulador desenvolvido por RSP · Agronegócio & Finanças")
