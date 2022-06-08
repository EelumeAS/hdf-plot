#!/usr/bin/env python
#import matplotlib.pyplot as plt

#plt.plot([1, 2, 3, 4])
#plt.ylabel('some numbers')
#plt.show()

import os
import h5py
import numpy as np
import pandas as pd
pd.options.plotting.backend = "plotly"
import plotly.express as px
import plotly as plt
import webbrowser
import ipywidgets as ipw

def figures_to_html(figs, filename="dashboard.html"):
    dashboard = open(filename, 'w')
    dashboard.write("<html><head></head><body>" + "\n")
    for fig in figs:
        inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
        dashboard.write(inner_html)
    dashboard.write("</body></html>" + "\n")
    webbrowser.open('file://' + os.path.realpath(filename))

#f = h5py.File('data/db-0011-Eely_20220121-20220121-115131.h5', 'r')

#data = f['DatagramBase/CalculatedData/NavigationSolutionData/slotID0']

#data[...] = np.arange(100)
#print(data[0:100][0])
#print(data.keys())

#ds = pd.read_hdf('data/db-0011-Eely_20220121-20220121-115131.h5')

f = h5py.File('data/db-0011-Eely_20220121-20220121-115131.h5', 'r')
print(f)

nav_path = 'DatagramBase/CalculatedData/NavigationSolutionData/slotID0/'
ds = pd.DataFrame(np.array(f[nav_path]))

print(ds)
print(ds['latitude'])
print(ds['dataValidTime'])
#fig = ds.plot()
#fig.show()

#ds['dataValidTime'].apply(lambda t: pd.to_datetime(t))

ds['dataValidTime'] = pd.to_datetime(ds['dataValidTime'], unit = "us")

print(ds['dataValidTime'])

#fig = px.line(ds, x = 'dataValidTime', y=['latitude', 'latitudeStdDev'])
figs = [    px.line(ds, x = 'dataValidTime', y=['latitude']),
            px.line(ds, x = 'dataValidTime', y=['latitudeStdDev']),
            px.line(ds, x = 'dataValidTime', y=['longitude'])]
for fig in figs:
    fig.for_each_trace(lambda t: t.update(name=nav_path + t.name, legendgroup=nav_path + t.name, hovertemplate = t.hovertemplate.replace(t.name, nav_path + t.name)))
    fig.update_layout(width=800, height=600)


figures_to_html(figs)

#fig0 = ipw.HBox(figs)

#fig0.show()
