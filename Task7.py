import requests
from bs4 import BeautifulSoup
import pprint

URL = ("https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in")
Page = requests.get(URL)
soup = BeautifulSoup(Page.text, "html.parser")


####   Task--1   ####


def scrap_top_list():
	main__div = soup.find("div", class_="lister")
	tbody = main__div.find("tbody", class_="lister-list")
	trs = tbody.find_all("tr")
	

	movie_url = [] 
	movie_rank = []

	for tr in trs:
		position = tr.find("td", class_="titleColumn").get_text().strip()
		rank = ""
		for i in position:
			if "." not in i:
				rank +=i
			else:
				break
		movie_rank.append(rank)

		link = tr.find("td", class_ = "titleColumn").a["href"]
		movie_link = "https://www.imdb.com" + link
		movie_url.append(movie_link)
		
	Top_movies = []
	for i in range (0,len(movie_rank)):
		Top_movies.append(movie_url[i])
	return(Top_movies)


####   Task--5    ####


def get_movie_list_details(movie_url):

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
	# print(more_details)
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


####   Task--7   ####


List_of_directors = []
dic = {}
def analyse_movie_director():
	for i in movie_scrap_list:
		for j in i["Director"]:
			if j in List_of_directors:
				continue
			else:
				List_of_directors.append(j)


	for i in List_of_directors:
		count = 0
		for j in movie_scrap_list:
			if i in j["Director"]:
				count+=1
		dic[i] = count
	return dic


Top_movies=scrap_top_list()
more_details=Top_movies[:10]
movie_scrap_list = []
for i in more_details:
	movie_details_list=get_movie_list_details(i)
	movie_scrap_list.append(movie_details_list)
pprint.pprint(analyse_movie_director())