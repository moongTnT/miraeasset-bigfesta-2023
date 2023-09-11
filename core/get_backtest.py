import bt


def get_base_backtest(*args, **kwargs):
    """
    # Kwargs
    name: str
    etf_price: pd.DataFrame
    """
    name = kwargs.pop("name")
    etf_price = kwargs.pop("etf_price")
    
    strategy = bt.Strategy(name=name,
                                algos=[
                                    bt.algos.SelectAll(),
                                    bt.algos.WeighEqually(),
                                    bt.algos.RunQuarterly(),
                                    bt.algos.Rebalance()
                                    ]
                                )
    
    return bt.Backtest(strategy, etf_price)

def get_eql_backtest(*args, **kwargs):
    """
    # Kwargs
    name: str
    child_prices: pd.DataFrame
    """
    name = kwargs.pop("name")
    child_prices = kwargs.pop("child_prices")
    
    strategy = bt.Strategy(name=name,
                                algos=[
                                    bt.algos.SelectAll(),
                                    bt.algos.WeighEqually(),
                                    bt.algos.RunQuarterly(),
                                    bt.algos.Rebalance()
                                    ]
                                )
    
    return bt.Backtest(strategy, child_prices)

def get_mkw_backtest(*args, **kwargs):
    """
    # Kwargs
    name: str
    child_prices: pd.DataFrame
    weigh: pd.DataFrame
    """
    name = kwargs.pop("name")
    child_prices = kwargs.pop("child_prices")
    weigh=kwargs.pop("weigh")
    
    strategy = bt.Strategy(name=name,
                                algos=[
                                    bt.algos.WeighTarget(weigh),
                                    bt.algos.Rebalance()
                                    ]
                                )
    
    return bt.Backtest(strategy, child_prices)

def get_bdd_mkw_backtest(*args, **kwargs):
    """
    # Kwargs
    name: str
    child_prices: pd.DataFrame
    weigh: pd.DataFrame
    """
    name = kwargs.pop("name")
    child_prices = kwargs.pop("child_prices")
    weigh=kwargs.pop("weigh")
    
    strategy = bt.Strategy(name=name,
                                algos=[
                                    bt.algos.WeighTarget(weigh),
                                    bt.algos.Rebalance()
                                    ]
                                )
    
    return bt.Backtest(strategy, child_prices)

def get_user_custom_backtest(*args, **kwargs):
    """
    # Kwargs
    name: str
    child_prices: pd.DataFrame
    weigh: pd.DataFrame
    """
    name = kwargs.pop("name")
    child_prices = kwargs.pop("child_prices")
    weigh=kwargs.pop("weigh")
    
    strategy = bt.Strategy(name=name,
                                algos=[
                                    bt.algos.WeighTarget(weigh),
                                    bt.algos.Rebalance()
                                    ]
                                )
    
    return bt.Backtest(strategy, child_prices)