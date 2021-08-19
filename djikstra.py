from collections import deque, namedtuple
# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
  return Edge(start, end, cost)


class Graph:
    def _init_(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )




    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        print("total shortest distance:", distances[dest], " km")
        return path



from geopy import distance
from geopy.geocoders import Nominatim


def getdistance(x,y):
    return distance.distance(x,y).km

def getcoordinates(x):
    geolocator = Nominatim(user_agent="pycharm")
    location = geolocator.geocode(x)
    return location.latitude, location.longitude

KL = getcoordinates("Kuala Lumpur International Airport")
SL = getcoordinates("Gimpo International Airport")
TK = getcoordinates("Haneda International Airport")
IN = getcoordinates("Soekarno Hatta International Airport")
TH = getcoordinates("Bangkok International Airport")
VN = getcoordinates("Vancouver International Airport")
TP = getcoordinates("Taipei Songshan Airport")
HK = getcoordinates("Hong Kong International Airport")
HN = getcoordinates("Noi Bai International Airport")

from gmplot import gmplot

# Place map
gmap = gmplot.GoogleMapPlotter(2.74552, 101.70151, 3)

# Polygon
city_lat, city_long = zip(*[
    KL, IN, KL, TP, KL, HK, KL, TH, TH,HN, IN, HN, HN, SL, HN, TP,
    HK, VN, HK, TK, TP, HK, TP, SL, SL, TK, TK, VN,
    ])
gmap.plot(city_lat, city_long, 'cornflowerblue', edge_width=2)



# Draw
# gmap.draw("my_map_new.html") already draw.. no need to draw everytime..
# since gmplot has some bugs in windows wheres markers not work, i use native maps markers api to mark the cities location





graph = Graph([
    ("KL", "IN", 1182.854293401512),  ("KL", "TP",3231.8242631574694),  
    ("KL", "HK",2524.3444234808403), ("KL", "TH", 1183.3989427180807),
    ("TH", "HN", 3026.9080409795506), ("IN", "HN",969.4356186447203 ), 
    ("HN", "SL", 2740.2380294860536),  ("HN", "TP",1666.9306385691227),
    ("HK", "VN", 10249.480684105873), ("HK","TK",2881.5743863405123),
    ("TP", "HK", 808.364970767223), ("TP","SL",1484.357658719539),
    ("SL", "TK",1158.7109083879723 ), ("TK","VN",7550.354524613018)
])

print("_________________________________________________")
print("Available city :")
print("IN(Jakarta)   ||    HN(Hanoi)   ||    SL(Seoul) ||    TP(Taipei)    ||  HK(Hong Kong)  ||   TH(Bangkok) ||  TK (Tokyo) || VN (Vancouver)  ")
print("_________________________________________________")
destination=input("Enter destination: ")
print("Warning..No direct path to your destination available..")
print("Showing alternative route: ")

s=graph.dijkstra("KL", destination)

j="->".join(s);
print(j)


import webbrowser
url = 'polyline-before.html'
webbrowser.open(url, new=2)  # open in new tab

#write destination to be read for plotting html

# write the shortest path to be read for plotting html
f = open("file.txt", "w")
f.write(j)
f.close()

import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

positive_text = open('text/positive_words.txt', 'r')
negative_text = open('text/negative_words.txt', 'r')

#.lower() - return lowercased string from given string
#.split() - split at the specified separator
positive_list = positive_text.read().lower().split()
negative_list = negative_text.read().lower().split()


def get_sentiment(list,titless):
    positive_count = 0
    negative_count = 0
    neutral_count = 0


    #count the word frequency
    for word in list:
        if word in positive_list:
            positive_count += 1
        elif word in negative_list:
            negative_count += 1
        else:
            neutral_count += 1

    #print the word frequency
    print('positive word count: ', positive_count,'\nnegative word count: ', negative_count, '\nneutral word count: ', neutral_count)

    # create graph

    sent_value = ['Positive', 'Negative']

    trace0 = go.Bar(
        x=sent_value,
        y=[positive_count, negative_count],
    )
    data = [trace0]
    layout = go.Layout(
        title=titless
    )

    fig = go.Figure(data=data, layout=layout)
    plot(fig)

    #get conclusion regarding the political sentiment
    if positive_count > negative_count:
        print('\nThe article shows positive sentiment')
        print(
            "_________________________________________________")
        return "positive"
    elif negative_count> positive_count:
        print('\nThe article shows negative sentiment')
        print(
            "_________________________________________________")
        return "negative"
    else:
        print('\nThe article shows neutral sentiment')
        print(
            "_________________________________________________")
        return "neutral"


print("_______________________________")
print("Check Sentiment and automatically plot on plot ly")

h=j.split("->")

def remove_city_path(city):
    if city==destination:
        print("cannot remove",city,"since",city,"is the user destination")
    else:
        graph.remove_edge(city, "IN")
        graph.remove_edge(city, "TP")
        graph.remove_edge(city, "HK")
        graph.remove_edge(city, "TK")
        graph.remove_edge(city, "TH")
        graph.remove_edge(city, "VN")
        graph.remove_edge(city, "SL")
        graph.remove_edge(city, "HN")
        graph.remove_edge(city, "IN")



for city_visited in h:
    if city_visited.lower() == "HN":

        print("Sentiment for HANOI")
        uk_text = open('text/HN.txt', 'r')
        g = get_sentiment(HN.read().lower().split(),"HANOI")
        if g=="negative":
            # remove all edges with HN in it
            remove_city_path(city_visited)



    elif city_visited.lower() == "TP":
        print("Sentiment for TAIPEI")
        us_text = open('text/TP.txt', 'r')
        g = get_sentiment(TP.read().lower().split(),"TAIPEI")
        if g == "negative":
            # remove all edges with TP in it
            remove_city_path(city_visited)



    elif city_visited.lower() == "SL":
        print("Sentiment for SOUTH Korea")
        nk_text = open('text/SL.txt', 'r',encoding="utf8")
        g=get_sentiment(SL.read().lower().split(),"South Korea")
        if g=="negative":
            # remove all edges with SL in it
            remove_city_path(city_visited)


    elif city_visited.lower() == "TK":
        print("Sentiment for TOKYO")
        colombia_text = open('text/TK.txt', 'r',encoding="utf8")
        g=get_sentiment(TK.read().lower().split(),"TOKYO")
        if g=="negative":
            # remove all edges with TK in it
            remove_city_path(city_visited)


    elif city_visited.lower() == "IN":
        print("Sentiment for INDONESIA")
        france_text = open('text/IN.txt', 'r',encoding="utf8")
        g=get_sentiment(france_text.read().lower().split(),"INDONESIA")
        if g=="negative":
            # remove all edges with IN in it
            remove_city_path(city_visited)


    elif city_visited.lower() == "TH":
        print("Sentiment for THAILAND")
        doha_text = open('text/TH.txt', 'r',encoding="utf8")
        g=get_sentiment(doha_text.read().lower().split(),"THAILAND")
        if g=="negative":
            # remove all edges with TH in it
            remove_city_path(city_visited)


    elif city_visited.lower() == "VN":
        print("Sentiment for Vancouver")
        narita_text = open('text/VN.txt', 'r',encoding="utf8")
        g=get_sentiment(narita_text.read().lower().split(),"Vancouver")
        if g=="negative":
            # remove all edges with VN in it
            remove_city_path(city_visited)


    
    elif city_visited.lower() == "HK":
        print("Sentiment for Hong Kong")
        hongkong_text = open('text/HK.txt', 'r',encoding="utf8")
        g=get_sentiment(hongkong_text.read().lower().split(),"Hong Kong")
        if g=="negative":
            # remove all edges with HK in it
            remove_city_path(city_visited)


new_graph=graph.dijkstra("kl", destination)

new_path="->".join(new_graph);
print(new_path)


url = 'polyline-after.html'
webbrowser.open(url, new=2)  # open in new tab

z = open("after.txt", "w")
z.write(new_path)
z.close()




#Get the total distribution taken of random routes taken for end user

KL_INDONESIA = 1182.854293401512
KL_TAIPEI = 3231.8242631574694
KL_HONGKONG = 2524.3444234808403
KL_THAI = 1183.3989427180807
THAI_HANOI = 3026.9080409795506
INDONESIA_HANOI = 969.4356186447203
HANOI_SEOUL = 2740.2380294860536
HANOI_TAIPEI = 1666.9306385691227
HONGKONG_VANCOUVER = 10249.480684105873
HONGKONG_TOKYO = 2881.5743863405123
TAIPEI_HONGKONG = 808.364970767223
TAIPEI_SEOUL =1484.357658719539
SEOUL_TOKYO =1158.7109083879723
TOKYO_VANCOUVER = 7550.354524613018

TotalDist = 40658.7773834

KL_INDONESIA = 1182.854293401512/TotalDist
KL_TAIPEI = 3231.8242631574694/TotalDist
KL_HONGKONG = 2524.3444234808403/TotalDist
KL_THAI = 1183.3989427180807/TotalDist
THAI_HANOI = 3026.9080409795506/TotalDist
INDONESIA_HANOI = 969.4356186447203/TotalDist
HANOI_SEOUL = 2740.2380294860536/TotalDist
HANOI_TAIPEI = 1666.9306385691227/TotalDist
HONGKONG_VANCOUVER = 10249.480684105873/TotalDist
HONGKONG_TOKYO = 2881.5743863405123/TotalDist
TAIPEI_HONGKONG = 808.364970767223/TotalDist
TAIPEI_SEOUL =1484.357658719539/TotalDist
SEOUL_TOKYO =1158.7109083879723/TotalDist
TOKYO_VANCOUVER = 7550.354524613018/TotalDist


print("Probability Distribution for KL to Colombia = ",KL_INDONESIA,
      "\nProbability Distribution for KL to United States = ",KL_TAIPEI,
      "\nProbability Distribution for KL to doha = ",KL_HONGKONG,
      "\nProbability Distribution for KL to hong kong = ",KL_THAI,
      "\nProbability Distribution for KL to United States = ",THAI_HANOI,
      "\nProbability Distribution for KL to doha = ",INDONESIA_HANOI,
      "\nProbability Distribution for KL to hong kong = ",HANOI_SEOUL,
      "\nProbability Distribution for KL to United States = ",HANOI_TAIPEI,
      "\nProbability Distribution for KL to doha = ",HONGKONG_VANCOUVER,
      "\nProbability Distribution for KL to hong kong = ",HONGKONG_TOKYO,
      "\nProbability Distribution for KL to United States = ",TAIPEI_HONGKONG,
      "\nProbability Distribution for KL to doha = ",TAIPEI_SEOUL,
      "\nProbability Distribution for KL to hong kong = ",SEOUL_TOKYO,
      "\nProbability Distribution for KL to hong kong = ",TOKYO_VANCOUVER,
      
      )