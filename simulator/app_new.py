import streamlit as st
import texts_new

from covid19 import data

def create_basic_sidebar(): 

    MIN_DATA_BRAZIL = '2020-03-26'
    DEFAULT_CITY = 'São Paulo/SP'
    DEFAULT_STATE = 'SP'
    MIN_CASES_TH = 10

    def format_local(key):
        return {
            'state': 'Estado',
            'city': 'Município'
        }.get(key, key)

    @st.cache
    def make_place_options(cases_df, population_df):
        return (cases_df
                .swaplevel(0,1, axis=1)
                ['totalCases']
                .pipe(lambda df: df >= MIN_CASES_TH)
                .any()
                .pipe(lambda s: s[s & s.index.isin(population_df.index)])
                .index)

    @st.cache
    def make_date_options(cases_df, place):
        return (cases_df
                [place]
                ['totalCases']
                .pipe(lambda s: s[s >= MIN_CASES_TH])
                [MIN_DATA_BRAZIL:]
                .index
                .strftime('%Y-%m-%d'))

    st.sidebar.markdown(texts_new.INTRODUCTION_SIDEBAR)

    w_r0_model = st.sidebar.checkbox(texts_new.R0_MODEL_DESC)
    w_seir_model = st.sidebar.checkbox(texts_new.SEIR_MODEL_DESC)
    w_queue_model = st.sidebar.checkbox(texts_new.QUEUE_MODEL_DESC)
    
    st.sidebar.markdown(texts_new.BASE_PARAMETERS_DESCRIPTION)

    st.sidebar.markdown("**Parâmetro de UF/Município**")
    st.sidebar.markdown("Unidade")
    
    w_location_granularity = st.sidebar.radio(
        "Unidade",
        options=("state", "city"),
        index=1,
        format_func=format_local)

    if w_location_granularity == 'city':
        cases_df = data.load_cases(w_location_granularity, 'wcota')
        population_df = data.load_population(w_location_granularity)
        options_place = make_place_options(cases_df, population_df)
        index=options_place.get_loc(DEFAULT_CITY)
        location = st.sidebar.selectbox(
            'Município',
            options=options_place,
            index=options_place.get_loc(DEFAULT_CITY))
    elif w_location_granularity == "state":
        
        cases_df = data.load_cases(w_location_granularity, 'ms')
        population_df = data.load_population(w_location_granularity)
        options_place = make_place_options(cases_df, population_df)
        
        index=options_place.get_loc(DEFAULT_STATE)
        location = st.sidebar.selectbox(
            'Estado',
            options=options_place,
            index=options_place.get_loc(DEFAULT_STATE))
    # options_place = 

    # population_df = data.load_population(w_granularity)
    st.sidebar.selectbox('Data', ('2020-04-15', '2020-04-14'))

if __name__ == '__main__':

    create_basic_sidebar()
    st.markdown(texts_new.INTRODUCTION)