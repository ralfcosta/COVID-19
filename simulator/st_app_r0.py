import streamlit as st
import numpy as np

from st_utils import texts
from st_utils.viz import plot_r0
from covid19.estimation import ReproductionNumber

SAMPLE_SIZE = 500
MIN_DAYS_r0_ESTIMATE = 14
MIN_CASES_TH = 10

@st.cache
def make_brazil_cases(cases_df):
    return (cases_df
            .stack(level=1)
            .sum(axis=1)
            .unstack(level=1))

def prepare_for_r0_estimation(df):
    return (
        df
        ['newCases']
        .asfreq('D')
        .fillna(0)
        .rename('incidence')
        .reset_index()
        .rename(columns={'date': 'dates'})
        .set_index('dates')
    )

def estimate_r0(cases_df,
                w_location,
                w_date,
                sample_size = SAMPLE_SIZE,
                min_days = MIN_DAYS_r0_ESTIMATE):
    
    incidence = (
        cases_df
        [w_location]
        .query("totalCases > @MIN_CASES_TH")
        .pipe(prepare_for_r0_estimation)
        [:w_date]
    )

    if len(incidence) < MIN_DAYS_r0_ESTIMATE:
        used_brazil = True
        incidence = (
            make_brazil_cases(cases_df)
            .pipe(prepare_for_r0_estimation)
            [:w_date]
        )
    else:
        used_brazil = False

    Rt = ReproductionNumber(incidence=incidence,
                            prior_shape=5.12, prior_scale=0.64,
                            si_pars={'mean': 4.89, 'sd': 1.48},
                            window_width=MIN_DAYS_r0_ESTIMATE - 2)
    Rt.compute_posterior_parameters()
    samples = Rt.sample_from_posterior(sample_size=sample_size)
    return samples, used_brazil

def create_r0_interface(w_date,
                        w_location,
                        cases_df):

    r0_samples, used_brazil = estimate_r0(cases_df,
                                          w_location,
                                          w_date)

    if used_brazil:
        st.write(texts.r0_NOT_ENOUGH_DATA(w_location, w_date))
        location = 'Brasil'
    else:
        location =  w_location

    st.markdown(texts.r0_ESTIMATION(location, w_date))                      
    st.altair_chart(plot_r0(r0_samples,
                            w_date, 
                            location,
                            MIN_DAYS_r0_ESTIMATE))

    r0_dist = r0_samples[:, -1]
    st.markdown(f'**O $R_{{0}}$ estimado está entre '
                f'${np.quantile(r0_dist, 0.01):.03}$ e ${np.quantile(r0_dist, 0.99):.03}$**')
    st.markdown(texts.r0_CITATION)
