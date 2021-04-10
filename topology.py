import numpy as np
from distance import distance_interpole


class topology():
    def line_topology(self, nbVertex=10):
        """
        :return array of matrix d'adjancence
        """
        res = np.zeros((nbVertex, nbVertex))
        for i in range(nbVertex-1):
            res[i+1, i] = 1
            res[i, i+1] = 1
        return res

    def full_topology(self, nbVertex = 10):
        """
        :return array of matrix d'adjancence
        """
        res = np.ones((nbVertex, nbVertex))
        for i in range(nbVertex):
            res[i,i] = 0
        return res

    def star_topology(self, nbVertex = 10):
        """
        :return array of matrix d'adjancence
        """
        res = np.zeros((nbVertex, nbVertex))
        for i in range(1, nbVertex):
            res[i,0] = 1
            res[0,i] = 1
        return res

    def ring_topology(self, nbVertex = 10):
        """
        :return array of matrix d'adjancence
        """
        res = np.zeros((nbVertex, nbVertex))
        res[0, nbVertex-1] = 1
        res[nbVertex-1, 0] = 1
        for i in range(nbVertex-1):
            res[i+1, i] = 1
            res[i, i+1] = 1
        return res

    def make_dataset(self, n = 10):
        """
        :return une liste de donnees des matrices d'adjacence
        """
        res = []
        for i in range(4,n):
            res.append(self.ring_topology(i))
            res.append(self.line_topology(i))
            res.append(self.full_topology(i))
            res.append(self.star_topology(i))
        return res


    def identifier(self, dataset, matrice_ajacence):
        """
        cette fonction permet de trouver les graphes similaires en savant une matrice d'adjacence
        :return on retourne les 4 ids des primiers similaire graphes
        """
        #res = []
        distance = {}
        for i in range(len(dataset)):
            distance[i] = distance_interpole().distance_2graphe_diff_vertex_v2(dataset[i], matrice_ajacence)#distance_2graphe_diff_vertex_v2
            #distance_2graphe_diff_vertex_simple
        ids = []
        for i in sorted(distance.items(), key = lambda x: x[1])[:4]:
            id, _ = i
            ids.append(id)
        return ids