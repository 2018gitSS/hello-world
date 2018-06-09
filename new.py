"""
class03p16.py

This script should plot a fitted line on top of the 2018 prices
ref:
http://www.ml4.us/class03/pdf1.png
http://www.stat.purdue.edu/~jennings/stat514/stat512notes/topic3.pdf
"""

import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg



img=mpimg.imread ('ML_Cloud_Predictor_Home.png')
imgplot = plt.imshow(img)
#plt.show() 

#default value
ticker = 'AMZN'
trend = 1
predict_time = 30 
ticker = input ("What stock ticker that you are interested?     ")
csv_name = ticker + '.csv'
trend = int(input ("How many years of trend do you like to know?    "))
predict_time = int(input ("Predict future price in days from today?   "))
print ("ticker = %s , trend = %d, predict price after %d days " %(ticker,trend,predict_time))



# done with user interaction

#delcsvfile   = 'http://spy611.com/csv/allpredictions.csv'
#csvfile = 'http://tkrprice.herokuapp.com/static/CSV/history/NFLX.csv'
csvfile = 'http://tkrprice.herokuapp.com/static/CSV/history/' + csv_name 
print('csvfile=', csvfile)
cp_df     = pd.read_csv(csvfile).sort_values(['Date'])
cp2016_sr = (cp_df.Date > '2018') & (cp_df.Date < '2019')
cp2016_df = cp_df[['Date','Close']][cp2016_sr]

def colvec(arylst):
    # This should help me create column vectors from arrays or lists:
    return np.array(arylst).reshape((len(arylst),1))

x_a      = colvec(range(len(cp2016_df)))
ones_l   = [1]*len(cp2016_df)
ones_a   = colvec(ones_l)
xvals_a  = np.hstack((ones_a,x_a))
yvals_a  = colvec(cp2016_df.Close)
middle_a = np.linalg.pinv(np.matmul(xvals_a.T,xvals_a))
rhs_a    = np.matmul(xvals_a.T,yvals_a)
beta_a   = np.matmul(middle_a,rhs_a)
x_in_a   = xvals_a
yhat_a   = np.matmul(x_in_a,beta_a)
cp2016_df['yhat'] = yhat_a

print('Beta for a line fitted to the ticker')
print (beta_a)

beta_l = beta_a

# To make a better plot I should convert X-values from integers to series of 
#strings: f X-matrix is always 1:
xval_l = [[1,60]]
yhat_f = np.matmul(xval_l,beta_l)
print('I predict the price 60 days after the first price to be:')
print(yhat_f)
xval_l = [[1,90]]
yhat_f = np.matmul(xval_l,beta_l)
print('I predict the price 90 days after the first price to be:')
print(yhat_f)

"""
xval_l = [[1,350]]
yhat_f = np.matmul(xval_l,beta_l)
print('I predict the price 350 days after the first price to be:')
print(yhat_f)
"""

cpdate2016_df = cp2016_df.set_index(['Date'])
# I should plot cp (closing price), and fitted line:
title_name = ticker + ' 2018'
#cpdate2016_df.plot.line(title="NFLX 2018")
cpdate2016_df.plot.line(title=title_name)
plt.show()

'bye'
