# importing the requests library 
import requests 
import pandas as pd
import json
import numpy as np
from pandas.io.json import json_normalize
from datetime import datetime  
from datetime import timedelta 

# Variable setup
station_mine = 'IWATERLO57'
station_other = ['IONTARIO734']# ['ICAMBRID183']# 'IKITCHEN16' 'IONTARIO734', 'IWOOLWIC7',  ['IONTARIO1036'] #'IKITCHEN15']#, 'IKITCHEN16', 'IWATERLO55', 'IONTARIO1036']
start_datestring = '20190101'
end_datestring = '20200101'
API_KEY = '6343f2a1cd104ac283f2a1cd10fac2b6'

#Setup datetime obj
start_datetime_obj = datetime.strptime(start_datestring, '%Y%m%d')
end_datetime_obj = datetime.strptime(end_datestring, '%Y%m%d')
number_of_days = abs((start_datetime_obj - end_datetime_obj).days)

for station in station_other:
	print("Working on station:", station)

	# dataframe setup
	main_df = pd.DataFrame()
	first_pass = True

	print("Spinning up extractor..")
	for i in range(number_of_days):
		datestring = (start_datetime_obj + timedelta(days=i)).strftime('%Y%m%d')
		print("Working on date:", datestring)

		# api-endpoint 
		URL = "https://api.weather.com/v2/pws/history/daily?stationId=" + station + "&format=json&units=m&date=" + datestring + "&apiKey=" + API_KEY

		# sending get request and saving the response as response object 
		r = requests.get(url = URL)

		print(r.status_code)

		if r.status_code == 200:
			# extracting data in json format 
			data = r.json()
			df_obs = json_normalize(data['observations'])

			if first_pass:
				main_df = df_obs
				first_pass = False
			else:
				main_df = main_df.append(df_obs, ignore_index = True)
		else:
			main_df = main_df.append([{'epoch': np.nan, 'humidityAvg': np.nan, 'humidityHigh': np.nan, 'humidityLow': np.nan, 'lat': np.nan, 'lon': np.nan,
	       'metric.dewptAvg': np.nan, 'metric.dewptHigh': np.nan, 'metric.dewptLow': np.nan,
	       'metric.heatindexAvg': np.nan, 'metric.heatindexHigh': np.nan, 'metric.heatindexLow': np.nan,
	       'metric.precipRate': np.nan, 'metric.precipTotal': np.nan, 'metric.pressureMax': np.nan,
	       'metric.pressureMin': np.nan, 'metric.pressureTrend': np.nan, 'metric.tempAvg': np.nan,
	       'metric.tempHigh': np.nan, 'metric.tempLow': np.nan, 'metric.windchillAvg': np.nan,
	       'metric.windchillHigh': np.nan, 'metric.windchillLow': np.nan, 'metric.windgustAvg': np.nan,
	       'metric.windgustHigh': np.nan, 'metric.windgustLow': np.nan, 'metric.windspeedAvg': np.nan,
	       'metric.windspeedHigh': np.nan, 'metric.windspeedLow': np.nan, 'obsTimeLocal': datestring,
	       'obsTimeUtc': np.nan, 'qcStatus': -9999, 'solarRadiationHigh': np.nan, 'stationID': np.nan, 'tz': np.nan,
	       'uvHigh': np.nan, 'winddirAvg': np.nan}], ignore_index = True)
			first_pass = False


	print("Saving dataframe to csv..")
	main_df.to_csv(station + '_data.csv')

print("All station data successfully saved!")
