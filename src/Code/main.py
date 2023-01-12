from functions import import_libraries, url_creator
from variables import url

import_libraries()

driver.get(url)
time.sleep(2)
soup = bs(driver.page_source,"lxml")
all_a = soup.find_all('a')

ranking = []
all_td = soup.find_all("td", class_="collection_rank")
for td in all_td:
       ranking.append(td.get_text(strip=True))

name = []
all_td = soup.find_all("td", class_="collection_objectname browse")
for td in all_td:
       name.append(td.a.get_text(strip=True))

all_a_in_td = []
game_id = []
for i in range(0, len(all_td)):
    all_a_in_td.append(str(all_td[i].a))
for i in all_a_in_td:
    game_id.append(i.split("/")[2])

print(f"This should be 100: {len(game_id)}")    

url_creator(2, 15)

for i in urls:
   time.sleep(2)
   driver.get(i)
   soup = bs(driver.page_source,"lxml")
   all_a = soup.find_all('a')
    
   all_td = soup.find_all("td", class_="collection_rank")
   for td in all_td:
      ranking.append(td.get_text(strip=True))

   all_td = soup.find_all("td", class_="collection_objectname browse")
   for td in all_td:
         name.append(td.a.get_text(strip=True))

   all_a_in_td = []
   for x in range(0, len(all_td)):
      all_a_in_td.append(str(all_td[x].a))
   for x in all_a_in_td:
      game_id.append(x.split("/")[2])

print(f"This should be 1500: {len(game_id)}")    

BGG_top = pd.DataFrame({"game_id": game_id,
                    "name": name,
                    "ranking": ranking})

BGG_top.to_csv("BGG_top_2022_10_23.csv", index=False)

bgg = boardgamegeek.BGGClient()
indices = game_id.copy()

game_data = []
count = 1
for i in range(0, 1500, 150):
    chunk_of_games = bgg.game_list(indices[i: i + 150])
    game_data.extend([game.data() for game in chunk_of_games])

    print(str(count)+"/10  - "+str(i + 150), end="\r")
    count += 1

print(f"This should be 1500: {len(game_data)}")

expansion = [g["expansion"] for g in game_data]                
accessory = [g["accessory"] for g in game_data]                  
categories = [g["categories"] for g in game_data]            
mechanics = [g["mechanics"] for g in game_data]                
yearpublished = [g["yearpublished"] for g in game_data]        
minplayers = [g["minplayers"] for g in game_data]          
maxplayers = [g["maxplayers"] for g in game_data]          
playingtime = [g["playingtime"] for g in game_data]        
minplaytime = [g["minplaytime"] for g in game_data]        
maxplaytime = [g["maxplaytime"] for g in game_data]         
minage = [g["minage"] for g in game_data]                      
usersrate = [g["stats"]["usersrated"] for g in game_data]       
average = [g["stats"]["average"] for g in game_data]           
bayesaverage = [g["stats"]["bayesaverage"] for g in game_data]    
stddev = [g["stats"]["stddev"] for g in game_data]             
owned = [g["stats"]["owned"] for g in game_data]                 
numcomments = [g["stats"]["numcomments"] for g in game_data]    
numweights = [g["stats"]["numweights"] for g in game_data]       
averageweight = [g["stats"]["averageweight"] for g in game_data] 
total_votes_suggested_players = [g["suggested_players"]["total_votes"] for g in game_data]

recommended_players = []
votes_for_best_num_players = []
recommended_players_final = []
votes_for_best_num_players_final = []

for g in game_data:
    temp_maxkey_list = []
    temp_maxvalue_list = []
    temp_votes = []
    temp_player_list = list(g["suggested_players"]["results"].keys())
    for num_plyrs in temp_player_list:
        temp_votes.append(g["suggested_players"]["results"][num_plyrs]["best_rating"])
        if max(temp_votes) == g["suggested_players"]["results"][num_plyrs]["best_rating"]:
            temp_maxkey_list.append(g["suggested_players"]["results"][num_plyrs])
            temp_maxvalue_list.append(max(temp_votes))     
        votes_for_best_num_players.append(max(temp_maxvalue_list))
        for k, v in g["suggested_players"]["results"].items():
            if v["best_rating"] == votes_for_best_num_players[-1]:
                recommended_players.append(k)
    recommended_players_final.append(recommended_players[-1])
    votes_for_best_num_players_final.append(votes_for_best_num_players[-1])

recom_plyrs_int = []

for i in recommended_players_final:
    try:
        recom_plyrs_int.append(int(i))
    except:
        recom_plyrs_int.append(int('8'))

BGG_top_full = pd.DataFrame({"game_id": indices,
                    "name": name,
                    "ranking": ranking,
                    "expansion": expansion,
                    "accessory": accessory,
                    "categories": categories,
                    "mechanics": mechanics,
                    "yearpublished": yearpublished,
                    "minplayers": minplayers,
                    "maxplayers": maxplayers,
                    "playingtime": playingtime,
                    "minplaytime": minplaytime,
                    "maxplaytime": maxplaytime,
                    "minage": minage,
                    "usersrate": usersrate,
                    "average": average,
                    "bayesaverage": bayesaverage,
                    "stddev": stddev,
                    "numcomments": numcomments,
                    "numweights": numweights,
                    "averageweight": averageweight,
                    "votes_suggested_players": total_votes_suggested_players,
                    "recom_plyrs_int": recom_plyrs_int,
                    "votes_best_players": votes_for_best_num_players_final})

BGG_top_full.to_csv("BGG_top_full_2022_11_01.csv", index=False)

BGG_df = pd.read_csv('BGG_top_full_2022_11_01.csv')

BGG_df["categories"] = BGG_df['categories'].str.replace("[","").str.replace("]","").str.replace("'","").str.replace('"','')

for i in BGG_df["categories"]:
    BGG_df["categories"] = BGG_df["categories"].str.strip()

CAT_count = BGG_df['categories'].str.get_dummies(',')
CAT_count.columns = CAT_count.columns.str.strip()
numcat = CAT_count.sum(axis=1)
BGG_df["numcat"] = numcat

BGG_df[["playingtime", "name", "ranking"]].sort_values("playingtime", ascending=False).head(20)
dfi.export("maxplaytime_graphic.png")

BGG_df["mechanics"] = BGG_df["mechanics"].replace(regex=['Deck, Bag, and Pool Building'],value='Deck Bag and Pool Building')
BGG_df["mechanics"] = BGG_df["mechanics"].replace(regex=['I Cut, You Choose'],value='I Cut You Choose')
BGG_df["mechanics"] = BGG_df["mechanics"].replace(regex=['Worker Placement, Different Worker Types'],value='Worker Placement Different Worker Types')

BGG_df["mechanics"] = BGG_df['mechanics'].str.replace("[","").str.replace("]","").str.replace("'","").str.replace('"','')
for i in BGG_df["mechanics"]:
    BGG_df["mechanics"] = BGG_df["mechanics"].str.strip()
MECH_count = BGG_df['mechanics'].str.get_dummies(',')
MECH_count.columns = MECH_count.columns.str.strip()
nummech = MECH_count.sum(axis=1)
BGG_df["nummech"] = nummech

id = BGG_df['game_id']

driver = webdriver.Chrome(executable_path=r"/usr/local/bin/chromedriver_2")
time.sleep(2)

urls = []
for i in range(0, len(id)):
     urls.append(f"https://boardgamegeek.com/boardgame/{id[i]}")

avgpriceusd = []
langdep = []
contador = 1
print(f"Please stand by. This process may take upwards of an hour.")
for i in urls:
      print(f"{contador} of {len(urls)}")
      driver.get(i)
      time.sleep(1)
      soup = bs(driver.page_source,"lxml")
      all_a = soup.find_all('a')

      price = []
      all_price = soup.find_all("strong", class_="ng-binding")
      for strong in all_price:
            price.append(strong.get_text(strip=True))
      print(f"price {price}")

      usd = []
      for i in price:
            print(f"i in price {i}")
            if i != '(unavaible)':
                  if i.startswith('$'):
                        usd.append(i)
                        print(f"usd {usd[-1]}")
            else:
                  pass 
      usd = [d.replace('$', '').replace(',','') for d in usd]  
      usd = [float(d) for d in usd]
      avgprice = []
      print(sum(usd))
      print(len(usd))
      try:
            avgprice = sum(usd) / len(usd)
            avgpriceusd.append(round(avgprice, 2))
            print(f"avgpriceusd {avgpriceusd[-1]}")

      except:
            avgpriceusd.append(None)  
            print(f"None appended")

      print("all feat started")
      all_feat = soup.find_all("span", class_="ng-isolate-scope")
      for span in all_feat:
            langtemp = []
            langtemp.append(span.get_text(strip=True))
      langdep.append(langtemp[-1])
      print(langdep[-1])
      contador += 1

langdepshort = []
for i in langdep:
    langdepshort.append(i[:-21])

BGG_df["langdep"] = langdepshort
BGG_df["avgprice"] = avgpriceusd

BGG_df.to_csv("BGG_full_2022_11_01.csv", index=False)

BGG_df.drop('game_id', axis = 1, inplace = True)
BGG_df.drop('expansion', axis = 1, inplace = True)
BGG_df.drop('accessory', axis = 1, inplace = True)
BGG_df.drop('minplayers', axis = 1, inplace = True)
BGG_df.drop('maxplayers', axis = 1, inplace = True)
BGG_df.drop('minplaytime', axis = 1, inplace = True)
BGG_df.drop('maxplaytime', axis = 1, inplace = True)
BGG_df.drop('votes_suggested_players', axis = 1, inplace = True)
BGG_df.drop('votes_best_players', axis = 1, inplace = True)

langdeptemp = {}
langdeptemp = BGG_df["langdep"].copy()
langdepset = set(langdeptemp)

langdeplegend = {
    "1": "No necessary in-game text",
    "2": "Some necessary text - easily memorized or small crib sheet",
    "3": "Moderate in-game text - needs crib sheet or paste ups",
    "4": "Extensive use of text - massive conversion needed to be playable",
    "5": "Unplayable in another language"
}

langdepint = []
for dep in BGG_df["langdep"]:
    if dep in langdeplegend.values():
        langdepint.append(list(langdeplegend.keys())[list(langdeplegend.values()).index(dep)])
    else:
        langdepint.append(0)

langdepint = [int(i) for i in langdepint]

BGG_df.drop('langdep', axis = 1, inplace = True)
BGG_df["langdep"] = langdepint

BGG_df.to_csv("BGG_finaldf_from_BGG20221101.csv", index=False)

plt.figure(figsize=(8,8))
sns.color_palette("colorblind")
sns.heatmap(BGG_df.corr(),
            vmin=-1,
            vmax=1,
            cmap=sns.diverging_palette(145, 280, s=85, l=25, n=7),
            cbar_kws=dict(use_gridspec=False,location="right",pad=0.01,shrink=0.5),
            square=True,
            linewidths=.1,
            annot=True,
            annot_kws={"size":6})
plt.savefig("corr.png")
plt.show()


sns.pairplot(BGG_df)
plt.savefig("pairplot.png")
plt.show()


sns.jointplot(x=BGG_df['nummech'],
              y=BGG_df['averageweight'],
              color="#4CB391",
             height = 4)
plt.savefig("mech_v_weight.png")
plt.show()


sns.jointplot(x=BGG_df['average'],
              y=BGG_df['nummech'],
              color="#4CB391",
             height = 4)
plt.savefig("avg_v_mech.png")
plt.show()


sns.jointplot(x=BGG_df['average'],
              y=BGG_df['averageweight'],
              color="#4CB391",
             height = 4)
plt.savefig("avg_v_weight.png")
plt.show()


sns.jointplot(x=BGG_df['ranking'],
              y=BGG_df['average'],
              color="#4CB391",
             height = 4)
plt.savefig("rank_v_avg_dispersion.png")
plt.show()


trace1 = go.Scatter(
                    x = BGG_df["ranking"],
                    y = BGG_df["bayesaverage"],
                    mode = "lines",
                    name = "Bayes Average",
                    #marker = dict(color = 'green'),
                    marker = dict(color = 'rgba(95, 158, 160, 0.8)'),
                    text= BGG_df["bayesaverage"])
trace2 = go.Scatter(
                    x = BGG_df["ranking"],
                    y = BGG_df["average"],
                    mode = "lines",
                    name = "2015",
                    #marker = dict(color = 'blue'),
                    marker = dict(color = 'rgba(100, 149, 237, 0.8)'),
                    text= BGG_df["average"])
data = [trace1, trace2]
layout = dict(title = 'Promedio y Promedio Bayesnesiano por Ranking',
              xaxis= dict(title= 'Ranking',ticklen= 5,zeroline= False),
              yaxis= dict(title= 'Valoracion',ticklen= 5,zeroline= False)
             )
fig = go.Figure(data = data, layout=layout)
fig.write_image("avg_v_bayesavg.png")
display(fig)


sns.jointplot(x=BGG_df['average'],
              y=BGG_df['yearpublished'],
              color="#4CB391",
             height = 4)
plt.savefig("avg_v_yrpublished.png")
plt.show()


trace = go.Scatter(
                    x = BGG_df["ranking"],
                    y = BGG_df["yearpublished"],
                    mode = "markers",
                    name = "yearpublished",
                    marker = dict(color = 'rgba(95, 158, 160, 0.8)')
)
data = [trace]
layout = dict(title = 'Year Published v Ranking (zoomed)',
              xaxis= dict(title= 'Ranking',ticklen= 5,zeroline= False),
              yaxis= dict(title= 'Year Published',ticklen= 5,zeroline= False)
             )

#fig = dict(data = data, layout = layout)
fig = go.Figure(data = data, layout=layout, layout_yaxis_range=[1990,2025])
plt.savefig("rank_v_yrpublished_zoomed.png")
display(fig)


plt.subplots(figsize=(8,8))
wordcloud = WordCloud(
                          background_color='white',
                          width=512,
                          height=384
                         ).generate(" ".join(BGG_df["categories"]))
plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('cat_wordcloud.png')
plt.show()





