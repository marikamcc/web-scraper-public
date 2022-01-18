import requests, os, time

def foldercheck(title, location):
	check_folder = os.path.isdir(location + title)
	if not check_folder:
		os.makedirs(location+title)
		print('new folder: ', location+title)
	else:
		print('folder ', location+title, 'already exists.')


if __name__ == '__main__':
	#base_url hard-coded!
	base_url = 'SOME_URL_HERE' 
	api_url = base_url+'/feed'+'?order[chapter]=asc&order[volume]=asc&limit=500&translatedLanguage[]=en'

	#Get title and make folder
	title = requests.get(base_url).json()['data']['attributes']['title']['en']
	location = './' #current directory for now

	#Does this folder exist?
	foldercheck(title, location)

	#Request chapters (should I partition this by volume? Maybe eventually)
	r = requests.get(api_url)
	chapters = r.json()['data']

	count = 0
	for i in chapters: #letting me do like 40 at a time
		#print(count)

		#reference for getting ch numbers in 000 format:
		#https://stackoverflow.com/questions/134934/display-number-with-leading-zeros
		ch_title = format(int(i['attributes']['chapter']), "03d")+'_'+i['attributes']['title']

		#Chapter folder check
		foldercheck(ch_title, location+title+'/')

		#There was a wait time here for the specific API I was querying
		
		
		one_chapter = requests.get('SOME_URL_WENT_HERE' + i['id']).json()
		imgBaseUrl = one_chapter['baseUrl']+'/data/'
		imgHash = one_chapter['chapter']['hash']+'/'

		count += 1

		#downloads pages in the chapter
		#does NOT make the filenames nice
		#does NOT check if it downloads correctly
		for j in one_chapter['chapter']['data']:
			r = requests.get(imgBaseUrl+imgHash+j)
			filename = os.path.basename(imgBaseUrl+imgHash+j)
			outfile = os.path.join(location+title+'/'+ch_title, filename)
			
			#Have I dl'ed this page yet?
			check_page = os.path.isfile(outfile)
			if not check_page:
				with open(outfile, 'wb') as f:
					f.write(r.content)
			else:
				print('page already downloaded!')