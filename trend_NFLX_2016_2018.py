# class0310.py

# Use Pandas to plot prices of GSPC for 2016.

import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
from datetime import datetime
csvfile = 'http://tkrprice.herokuapp.com/static/CSV/history/NFLX.csv'
#csvfile = 'http://ichart.finance.yahoo.com/table.csv?s=%5EGSPC'
# Goog: In pandas how to sort a dataframe?
cp_df     = pd.read_csv(csvfile).sort_values(['Date'])
# Goog: In pandas how to filter?
cp2016_sr = (cp_df.Date > '2016') & (cp_df.Date < '2019')
cp2016_df = cp_df[['Date','Close']][cp2016_sr]
# Goog: In pandas how to convert column into index?
cpdate2016_df = cp2016_df.set_index(['Date'])
# Goog: In pandas how to plot?
cpdate2016_df.plot.line(title="NFLX 2016 - 2018")
plt.show()

'bye'
