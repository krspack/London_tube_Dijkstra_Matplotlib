# London_tube_Dijkstra_Matplotlib
Dijkstra algorithm applied to London tube. The script helps you find the quickest way from one tube station to another. Input: any two existing stations. Output: the quickest route + plot of the route in Matplotlib.

I got the idea from @AparnApu (https://github.com/AparnApu/LondonTube-as-Graph) and @MarkDunne (http://markd.ie/2016/04/10/The-London-Tube-as-a-Graph/) both of whom have used Networkx with an inbuilt function for the Dijkstra algorithm. I decided to omit Networkx for study reasons and try to write my own implementation instead. Thanks also to @MarkDunne for the data on stations and lines.

The script does not take into account realtime transport data, nor does it count with real timetables, but it does reflect time needed to change lines (i.e. walk to another platform and wait for another train). This significantly improves the results and makes them closer to results given by the Transport for London app.
