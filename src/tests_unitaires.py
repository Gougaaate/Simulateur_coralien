# Module de tests unitaires des 4 classes créées
# @author : Adam GG

import unittest
from rochers import Rocher, creation_rochers
from organismes import Organisme, Corail, Plancton, creation_plancton, creation_corail
from random import uniform,randint


with open("parametres.txt","r") as parametres:   # les paramètres sont stockés dans le fichier parametres.txt
    L=parametres.readlines()
    M=[]
    for i in L:
        j=i.split(' ')
        M.append(j)

nb_rochers = int(M[3][0])           # nombre de rochers générés dans l'aquarium
r_larve = float(M[5][0])            # rayon des larves
nb_plancton_init = int(M[6][0])     # quantité initiale de plancton
r_plancton = float(M[8][0])         # rayon du plancton
dimx = int(M[9][0])                 # longueur de l'aquarium
dimy = int(M[10][0])                # largeur de l'aquarium
r_min = float(M[11][0])             # rayon minimal des rochers
r_max = float(M[12][0])             # rayon maximal des rochers
dific_app = int(M[16][0])           # coefficient qui caractérise la difficulté d'apparition des larves
dific_ponte = int(M[15][0])         # coefficient qui caractérise la dificulté des coraux à pondre des larves
capa = int(M[14][0])                # capacité de nourriture des larves (quantité servant de référence)
vitesse_l = float(M[1][0])          # Vitesse maximale des larves
vitesse_p = float(M[0][0])          # Vitesse maximale du plancton
endurance = int(M[18][0])           # coefficent qui modélise la capacité des coraux à se déplacer longtemps sans manger



class TestRocher(unittest.TestCase):                                        # Classe test de Rocher

    def test_constructeur(self):
        """Test du constructeur de la classe Rocher
        """
        rocher = Rocher(uniform(0,20),uniform(0,20),uniform(0.1,6))         # Test de l'instanciation
        self.assertEqual(rocher.pos, rocher._pos)
        self.assertEqual((rocher.x,rocher.y),rocher._pos)

    def test_creation_rocher(self):
        """Test du bon fonctionnement des variables d'instance
        """
        rocher = Rocher(3,4,2)
        self.assertEqual(rocher.pos, (3,4))
        self.assertEqual(rocher.r,2)

class TestOrganisme(unittest.TestCase):                                              # Classe test de Organisme

    def test_constructeur(self):
        """Test du décorateur de la superclasse Organisme
        """
        organisme = Organisme(uniform(0,20),uniform(0,20))
        self.assertEqual((organisme.x,organisme.y),(organisme.x,organisme.y))         # Test des décorateurs et de la bonne instanciation
        self.assertEqual(organisme.pos,(organisme.x,organisme.y))

    def test_creation_organisme(self):
        """Test du bon fonctionnement des variables d'instance
        """
        organisme = Organisme(8,9)
        self.assertEqual((8,9),organisme.pos)                                        # La posiiton est bien celle souhaitée


class TestCorail(unittest.TestCase):                                                  # Classe test de Corail

    def test_constructeur(self):
        """Test du constructeur de la classe Corail
        """
        corail = Corail(2,3,4)
        self.assertEqual(corail.r,4)                                                    # Vérification de la bonne instanciaton
        self.assertEqual(corail.x,2)
        self.assertEqual(corail.y,3)
        self.assertEqual(corail.capa,20)
        self.assertEqual(corail.age,0)
        self.assertTrue(corail.sante in [i for i in range(corail.capa//2,corail.capa+1)])
        self.assertEqual(corail.color,(0,110,190))

    def test_car(self):
        """Test de bon fonctionnement de la méthode 'car'
        """
        corail = Corail(uniform(0,20),uniform(0,20),uniform(0,20),randint(0,4))
        self.assertEqual('C',corail.car())                                          # Bonne lettre correspondante

    def test_vieillir(self):
        """Test du vieillissement des coraux
        """
        corail = Corail(uniform(0,dimx),uniform(0,dimy),r_larve,randint(0,3))
        a = corail.age
        corail.vieillir()
        self.assertEqual(corail.age, a + 1 )                                         # Vérification que l'âge augmente bien de 1


    def test_bouger(self):
        """Test du mouvement des coraux
        """
        R = creation_rochers(randint(1, 5), dimx, dimy, r_max, r_min)
        C = creation_corail(randint(10, 100), dimx, dimy, r_larve, R, capa)
        L=[]                                                                   # Liste contenant les coraux après mouvement
        listeSante = []                                                        # Liste contenant les points de santé de tous les coraux avant mouvement
        listeSante2 = []                                                       # Liste contenant les points de santé de tous les coraux après mouvement

        for i in C:
            listeSante.append(i.sante)
            i.bouger(R, C, vitesse_l, 0)
            L.append(i)
            listeSante2.append(i.sante)

        for j in range(len(C)):
            self.assertTrue(abs(C[j].x - L[j].x) < vitesse_l and abs(C[j].y - L[j].y) < vitesse_l)       # Vérification que les coordonnées après déplacement soient dans le bon intervalle


        for k in range(len(listeSante)):
            self.assertEqual(listeSante[k],listeSante2[k]+1)                    # Si l'endurance est à 0, les larves perdent de la santé à chaque déplacement

    def test_mourir(self):
        """Test de la mort des coraux et du changement en calcaire
        """
        R = creation_rochers(randint(1, 5), dimx, dimy, r_max, r_min)
        C = creation_corail(randint(10, 100), dimx, dimy, r_larve, R, capa)
        k = len(R)
        for i in C:
            i.age=2                                            # Donne un âge différent de 0 aux coraux pour qu'ils puissent devenir du calcaire en mourant
        x = C[0].x
        y = C[0].y
        r = C[0].r
        self.assertIn(C[0], C)                                             # Test 'témoin' pour le test suivant
        C[0].mourir(R,C,7)                                                 # pH = 7 : on est sûr qu'ils deviennent du calcaire
        self.assertNotIn(Corail(x,y,r,age=2), C)                           # Vérifie que les coraux morts disparaissent de la liste des coraux
        self.assertEqual(k+1,len(R))                                       # Nouveau rocher ajouté

    def test_grossir(self):
        """Test du grossissement des coraux
        """
        corail = Corail(uniform(0,10),uniform(0,10),uniform(0,10),age=randint(1,3))
        corail.sante=corail.capa
        r=corail.r
        corail.grossir()
        self.assertEqual(r*1.4,corail.r)                                   # Vérifie que le rayon augmente du bon coefficient

    def test_pondre(self):
        """Test de la ponte
        """
        R =[]
        C = creation_corail(1, dimx, dimy, r_larve, R, capa)
        longueur = len(C)
        for k in C:                                                     # Vérifie les conditions pour que les coraux puissent pondre
            k.age = 3
        C[0].pondre(C,r_larve,(101,101,101),R,0,0)
        self.assertEqual(len(C), 2)                          # Vérifie qu'il y a bien un corail de plus
        self.assertEqual(C[-1].color,(101,101,101))                     # Et que sa couleur est la bonne

class TestPlancton(unittest.TestCase):                                  # Classe test de Plancton

    def test_car(self):
        """Test de la méthode 'car' de la classe Plancton
        """
        p = Plancton (uniform(0,10),uniform(0,10))
        self.assertEqual(p.car(),'P')                                   # La lettre est bien la bonne


    def test_bouger(self):
        """Test du mouvement du plancton
        """
        R = creation_rochers(nb_rochers, 10, 10, 2, 0)
        P = creation_plancton(nb_plancton_init, 10, 10, R)
        L = []                                                          # Liste contenant les planctons initiaux
        for i in P:
            L.append(i)
            i.bouger(R, vitesse_p)

        for j in range(len(P)):
            self.assertTrue(abs(P[j].x - L[j].x) < vitesse_l and abs(P[j].y - L[j].y) < vitesse_l)  # Vérification que les coordonnées après déplacement soient dans le bon intervalle


if __name__ == '__main__':
    unittest.main()