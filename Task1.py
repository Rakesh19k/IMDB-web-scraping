import requests
from bs4 import BeautifulSoup
import pprint

url = ("https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in")

page = requests.get(url)
soup = BeautifulSoup(page.text,"html.parser")



######  Task--1  ######


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


#####   TASK--2   #####


def group_by_year(movies):
	years = []
	for i in movies:
		year = i["year"]
		if year not in years:
			years.append(year)
	movie_dict = {i:[]for i in years}
	for i in movies:
		year = i["year"]
		for x in movie_dict:
			if str(x) == str(year):
				movie_dict[x].append(i)
	return movie_dict

group_by_year(scrapped)


####   Task--3   ####



dec_arg = group_by_year(scrapped)

def group_by_decade(movies):
	moviedec = {}
	list1 = []
	for j in movies:
		Mod = j%10
		decade = j-Mod
		if decade not in list1:
			list1.append(decade)
	list1.sort()

	for i in list1:
		moviedec[i] = []
	for i in moviedec:
		dec10 = i + 9
		for x in movies:
			if x<= dec10 and x>=i:
				for v in movies[x]:
					moviedec[i].append(v)
	return (moviedec)

pprint.pprint (group_by_decade(dec_arg))
