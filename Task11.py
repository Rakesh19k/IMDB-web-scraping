import requests,os
from bs4 import BeautifulSoup
import pprint
import json
import random
import time

url = ("https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in")

page = requests.get(url)
soup = BeautifulSoup(page.text,"html.parser")

####   Task--1   ####


def scrap_top_list():
	main__div = soup.find("div", class_="lister")
	tbody = main__div.find("tbody", class_="lister-list")
	trs = tbody.find_all("tr")
	

	movie_name = []
	movie_rating = []
	movie_realease = []
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


		name = tr.find("td", class_= "titleColumn").a.get_text()
		movie_name.append(name)
		

		span_ = tr.find("td", class_= "titleColumn").span.get_text()
		movie_realease.append(span_)


		rating = tr.find("td",class_="ratingColumn imdbRating").strong.get_text()
		movie_rating.append(rating)


		link = tr.find("td", class_ = "titleColumn").a["href"]
		movie_link = "https://www.imdb.com" + link
		movie_url.append(movie_link)
		
	Top_movies = []
	details = {"name":"", "position":"", "year":"", "rating":"","url":""}
	for i in range (0,len(movie_rank)):
		details["name"] = str(movie_name[i])
		details["position"] = int(movie_rank[i])
		movie_realease[i] = movie_realease[i][1:5]
		details["year"] = int(movie_realease[i])
		details["rating"] = float(movie_rating[i])
		details["url"] = movie_url[i]
		Top_movies.append(details.copy())
	return(Top_movies)
scrapped = scrap_top_list()


####    Task--8   ####


def scrap_movie_details(movie_url):

	random_sleep = random.randint(1,3)

	movie_id = ""
	for _id in movie_url[27:]:
		if "/" not in _id:
			movie_id += _id
		else:
			break
	file_name = movie_id + ".json"
	# return file_name

	text = None
	if os.path.exists("Data/Movie_details/"+ file_name):
		f = open("Data/Movie_details/"+ file_name)
		text = f.read()
		jload = json.loads(text)
		return jload
	
	if text is None:
		time.sleep(random_sleep)

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
	# return movie_details_list

	file1 = open("Data/Movie_details/"+ file_name,"w")
	data = json.dump(movie_details_dic, file1)
	return movie_details_dic

####    Task--6   ####

def get_movie_list_details(movie_list):
	movie_details_list = []
	for i in movie_list:
		detail = scrap_movie_details(i["url"])
		movie_details_list.append(detail)
	return movie_details_list
movies_detail = get_movie_list_details(scrapped)


####   Task--11   ####

def analyse_movies_gener(movie_list):
	gener_list = []
	for movie in movie_list:
		gener = movie["Gener"]
		for i in gener:
			if i not in gener_list:
				gener_list.append(i)
	analyse_gener = {gener_type:0 for gener_type in gener_list}
	for gener_type in gener_list:
		for movie in movie_list:
			if gener_type in movie["Gener"]:
				analyse_gener[gener_type] +=1
	return analyse_gener
pprint.pprint (analyse_movies_gener(movies_detail)