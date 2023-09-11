
import numpy as np
import statsmodels.api as sm

from data.get_data import get_prices_df

def get_lowest_PBR_stks(docs_list):

    PBR_KEY = "priceToBook"
    SYMBOL_KEY = "symbol"

    pbr_list = []

    for docs in docs_list['metadatas']:
        if PBR_KEY in docs.keys():
            pbr_list.append((docs[PBR_KEY], docs[SYMBOL_KEY]))

    pbr_list.sort()
    
    return pbr_list[:round(len(pbr_list)*0.2)]

def get_momentums(filter_list):

    def get_k_ratio(prices_df):

        prices_df = prices_df.dropna()

        ret = prices_df.pct_change().iloc[1:]

        ret_cum = np.log(1+ret).cumsum()

        x = np.array(range(len(ret)))
        y = ret_cum.iloc[:].values

        reg = sm.OLS(y, x).fit()

        return (reg.params/reg.bse) # K-ratio


    tickers = [fltr['symbol'] for fltr in filter_list]

    prices_df = get_prices_df(
        tickers=tickers,
        start_date="2022-08-29"
    )

    kratio_list = []

    for t in tickers:

        kratio = get_k_ratio(prices_df=prices_df[t.lower()])

        kratio_list.append((round(kratio[0], 2), t))

    kratio_list.sort(reverse=True)

    return kratio_list[:round(len(kratio_list)*0.2)]
    
    