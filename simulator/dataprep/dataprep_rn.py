class DataPrepRN:

    @staticmethod
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

    @staticmethod
    def load_incidence_by_location(cases_df, date, location, min_casest_th):

        return (
            cases_df
            [location]
            .query("totalCases > @min_casest_th")
            .pipe(DataPrepRN.prepare_for_r0_estimation)
            [:date]
        )
    @staticmethod
    def make_brazil_cases(cases_df):
        return (cases_df
                .stack(level=1)
                .sum(axis=1)
                .unstack(level=1))