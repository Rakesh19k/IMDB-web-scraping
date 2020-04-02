import requests
from bs4 import BeautifulSoup
import pprint 



#####    Task--4    #####



def scrap_movie_details(movie_url):
	page = requests.get(movie_url)
	soup = BeautifulSoup(page.text, "html.parser")
	title_div = soup.find("div", class_= "title_wrapper").h1.get_text()

	movie_name = ""
	for i in title_div:
		if "(" not in i:
			movie_name = (movie_name + i).strip()
		else:
			break


	sub_div = soup.find("div", class_= "subtext")
	running = sub_div.find("time").get_text().strip()
	runtime = int(running[0])*60
	if "min" in running:
		running_minutes = int(running[3:].strip("min"))
		movie_running = runtime + running_minutes
	else:
		movie_running = runtime

	genres = sub_div.find_all("a")
	genres.pop()
	gener = []
	for i in genres:
		movie_genre = i.get_text()
		gener.append(movie_genre)


	summary = soup.find("div", class_="plot_summary")

	movie_bio = summary.find("div", class_="summary_text").get_text().strip()

	director = soup.find("div", class_="credit_summary_item")

	director_list = director.find_all("a")
	director_name = []
	for i in director_list:
		movie_director = i.get_text()
		director_name.append(movie_director)
	
	more_details = soup.find("div",{"class":"article","id":"titleDetails"})
	more_details_list = more_details.find_all("div")
	for div in more_details_list:
		tag_h4 = div.find_all("h4")
		for text in tag_h4:
			if "Language:" in text:
				tag_anchor = div.find_all("a")
				movie_language=[]
				for i in tag_anchor:
					movie_language.append(i.get_text())
			elif "Country:" in text:
				ancher = div.find_all("a")
				for i in ancher:
					country =i.get_text()
			elif "Release Date:" in text:
				date = div.get_text().strip()
				release_date = date[14:-24]
				
				
	movie_poster = soup.find("div", class_="poster").a["href"]
	poster_link = "https://www.imdb.com" + movie_poster

	movie_details_dic = {"Name":"","Runtime":"","Gener":"","Bio":"","Director":"","Country":"","Language":"","Date":"","Poster_link":""}


	movie_details_dic["Name"] = movie_name
	movie_details_dic["Runtime"] = movie_running
	movie_details_dic["Gener"] = gener
	movie_details_dic["Bio"] = movie_bio
	movie_details_dic["Director"] = director_name
	movie_details_dic["Country"] = country
	movie_details_dic["Language"] = movie_language
	movie_details_dic["Date"] = release_date	
	movie_details_dic["Poster_link"] = poster_link
	return (movie_details_dic)
url1="https://www.imdb.com/title/tt8130968/"
pprint.pprint (scrap_movie_details(url1))
# scrap_movie_details(url1)
