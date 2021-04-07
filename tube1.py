
import csv
import pandas as pd
import matplotlib.pyplot as plt


class Edge:
    def __init__(self, edge_id, from_vertex, to_vertex, time, line):
       self.edge_id = edge_id
       self.from_vertex = from_vertex   # id of the vertex
       self.to_vertex = to_vertex    # id of the vertex
       self.time = time    # in minutes
       self.line = line   # id of the line
       self.coordinates = None

class Vertex:  # tube station
    def __init__(self, name, station_id, lat, long):
        self.name = name
        self.station_id = station_id
        self.lat = lat  # latitude
        self.long = long  # longitude
        self.visited = False
        self.neighbours = []  # station_id
        self.edges = []  # edge_id

    def get_neighbours(self):
        neighbours_ids = list(self.neighbours,keys())
        neighbours_vertices = [all_vertices[id_number] for id_number in neighbours_ids]
        return neighbours_vertices

class Graph:    # tube network
  def __init__(self, directed = False):
    self.directed = directed
    self.all_vertices = all_vertices
    self.all_edges = all_edges

  def get_vertex(self, vertex_id):
      return self.all_vertices[vertex_id]

  def get_coordinates(self, edge):   # type Graph, type Edge
      from_vertex = self.get_vertex(edge.from_vertex)  # type Vertex
      to_vertex = self.get_vertex(edge.to_vertex)  # type Vertex
      edge.coordinates = {'lat_from': from_vertex.lat, 'long_from': from_vertex.long, 'lat_to': to_vertex.lat, 'long_to': to_vertex.long}
      return edge.coordinates
      
  def get_edges_from(self, vertex):   # input: vertex > ids of corresponding edges. Output: type Edges
      edges_selected = [self.all_edges[edge_id] for edge_id in vertex.edges]
      return edges_selected
  """
  def get_edges_between (self, vertex1, vertex2):
      edges = []
      if self.station_id not in vertex2.neighbours:
        return 'no direct link between given stations'
      else:
        for e_id in vertex1.edges:
            e = self.all_edges[e_id]
            if (e.from_vertex == vertex2) or (e.to_vertex == vertex2):
            edges.append(e)
      return edges
   """
      
  '''
  # 294, 221
  x = tube.get_vertex(221)
  y = tube.get_vertex(294)
  print(x.name, ' ', y.name)
  x_edge = x.get_edge(y)
  y_edge = y.get_edge(x)
  print(x_edge.edge_id, " ", y_edge.edge_id)
  '''

  def find_route(self, start, end):
        # Dijkstra algorithm implementation to navigate the London tube
        # input: names of tube stations in string format, case sensitive

        # 1. travese vertices
        # =========================
        # input turned into corresponding vertices:
        start = int(stations_codelist.loc[start]['id'])
        start = self.get_vertex(start)
        end = int(stations_codelist.loc[end]['id'])
        end = self.get_vertex(end)

        # variables outside the main for-loop
        unvisited = dict([(id_n, 1000) for (id_n, vertex) in self.all_vertices.items()])
        unvisited[start.station_id] = 0
        visited = []
        current = start
        routes = {current.station_id: [{'name': current.name, 'id': current.station_id, 'line': None, 'lat': current.lat, 'long': current.long}]}
        latest = None

        # traverse vertices:
        while end.visited == False:

            for neighbour_id in current.neighbours:
                neighbour = self.get_vertex(neighbour_id)
                edge_ids = self.get_edges_between(current, neighbour_id)  #[]
                # ------------------------------------------------------------uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
                
                edge_to_neighbour = current.get_edge(neighbour)
                neighbour_time = edge_to_neighbour.time
                neighbour_line = edge_to_neighbour.line

                # store the quickest path to each visited vertex in dict called Routes:
                if neighbour.station_id in unvisited:
                    if unvisited[neighbour.station_id] > (unvisited[current.station_id] + neighbour_time):
                        unvisited[neighbour.station_id] = unvisited[current.station_id] + neighbour_time
                        routes[neighbour.station_id] = routes[current.station_id][:]
                        routes[neighbour.station_id].append({"name": neighbour.name, "id": neighbour.station_id, "line" : neighbour_line, 'lat': neighbour.lat, 'long': neighbour.long})

            # make sure visited vertices will not be visited again. Close the loop by changing Current:
            current.visited = True
            visited.append(unvisited.pop(current.station_id))
            for station_id, distance in unvisited.items():
                if distance == min(unvisited.values()):
                    next_key = station_id
            latest = current
            current = self.get_vertex(next_key)

        print(routes[end.station_id])

        # 2. plot the quickest route
        # =============================
        # functions:
        def get_edges(route_to_end = routes[end.station_id]):
            # creates a) a list of edges on the route, b) gps coordinates marking limits of the figure
            coordinates_limits = dict(zip(['min_lat', 'max_lat', 'min_long', 'max_long'], [1000, -1000, 1000, -1000]))
            edges_to_plot = []

            for i in range(1, len(route_to_end)):  # loop through a list of dictionaries
                vertex1 = self.get_vertex(route_to_end[i-1]['id'])
                vertex2 = self.get_vertex(route_to_end[i]['id'])
                edge = vertex1.get_edge(vertex2)
                print(vertex1.name, ' ', vertex2.name)
                edge_coordinates = self.get_coordinates(edge)
                edges_to_plot.append(edge)
                print(edge.from_vertex, " ", edge.to_vertex)
                print("--")

                # updates max and min coordinates:
                if True:
                    if edge.coordinates['lat_from'] > coordinates_limits['max_lat']:
                        coordinates_limits['max_lat'] = edge.coordinates['lat_from']
                    if edge.coordinates['lat_from'] < coordinates_limits['min_lat']:
                        coordinates_limits['min_lat'] = edge.coordinates['lat_from']
                    if edge.coordinates['long_from'] > coordinates_limits['max_long']:
                        coordinates_limits['max_long'] = edge.coordinates['long_from']
                    if edge.coordinates['long_from'] < coordinates_limits['min_long']:
                        coordinates_limits['min_long'] = edge.coordinates['long_from']
                    if edge.coordinates['lat_to'] > coordinates_limits['max_lat']:
                        coordinates_limits['max_lat'] = edge.coordinates['lat_to']
                    if edge.coordinates['lat_to'] < coordinates_limits['min_lat']:
                        coordinates_limits['min_lat'] = edge.coordinates['lat_to']
                    if edge.coordinates['long_to'] > coordinates_limits['max_long']:
                        coordinates_limits['max_long'] = edge.coordinates['long_to']
                    if edge.coordinates['long_to'] < coordinates_limits['min_long']:
                        coordinates_limits['min_long'] = edge.coordinates['long_to']
            return edges_to_plot, coordinates_limits

        get_line_colour = lambda line_id: '#999999' if line_id == None else str('#'+lines.l[line_id]['colour'])
        get_legend = lambda line_id: None if line_id == None else str(lines.l[line_id]['name'])
        get_station_name = lambda station_id: self.all_vertices[station_id].name

        # plot
        ax = plt.subplot()
        edges_to_plot, coordinates_limits = get_edges(routes[end.station_id])

        latest_line_colour = None
        for edge in edges_to_plot:
            print(edge.edge_id)
            print(edge.from_vertex, get_station_name(edge.from_vertex))
            print(edge.to_vertex, get_station_name(edge.to_vertex))
            print(dict(bigtab.iloc[edge.edge_id]))
            print('----')
            line_colour = get_line_colour(edge.line)
            if line_colour == latest_line_colour:
                mylegend = None
            else:
                mylegend = get_legend(edge.line)
            latest_line_colour = line_colour

            plt.plot([edge.coordinates['long_from'], edge.coordinates['long_to']], [edge.coordinates['lat_from'], edge.coordinates['lat_to']], marker='o', linestyle='--', color = line_colour, label = mylegend)
            ax.annotate(get_station_name(edge.from_vertex), xy = (edge.coordinates['long_from'], edge.coordinates['lat_from']), xytext = (edge.coordinates['long_from'] + 0.005, edge.coordinates['lat_from'] - 0.01))

        ax.set_xticks([-0.60, -0.55, -0.50, -0.45, -0.40, -0.35, -0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15, 0.20])
        ax.set_yticks([51.40, 51.45, 51.50, 51.55, 51.60, 51.65, 51.70])
        ax.set_xlim((coordinates_limits['min_long'] - 0.02), (coordinates_limits['max_long'] + 0.02))
        ax.set_ylim((coordinates_limits['min_lat']  - 0.02), (coordinates_limits['max_lat'] + 0.02))
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.legend()

        plt.show()

        return 'from: {} to: {}, duration: {} minutes + time to change between lines'.format(start.name, end.name, visited[-1])


# 3. handling the input data'
# ==========================
# create DataFrames from csvs, create a codelist to map each station name to an ID
stations_df = pd.read_csv('stations.csv')
stations_codelist = stations_df[['id', 'name']].set_index('name', drop=True, append=False, inplace=False, verify_integrity=True)  # print(stations_codelist.loc['Bank']['id'])

connections_df = pd.read_csv('connections.csv')
bigtab = connections_df.merge(stations_df, how = 'left', left_on = 'station1', right_on = 'id')
bigtab['edge_id'] = range(len(bigtab))
# print(bigtab.head())
# bigtab.to_csv('new-csv-file.csv')


# populate all_edges, connect class Vertex with class Edge by filling vertex.neighbours and vertex.edges dictionaries. 

all_vertices = {}
all_edges = {}    
for i in range(len(bigtab)):
    row = dict(bigtab.iloc[i])
    all_vertices[tuple(row['station1'], row['line'])] = Vertex(row['name'], tuple(row['station1'], row['line']), row['lat'], row['long'])
    all_vertices[tuple(row['station2'], row['line'])] = Vertex(row['name'], tuple(row['station2'], row['line']), row['lat'], row['long'])
    all_edges[i] = Edge(row['edge_id'], row['station1'], row['station2'], row['time'], row['line'])
    vertex_to_update = all_vertices[tuple(row['station1'], row['line'])]
    vertex_to_update2 = all_vertices[tuple(row['station2'], row['line'])]
    vertex_to_update.edges.append(i)
    vertex_to_update2.edges.append(i)
    vertex_to_update.neighbours.append(tuple(row['station2'], row['line']))
    vertex_to_update2.neighbours.append(tuple(row['station1'], row['line']))

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

# call the find_route function
# print(tube.find_route('West Ruislip', 'West India Quay'))

"""
for v in tube.all_vertices.values():
    print(v.name, " ", v.station_id, " station: edge: ", v.neighbours, " edge: edge: ", v.edges)
    x = v.edges.values()
    for xx in x:
        print('line: ', xx.line, ' from: ', xx.from_vertex, " to: ", xx.to_vertex)
    print("__")
"""







