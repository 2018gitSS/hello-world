"""
Command: python web.py 
    enter AMZN ticker name   (AMZN will be default if enter was pressed)
The text output the prediciton of 60 days or 90 days later.
The index.html will show the logo and the stock 2018 price prediction

ref:
http://www.ml4.us/class03 for formula
http://www.ml4.us/class03/pdf1.png
http://www.stat.purdue.edu/~jennings/stat514/stat512notes/topic3.pdf
"""
import os,sys,string
import datetime
import pandas as pd
import numpy  as np
#import matplotlib.pyplot as plt
import matplotlib.image as mpimg



#img=mpimg.imread ('ML_Cloud_Predictor_Home.png')
#imgplot = plt.imshow(img)
#plt.show() 

#user input and default value
ticker = input ("What stock ticker that you are interested?     ")
if len(ticker) == 0 :
    ticker = 'AMZN'
csv_name = ticker + '.csv'

trend = ''
predict_time = ''
#trend = int(input ("How many years of trend do you like to know?    "))
#trend = input ("How many years of trend do you like to know?    ")
if len(trend) == 0 :
    trend = 3
else:
   trend = int(trend)  
#predict_time = int(input ("Predict future price in days from today?   "))
#predict_time = input ("Predict future price in days from today?   ")
if len(predict_time) == 0 :
    predict_time = 90
else:
    predict_time = int(predict_time)
 
print ("ticker = %s , trend = %d, predict price after %d days " %(ticker,trend,predict_time))



# done with user interaction

#delcsvfile   = 'http://spy611.com/csv/allpredictions.csv'
#csvfile = 'http://tkrprice.herokuapp.com/static/CSV/history/NFLX.csv'
csvfile = 'http://tkrprice.herokuapp.com/static/CSV/history/' + csv_name 
print('csvfile=', csvfile)
cp_df     = pd.read_csv(csvfile).sort_values(['Date'])
cp201x_sr = (cp_df.Date > '2018') & (cp_df.Date < '2019')
cp201x_df = cp_df[['Date','Close']][cp201x_sr]

def colvec(arylst):
    # This should help me create column vectors from arrays or lists:
    return np.array(arylst).reshape((len(arylst),1))

x_a      = colvec(range(len(cp201x_df)))
ones_l   = [1]*len(cp201x_df)
ones_a   = colvec(ones_l)
xvals_a  = np.hstack((ones_a,x_a))
yvals_a  = colvec(cp201x_df.Close)
middle_a = np.linalg.pinv(np.matmul(xvals_a.T,xvals_a))
rhs_a    = np.matmul(xvals_a.T,yvals_a)
beta_a   = np.matmul(middle_a,rhs_a)
x_in_a   = xvals_a
yhat_a   = np.matmul(x_in_a,beta_a)
cp201x_df['yhat'] = yhat_a

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

#generate graph without using XWindow
import matplotlib
matplotlib.use('Agg')
# Order is important here.
# Do not move the next import:
import matplotlib.pyplot as plt





cpdate201x_df = cp201x_df.set_index(['Date'])
# I should plot cp (closing price), and fitted line:
title_name = ticker + ' 2018'
#cpdate201x_df.plot.line(title="NFLX 2018")
cpdate201x_df.plot.line(title=title_name)
#plt.show()
plt.grid(True)
plt.savefig('predict_2018_'+ticker+'.png')
plt.close()

#write a inde.html file for webpage 
baseDir = os.getcwd()
output_file = os.path.normpath('%s/index.html' %(baseDir))
ResultHtml = open(output_file, "w")
ResultHtml.write("<html>\n<head>\n\t<title>Test Results</title>\n")
#ResultHtml.write("\t<link href=\"./style.css\" rel=\"stylesheet\" type=\"text/css\">\n")
ResultHtml.write("</head>\n<body>\n")
resultStr_1 = "<h2>Time:" + str(datetime.datetime.today())+ "</h2>" 
ResultHtml.write (resultStr_1)
logo_msg = "This is logo image of ML predictor"
img_name = 'predict_2018_'+ticker+'.png'
img_name_path = '%s/%s' %(baseDir,img_name)
img_msg = 'prediction image --- ' + ticker 
result_logo_str = "<img src =  %s alt = %s >" %(baseDir + '/ML_Cloud_Predictor_Home.png' ,logo_msg ) 
result_predict_str = "<img src =  %s alt = %s >" %(img_name_path, img_msg ) 
ResultHtml.write (result_logo_str)
ResultHtml.write (result_predict_str)
ResultHtml.flush()
ResultHtml.close()
'bye'
