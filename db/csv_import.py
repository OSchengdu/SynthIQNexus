import sqlite3
import pandas as pd

def import_air_quatity():
    conn = sqlite3.connect('a.db')
    df = pd.read_csv('Air_Quality.csv', delimiter='\t') 
    df.to_sql('air_quality', conn, if_exists='replace', index=False)
    conn.close()
# NOTE: 不清楚sqlite性能如何，是否需要对该文件分块处理
def import_ev():
    conn = sqlite3.connect('e.db')
    df = pd.read_csv('Electric_Vehicle_Population_Data.csv')
    df.to_sql('ev_population', conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":
    import_air_quatity()
    import_ev()
