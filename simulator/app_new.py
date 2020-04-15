import streamlit as st
import texts_new

if __name__ == '__main__':

    st.sidebar.markdown(texts_new.INTRODUCTION_SIDEBAR)

    w_r0_model = st.sidebar.checkbox(texts_new.R0_MODEL_DESC)
    w_seir_model = st.sidebar.checkbox(texts_new.SEIR_MODEL_DESC)
    w_queue_model = st.sidebar.checkbox(texts_new.QUEUE_MODEL_DESC)
    
    st.sidebar.markdown(texts_new.BASE_PARAMETERS_DESCRIPTION)

    st.sidebar.markdown("**Parâmetro de UF/Município**")
    st.sidebar.markdown("Unidade")
    
    w_location_granularity = st.sidebar.radio(
        "Unidade",
        ("Estado", "Município")
    )

    #if w_location_granularity == 'Estado':
    #    st.sidebar.selectbox()


