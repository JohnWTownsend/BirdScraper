import xlsxwriter
from bs4 import BeautifulSoup
import urllib2
import contextlib
import sys


workbook = xlsxwriter.Workbook("ThisIsTest.xlsx")
worksheet = workbook.add_worksheet()


#worksheet.write('A1', 'Testing')

#for i in range(10):
#    worksheet.write(i,0,"yo")


print "-----Bird Machine-----"
print ""
state = raw_input("State: ")
amtBirds = int(raw_input("# of Birds: "))
worksheet.set_column(0, 3*amtBirds, 20)

birds = []

presCol = 1
counter = 0
for i in range(amtBirds):
	birds.append(raw_input("Bird" + str(i+1) + ": "))
	worksheet.write(0,presCol,birds[counter])
	worksheet.write(1,presCol, "Birds/Route")
	worksheet.write(1,presCol+1, "isIn?")
	presCol += 2
	counter +=1


worksheet.write(0,0,state)
worksheet.write(1,0, "Route")

def birdcheck(url, birds, row):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read(), "html.parser")
	data = soup.get_text()
	worksheet.write(row, 0, data[129:150])#Trail name
	count = 1
	for i in range(amtBirds):
		if data.find(birds[i]) != -1:
			spot = data.find(birds[i])
			worksheet.write(row, count, data[spot+60: spot+66])#BirdsperRoute
			worksheet.write(row, count+1, "YES")
		else:
			worksheet.write(row, count, "0")
			worksheet.write(row, count+1, "NO")
		count += 2
	print str(row-1)
mainUrl = "https://www.mbr-pwrc.usgs.gov/bbs/trend/rtehtm13a_nlcd.html"
mainPage = urllib2.urlopen(mainUrl)
mainSoup = BeautifulSoup(mainPage.read(), "html.parser")

for link in mainSoup.find_all('a'):
	linkc = str(link.contents)
	if linkc.find(state) != -1:
		stateUrl = 'https://www.mbr-pwrc.usgs.gov' + link.get('href')

if stateUrl[0] == 'h':
	pass
else:
	sys.exit("ERROR:State Not Valid")


statePage = urllib2.urlopen(stateUrl)
stateSoup = BeautifulSoup(statePage.read(), "html.parser")
row = 2
for link in stateSoup.find_all('a'):
	if link.get('href').find("/rtena213") != -1:
		url = 'https://www.mbr-pwrc.usgs.gov' + link.get('href')
		page = urllib2.urlopen(url)
		birdcheck(url, birds, row)
		row += 1
workbook.close()
