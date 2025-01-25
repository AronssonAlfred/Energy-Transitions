import numpy as np
import pandas as pd
from math import log
from scipy.optimize import least_squares 
import re


def y(theta, t):
    return theta[0] / (1 + np.exp(- theta[1] * (t - theta[2])))

def fit(dt):
    xs = dt['Year'].to_numpy()
    ys = dt['Value'].to_numpy()
    my = max(xs)
    mv = max(ys)
    def fun(theta):
        return y(theta, xs) - ys
    theta0 = [mv, 0.3, my - 5]
    res1 = least_squares(fun, theta0, max_nfev=10000) # method = 'lm',
    if res1.x[2] > my:
        yr = my
    else:
        yr = round(res1.x[2])
    mat = y([1, res1.x[1], res1.x[2]], my)
    d = [{'Fit': 'S','L': res1.x[0], 'K': res1.x[1], 'TMax': res1.x[2], 'Year': yr, 'Maturity' : mat}]
    df = pd.DataFrame(d)
    return(df)

###Insert your input file name here (with the path, if necessary)
file_in = "solar_data.csv"
x = re.search(r"(.+)\.csv$", file_in)
file_out = x.group(1) + "_fit.csv"

df = pd.read_csv(file_in)


df3 = df.groupby(['Country', 'Fuel'])[['Year', 'Value']] .apply(fit).reset_index()


df4 = pd.merge(df3, df[['Country', 'Fuel','Year', 'Total']], how = "inner")

df5 = df4.rename(columns={"Total": "Size"})
df5['G'] = df5['K'] * df5['L'] / 4
df5['G.Size'] = df5['G'] / df5['Size']
df5['L.Size'] = df5['L'] / df5['Size']
df5['dT'] = log(81) / df5['K']

df6 = df5[['Country', 'Fuel', 'Fit', 'L', 'L.Size', 'TMax', 'K', 'dT', 'G', 'G.Size', 'Maturity', 'Size']]

df6.to_csv(file_out, index=False) 