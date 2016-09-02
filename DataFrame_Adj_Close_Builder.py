import pandas as pd
from datetime import date

path_of_control_stock="SPY"
stock_basedir = "data/"

class DataFrame_Adj_Close_Builder:

    def __init__(self, adjusted_close_id="Adj Close", refer_date_id="Date"):
        self.adjusted_close_id = adjusted_close_id
        self.refer_date_id = refer_date_id
        self._dates = None
        self._df = None

    def _setDateRange(self, start_date, end_date):
        self._dates = pd.date_range(start=start_date, end=end_date)

    def _initDataFrame(self):
        self._df = pd.DataFrame(index=self._dates)

    def _removeInactiveDays(self, control_path, basedir):
        control_trader = pd.read_csv(basedir+control_path+".csv",  index_col=self.refer_date_id, parse_dates=True,
                                           usecols=[self.refer_date_id, self.adjusted_close_id], na_values=["nan"])
        self._df = self._df.join(control_trader, how="inner")
        self._df = self._df.rename(columns={self.adjusted_close_id: self.adjusted_close_id + " " + control_path})

    def _join(self, indexes, basedir):
        for index in indexes:
            df_tmp = pd.read_csv(basedir+"{}.csv".format(index),index_col=self.refer_date_id, parse_dates=True,
                                 usecols=[self.refer_date_id, self.adjusted_close_id], na_values=["nan"])
            df_tmp = df_tmp.rename(columns={self.adjusted_close_id: self.adjusted_close_id + " " + index})
            self._df = self._df.join(df_tmp)

    def Build_from_csv(self, indexes, basedir=stock_basedir, control_path=path_of_control_stock,
                       start_date="1970-01-01", end_date=date.today()):
        self._setDateRange(start_date, end_date)
        self._initDataFrame()
        self._removeInactiveDays(control_path, basedir)
        self._join(indexes, basedir)

    def SubSet(self, start_date="1970-01-01", end_date=date.today(), index_sub_set=-1):
        if self._df is None:
            print "Error: missing information, DataFrame not properly built"
        tmp_df = DataFrame_Adj_Close_Builder()
        tmp_df._setDateRange(start_date=start_date, end_date=end_date)
        tmp_df._initDataFrame()
        if index_sub_set == -1:
            tmp_df._df = tmp_df._df.join(self._df, how="inner")
        else:
            tmp_df._df = tmp_df._df.join(self._df[index_sub_set], how="inner")
        return tmp_df

    def dataframe(self):
        return self._df
