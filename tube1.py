
import csv
import pandas as pd
import matplotlib.pyplot as plt


class Vertex:  # tube station
    def __init__(self, name, id_number, lat, long):
        self.name = name
        self.id_number = id_number
        self.edges = {}  # {vertex.id_number: [duration, line]}
        self.lat = lat  # latitude
        self.long = long  # longitude
        self.visited = False   

    def get_edges(self):
        return list(self.edges.keys())

    def add_edge(self, vertex_id, line_num, duration = 0):
        self.edges.update({vertex_id: [duration, line_num]})
        return list(self.edges.keys())

class Graph:    # tube network
  def __init__(self, directed = False):
    self.directed = directed
    self.graph_dict = {}  # vertex.id_number: vertex
    self.gps = {}  # {vertex.id_number: [vertex.lat, vertex.long]}

  def add_vertex(self, vertex):
    self.graph_dict[vertex.id_number] = vertex 

  def add_edges(self, from_vertex_id, to_vertex_id, line_num, duration = 0):
    from_vertex.add_edge(to_vertex) 
    self.graph_dict[from_vertex_id].add_edge(to_vertex_id, line_num, duration)
    if not self.directed: 
        self.graph_dict[to_vertex_id].add_edge(from_vertex_id, line_num, duration) 

  def find_route(self, start, end):
        # Dijkstra algorithm implementation to navigate the London tube
        # input: names of tube stations in string format, case sensitive
      
        # 1. travese vertices
        # =========================
        # input turned into corresponding vertices:
        start = int(stations_codelist.l[start]['id_number'])
        start = self.graph_dict[start]
        end = int(stations_codelist.l[end]['id_number'])
        end = self.graph_dict[end]
       
        # variables outside the main for-loop
        unvisited = dict([(id_n, 1000) for (id_n, vertex) in self.graph_dict.items()])  
        unvisited[start.id_number] = 0 
        visited = []
        current = start 
        routes = {current.id_number: [{'name': current.name, 'id': current.id_number, 'line': None, 'lat': current.lat, 'long': current.long}]}  # zapisuje se cesta k aktualnimu vrcholu a po jake lince (to v teto fazi chybi)
        latest = None 
        
        # traverse vertices:
        while end.visited == False:
               
            for neighbour_id, time_and_line in current.edges.items():
                neighbour_time = time_and_line[0]
                line_number = time_and_line[1]
                neighbour = self.graph_dict[neighbour_id]   
                
                # store the quickest path to each visited vertex in dict called Routes:
                if neighbour.id_number in unvisited:
                    if unvisited[neighbour.id_number] > (unvisited[current.id_number] + neighbour_time):  
                        unvisited[neighbour.id_number] = unvisited[current.id_number] + neighbour_time   
                        routes[neighbour.id_number] = routes[current.id_number][:]  
                        routes[neighbour.id_number].append({"name": neighbour.name, "id": neighbour_id, "line" : line_number, 'lat': neighbour.lat, 'long': neighbour.long})
                       
            # make sure visited vertices will not be visited again. Close the loop by changing Current:
            current.visited = True   
            visited.append(unvisited.pop(current.id_number))            
            for id_number, distance in unvisited.items():
                if distance == min(unvisited.values()):
                    next_key = id_number
            latest = current
            current = self.graph_dict[next_key]
            
        # 2. plot the quickest route
        # =============================
        # functions:
        def get_edges(route_to_end = routes[end.id_number]):
            # creates a) a list of dictionaries - edges on the route, b) gps coordinates marking limits of the figure
            coordinates_limits = dict(zip(['min_lat', 'max_lat', 'min_long', 'max_long'], [1000, -1000, 1000, -1000]))
            temp = [None, Vertex('empty', None, None, None)] 
            gps_edges = []   # connnections between vertices
            
            for item in route_to_end:
                # stores edges between couples of adjacent vertices
                temp.pop(0)  
                vertex = self.graph_dict[item['id']]
                temp.append(vertex)
                first_vertex_id = temp[0].id_number
                second_vertex_edges = temp[1].edges
                edge_time = second_vertex_edges.get(first_vertex_id, [None, None])[0]
                edge_line = second_vertex_edges.get(first_vertex_id, [None, None])[1]
                gps_edges.append({'line': edge_line, 'from_vertex': first_vertex_id, 'lat_from': temp[0].lat, 'long_from': temp[0].long, 'to_vertex': vertex.id_number, 'lat_to': vertex.lat, 'long_to': vertex.long})
                
                # updates max and min coordinates:
                if temp[1].lat != None:
                    if temp[1].lat > coordinates_limits['max_lat']:
                        coordinates_limits['max_lat'] = temp[1].lat
                    if temp[1].lat < coordinates_limits['min_lat']:
                        coordinates_limits['min_lat'] = temp[1].lat 
                    if temp[1].long > coordinates_limits['max_long']:
                        coordinates_limits['max_long'] = temp[1].long
                    if temp[1].long < coordinates_limits['min_long']:
                        coordinates_limits['min_long'] = temp[1].long 
            return gps_edges, coordinates_limits
         
        get_line_colour = lambda line_id: '#999999' if line_id == None else str('#'+lines.l[line_id]['colour'])
        get_legend = lambda line_id: None if line_id == None else str(lines.l[line_id]['name'])
        get_station_name = lambda station_id: tube.graph_dict[station_id].name
        
        # plot
        ax = plt.subplot()
        gps_edges, coordinates_limits = get_edges(routes[end.id_number])
        
        latest_line_colour = None
        for edge in gps_edges:
            line_colour = get_line_colour(edge['line'])
            if line_colour == latest_line_colour:
                mylegend = None
            else:
                mylegend = get_legend(edge['line'])
            latest_line_colour = line_colour 
            
            plt.plot([edge['long_from'], edge['long_to']], [edge['lat_from'], edge['lat_to']], marker='o', linestyle='--', color = line_colour, label = mylegend)
            if edge['long_from'] != None:
                ax.annotate(get_station_name(edge['from_vertex']), xy = (edge['long_from'], edge['lat_from']), xytext = (edge['long_from'] + 0.005, edge['lat_from'] - 0.01))
        
        ax.set_xticks([-0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2])
        ax.set_yticks([51.4, 51.5, 51.6, 51.7])
        ax.set_xlim((coordinates_limits['min_long'] - 0.02), (coordinates_limits['max_long'] + 0.02))
        ax.set_ylim((coordinates_limits['min_lat']  - 0.02), (coordinates_limits['max_lat'] + 0.02))
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.legend()
        
        plt.show()

        return 'from: {} to: {}, duration: {} minuts + time to change between lines'.format(start.name, end.name, visited[-1]) 

# handling the input data
stations_df = pd.read_csv('stations.csv')
stations = {} 
stations_codelist = []
stations_indices = []
for i in range(len(stations_df)):
    row = stations_df.iloc[i]
    station_details = list(row)
    stations[station_details[0]] = Vertex(station_details[3], station_details[0], station_details[1], station_details[2])
    stations_codelist.append({'id_number': row[0], 'name': row[3]})
    stations_indices.append(station_details[3])
stations_codelist = pd.DataFrame(dict(l = stations_codelist), index = stations_indices)  
    
with open('connections.csv') as c: 
    connections_reader = csv.DictReader(c) 
    for row in connections_reader:
        row = dict([(c, int(d)) for (c,d) in row.items()])  # pretypovani
        stations[row['station1']].edges[row['station2']] = [row['time'], row['line']]  
        stations[row['station2']].edges[row['station1']] = [row['time'], row['line']] 

li_list = []
indices = []
with open('lines.csv') as li: 
    li_reader = csv.DictReader(li)
    for row in li_reader:
        li_list.append(row)
        indices.append(row['line'])
        indices = [int(item) for item in indices]
lines = pd.DataFrame(dict(l = li_list), index = indices)

tube = Graph()
tube.graph_dict = stations

# call the find_route function
print(tube.find_route('Walthamstow Central', 'Surrey Quays'))
