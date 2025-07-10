from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.graph = None
        self.idmap = {}

    def get_years(self):
        return DAO.get_years()

    def get_shapes(self, anno):
        return DAO.get_shapes(anno)

    def buildGraph(self, anno, forma):
        self.graph = nx.DiGraph()
        allNodes = DAO.getAllNodes(anno, forma)
        for n in allNodes:
            self.idmap[n.id] = n
        self.graph.add_nodes_from(allNodes)
        allArchi = DAO.getAllArchi(anno, forma)
        self.graph.add_edges_from(allArchi)


    def getGraphDetails(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()