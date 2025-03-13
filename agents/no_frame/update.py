from dork import DorkAgent
import pandas as pd

class DataUpdater:
    def __init__(self):
        # dork
        # from dork import DorkAgent
        self.dork_agent = DorkAgent(es_hosts=["https://localhost:9200"])

    def _init_sqlite(self):
        pass

    def _fetch_data(self, data_list:list[str]):
        pass
    
    def _clean_data(self, raw_df:pd.DataFrame, data_name:str) -> pd.DataFrame:
        pass

    def _update_sqlite(self, clean_df: pd.DataFrame, table: str):
        pass

    def _update_elasticsearch(self, clean_df: pd.DataFrame, index: str):
        pass

    def _update_task(self):
        # dork 
        self.dork_agent.sync_from_sqlite(CONFIG["sqlite_db_path"])

    def run(self):
        pass

    def DataUpdater():
        pass


if __name__=="__main__":
    # get config file
    with open(".cfgr", "w") as f:
        f.write(config)

    # havent achive this function yet 
    updater = DataUpdater()
    updater.run()

