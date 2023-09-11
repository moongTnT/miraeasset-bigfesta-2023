from dateutil.relativedelta import relativedelta
import pandas as pd


def get_cap_weigh(*args, **kwargs):
    """
    #Kwargs
    child_prices: pd.DataFrame
        구성종목들의 주가 데이터
    pdf_df: pd.DataFrame
        구성종목들의 pdf데이터. "child_stk_tkr"와 "float_shares" 컬럼이 존재해야합니다
    """
    child_prices = kwargs.pop("child_prices")
    pdf_df = kwargs.pop("pdf_df")
    
    quartely_child_prices = child_prices.resample(rule='Q').apply(lambda x: x[0])
    
    dateindex_list = quartely_child_prices.index.to_list()
    
    # 날짜 리샘플링 후 없는 날짜 -> 있는 날짜(해당 월 말일)로 조정
    for i, date in enumerate(dateindex_list):
        while not date in child_prices.index:
            date = date - relativedelta(days=1)
        dateindex_list[i] = date
        
    quartely_child_prices.index = dateindex_list
    
    # 티커별 유동주식수
    float_shares_df = pdf_df[['child_stk_tkr', "float_shares"]]
    
    # 유동시가총액 산출
    quartely_child_cap = quartely_child_prices.copy()

    for tkr in quartely_child_cap.columns:

        if len(float_shares_df[float_shares_df['child_stk_tkr']==tkr.upper()]['float_shares']) >= 1:
        
            float_shares = float_shares_df[float_shares_df['child_stk_tkr']==tkr.upper()]['float_shares'].values[0]

            quartely_child_cap[tkr] = quartely_child_cap[tkr.lower()] * float_shares
        
    # 최종 비중 산출
    quartely_child_cap_weigh = quartely_child_cap.copy()

    for i in range(quartely_child_cap_weigh.shape[0]):

        total_cap = quartely_child_cap_weigh.iloc[i].sum()

        quartely_child_cap_weigh.iloc[i] = quartely_child_cap_weigh.iloc[i]/total_cap
        
    return quartely_child_cap_weigh


def get_bdd_cap_weigh(*args, **kwargs):
    """
    # Kwargs
    child_prices: pd.DataFrame
        구성종목들의 주가 데이터
    pdf_df: pd.DataFrame
        구성종목들의 pdf데이터. "child_stk_tkr"와 "float_shares" 컬럼이 존재해야합니다
    upper_bound: float
        상한 비중
    iter: int
        상한 비중에 도달할 때까지 비중 최적화 반복횟수. default=40
    """
    child_prices = kwargs.pop("child_prices")
    pdf_df = kwargs.pop("pdf_df")
    upper_bound = kwargs.pop("upper_bound")
    iter = kwargs.pop("iter", 40)
    
    quartely_child_prices = child_prices.resample(rule='Q').apply(lambda x: x[0])
    
    dateindex_list = quartely_child_prices.index.to_list()
    
    # 날짜 리샘플링 후 없는 날짜 -> 있는 날짜(해당 월 말일)로 조정
    for i, date in enumerate(dateindex_list):
        while not date in child_prices.index:
            date = date - relativedelta(days=1)
        dateindex_list[i] = date
        
    quartely_child_prices.index = dateindex_list
    
    # 티커별 유동주식수
    float_shares_df = pdf_df[['child_stk_tkr', "float_shares"]]
    
    # 유동시가총액 산출
    quartely_child_cap_upper_bound = quartely_child_prices.copy()
    
    
    # 최종 비중 산출
    weigh_serires_list = []

    for i in range(quartely_child_cap_upper_bound.shape[0]):

        prev = quartely_child_cap_upper_bound.iloc[i]/quartely_child_cap_upper_bound.iloc[i].sum()

        prev = prev.sort_values(ascending=False)

        for j in range(iter):
            test_weigh = prev/prev.sum()
            test_weigh = test_weigh.apply(lambda x : upper_bound if x > upper_bound else x)
            test_weigh = test_weigh/test_weigh.sum()
            prev = test_weigh

        weigh_serires_list.append(test_weigh)

    quartely_child_cap_upper_bound_weigh = pd.concat(weigh_serires_list, axis=1).T
    
    return quartely_child_cap_upper_bound_weigh