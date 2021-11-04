from operator import itemgetter
from enum import Enum

class VertexColor(Enum):
    white = 1
    gray = 2
    black = 3


class Vertex():
    """
    Hold a vertex with its attributes
    """
    def __init__(self, name):
        self.name = name
        # Use the the regular graph
        self.edges_to = []
        # Use for the reverse graph
        self.edges_from = []

        # Properties for DFS search
        # color - white - for initial state, gray - for discovered vertex or black - for finished vertex
        self.color = VertexColor.white
        self.predecessor = None
        self.discovery_time = None
        self.finish_time = None

    def add_edge_to(self, vertex):
        self.edges_to.append(vertex)

    def add_edge_from(self, vertex):
        self.edges_from.append(vertex)

    def print(self):
        print('vertex name ' + str(self.name))


class BipartiteGraph():
    """"
    Construct a bipartite graph
    """
    def __init__(self):
        self.vertexList = []
        self.isDebug = True

    def create_vertex(self, name):
        # Create vertex by its name, the names are unique identify a vertex
        v = Vertex(name=name)
        self.vertexList.append(v)

    def create_edge(self, from_name, to_name):
        # create an edge from vertex to vertex
        src_vertex = next((x for x in self.vertexList if x.name == from_name), None)
        dst_vertex = next((x for x in self.vertexList if x.name == to_name), None)

        # Use for the regular graph
        src_vertex.add_edge_to(vertex=dst_vertex)
        # Use for the reverse graph
        dst_vertex.add_edge_from(vertex=src_vertex)

    def calc_dfs(self, vertexList, graph_direction):
        # calculate DFS with a list that will be served as a stack
        # DFS initialization
        # params: vertexList - list of vertices for dfs order
        # params: graph_direction - True for regular graph direction, set False for reveres graph
        dfs = []

        for v in vertexList:
            v.color = VertexColor.white
            v.predecessor = None
            v.discovery_time = None
            v.finish_time = None

        # DFS starts here
        forest = []
        current_time = 0
        for v in vertexList:
            if v.color == VertexColor.white:
                current_time, dfs, depth_forest = self.dsf_visit(graph_direction = graph_direction, current_time = current_time, u_vertex= v, dfs = dfs, depth_forest = [])
                forest.append(depth_forest)

        # if self.isDebug:
        #     # Print the dfs order
        #     print('DFS order:\n')
        #     for v in dfs:
        #         v.print()

        return dfs, forest


    def calc_ssc(self):
        # Calculate strongly connected component for the graph, return the strongly connected components
        # reverse the graph and run DFS on the reverse graph using the above DFS order

        dsf_on_graph, _ = self.calc_dfs(vertexList=self.vertexList, graph_direction=True)

        dsf_on_graph_rev = dsf_on_graph.copy()
        dsf_on_graph_rev.reverse()

        dsf_on_reverse_graph, forest = self.calc_dfs(vertexList=dsf_on_graph_rev, graph_direction=False)

        # Sort the list in ascending numerical or lexicographical order
        for component_num, component in enumerate(forest):
            component.sort()
        sorted_forest = sorted(forest, key=itemgetter(0))

        # Output the vertices of each tree in the depth first forest
        return sorted_forest

    def dsf_visit(self, graph_direction, current_time, u_vertex, dfs, depth_forest):

        depth_forest.append(u_vertex.name)

        current_time = current_time + 1
        u_vertex.discovery_time = current_time
        u_vertex.color = VertexColor.gray

        # Get all its edges and insert to the stack
        if graph_direction:
            u_vertex_edges = u_vertex.edges_to
        else:
            u_vertex_edges = u_vertex.edges_from

        for v_vertex in u_vertex_edges:
            if v_vertex.color == VertexColor.white:
                v_vertex.predecessor = u_vertex
                current_time, dfs, depth_forest = self.dsf_visit(graph_direction = graph_direction, current_time = current_time, u_vertex= v_vertex, dfs = dfs, depth_forest = depth_forest)

        u_vertex.color = VertexColor.black
        current_time = current_time + 1
        u_vertex.finish_time = current_time

        # Hold the dfs results
        dfs.append(u_vertex)

        return current_time, dfs, depth_forest

    def isVertex(self, name):
        # Check if vertex is in the graph (in accordance with it's name)
        for v in self.vertexList:
            if str(v.name) == str(name):
                return True
        return False


def print_scc(scc, flag):
    # Print SCC, flag == True --> print the Unit test examples, Flag == False ---> print the example in Exercise #2 assignment
    print('SCC output\n')
    print('Number of SCC is ' + str(len(scc)))

    if flag:
        for component_num, component in enumerate(scc):
            print('Component number ' + str(component_num+1) + ' is : ' + str(component))
        print(scc)

    # Print the SCC output as shown in the Exercise #2 assignment
    else:
        for component_num, component in enumerate(scc):
            print('Component number ' + str(component_num+1) + ' is : {', end='')
            # iterate over the SCC's components list
            for index, num in enumerate(component):
                if index+1 != len(component):
                    print("x%d, " % num, end='')
                # Last element of the component
                else:
                    print("x%d}" % num)


def ssc_ut():
    # Create a graph for this unit test
    graph = BipartiteGraph()
    flag = True


    if False:
        # Unit test 1
        # this unit test mimic the picture from the following link
        # https://www.geeksforgeeks.org/strongly-connected-components/
        graph.create_vertex(name=0)
        graph.create_vertex(name=1)
        graph.create_vertex(name=2)
        graph.create_vertex(name=3)
        graph.create_vertex(name=4)

        graph.create_edge(from_name=0, to_name=2)
        graph.create_edge(from_name=0, to_name=3)
        graph.create_edge(from_name=1, to_name=0)
        graph.create_edge(from_name=2, to_name=1)
        graph.create_edge(from_name=3, to_name=4)

    elif False:
        # Unit test 2 - example took from Corman book on page 616 third edition
        # Corman book: https://edutechlearners.com/download/Introduction_to_algorithms-3rd%20Edition.pdf
        graph.create_vertex(name='a')
        graph.create_vertex(name='b')
        graph.create_vertex(name='c')
        graph.create_vertex(name='d')
        graph.create_vertex(name='e')
        graph.create_vertex(name='f')
        graph.create_vertex(name='g')
        graph.create_vertex(name='h')

        graph.create_edge(from_name='a', to_name='b')

        graph.create_edge(from_name='b', to_name='c')
        graph.create_edge(from_name='b', to_name='e')
        graph.create_edge(from_name='b', to_name='f')

        graph.create_edge(from_name='c', to_name='d')
        graph.create_edge(from_name='c', to_name='g')

        graph.create_edge(from_name='d', to_name='c')
        graph.create_edge(from_name='d', to_name='h')

        graph.create_edge(from_name='e', to_name='a')
        graph.create_edge(from_name='e', to_name='f')

        graph.create_edge(from_name='f', to_name='g')

        graph.create_edge(from_name='g', to_name='f')
        graph.create_edge(from_name='g', to_name='h')

        graph.create_edge(from_name='h', to_name='h')

    elif False:
        # example is taken from here: https://inginious.org/course/competitive-programming/graphs-scc
        for i in range(0,16,1):
            print(i)
            graph.create_vertex(name=i)

        graph.create_edge(from_name=0, to_name=1)
        graph.create_edge(from_name=0, to_name=5)

        graph.create_edge(from_name=1, to_name=2)
        graph.create_edge(from_name=1, to_name=3)
        graph.create_edge(from_name=1, to_name=8)

        graph.create_edge(from_name=2, to_name=0)

        graph.create_edge(from_name=3, to_name=2)
        graph.create_edge(from_name=3, to_name=7)
        graph.create_edge(from_name=3, to_name=4)

        graph.create_edge(from_name=4, to_name=6)

        graph.create_edge(from_name=5, to_name=4)

        graph.create_edge(from_name=6, to_name=5)

        graph.create_edge(from_name=7, to_name=12)
        graph.create_edge(from_name=7, to_name=10)
        graph.create_edge(from_name=7, to_name=8)

        graph.create_edge(from_name=8, to_name=11)

        graph.create_edge(from_name=9, to_name=7)

        graph.create_edge(from_name=10, to_name=14)
        graph.create_edge(from_name=10, to_name=11)

        graph.create_edge(from_name=11, to_name=9)
        graph.create_edge(from_name=11, to_name=15)

        graph.create_edge(from_name=12, to_name=13)
        graph.create_edge(from_name=12, to_name=14)

        graph.create_edge(from_name=13, to_name=15)

        graph.create_edge(from_name=14, to_name=12)

        graph.create_edge(from_name=15, to_name=14)

    elif True:
        flag = False
        # Example is taken from the given assignment exercise
        # Make sure to that string which represent the graph is in the syntax as shown in the Exercise #2 assignment
        # Input string
        graph_string = "1 2,2 3,3 1,3 4,4 4"

        # Check if the graph_string is an empty string or None value or any "falsy" value
        # The definition of "falsy" values can be find here: https://docs.python.org/2/library/stdtypes.html#truth-value-testing section 5.1
        if not graph_string:
            if graph_string == "":
                print("The given string represents the graph is an empty string\n")
                print('SCC output\n')
                print('Number of SCC is 0\n' + '[]')
            else:
                print("The given string represents the graph is a None value or any 'falsy' value")
        else:
            # Split the graph_string to it's edges
            edges_list = graph_string.split(",")
            # Go over the edges in the edges_list
            for edge_string in edges_list:
                # Get the vertices of the edge
                str_split = edge_string.split()
                vertex1 = int(str_split[0])
                vertex2 = int(str_split[1])

                # Create the vertices if were'nt created yet
                for v in [vertex1, vertex2]:
                    if graph.isVertex(name=v) is False:
                        graph.create_vertex(name=v)

                # Create the edge
                graph.create_edge(from_name=vertex1, to_name=vertex2)

            # Run SCC algorithm and print the output
            scc = graph.calc_ssc()
            print_scc(scc=scc, flag=flag)

    if flag:
        scc = graph.calc_ssc()
        print_scc(scc=scc, flag=flag)

if __name__ == '__main__':
    # This program run strongly connected component on the input dataset
    ssc_ut()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
