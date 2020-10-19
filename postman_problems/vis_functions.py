import osmnx as ox
import networkx as nx
import pandas as pd
from collections import Counter

# calc shortest path between optional nodes and add to graph
def create_req_and_opt_graph(req_comp_g_contracted, complete_g, circuit_rpp):
    final_graph = req_comp_g_contracted.copy()
    unexpanded_edges = 0
    unexpanded_edges_list = []
    granular_connector_edges = 0
    granular_connector_edges_list = []
    granular_req_edges = 0
    granular_req_edges_list = []
    optional_edges = 0
    optional_edges_list = []
    for e in circuit_rpp:
        if [e[0], e[1]] not in unexpanded_edges_list:
            unexpanded_edges+=1
            unexpanded_edges_list+=[[e[0], e[1]]]
        # add granular optional edges to final_graph
        path = e[3]['path']
        for pair in list(zip(path[:-1], path[1:])):
            if (req_comp_g_contracted.has_edge(pair[0], pair[1])):
                edge = req_comp_g_contracted[pair[0]][pair[1]][0]
                if edge.get('granular_type') == 'connector':
                    if [pair[0], pair[1]] not in granular_connector_edges_list:
                        granular_connector_edges+=1
                        granular_connector_edges_list+=[[pair[0], pair[1]]]
                elif 1 in req_comp_g_contracted[pair[0]][pair[1]] and req_comp_g_contracted[pair[0]][pair[1]][1].get('granular'):
                    if [pair[0], pair[1]] not in granular_connector_edges_list:
                        granular_connector_edges+=1
                        granular_connector_edges_list+=[[pair[0], pair[1]]]
                else:
                    if [pair[0], pair[1]] not in granular_req_edges_list:
                        final_graph[pair[0]][pair[1]][0]['granular_type'] = 'req street'
                        granular_req_edges+=1
                        granular_req_edges_list+=[[pair[0], pair[1]]]
            else:
                final_graph.add_edge(pair[0], pair[1], granular=True, granular_type='optional')
                if [pair[0], pair[1]] not in optional_edges_list:
                    optional_edges+=1
                    optional_edges_list+=[[pair[0], pair[1]]]
        for n in path:
            final_graph.add_node(n, y=complete_g.nodes[n]['y'], x=complete_g.nodes[n]['x'])
    print('Edges in Circuit')
    print('\tTotal Unexpanded Edges: {}'.format(unexpanded_edges))
    print('\tTotal Edges (All Contracted Edges Granularized): {}'.format(granular_connector_edges+granular_req_edges+optional_edges))
    print('\t\tGranular Connector Edges: {}'.format(granular_connector_edges))
    print('\t\tGranular Required Edges: {}'.format(granular_req_edges))
    print('\t\tGranular Optional Edges: {}'.format(optional_edges))
    return final_graph

def create_number_of_passes_graph(circuit_rpp, complete_g):
    ## Create graph directly from rpp_circuit and original graph w y/x (complete_g)
    color_seq = [None, 'black', 'magenta', 'orange', 'yellow']
    grppviz = nx.Graph()
    edges_cnt = Counter([tuple(sorted([e[0], e[1]])) for e in circuit_rpp])
    for e in circuit_rpp:
        for n1, n2 in zip(e[3]['path'][:-1], e[3]['path'][1:]):
            if grppviz.has_edge(n1, n2):
                grppviz[n1][n2]['linewidth'] += 2
                grppviz[n1][n2]['cnt'] += 1
            else:                
                grppviz.add_edge(n1, n2, linewidth=2.5)
                grppviz[n1][n2]['cnt'] = 1
                grppviz.add_node(n1, y=complete_g.nodes[n1]['y'], x=complete_g.nodes[n1]['x'])
                grppviz.add_node(n2, y=complete_g.nodes[n2]['y'], x=complete_g.nodes[n2]['x']) 
    for e in grppviz.edges(data=True):
        e[2]['color_cnt'] = color_seq[e[2]['cnt']]
    return grppviz, edges_cnt
    
"""
# calc shortest path between optional nodes and add to req_comp_g_uncontracted graph
def create_final_graph(req_comp_g_contracted, complete_g, circuit_rpp):
    final_graph = req_comp_g_contracted.copy()
    edges_1 = len(list(final_graph.edges()))
    print('Contracted edge # = {}.'.format(edges_1))
    for e in [e for e in circuit_rpp if e[3]['required']==0]:
        # add granular optional edges to final_graph
        path = e[3]['path']
        for pair in list(zip(path[:-1], path[1:])):
            if final_graph.has_edge(pair[0], pair[1]):
                #print('Pair present: {}'.format(pair))
                continue
            final_graph.add_edge(pair[0], pair[1], granular='True', granular_type='optional')
            #print('Pair added: {}'.format(pair))
        # add granular nodes from optional edge paths to final_graph
        for n in path:
            final_graph.add_node(n, y=complete_g.nodes[n]['y'], x=complete_g.nodes[n]['x'])
    edges_2 = len(list(final_graph.edges()))
    print('Final edge # = {}.'.format(edges_2))
    print('Edges added = {}.'.format(edges_2-edges_1))
    return final_graph
"""
