import requests,os,json
from bs4 import BeautifulSoup
import pprint,time
from Task1 import scrapped
from Task13 import scrap_movie_details


movie_list =[]
for i in scrapped:
	url = i["url"]
	main_data = scrap_movie_details(url)
	movie_list.append(main_data)
# print (movie_list)

def analyse_co_actors():
	co_actors = {}
	for i in movie_list:
		id_ = i["Cast"][0]["actor_id"]
		if id_ not in co_actors:
			co_actors[id_] = {}
			co_actors[id_]["name"] = i["Cast"][0]["actor_name"]
			co_actors[id_]["frequent_co_actors"] = []
			# print (co_actors)
			# break
		for j in i["Cast"][1:5]:
			flag = True
			if len(co_actors[id_]["frequent_co_actors"])>0:
				for k in co_actors[id_]["frequent_co_actors"]:
					if k["actor_id"]==j["actor_id"]:
						k["Num_movie"]+=1
						flag = False

			if flag:
				a = {}
				a["actor_id"]=j["actor_id"]
				a["actor_name"]=j["actor_name"]
				a["Num_movie"]=1
			co_actors[id_]["frequent_co_actors"].append(a)
	return co_actors


pprint.pprint (analyse_co_actors())



