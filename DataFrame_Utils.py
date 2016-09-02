from matplotlib import pyplot as plt


class DataFrame_Utils:

    @staticmethod
    def add_suffix(df, suffix):
        columns = list(df.columns.values)
        for c in columns:
            df = df.rename(columns={str(c): str(c)+str(suffix)})
        return df

    @staticmethod
    def plot_data(dfs, normalize=False):
        fig, ax = plt.subplots()
        for df in dfs:
            if normalize:
                norm = DataFrame_Utils.normalize(df)
                norm.plot(ax=ax)
            else:
                df.plot(ax=ax)
        plt.show()

    @staticmethod
    def normalize(df):
        return df / df.ix[len(df.index) - 1, :]

    @staticmethod
    def daily_returns(df):
        daily_returns = (df/df.shift(1)) - 1
        daily_returns.ix[0, :] = 0
        return daily_returns

    @staticmethod
    def comulative_returns(df, start=0, end=-1):
        s = start + 1
        if start < end:
            comulative_returns = (df.ix[start:s].values/df.ix[len(df.index) - 1, :].values) - 1
            return comulative_returns[0, 0]
        else:
            if end == -1:
                comulative_returns = (df.ix[start:s].values/df.ix[len(df.index) - 1, :].values) - 1
                return comulative_returns[0, 0]
            else:
                print "end should be after the start"

    @staticmethod
    def compute_Bollinger_Bands(df, suffix="2s", window=20):
        rolling_mean = df.rolling(window=window).mean()
        rolling_std = df.rolling(window=window).std()
        dev_plus = DataFrame_Utils.add_suffix(rolling_mean.add(2*rolling_std), "+"+str(suffix))
        dev_minus = DataFrame_Utils.add_suffix(rolling_mean.subtract(2*rolling_std), "-"+str(suffix))
        return rolling_mean, rolling_std, dev_plus, dev_minus
