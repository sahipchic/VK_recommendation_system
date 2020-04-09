import pymysql
from sqlalchemy import create_engine
import pandas as pd

def main():
    movies_df = pd.read_csv('movies.csv')

    con = pymysql.connect(
        host="remotemysql.com",
        port=int(3306),
        user="AmLB63D4F9",
        passwd="ARsY8WGMUO",
        db="AmLB63D4F9",
        charset='utf8mb4')

    db_data = 'mysql+mysqldb://' + 'root' + ':' + '12345' + '@' + 'localhost' + ':3306/' \
           + 'book' + '?charset=utf8mb4'

    engine = create_engine("mysql+pymysql://AmLB63D4F9:ARsY8WGMUO@remotemysql.com/AmLB63D4F9?host=remotemysql.com?port=3306")

    with con:
        cur = con.cursor()
        movies_df.to_sql('movies', engine, if_exists='append', index=False)

    con.close()


if __name__ == '__main__':
    main()