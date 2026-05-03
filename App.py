import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Controle de Pets - Stark Gamestore", layout="wide")

st.title("🐾 Controle de Pets")
st.write("Adicione seus pets, acompanhe os valores e veja o total da sua coleção.")

# Arquivo simples para salvar os dados
arquivo_dados = "lista_de_pets.csv"

# Função para carregar os dados
def carregar_dados():
    try:
        return pd.read_csv(arquivo_dados)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Nome", "Peso (kg)", "Valor (Tokens)"])

# Inicializa os dados na sessão
df_pets = carregar_dados()

# --- Formulário de Cadastro ---
st.subheader("➕ Adicionar Novo Pet")
with st.form("form_pet", clear_on_submit=True):
    nome = st.text_input("Nome do Pet (ex: Rubi Squid, Mimic, etc.)")
    peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1)
    valor = st.number_input("Valor (Tokens)", min_value=0, step=1)
    
    submit = st.form_submit_button("Salvar Pet")
    
    if submit:
        if nome != "":
            novo_pet = pd.DataFrame([[nome, peso, valor]], columns=["Nome", "Peso (kg)", "Valor (Tokens)"])
            df_atualizado = pd.concat([df_pets, novo_pet], ignore_index=True)
            df_atualizado.to_csv(arquivo_dados, index=False)
            st.success(f"Pet '{nome}' adicionado com sucesso!")
            st.rerun()
        else:
            st.warning("Por favor, preencha o nome do pet.")

# --- Painel de Totais ---
st.subheader("📊 Resumo da Coleção")
total_pets = len(df_pets)
total_peso = df_pets["Peso (kg)"].sum()
total_valor = df_pets["Valor (Tokens)"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total de Pets", f"{total_pets}")
col2.metric("Peso Total", f"{total_peso:.1f} kg")
col3.metric("Valor Total", f"{total_valor:,.0f} Tokens".replace(",", "."))

# --- Tabela de Pets Cadastrados ---
st.subheader("📋 Pets Cadastrados")
if total_pets > 0:
    st.dataframe(df_pets, use_container_width=True)
    
    if st.button("🗑️ Limpar toda a lista"):
        df_limpo = pd.DataFrame(columns=["Nome", "Peso (kg)", "Valor (Tokens)"])
        df_limpo.to_csv(arquivo_dados, index=False)
        st.rerun()
else:
    st.info("Nenhum pet cadastrado ainda.")
                                      
