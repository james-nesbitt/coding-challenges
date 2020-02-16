
"""
    This is the solution to the problem:

    If given a set of graph edges representing airport connections, discover all
    possible routes from every starting point(leaf) to end destination points(leaf)

    The solution does some early processing, turning the edge list into a map
    of airports to destinations lists, and a list of head leafs, and tail leafs.
    Then we iterate across all starts, and detect which leafs .

    This came out of an interview with Hootsuite
"""

def build_graph(stops):
    """ convert a list of stops to a dict graph """
    nodes = {}
    for stop in all_stops:
        if stop[0] not in nodes:
            nodes[stop[0]] = []
        if stop[1] not in nodes:
            nodes[stop[1]] = []
        nodes[stop[0]].append(stop[1])

    return nodes


def head_and_tail(graph):
    """ return a list of head nodes and a list of leaf nodes for a graph """
    head_nodes = []
    tail_nodes = []
    for start, start_edges in graph.items():
        # detect leaf nodes
        if len(start_edges) == 0:
            tail_nodes.append(start)

        # detect head nodes
        for end, end_edges in graph.items():
            if start != end and start in end_edges:
                break;
        else:
            head_nodes.append(start)

    return head_nodes, tail_nodes


def get_route(nodes, start, stop):
    """ determine the ordered path from a start to a stop """
    route = [start]

    if start in nodes:
        for end in nodes[start]:
            if end == stop:
                route.append(end)
                break;
            else:
                route.extend(get_route(nodes, end, stop))

    if route[len(route)-1] != stop:
        return []

    return route

# +++  MAIN +++

"""
    Edges are represented as a list of airport pair (tuples)
"""
all_stops = [
    ('YYZ','CHO'),
    ('NYJ', 'YVR'),
    ('CHO','NYJ'),
    ('NYC', 'STL')
]

graph = build_graph(all_stops)
starting, stopping = head_and_tail(graph)
for start in starting:
    for stop in stopping:
        route = get_route(graph, start, stop)
        print('{} -> {}'.format(start, stop))
        if len(route):
            print(route)
        else:
            print('no route found')
