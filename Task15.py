import pprint
from Task1 import scrapped
from Task13 import scrap_movie_details



movie_list =[]
for i in scrapped:
	url = i["url"]
	main_data = scrap_movie_details(url)
	movie_list.append(main_data)
# print (movie_list)


def actor_count():
	count_dic = {}
	for i in movie_list:
		for j in i["Cast"]:
			if j["actor_id"] not in count_dic:
				count_dic[j["actor_id"]] = {}
				count_dic[j["actor_id"]]["actor_name"] = j["actor_name"]
				count_dic[j["actor_id"]]["Num_movies"]=1
			else:
				count_dic[j["actor_id"]]["Num_movies"]+=1

	return count_dic

pprint.pprint (actor_count())