import streamlit as st

if __name__ == '__main__':

    st.sidebar.markdown("# Projeções")
    st.sidebar.markdown("Selecione as projeções que deseja simular")
    st.sidebar.markdown("Selecione as projeções que deseja simular")

    w_r0_model = st.sidebar.checkbox("Número de reprodução básico")
    w_seir_model = st.sidebar.checkbox("Previsão de infectados (modelo SEIR-Bayes)")
    w_queue_model = st.sidebar.checkbox("Simulação de fila hospitalar")
    
    st.sidebar.markdown("# Seleção de parâmetros")
g