# Enplanement Forecasting

## Installation
Runtime: Python 3.8+
Install requirements `pip install -r requirments.txt`
Postbuild: run commands in postbuild.txt on command line.

## How to Run
Config parameters in config.py:  
```python
metric = 'MAPE' # metric used to compare all results (MAE, RMSE, R2 also available)
train_prop = .7 # the size of the train split on each series
fcst_length = 38 # the size of the forecast into future periods
```
Run all notebooks in order:
- `00 - prepare_data.ipynb`: Prepares the raw data by selecting enplanements only and slicing the data into four different CSV files representing each time series to forecast
- `01 - arima_orders.ipynb`: selects the optimal ARIMA orders for each series
- `02 - fcsts_orig_data.ipynb`: forecasts using the original data with no considerations of the structural breaks caused from COVID
- `03 - fcsts_ignore_covid_periods`: forecasts using only data from pre-COVID periods
- `04 - fcsts_with_outlier_detection`: finds structural breaks in data using X13 method and applies findings to the ARIMA, Prophet, and weighted-average mdoels to forecast
- `05 - model_evaluations_on_new_data.ipynb`: tests each model's accuracy using four new introduced data points
- `06 - results_vis.ipynb`: visualizes each model's forecast and test-set predictions