from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import csv

def getStats():


	with open('football-reference/qbidentifiers.csv', newline='') as csvfile:
		data = list(csv.reader(csvfile))
	print(data)
	stats = []
	
	for x in data:
		
		currentarray = x[0]
		currentstring = "".join(currentarray)
		print(currentstring)
		url = "https://www.pro-football-reference.com/players/" + currentstring[0] + "/" + currentstring + ".htm#passing::none"

		page = urlopen(url).read()
		soup = BeautifulSoup(page)

		table = soup.find("tfoot")
		count = 0
		pre_df = dict()
		features_wanted =  {'pass_rating', 'pass_int', 'pass_adj_net_yds_per_att'} #add more features here!!
		rows = table.find_all('tr')
		for row in rows:
			if (row.find('th', {"scope":"row"}) != None):
				
				for f in features_wanted:
					cell = row.find("td",{"data-stat": f})
					
					a = cell.text.strip().encode()
					text=a.decode("utf-8")
					if f in pre_df:
						pre_df[f].append(text)
					else:
						pre_df[f]=[text]
            
				df = pd.DataFrame.from_dict(pre_df)
				print(df)
		
		statlist = df[17].values.tolist()
		stats.extend(statlist)

        
def csvDump():
    stats.to_csv("scraped_data.csv")