import json
from functools import wraps

import pymysql

with open('conf.json') as f:
    config = json.load(f)


def with_db_connection(f):
    """
    함수 f의 시작 전 후에 DB 커넥션 연결과 종료를 해주는 데코레이터 입니다
    """
    @wraps(f)
    def with_db_connection_(*args, **kwargs):
        conn = pymysql.connect(**config["db_config"],
                               cursorclass=pymysql.cursors.DictCursor)
        try:
            ret = f(*args, connection=conn, **kwargs)
        except:
            conn.rollback()
            print("SQL failed")
            raise
        else:
            conn.commit()
        finally:
            conn.close()
        
        return ret
    
    return with_db_connection_


@with_db_connection
def fetch_data_from_db(*args, **kwargs):
    """
    query를 인자로 받아 실행하고 출력을 DataFrame으로 변경해주는 함수입니다
    """
    conn = kwargs.pop("connection")
    query = kwargs.pop("query")
    
    cursor = conn.cursor()
    
    cursor.execute(query)
    
    return cursor.fetchall()


def fetch_theme_info(*args, **kwargs):
    
    sql = """
    SELECT * FROM os_theme_info
    """
    
    return fetch_data_from_db(query=sql)


def fetch_index_info(*args, **kwargs):
    
    etf_tkr = kwargs.pop("etf_tkr")
    
    sql = f"""
    SELECT upper_bound FROM os_index_info 
        WHERE etf_tkr='{etf_tkr}'
    """
    
    return fetch_data_from_db(query=sql)


def fetch_pdf_info(*args, **kwargs):
    
    etf_tkr = kwargs.pop("etf_tkr")
    
    sql = f"""
    SELECT pdf.child_stk_tkr, pdf.child_stk_name, stk.float_shares
        FROM os_pdf_info pdf
        INNER JOIN os_stk_info stk
        ON pdf.child_stk_tkr=stk.stk_tkr
        WHERE pdf.etf_tkr='{etf_tkr}'
    """
    
    return fetch_data_from_db(query=sql)


def fetch_stk_prices(*args, **kwargs):
    
    tickers = kwargs.pop("tickers")
    start_date = kwargs.pop("start_date")
    
    sql = f"""
        SELECT * FROM os_stk_price
            WHERE stk_tkr in ({"'"+"','".join(tickers)+"'"})
            AND date>=date({"'"+start_date+"'"})
            ORDER BY stk_tkr, date
    """
    
    return fetch_data_from_db(query=sql)