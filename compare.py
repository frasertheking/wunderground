### Comparison Scripts

import sys,os,warnings,math,glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

station_names = ["IWATERLO55", "IWATERLO57", "IONTARIO734", "IKITCHEN16", "IKITCHEN15"]

master_temps = pd.DataFrame({"IWATERLO55": pd.read_csv("IWATERLO55_data.csv")['metric.tempAvg'].values,
							"IWATERLO57": pd.read_csv("IWATERLO57_data.csv")['metric.tempAvg'].values,
							#"IONTARIO1036": pd.read_csv("IONTARIO1036_data.csv")['metric.tempAvg'].values,
							"IONTARIO734": pd.read_csv("IONTARIO734_data.csv")['metric.tempAvg'].values,
							"IKITCHEN16": pd.read_csv("IKITCHEN16_data.csv")['metric.tempAvg'].values,
							"IKITCHEN15": pd.read_csv("IKITCHEN15_data.csv")['metric.tempAvg'].values}, columns=station_names)


temporary_mine = master_temps["IWATERLO57"]
temporary_mine[temporary_mine < -999] = np.nan

x_vals = np.arange(367)

fig, ax = plt.subplots(figsize=(10, 10))
#plt.rcParams.update({'font.size': 18})
plt.grid()
ax.set_title("Station Temperature Comparisons")
ax.set_xlabel('Day of Year (2019)')
ax.set_ylabel('Average Daily Temperature (C)')
ax.plot(x_vals, master_temps["IWATERLO55"], label="IWATERLO55", color="red")
ax.plot(x_vals, temporary_mine, label="MY STATION", color="blue")
ax.plot(x_vals, master_temps["IONTARIO734"], label="IONTARIO734", color="green")
ax.plot(x_vals, master_temps["IKITCHEN16"], label="IKITCHEN16", color="orange")
ax.plot(x_vals, master_temps["IKITCHEN15"], label="IKITCHEN15", color="purple")

ax.axhline(np.nanmean(master_temps["IWATERLO55"]), linestyle="--", color="red")
ax.axhline(np.nanmean(temporary_mine), linestyle="--", color="blue")
ax.axhline(np.nanmean(master_temps["IONTARIO734"]), linestyle="--", color="green")
ax.axhline(np.nanmean(master_temps["IKITCHEN16"]), linestyle="--", color="orange")
ax.axhline(np.nanmean(master_temps["IKITCHEN15"]), linestyle="--", color="purple")

ax.legend()
fig.savefig('comparisons_temperature.png', transparent=True)