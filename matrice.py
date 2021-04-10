import numpy as np
from sknetwork.utils import edgelist2adjacency, edgelist2biadjacency
class matrice():
    def matrice_adjacence(self, edge_list):
        """
        :para edge list 
        :type list
        :return matrice d'adjacence
        :rtype array (sparse matrix)
        cette fonction permet d'utiliser edge_list pour transmettre a une matrice d'adjacence.
        """
        adjacency = edgelist2adjacency(edge_list)
        myarray=adjacency.A
        n = myarray.shape[0]
        matrice = np.zeros((n,n))
        for i in range (myarray.shape[0]):
                matrice[i]=list(map(int, myarray[i]))
        return matrice
    def matrice_degree(self, mat_adjacency):
        """
        :para une matrice d'adjacence 
        :type array (sparse matrix)
        :return une matrice degree 
        :rtype array (sparse matrix)
        cette fonction permet d'utiliser la matrice d'adjacence pour trouver la matrice degree
        la matrice des degrés est une matrice qui contient des informations sur le degré de chaque sommet d'un graphe.
        """
        n = mat_adjacency.shape[0]
        degree = np.zeros((n, n))
        temps = mat_adjacency.sum(axis = 1)
        for i in range(n):
            degree[i][i] = temps[i]
        return degree
        
    def matrice_laplacien(self, mat_adjacency):
        """
        :para une matrice d'adjacence sparse
        :type array (sparse matrix)
        :return une matrice laplacienne
        :rtype array (sparse matrix)
        cette fonction permet d'utiliser la matrice d'adjacence pour trouver la matrice laplacienne
        la matrice laplacienne a une interprétation algébrique ce qui rend son analyse spectrale fructueuse.
        """
        degree = self.matrice_degree(mat_adjacency)
        res = degree - mat_adjacency
        return res
