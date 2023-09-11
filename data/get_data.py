from data.fetch_data import fetch_pdf_info, fetch_stk_prices
import pandas as pd

def get_pdf_df(*args, **kwargs):
    """
    # Kwargs
    etf_tkr: str
        ETF 티커
    """
    etf_tkr = kwargs.pop("etf_tkr")
    
    pdf = fetch_pdf_info(etf_tkr=etf_tkr)

    return pd.DataFrame(pdf)

def get_prices_df(*args, **kwargs):
    """
    # Kwargs
    tickers: list[str]
        티커 리스트
    start_date: str
        불러올 가격의 시작날짜
    """
    tkrs = kwargs.pop("tickers")
    start_date = kwargs.pop("start_date")

    child_prices_from_db = fetch_stk_prices(tickers=tkrs, start_date=str(start_date))
    child_prices_df = pd.DataFrame(child_prices_from_db)

    tmp_price_df_list = []

    for tkr, price_df in child_prices_df.groupby("stk_tkr"):
        df_tmp = price_df[['date', 'close']].set_index("date", drop=True)
        df_tmp.index = pd.DatetimeIndex(df_tmp.index)
        df_tmp.rename(columns={"close": tkr.lower()}, inplace=True)

        tmp_price_df_list.append(df_tmp)

    child_prices = pd.concat(tmp_price_df_list, axis=1).dropna()
    
    return child_prices

def get_base_price_df(*args, **kwargs):
    """
    # Kwargs
    etf_tkr: str
        etf 티커
    start_date: str
        불러올 가격의 시작날짜
    """
    etf_tkr = kwargs.pop("etf_tkr")
    start_date = kwargs.pop("start_date")
    
    child_prices_from_db = fetch_stk_prices(tickers=[etf_tkr], start_date=str(start_date))
    child_prices_df = pd.DataFrame(child_prices_from_db)
    
    etf_price = child_prices_df[['date', 'close']].set_index(keys="date", drop=True).rename(columns={"close": etf_tkr})
    etf_price.index = pd.DatetimeIndex(etf_price.index)
    
    return etf_price