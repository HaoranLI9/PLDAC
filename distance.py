import numpy as np
from matrice import matrice
from scipy.interpolate import interp1d
class distance_simple():
    """
    ne considerant pas les differents noeuds
    """
    def distance_2graph(self, matrice_G1, matrice_G2):
        """
        :para 2 matrices de 2 graphe,
        :type array (sparse matrix)
        :return distance entre 2 graphes 
        :rtype double
        en utilisant valeurs propres des matrices, cette fonction retourne la distance.
        Les matrices, elles sont souvent matrice d'adjacence. elles peuvent etre les matrices laplaciennes ou autres
        """
        VP1 = np.linalg.eig(matrice_G1)[0]#les valeurs propres de premier graph
        VP1 = np.array(sorted(VP1,reverse=True))#ordonner les valeurs propres
        VP2 = np.linalg.eig(matrice_G2)[0]#les valeurs propres de deuxieme graph
        VP2 = np.array(sorted(VP2,reverse=True))#ordonner 
        res = np.linalg.norm(VP1 - VP2)**2#sum des carrés de différence de VP
        return res
    def distance_2graph_combine(self, adjacency_G1, adjacency_G2, alpha = 0.5):
        """
        :para 2 matrices d'adjancence, alpha qui define poids des adjacence et laplacien
        :type array (sparse matrix), alpha : double
        :return distance combine avec adjancence et laplacien
        :rtype double
        ici, on utilise αJSSA(G1, G2 ) + (1 − α)JSSL(G1, G2 ) (14) with α ∈ [0, 1], a weighting factor
        JSSA distance d'adjacence, JSSL distance de laplacien
        JSS : Joint Spectral Similarity voir l'article de reference
        alpha: weighting factor α controls the significance of each distance 
        and allows more importance to be given to the A-spectral distance or to the L-spectral distance.
        """
        JSSA = self.distance_2graph(adjacency_G1, adjacency_G2)
        JSSL = self.distance_2graph(matrice().matrice_laplacien(adjacency_G1), matrice().matrice_laplacien(adjacency_G2))
        JSS  = alpha * JSSA + (1 - alpha) * JSSL
        return JSS

class distance_interpole():
    """
    on considere le cas ou il y a different noeuds
    """
    def distance_2graphe_diff_vertex_simple(self, adjacency_G1, adjacency_G2, alpha = 0.5):
        """
        :para 2 matrices d'adjancence, alpha a weighting factor
        :type array, alpha : double
        :return distance entre 
        :rtype double
        cette fonction est une méthode simple pour calculer la distance entre 2 graphes avec noeuds differents
        comme le papier de Bay-Ahmed, on compte seulment les K premiers valeurs propres. k = min(N1, N2)
        """
        N1, N2 = adjacency_G1.shape[0], adjacency_G2.shape[0]
        k = min(N1, N2)
        VP1 = np.linalg.eig(adjacency_G1)[0]#les valeurs propres de premier graph
        VP1 = np.array(sorted(VP1,reverse=True))[:k]#ordonner les valeurs propres
        VP2 = np.linalg.eig(adjacency_G2)[0]#les valeurs propres de deuxieme graph
        VP2 = np.array(sorted(VP2,reverse=True))[:k]#ordonner 
        JSSA = np.linalg.norm(VP1 - VP2)**2#sum des carrés de différence de VP

        VP3 = np.linalg.eig(matrice().matrice_laplacien(adjacency_G1))[0]#les valeurs propres de premier graph
        VP3 = np.array(sorted(VP3,reverse=True))[:k]#ordonner les valeurs propres
        VP4 = np.linalg.eig(matrice().matrice_laplacien(adjacency_G2))[0]#les valeurs propres de deuxieme graph
        VP4 = np.array(sorted(VP4,reverse=True))[:k]#ordonner 
        JSSL = np.linalg.norm(VP3 - VP4)**2#sum des carrés de différence de VP

        JSS = alpha * JSSA + (1 - alpha) * JSSL
        return JSS

    def interpolateEigenvalues(self, array1, array2, kind='linear'):
        """
        Fonction permettant d'interpoler l'ensemble des valeurs propre le plus petit pour avoir autant de valeur que dans le plus grand ensemble
        :param array1: tableau de valeurs propre
        :type array1: Numpy 1D array
        :param array2: tableau de valeurs propre
        :type array2: Numpy array
        :return: array1, array2
        :rtype: Numpy 1d Array, Numpy 1d Array
        """
        minArray = array1
        maxArray = array2
        if array1.shape[0]>array2.shape[0]:
            minArray = array2
            maxArray = array1
        elif array1.shape[0]==array2.shape[0]:
            return array1, array2

        common_x = np.linspace(0, 1, len(maxArray))
        x = np.linspace(0, 1, len(minArray))
        f = interp1d(x, np.array(sorted(minArray,reverse=True)), kind=kind)
        min1dArrayInterpolated = f(common_x)
        
        # ordered arrays
        min1dArrayInterpolated = np.array(sorted(min1dArrayInterpolated,reverse=True))
        maxArray = np.array(sorted(maxArray,reverse=True))

        if array1.shape[0]>array2.shape[0]:
            return maxArray, min1dArrayInterpolated
        return min1dArrayInterpolated, maxArray

    def linInterpolateEigenvalues(self, array1, array2):
        """
        Fonction permettant d'interpoler l'ensemble des valeurs propre le plus petit pour avoir autant de valeur que dans le plus grand ensemble
        
        :param array1: tableau de valeurs propre
        :type array1: Numpy 1D array
        :param array2: tableau de valeurs propre
        :type array2: Numpy array
        :return: array1, array2
        :rtype: Numpy 1d Array, Numpy 1d Array
        """
        minArray = array1
        maxArray = array2
        if array1.shape[0]>array2.shape[0]:
            minArray = array2
            maxArray = array1
        elif array1.shape[0]==array2.shape[0]:
            return array1, array2
        
        x = np.linspace(0,1, len(maxArray))
        xp = np.linspace(0,1, len(minArray))
        fp = np.array(sorted(minArray,reverse=True))
        min1dArrayInterpolated = np.interp(x, xp, fp)
        
        # ordered arrays
        min1dArrayInterpolated = np.array(sorted(min1dArrayInterpolated,reverse=True))
        maxArray = np.array(sorted(maxArray,reverse=True))

        if array1.shape[0]>array2.shape[0]:
            return maxArray, min1dArrayInterpolated
        return min1dArrayInterpolated, maxArray

    def distance_2graphe_diff_vertex_v2(self, adjacency_G1, adjacency_G2, alpha = 0.5):
        """
        Version 2 de la méthode de calcul de distance avec 2 graphes n'ayant pas le même nombre de noeuds.
        Cette version 2 consiste à interpoller l'ensemble des valeurs propres le plus petit pour avoir deux ensembles de mêmes taille à comparer
        :para 2 matrices d'adjancence, alpha a weighting factor
        :type array, alpha : double
        :return distance entre 
        :rtype double
        cette fonction est une méthode simple pour calculer la distance entre 2 graphes avec noeuds differents
        comme le papier de Bay-Ahmed, on compte seulment les K premiers valeurs propres. k = min(N1, N2)
        """
        VP1 = np.linalg.eig(adjacency_G1)[0]#les valeurs propres de premier graph
        VP2 = np.linalg.eig(adjacency_G2)[0]#les valeurs propres de deuxieme graph
        VP1, VP2 = self.interpolateEigenvalues(VP1, VP2, kind='nearest')
        #VP1 = np.array(sorted(VP1,reverse=True))# ordonner les valeurs propres
        #VP2 = np.array(sorted(VP2,reverse=True)) 

        JSSA = np.linalg.norm(VP1 - VP2)**2#sum des carrés de différence de VP

        VP3 = np.linalg.eig(matrice().matrice_laplacien(adjacency_G1))[0]#les valeurs propres de premier graph
        VP4 = np.linalg.eig(matrice().matrice_laplacien(adjacency_G2))[0]#les valeurs propres de deuxieme graph
        VP3, VP4 = self.interpolateEigenvalues(VP3, VP4, kind='nearest')
        #VP3 = np.array(sorted(VP3,reverse=True))# ordonner les valeurs propres
        #VP4 = np.array(sorted(VP4,reverse=True)) 

        JSSL = np.linalg.norm(VP3 - VP4)**2#sum des carrés de différence de VP

        JSS = alpha * JSSA + (1 - alpha) * JSSL
        return JSS