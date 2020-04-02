import requests,os,json
from bs4 import BeautifulSoup
import pprint,time

url = ("https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in")


#####    Task--1    #####


page = requests.get(url)
soup = BeautifulSoup(page.text,"html.parser")
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
# pprint.pprint(scrapped)


#####    Task--12    #####



def scrap_movie_casts():
	for i in scrapped:
		cast_link = (i["url"] + "fullcredits/?ref_=tt_ov_st_sm")
		name = i["name"]
		file_name = name + "_cast" + ".json"



		if os.path.exists("Cast_file/" + str(file_name)):
			read = open("Cast_file/" + str(file_name),"r+")
			data = json.load(read)
			return data
		# 	pprint.pprint (data)

		else:

			page = requests.get(cast_link)
			soup = BeautifulSoup(page.text,"html.parser")

			time.sleep(5)

			main_table = soup.find("table", class_="cast_list")
			tbody = main_table.find_all("td", class_="")

			cast_list = []
			for actor in tbody:
				actor_dic = {}
				_id = actor.find("a").get("href")[6:15]
				name = actor.find("a").get_text().strip()
				actor_dic["actor_id"] =str(_id)
				actor_dic["actor_name"] = str(name)
				cast_list.append(actor_dic.copy())

			file = open("Cast_file/"+ str(file_name), "w" )
			data = json.dump(cast_list,file)

			return cast_list
			# pprint.pprint(cast_list)
			
scrap_movie_casts()
	