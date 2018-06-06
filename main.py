from DataFrame_Adj_Close_Builder import DataFrame_Adj_Close_Builder
from DataFrame_Utils import DataFrame_Utils as d_utils

db = DataFrame_Adj_Close_Builder()

indexes = ["GOOG", "IBM", "GLD", "AAPL"]
index = ["Adj Close AAPL"]
db.Build_from_csv(indexes=indexes, start_date="2010-01-01", end_date="2012-05-30")
selected_stock = db.dataframe()[index]
rolling_mean, rolling_std, dev_plus, dev_minus = d_utils.compute_Bollinger_Bands(df=selected_stock, window=20)
d_utils.plot_data([dev_plus, dev_minus, selected_stock], normalize=False)
d_utils.plot_data([d_utils.daily_returns(selected_stock).rename({"Adj Close APPL": "APPL Daily Returns"})])
print str(d_utils.comulative_returns(selected_stock)*100)+" %"

db.Build_from_csv(indexes=["FAKE2"], start_date="2005-01-01", end_date="2012-05-30")
inconsistent_data = db.dataframe()[["Adj Close FAKE2"]]
inconsistent_data = inconsistent_data.fillna(method="ffill")
inconsistent_data = inconsistent_data.fillna(method="bfill")
d_utils.plot_data([inconsistent_data])
