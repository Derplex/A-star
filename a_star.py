#class definitions ------------------------------------------------------------------------------------------------------------------------------------------------------

#define class for a node with properties  name, parent node and the lower bound. The lower bound is an extra value given to a node to make Dijkstra into A*.
class Node():
    def __init__(self, name, parent_node, lower_bound):
        self.name = name
        self.parent_node = parent_node
        self.lower_bound = lower_bound

#define class for a list with the to check nodes (discovered and not permanent) with some related functions.
class NodeChecker():
    def __init__(self):
        self.container = []

    #function to add a node to the list
    def add(self, node):
        self.container.append(node)

    #function to get the permanent node (node with lowest cost) in the current container list.
    def get_permanent(self):
    # Check if there are any nodes in the container that haven't been added to the permanent list
        lowest_node = None
        for node in self.container:
            if lowest_node == None:
                lowest_node = node
                continue
            if (get_edge_length(node.name, node.parent_node.name) + get_lower_bound(node.name)) < (get_edge_length(lowest_node.name, lowest_node.parent_node.name) + get_lower_bound(lowest_node.name)):
                lowest_node = node
        self.container.remove(lowest_node)
        return lowest_node

    #function that returns True if container is empty
    def empty(self):
        return len(self.container) == 0

    #function that puts the names of all nodes in container into a seperate list
    def get_names(self):
        list_names = []
        for node in self.container:
            list_names.append(node.name)
        return list_names
    
    def get_node(self, node_name):
        for node in self.container:
            if node.name == node_name:
                return node
        return False

#function definitions ----------------------------------------------------------------------------------------------------------------------------------------------------

#function that returns the lower bound of a given node
def get_lower_bound(node_name):
    if len(list_nodes) == 0:                #if there are no nodes it returns False
        return False
    
    for tuple in list_nodes:                #for every node in the list of nodes it returns the lower bound of the given node name
        if tuple[0] == node_name:
            return tuple[1]
    return None                             #if the node does not exist it returns None

#function that returns a list with the neighbours of a given node
def get_neighbours(node_name):
    list_neighbours = []                            #define the list with the nodes

    for edge in list_edges:                         #for every edge in the list of edges it checks if the node is in the first or second position
        if edge[0] == node_name:                    #and then adds the other node to the list
            list_neighbours.append(edge[1])
        elif edge[1] == node_name:
            list_neighbours.append(edge[0])
    return list_neighbours

#function that returns the length of a given edge
def get_edge_length(first_node_name, second_node_name):                 #input of the nodes of the requested edge
    for edge in list_edges:
        if first_node_name in edge and second_node_name in edge:        #if both nodes are in the tuple of the edge return this edge
            return edge[2]
    return None

#function that returns the list of the shortest path taken and the length of this path (the A* algorithm)
def find_path(start_name, finish_name):
    #define the list of permanent nodes and the classes of node_checker and the start node
    list_permanent_nodes = []
    node_checker = NodeChecker()
    start_node = Node(start_name, None, get_lower_bound(start_name))

    node_checker.add(start_node)                                                #add the start node to the container

    while not node_checker.empty():                                             #this loop loops while container not empty
        current_node = node_checker.get_permanent()                             #the current node is the permanent node of the iteration (node with lowest cost)
        print("Got", current_node.name, "from node_checker")
        if current_node.name == finish_name:                                    #if the new permanent node is the finishing node it will get the path and the length
            path = []                                                           #this is the shortest path's list
            path_node = current_node                                            #path_node is used to add to path. The first node in the path is the final node
            while path_node.parent_node is not None:                            #parent_node of the start node is None, so this checks if the start node has been reached
                path.append(path_node.name)                                     #this appends the path_node to the path
                path_node = path_node.parent_node                               #path_node now parent node of the previous path node to
            path.reverse()                                                      #reverse path for user experience (otherwise the path output starts at finishing node)
            length = get_edge_length(start_name, path[0])                       #this gets the length of the starting node and the first node in the path
            for i in range(0, len(path) - 1):                                   #this loops for i between 0 and the last index of path
                length = length + get_edge_length(path[i], path[i + 1])         #sum the lengths of all the edges in the path
            return path, length                                                 #return the path (reversed version) and the total length of the path
        if current_node not in list_permanent_nodes:                            #check if the current_node is a permanent node
            list_permanent_nodes.append(current_node)                           #if current_node is not permanent, then make it permanent (put in the permanent list)

            for neighbour in get_neighbours(current_node.name):                 #for every neighbour in the list of neighbours of current node (created in this line)
                if neighbour in node_checker.get_names():                       #check if the neighbour is in the container
                    temp_node = node_checker.get_node(neighbour)
                    if (get_edge_length(neighbour, temp_node.parent_node.name) + get_lower_bound(neighbour)) < (get_edge_length(neighbour, current_node.name) + get_lower_bound(neighbour)):
                        continue
                    else:
                        node_checker.container.remove(temp_node)
                        node_checker.add(Node(neighbour, current_node, get_lower_bound(neighbour)))
                    continue
                for node in list_permanent_nodes:                               #for every node in the list of permanent nodes
                    if neighbour == node.name:                                  #it checks if the neighbour is in the list of permanent nodes
                        break
                else:                                                           #else append the neighbour node to the container list
                    node_checker.add(Node(neighbour, current_node, get_lower_bound(neighbour)))
        frontier = []
        for node in node_checker.container:
            frontier.append(node)
            

    return [False], 'Finishing node is not connected to starting node.'         #in case the algorithm cannot find the finishing node (it is not connected to start), it returns an error

#graph input -------------------------------------------------------------------------------------------------------------------------------------------------------------

#define the lists for the nodes and edges
list_nodes = [('1', 0.0), ('2', 0.0), ('3', 0.0), ('4', 0.0), ('5', 0.0), ('6', 0.0), ('7', 0.0)]     #consists of tuples (nodes) with (name_node, lower_bound)
list_edges = [('1', '2', 4.0), ('1', '3', 7.0), ('2', '3', 2.0), ('2', '4', 5.0), ('3', '4', 1.0), ('3', '5', 5.0), ('4', '5', 3.0), ('4', '6', 1.0), ('6', '7', 8.0), ('5', '7', 3.0)]     #consists of tuples (edges) with (name_first_node, name_second_node, length_edge)
start_name = '2'
finish_name = '7'
list_names_nodes = ['1', '2', '3', '4', '5', '6', '7']

print('This program performs A-star algorithm on an inserted network. Think of a network of nodes, with a lower bound, and edges and press enter to start the algorithm.')
# print('First define the number of nodes and edges.')

# #make the user define the number of nodes
# while True:
#     try:                                                                        #make sure the user cannot input anything other than int
#         number_nodes = int(input('Input the number of nodes:\n'))
#         if number_nodes < 2:                                                    #make sure the user cannot input less than 2 nodes (that would be a very sad graph)
#             print('The number of nodes must be larger than one.')
#             continue
#     except:
#         print('Invalid input. Try again.')
#         continue
#     break

# #calculate maximum number of edges
# edges_max = int((number_nodes * (number_nodes - 1)) / 2)

# #make user input the number of edges and check if this number is within limits
# while True:
#     try:                                                                       #make sure the user cannot input anything other than int
#         number_edges = int(input('Enter number of edges:\n'))
#         if number_edges < 1:                                                   #make sure the number of edges cannot be less than 1 (again, a very sad graph)
#             print('The number of edges must be larger than zero. Try again.')
#             continue
#         if number_edges > edges_max:                                           #make sure the number of edges cannot be higher than the max (a too enthusiastic graph)
#             print('The number of edges is too large for the number of nodes. Try again.')
#             continue
#     except:
#         print('Invalid input. Try again.')
#         continue
#     break

# #make the user input the names of the nodes
# list_names_nodes = []   #define the list with the names of all nodes
# inodes = 0              #variable to iterate for inputting the number of nodes
# print('\nNow input the names of the nodes.')
# while inodes < number_nodes:
#     name_node = input('Enter the name of a node:\n')
#     while name_node in list_names_nodes:                        #while the node is in the list, it would mean that the node already exists. Ask for another name.
#         name_node = input('This node already exists. Try again:\n')
#     while True:
#         try:                                                    #make sure the lower bound can only be an float
#             lower_bound = float(input('Input the lower bound of this node:\n'))
#         except:
#             print('Invalid input. Try again.')
#             continue
#         break
#     list_names_nodes.append(name_node)                          #append the name of the node and the node tuple to the respective lists
#     list_nodes.append((name_node, lower_bound))
#     inodes = inodes + 1

# #make the user define the edges and check if they are not entered twice and if the nodes in the edge exist
# print('\nNow input the edges.')
# iedges = 1                      #variable to iterate to insert all the nodes
# list_edges_no_length = []       #list used to check if an edge has already been inserted

# while iedges <= number_edges:
#     first_node = input('Insert first node of an edge:\n')
#     while first_node not in list_names_nodes:                               #make sure the node exists
#         first_node = input('This node does not exist. Try again:\n')
#     second_node = input('Insert second node of this edge:\n')
#     while second_node not in list_names_nodes or second_node == first_node:                              #make sure the node exists and that it is not the same as the first node
#         second_node = input('This node does not exist or is the same as the first node. Try again:\n')
#     while (first_node, second_node) in list_edges_no_length or (second_node, first_node) in list_edges_no_length:       #make sure the inputted edge does not exist
#         print('This edge already exists. Try again.')
#         first_node = input('Insert first node of this edge:\n') 
#         while first_node not in list_names_nodes:                               #make sure the node exists
#             first_node = input('This node does not exist. Try again:\n')
#         second_node = input('Insert second node of this edge:\n')
#         while second_node not in list_names_nodes:                              #make sure the node exists
#             second_node = input('This node does not exist. Try again:\n')
#     list_edges_no_length.append((first_node, second_node))

#     while True:
#         try:                                                                #make sure the length can only be an float
#             length = float(input('Insert length of this edge:\n'))
#         except:
#             print('Invalid input. Try again.')
#             continue
#         break
#     list_edges.append((first_node, second_node, length))                    #append the edge tothe list of edges
#     iedges = iedges + 1

# #make the user input the starting node
# start_name = input('\nInput the name of the starting node:\n')
# while start_name not in list_names_nodes:                       #while start node is not in the list names nodes the node does not exist, make the user try again.
#     start_name = input('This node does not exist. Try again:\n')

# #make the user input the finishing node
# finish_name = input('Input the name of the finishing node:\n')
# while finish_name not in list_names_nodes:                      #while finish node is not in the list names nodes the node does not exist, make the user try again.
#     finish_name = input('This node does not exist. Try again:\n')

# #ask the user if the inputs are correct
# print('\nThis is the inputted graph:')
# print('The inputted nodes are (the name of the node with its respective lower bound):')
# str_nodes = ''                                              #make a string to print the nodes
# for node in list_nodes:
#     str_nodes = str_nodes + str(node) + ', '
# str_nodes2 = str_nodes[:(len(str_nodes) - 2)]
# print(str_nodes2)
# print('The inputted edges are (first and second node and respective length):')
# str_edges = ''                                              #make a string to print the edges
# for edge in list_edges:
#     str_edges = str_edges + str(edge) + ', '
# str_edges2 = str_edges[:(len(str_edges) - 2)]
# print(str_edges2)
# print('The name of the starting node is: ', start_name)
# print('The name of the finishing node is: ', finish_name)
input('Press enter to continue.')

#A* algorithm ------------------------------------------------------------------------------------------------------------------------------------------------------------

path, total_length = find_path(start_name, finish_name)     #get the shortest path
print('\nShortest path:\n')                                   #print the output vertically
print(start_name)
for name in path:
    print('V')
    print(name)
print('\nWith total length:', total_length)                 #print the length of the path


#ask the user if it wants to run again with other starting and finishing nodes
#make the user input the starting node
while True:
    input('If you want to run again with other starting and finishing nodes, press enter.')
    start_name = input('\nInput the name of the starting node:\n')

    while start_name not in list_names_nodes:                       #while start node is not in the list names nodes the node does not exist, make the user try again.
        start_name = input('This node does not exist. Try again:\n')

    #make the user input the finishing node
    finish_name = input('Input the name of the finishing node:\n')
    while finish_name not in list_names_nodes:                      #while finish node is not in the list names nodes the node does not exist, make the user try again.
        finish_name = input('This node does not exist. Try again:\n')

    print('This is the name of the new starting node:', start_name)
    print('This is the name of the new finishing node:', finish_name)
    input('Press enter to continue.')
    
    path, total_length = find_path(start_name, finish_name)     #get the shortest path
    print('\nShortest path:\n')                                   #print the output vertically
    print(start_name)
    for name in path:
        print('V')
        print(name)
    print('\nWith total length:', total_length)                 #print the length of the path
