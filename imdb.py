#/usr/bin/python
import requests
import bs4
import os
import sys
import urllib
import json
from selenium import webdriver

os.system('clear')

outfile= open('imdbtop', 'a')

def movies_info():
		
	name = raw_input('Enter the movie name:\t')
	choice = raw_input("Do you want to enter the release year ( Y for yes ):\t")
	if(choice=='Y'):
		year= raw_input("Enter the year of release:\t")
		url= 'http://www.omdbapi.com/?t='+str(name)+'&y='+str(year)+'&plot=short&r=json'
	else:
		url = 'http://www.omdbapi.com/?t='+str(name)+'&y=&plot=short&r=json'
	response = urllib.urlopen(url)
	j=json.loads(response.read())
	title=  j['Title']
	year= j['Released']
	language= j['Language']
	director = j['Director']
	genre= j['Genre']
	actors= j['Actors']
	plot= j['Plot']
	rate= j['imdbRating']
	print ("\n\n----------------------------GET MOVIE INFORMATION-------------------------\n")
	print ("\n\t TITLE       : \t\t"+title)
	print ("\n\t RELEASED IN : \t\t"+year)
	print ("\n\t IMDB RATING : \t\t"+rate)
	print ("\n\t LANGUAGE    : \t\t"+language)
	print ("\n\t GENRE       : \t\t"+genre)
	print ("\n\t DIRECTOR    : \t\t"+director)
	print ("\n\t CAST        : \t\t"+actors)
	print ("\n\t PLOT        : \t\t"+plot)
	outfile.write("\n\n--------------------------------------GET MOVIE INFORMATION---------------------------------\n")
	outfile.write ("\n\t\t TITLE       : \t\t"+title)
	outfile.write ("\n\t\t RELEASED IN : \t\t"+year)
	outfile.write ("\n\t\t IMDB RATING : \t\t"+rate)
	outfile.write ("\n\t\t LANGUAGE    : \t\t"+language)
	outfile.write ("\n\t\t GENRE       : \t\t"+genre)
	outfile.write ("\n\t\t DIRECTOR    : \t\t"+director)
	outfile.write ("\n\t\t CAST        : \t\t"+actors)
	outfile.write ("\n\t\t PLOT        : \t\t"+plot)
	outfile.close()

def top_movies():

	url= 'http://www.imdb.com/chart/top'
	num= input('Enter the number of top movies you want to receive:\t')
	#driver = webdriver.Firefox()
	#driver.get(url)
	#html = driver.execute_script("return document.documentElement.innerHTML;")
    	#soup=bs4.BeautifulSoup(html,"lxml")
	#rows= soup.findAll('chart full-width')
	response=requests.get(url)
	html=response.text
	soup=bs4.BeautifulSoup(html,"lxml")
	#print soup.prettify()
	strnum= str(num)
	rows=soup.select('.chart.full-width tbody.lister-list tr')
	print ("\n"+"----------------------------TOP "+str(strnum)+" MOVIES ACCORDING TO IMDB RATINGS-----------------------------"+"\n\n")
	print (" \t   TITLE\t\t\t\t\t\t\t\t   IMDB RATING\n\n")
	outfile.write ("\n"+"---------------------------TOP "+str(strnum)+" MOVIES ACCORDING TO IMDB RATINGS-----------------------------"+"\n\n")
	outfile.write (" \t TITLE\t\t\t\t\t\t\t\t\t   IMDB RATING\n\n")
	for row in range(0, num):
		td= rows[row].select('td')
		#title= td[1].find('a').getText();
		title= td[1].get_text("  ", strip=True)
		title=title.encode('ascii','ignore')
		rating= td[2].find('strong').getText();
		print ("\n "+title.ljust(72)+"\t\t"+rating)
		outfile.write  ("\n "+title.ljust(75)+"\t\t\t\t"+rating)
def folder():
	path= raw_input("Enter the complete path of the folder where your movies are present:\t")
	movies= os.listdir(path)
	path1= path.encode('ascii','ignore')
	outfile.write("\n\n\t\tRatings for movies in the folder: "+str(path)+'\n')
	print ("\n\n\t\tRatings for movies in the folder: "+str(path)+'\n')
	for i in range(len(movies)):
		name = movies[i]
		name = name.replace(' ','+')
		url = 'http://www.omdbapi.com/?t='+str(name)+'&y=&plot=short&r=json'
		response = urllib.urlopen(url)
		j=json.loads(response.read())
		try:
			title=  j['Title']
			year= j['Released']
			print (year+'\n')
			rate = j['imdbRating']
			oldname= path+name
			oldname= oldname.encode('ascii','ignore')
			newname = "Title: "+title+"\nRating: "+rate+"\n Year: "+year
			namefile= "Title: "+title.ljust(30)+"\nRating: "+rate.ljust(5)+"\n Year: "+year.ljust(5)
			namefile= namefile.encode('ascii','ignore')
			newname= path+newname
			newname= newname.encode('ascii','ignore')
			print namefile+'\n'
			outfile.write(namefile+'\n')
			os.rename(oldname,newname)
		except KeyError:
           		print ("\nNo such movie titled '"+oldname+"' found or else read the instructions before using this feature!\n")
            		outfile.write ("\nNo such movie titled '"+oldname+"' found else read the instructions before using this feature!\n")

    
		
def driver():
	print "\n\n\t\t\t\t\t------------------------------------------------IMDB PORTAL------------------------------------------------"
        outfile.write("\\\n\n\t\t\t\t\t------------------------------------------------IMDB PORTAL------------------------------------------------")
        choice=input('Enter your choice:\n\n1) Search movie information by title\n2) Show top rated movies\n3) Rename folder with IMDB rating and year of release added to it\n\nInput: ')
    
    	if(choice==1):
        	movies_info()
        if(choice==2):
        	top_movies()
    	else:
            	folder()
            
        
driver()
while (1>0) :
    repeat=raw_input("\n\nDo you want to try again (Type 'Yes'/'Y'/'y' or else press anything)? ")
    if (repeat=='Yes') or (repeat=='Y') or (repeat=='y'):
        os.system('clear')
        driver()
    else:
        print "\nThank you for using!"
        outfile.write("\nThank you for using!")
        break

outfile.close()
