import random
import json
from generate_initial_layout import *
import networkx as nx

width = 800;
height = 600;

def clean_vertex(vertices, i):
    #print(vertices, i)
    u = vertices[i].strip()
    u = u[1:-1]
    return u

def add_node(u, nodes_to_id, id_to_nodes, cur_id):
    if u not in nodes_to_id:
        nodes_to_id[u] = cur_id
        id_to_nodes[cur_id] = u
        return cur_id + 1
    return cur_id

max_label_size = 16
def create_alphanum_dict(G):
 org_to_alphanum = dict()
 alphanum_to_org = dict()
 for n in G.nodes():
  n_short = n[:max_label_size]
  if n_short in alphanum_to_org.keys():
   n_short = n[:(max_label_size-2)]
   cnt = 2
   while True:
    cnt_str = str(cnt)
    if len(cnt_str)==1:
     cnt_str = '0'+cnt_str
    n_alphanum = n_short+cnt_str
    if not n_alphanum in alphanum_to_org.keys():
     org_to_alphanum[n] = n_alphanum
     alphanum_to_org[n_alphanum] = n
     break
    cnt = cnt + 1
  else:
   org_to_alphanum[n] = n_short
   alphanum_to_org[n_short] = n
 return org_to_alphanum, alphanum_to_org

def convert_nodes_to_alphanum(G, org_to_alphanum, alphanum_to_org):
 G2 = nx.Graph()
 for e in G.edges():
  u, v = e
  u2, v2 = org_to_alphanum[u], org_to_alphanum[v]
  G2.add_edge(u2, v2)
 return G2

def read_txt_file(fname):
  G = nx.Graph()
  f = open(fname, "r")
  while True:
    l = f.readline()
    if len(l)==0:
      break
    '''
    l = l.split('"')
    u = l[1]
    v = l[3]
    '''
    l = l.split(' -- ')
    u = l[0][1:len(l[0])-1]
    v = l[1][1:len(l[1])-2]
    G.add_edge(u, v)
  f.close()
  return G

def convert_txt_to_json(fname, fid, random_layout):
    if random_layout:
        f = open(fname, "r")
        content = f.read()
        lines = content.split("\n")
        edges = []
        for line in lines:
            if len(line)!=0:
                #print(line)
                vertices = line.split("--")
                u = clean_vertex(vertices, 0)
                v = clean_vertex(vertices, 1)
                #print(u, v)
                edges.append([u, v])
        print("Number of edges:", len(edges))
        nodes_to_id = dict()
        id_to_nodes = dict()
        cur_id = 0
        for edge in edges:
            u, v = edge
            cur_id = add_node(u, nodes_to_id, id_to_nodes, cur_id)
            cur_id = add_node(v, nodes_to_id, id_to_nodes, cur_id)
        print(len(nodes_to_id), len(id_to_nodes))

        G = nx.Graph()
        for edge in edges:
            u, v = edge
            G.add_edge(u, v)

        '''nodes = []
        for u in G.nodes():
            nodes.append({"id": nodes_to_id[u], 
            "x": random.random()*width, 
            "y": random.random()*height,
            "label": u})'''
        nodes = {}
        for u in G.nodes():
            nodes[nodes_to_id[u]] = {"id": nodes_to_id[u], 
            "x": random.random()*width, 
            "y": random.random()*height,
            "label": u}
        links = []
        for edge in edges:
            u, v = edge
            links.append({"source": nodes_to_id[u], "target": nodes_to_id[v]})
        #print(links)
        node_file = "nodes_{0}.js".format(fid)
        with open(node_file, "w") as file:
            json_string = json.dumps(nodes)
            file.write("nodes = " + json_string)
        
        link_file = "links_{0}.js".format(fid)
        with open(link_file, "w") as file:
            json_string = json.dumps(links)
            file.write("links_org = " + json_string)
        f.close()
    else:
        file_name = ["dataset/Graph_0.txt", "dataset/Graph_1.txt", "dataset/Graph_2.txt", "dataset/Graph_3.txt", "dataset/Graph_4.txt"]
        file_name = file_name[:int(fid)+1]

        for fname in file_name:
            G = read_txt_file(fname)
        print(G)
        org_to_alphanum, alphanum_to_org = create_alphanum_dict(G)
        #print("org_to_alphanum = ", org_to_alphanum)
        #print("alphanum_to_org = ", alphanum_to_org)
        G = convert_nodes_to_alphanum(G, org_to_alphanum, alphanum_to_org)

        number_lab_to_name_lab = dict()
        name_lab_to_number_lab = dict()
        edges_to_index = dict()
        edge_distance = dict()

        for u in G.nodes():
            if not u in name_lab_to_number_lab.keys():
                name_lab_to_number_lab[u] = len(name_lab_to_number_lab.keys())
                number_lab_to_name_lab[len(name_lab_to_number_lab.keys())-1] = u

        label_to_index = dict()
        index_to_label = dict()
        bfs_edges = []
        #center = "1149"
        center = nx.center(G)[0]
        #center = "algorithmic game"
        for e in nx.bfs_edges(G, center):
            #for e in nx.dfs_edges(G, center):
            u, v = e
            bfs_edges.append((u, v))
        bfs_edges2 = []
        for e in bfs_edges:
            u, v = e
            #u, v = number_lab_to_name_lab[u], number_lab_to_name_lab[v]
            u = u[:max_label_size]
            v = v[:max_label_size]
            bfs_edges2.append([u, v])
        bfs_edges = bfs_edges2
        G2 = nx.Graph()
        for e in G.edges():
            u, v = e
            #u, v = number_lab_to_name_lab[u], number_lab_to_name_lab[v]
            u = u[:max_label_size]
            v = v[:max_label_size]
            G2.add_edge(u, v)
        G = G2
        for i in range(len(bfs_edges)):
            edges_to_index[(bfs_edges[i][0], bfs_edges[i][1])] = i
        edge_list = []
        #for e in nx.bfs_edges(G, "machine learning"):
        for e in bfs_edges:
            #print(e)
            u, v = e
            if not u in label_to_index.keys():
                label_to_index[u] = len(label_to_index.keys())
                index_to_label[len(label_to_index.keys())-1] = u
            if not v in label_to_index.keys():
                label_to_index[v] = len(label_to_index.keys())
                index_to_label[len(label_to_index.keys())-1] = v
            edge_list.append([label_to_index[u], label_to_index[v]])
        #print(label_to_index)
        #print(index_to_label)
        #print("my_edges = ", bfs_edges)
        #print("label_to_id = ", label_to_index)
        #print("id_to_label = ", index_to_label)

        l = int(fid)
        #cur_dis = 50
        cur_dis = 200
        #cur_dis = 100
        #cur_dis = 169.30
        #cur_dis = 300
        #cur_dis = 600
        #cur_dis = 1200
        #cur_dis = 2000
        #cur_dis = 4000
        #cur_dis = 8000
        #init_dis = 100
        #init_fac = 2
        cur_lev = 0
        nodes_to_levels = {}
        nodes_to_files = {}


        while l>=0:
            G = read_txt_file(file_name[l])

            G = convert_nodes_to_alphanum(G, org_to_alphanum, alphanum_to_org)

            bfs_edges = []
            center = nx.center(G)[0]
            #center = "algorithmic game"
            for e in nx.bfs_edges(G, center):
                u, v = e
                bfs_edges.append((u, v))
            bfs_edges2 = []
            for e in bfs_edges:
                u, v = e
                #u, v = number_lab_to_name_lab[u], number_lab_to_name_lab[v]
                u = u[:max_label_size]
                v = v[:max_label_size]
                bfs_edges2.append([u, v])
            bfs_edges = bfs_edges2

            for i in range(len(bfs_edges)):
                e = bfs_edges[i]
                if (e[0], e[1]) in edges_to_index.keys():
                    edge_index = edges_to_index[(e[0], e[1])]
                elif (e[1], e[0]) in edges_to_index.keys():
                    edge_index = edges_to_index[(e[1], e[0])]
                else:
                    print("Edge not found!")
                    quit()
                nodes_to_levels[e[0]] = cur_lev
                nodes_to_levels[e[1]] = cur_lev
                edge_distance[edge_index] = cur_dis
                nodes_to_files[e[0]] = file_name[l]
                nodes_to_files[e[1]] = file_name[l]

            l -= 1
            #cur_dis += 50
            cur_dis += 25
            cur_lev -= 1

        min_lev = nodes_to_levels[list(nodes_to_levels.keys())[0]]
        for k in nodes_to_levels.keys():
            if min_lev>nodes_to_levels[k]:
                min_lev = nodes_to_levels[k]
        max_lev = - min_lev + 1
        for k in nodes_to_levels.keys():
            nodes_to_levels[k] = nodes_to_levels[k] + max_lev

        #print("edge_distance = ", edge_distance)
        #print("nodes_to_levels = ", nodes_to_levels)
        #print("nodes_to_files = ", nodes_to_files)

        G = G2
        cnt = {}
        #src = list(G.nodes())[0]
        src = center
        #print("src", src)
        numberOfNodes(G, src, -1, cnt)
        #print("cnt", cnt)
        #exit()
        crd_x = {}
        crd_y = {}
        crd_x[label_to_index[src]] = 500
        crd_y[label_to_index[src]] = 500
        label_to_id = {u:u for u in G.nodes()}
        get_drawing_coordinates(G, src, -1, 0, 2*math.pi, crd_x[label_to_index[src]], crd_y[label_to_index[src]], crd_x, crd_y, cnt, label_to_index, edges_to_index, edge_distance)
        #print("crd_x = ", crd_x)
        #print("crd_y = ", crd_y)

        nodes = []
        #for u in nodes_to_id:
        for u in G.nodes():
            nodes.append({})
        for u in G.nodes():
            #nodes.append({"id": nodes_to_id[u], "x": random.random()*width, "y": random.random()*height})
            nodes[label_to_index[u]] = \
                {"id": label_to_index[u], "x": crd_x[label_to_index[u]], "y": crd_y[label_to_index[u]], "label": u}
        links = []
        #for edge in edges:
        for edge in G.edges():
            u, v = edge
            #links.append({"source": nodes_to_id[u], "target": nodes_to_id[v]})
            links.append({"source": label_to_index[u], "target": label_to_index[v]})
        #print(links)
        node_file = "nodes_{0}.js".format(fid)
        with open(node_file, "w") as file:
            json_string = json.dumps(nodes)
            file.write("nodes = " + json_string)
        
        link_file = "links_{0}.js".format(fid)
        with open(link_file, "w") as file:
            json_string = json.dumps(links)
            #file.write("links = " + json_string)
            file.write("links_org = " + json_string)
        

def main():
    #fname = input("Enter file name:")
    fid = input("Enter file number:")
    fname = "dataset/Graph_{0}.txt".format(fid)
    random_layout = False
    #random_layout = True
    convert_txt_to_json(fname, fid, random_layout)

main()