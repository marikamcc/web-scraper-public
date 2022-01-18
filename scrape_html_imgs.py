from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import os

def soupifypage(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	html_page = urlopen(req)
	return BeautifulSoup(html_page, features="html.parser")

def foldercheck(title, location):
	check_folder = os.path.isdir(location + title)
	if not check_folder:
		os.makedirs(location+title)
		print('new folder: ', location+title)
	else:
		print('folder ', location+title, 'already exists.')

def getGoodLinks2(soup, cond1, cond2, substring):
    finallist = []
    for link in soup.findAll(cond1):
        temp = link.get(cond2)
        if temp != None and temp.find(substring) > 0:
            finallist.append(temp)
    return finallist



if __name__ == '__main__':
	#make main folder for this
	mainFolderName = 'NAME_WENT_HERE'
	mainFolderLoc = 'SOME_LOCATION_LOCALLY'
	foldercheck(mainFolderName, mainFolderLoc)

	#First scrape the main page for chapter links
	url = 'HEAD_NODE_URL'

	mainSoup = soupifypage(url)

	#pulls links from results of beautifulsoup
	#for a certain format, that corresponds to the book chapter
	#page links
	goodLinks = getGoodLinks2(mainSoup, 'a', 'href', 'SOME_SUBSTRING')

	##############Now the individual chapters part
	#Count is a proxy for Ch number
	#I could use enumerate(goodLinks), I think?  Would have to test more
	count = 0 
	for l in goodLinks:
		chapterSoup = soupifypage(l)
		cleanImges = getGoodLinks2(chapterSoup, 'img', 'src', 'FILE_EXTENSION')
		
		#Make a chapter folder
		ch_num = format(count, "03d")
		foldercheck(ch_num, mainFolderLoc+mainFolderName+'/')


		#loop throught each page (image file) of the book 
		#and save it
		page = 0
		for j in cleanImgs:
			filename = format(page, '02d')+'.webp'
			dest_folder = mainFolderLoc+mainFolderName+'/'+ch_num+'/'
			outfile = os.path.join(dest_folder, filename)

			r = requests.get(j)
			check_page = os.path.isfile(outfile)
			if not check_page:
			    with open(outfile, 'wb') as f:
			        f.write(r.content)
			else:
			    print('page already downloaded!')
		        
			page += 1

		count += 1