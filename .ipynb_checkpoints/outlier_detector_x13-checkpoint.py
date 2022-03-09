import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri
import rpy2
import pandas as pd
import os

try:
    importr('seasonal')
    importr('seasonalview')
except:
    ro.r("install.packages(c('seasonal','seasonalview'))")
    importr('seasonal')
    importr('seasonalview')

rscript = """rm(list=ls())
setwd('{wd}')
data <- data.frame(read.csv('data/{csv_name}.csv'))
y <- ts(data$PASSENGERS,start=c({start_year},{start_month}),deltat=1/12)
m <- seas(
    x = y,
    forecast.save = "forecasts",
    pickmdl.method = "best",
    arima.model = "{order}",
    outlier.critical = {crit}
    )
"""

def runr(csv_name,order,seasonal_order,pval=.95):
    """ runs X13 modeling process on a timeseries and returns a dataframe of resulting summary stats.
    works for monthly data only!

    Args:
        csv_name (str): the name of the csv file saved to the working directory.
            first column in this csv file is called "Date". 
            the only other column is called "PASSENGERS" (must be numeric type).
        order (tuple): the desired arima order.
        seasonal_order (tuple): the desired seasonal order.
        pval (float): one of .9, .95, or .99

    Returns:
        (DataFrame): the resulting summary stats from the best model found from ARIMA-SEATS / X13

    >>> df = runr('HOU-DOM.csv',order=(1,1,1),seasonal_order=(1,1,1))
    """
    df = pd.read_csv(os.path.join('data',csv_name+'.csv'),parse_dates=['Date'])
    start_year = df['Date'].min().year
    start_month = df['Date'].min().month

    pval_map = {
        .9:3,
        .95:4,
        .99:5
    }

    crit = pval_map[pval]

    order = str(order).replace(',','') + str(seasonal_order[:-1]).replace(',','')

    rs = rscript.format(wd=os.getcwd().replace('\\','/'),
        start_year=start_year,
        start_month=start_month,
        csv_name=csv_name,
        order=order,
        crit=crit)

    ro.r(rs)
    try:
        results = ro.DataFrame(ro.r("data.frame(summary(m))"))
        with localconverter(ro.default_converter + pandas2ri.converter):
            pd_results = ro.conversion.rpy2py(results) # pandas dataframe
    except rpy2.rinterface_lib.embedded.RRuntimeError: # default to a backup method since R is dumb
        results = ro.DataFrame(ro.r("data.frame(m[4]$est$coefficients)")) # html object
        with localconverter(ro.default_converter + pandas2ri.converter):
            pd_results = ro.conversion.rpy2py(results) # pandas dataframe
        pd_results.reset_index(inplace=True)
        pd_results.columns = ['term','coef']
        
    return pd_results