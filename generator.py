import numpy as np
class random():
    def make_random_adjacency(self, nbVertex):
        """
        :para nbVertex
        :type nt
        :return matrice d'adjacency
        :rtype array
        En savant le nombre de neoud, cette fontion est pour former une matrice d'adjacence random, car on ne peut pas lister tous les types manuellement
        """
        matrix = np.zeros((nbVertex, nbVertex))
        for i in range(nbVertex):
            for j in range(nbVertex):
                matrix[i][j] = np.random.randint(0,2) # ou round(np.random.rand())
            matrix[0][0]=1
        return matrix
    def make_random_edgelist(self,nbVertex=4):
        """
        :para nbVertex
        :type int
        :return edgelist
        :rtype array
        En savant le nombre de noeud, cette fonction peut former une liste d'arrete aleatoirement.
        """
        maxNbEdges = (nbVertex**2)-nbVertex

        edgelist = list()
        for vertex in range(nbVertex):
            tab = np.arange(nbVertex)
            tab = np.delete(tab, vertex) # delete the current vertex
            nbEdges = np.random.randint(0, maxNbEdges) # generate number of edges of this vertex
            for _  in range(nbEdges):
                n = np.random.choice(tab)
                edgelist.append((vertex, n))
                indx, = np.where(tab==n)
                tab = np.delete(tab, indx) # update tab
        return edgelist

    def make_random_adjacency_undirected(self, nbVertex):
        """
        :para nbVertex
        :type int
        :return matrice d'adjacency
        :rtype array
        cette fonction permet de former une matrice d'ajancence des graphes sans direction(undirected)
        Dans ce cas undirected, la matrice d'adjacence doit etre symetrique
        """
        matrix = np.zeros((nbVertex, nbVertex))
        while True:
            for i in range(nbVertex):
                for j in range(1+i, nbVertex):            
                    matrix[i][j] = matrix[j][i] = np.random.randint(0,2)#Matrice symétriqueque 
            if 0 not in np.sum(matrix, axis=1):#Graphe sans noeud isolée filter les matrices avec noeud isolée
                break
        return matrix
    
