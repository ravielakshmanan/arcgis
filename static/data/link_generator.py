# http://iridl.ldeo.columbia.edu/ds:/SOURCES/.UCSB/.CHIRPS/.v2p0/.monthly/.global/.precipitation/X/-20/40/RANGE/Y/10/20/RANGE/T/%28Jul%201900%29%28Dec%202018%29RANGE/T/%28Jan-Jun%29seasonalAverage/a://name/%28precip%29def/:a:/T/132/runningAverage//name/%28smoothed%29def/:a:/:a:%5BT%5Ddetrend-bfl/sub//name/%28trend%29def/:a/:ds/mark/precip/T/%28Jan-Jun%201986%29VALUE/.T/X/Y/precip/T/%28Jan-Jun%201986%29VALUE/T/removeGRID/smoothed/T/%28Jan-Jun%201986%29VALUE/T/removeGRID/trend/T/%28Jan-Jun%201986%29VALUE/T/removeGRID/table:/mark/:table/
url1 = "http://iridl.ldeo.columbia.edu/ds:/SOURCES/.UCSB/.CHIRPS/.v2p0/.monthly/.global/.precipitation/X/"
# url2 = "-20/40"
url3 = "/RANGE/Y/"
# url4 = "10/20"
url5 = "/RANGE/T/%28Jul%201900%29%28Dec%202018%29RANGE/T/%28"
# url6 = "Jan-Jun"
url7 = "%29seasonalAverage/a://name/%28precip%29def/:a:/T/132/runningAverage//name/%28smoothed%29def/:a:/:a:%5BT%5Ddetrend-bfl/sub//name/%28trend%29def/:a/:ds/mark/precip/T/%28"
# url8 = "Jan-Jun"
url9 = "%20"
# url10 = "1986"
url11 = "%29VALUE/.T/X/Y/precip/T/%28"
# url12 = "Jan-Jun"
url13 = "%20"
# url14 = "1986"
url15 = "%29VALUE/T/removeGRID/smoothed/T/%28"
# url16 = "Jan-Jun"
url17 = "%20"
# url18 = "1986"
url19 = "%29VALUE/T/removeGRID/trend/T/%28"
# url20 = "Jan-Jun"
url21 = "%20"
# url22 = "1986"
url23 = "%29VALUE/T/removeGRID/table:/mark/:table/.csv"

import os

filename = "trendline_links.csv"
file = open(filename, 'w')
for year in range(1981, 2020):
	print(year)
	for X in range(-180, 180, 20):
		x = str(X) + '/' + str(X+19)
		for Y in range(-80, 50, 20):
			y = str(Y) + '/' + str(Y+19)
			months = ['Jul-Sep']
			for month in months:
				url = url1+x+url3+y+url5+month+url7+month+url9+str(year)+url11+month+url13+str(year)+url15+month+url17+str(year)+url19+month+url21+str(year)+url23
				outFile = "X" + str(X) + '_' + str(X+19) + "Y" + str(Y) + "_" + str(Y+19) + "_" + month + "_" + str(year) + ".csv"
				newWrite = 'curl -g "' + url + '" >> ' + outFile
				print(newWrite)
				os.system(newWrite)
				file.write(newWrite)
				file.write('\n')
file.close()
