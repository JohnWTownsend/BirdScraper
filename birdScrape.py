import xlsxwriter
from bs4 import BeautifulSoup
import urllib2
import contextlib
import sys

'''This program uses the website https://www.mbr-pwrc.usgs.gov/bbs/trend/rtehtm13a_nlcd.html
   to pull information about bird routes and how frequently certain species are seen on said
   routes.'''


workbook = xlsxwriter.Workbook("ThisIsTest.xlsx") #create workbook
worksheet = workbook.add_worksheet() #create worksheet within workbook

print "-----Bird Scraper-----"
print ""
state = raw_input("State: ") #have user input which state to pull info from
amtBirds = int(raw_input("# of Birds: ")) #have user declare which birds they would like info on
birds = []

worksheet.set_column(0, 3*amtBirds, 20) #format excel spreadsheet to accomodate information

presCol = 1
counter = 0
for i in range(amtBirds):
	birds.append(raw_input("Bird" + str(i+1) + ": ")) #record birds user wants info on
	worksheet.write(0,presCol,birds[counter]) #write that bird to excel sheet
	worksheet.write(1,presCol, "Birds/Route")
	worksheet.write(1,presCol+1, "isIn?")
	presCol += 2 #increment +2 to keep in line with Birds/Route and isIn? columns
	counter +=1


worksheet.write(0,0,state)
worksheet.write(1,0, "Route")

def birdcheck(url, birds, row): #checks if all selected birds are in a given route using the url
	page = urllib2.urlopen(url) #opens given route page
	soup = BeautifulSoup(page.read(), "html.parser") #converts page into html and stores in soup
	data = soup.get_text() #stores html as text string in data
	worksheet.write(row, 0, data[129:150]) #Prints the route name that is being analyzed to spreadsheet
	count = 1
	for i in range(amtBirds): 
		if data.find(birds[i]) != -1: # != -1 because .find() returns -1 if finds nothing, but returns string index if finds argument given
			spot = data.find(birds[i]) #holds the spot current bird was found in spot var
			worksheet.write(row, count, data[spot+60: spot+66]) #Collects the amt of birds/route on route and prints to spreadsheet
			worksheet.write(row, count+1, "YES")
		else:
			worksheet.write(row, count, "0") # prints 0 for birds/route
			worksheet.write(row, count+1, "NO")
		count += 2
	print str(row-1) # prints current #route is being processed to terminal
	
mainUrl = "https://www.mbr-pwrc.usgs.gov/bbs/trend/rtehtm13a_nlcd.html" 
mainPage = urllib2.urlopen(mainUrl) #opens mainUrl
mainSoup = BeautifulSoup(mainPage.read(), "html.parser") #converts Mainurl to a scanable format with Beautiful soup

for link in mainSoup.find_all('a'): #goes through all anchor tags in html
	linkc = str(link.contents) #puts Text from anchor tag into linkc
	if linkc.find(state) != -1: #checks if user input state matches linkc
		stateUrl = 'https://www.mbr-pwrc.usgs.gov' + link.get('href') #creates reference to website of users desired state

if stateUrl[0] == 'h': #makes sure state was found 
	pass
else:
	sys.exit("ERROR:State Not Valid")


statePage = urllib2.urlopen(stateUrl) 
stateSoup = BeautifulSoup(statePage.read(), "html.parser")
row = 2
for link in stateSoup.find_all('a'): #navigates state webpage for all anchor tags
	if link.get('href').find("/rtena213") != -1: #/rtena213 was at the beginning of all links leading to bird & route info
		url = 'https://www.mbr-pwrc.usgs.gov' + link.get('href') 
		page = urllib2.urlopen(url)
		birdcheck(url, birds, row) #call function to see if each bird in birds array was found in route
		row += 1
workbook.close() #close and save excel workbook
