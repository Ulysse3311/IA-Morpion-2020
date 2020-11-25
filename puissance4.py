import numpy as np
import time


class Puiss4:

    def __init__(self):
        self.largeur = 12
        self.hauteur = 6
        self.grille = np.zeros((self.hauteur, self.largeur), dtype=np.int)
        self.nbCoups = 0
        self.gagnant = 0  # 0 si pas de gagnant sinon numéro du gagnant
        self.terminal = False

        self.CRED = '\33[31m'
        self.CEND = '\033[0m'
        self.CBLUE = '\33[34m'

    def actions(self):  # retourne la liste des actions possibles
        actionsPossibles = []
        for i in range(self.largeur):
            if self.grille[0, i] == 0:
                actionsPossibles.append(i)
        return actionsPossibles

    def copy(self):
        cop = Puiss4()
        cop.grille = np.copy(self.grille)
        cop.nbCoups = self.nbCoups
        cop.gagnant = self.gagnant
        cop.terminal = self.terminal
        return cop

    def printGrille(self):
        for i in range(self.hauteur):
            print("|", end=' ')
            for j in range(self.largeur):
                if (self.grille[i][j] == 1):
                    print(self.CBLUE + '0' + self.CEND, end=' ')
                elif self.grille[i][j] == 2:
                    print(self.CRED + '0' + self.CEND, end=' ')
                else:
                    print(" ", end=' ')
                print("|", end=' ')
            print()
        print("|", end=' ')
        for i in range(self.largeur):
            print("_", end=" ")
            print("|", end=' ')
        print()
        print("|", end=' ')
        for i in range(1, self.largeur + 1):
            print(i % 10, end=" ")
            print("|", end=' ')
        print()

    def terminalTest(self, dernierJoueur=False):
        if self.terminal:  # si on a déjà fait le test
            return True
        if self.nbCoups < 7:  # impossible d'aligner 4 pions en 6 coups
            return False

        self.gagnant = self.gagneTest(1)

        if self.gagnant:
            self.terminal = True
            return True
        else:
            if self.nbCoups > 41:  # nb maximal de coups autorisé
                self.terminal = True
                return True
            else:
                return False

    def resultat(self, action, joueur):
        p = True
        for i in range(self.hauteur - 1, -1, -1):
            if self.grille[i, action] == 0:
                self.grille[i, action] = joueur
                p = False
                self.nbCoups += 1
                break
        if p:
            print("Erreur, impossible de placer ce pion")

    def gagneTest(self, joueur):  # joueur = à 1 ou 2
        # horizontale
        for i in range(self.hauteur):
            for j in range(self.largeur - 3):
                if (self.grille[i][j] == self.grille[i][j + 1] == self.grille[i][j + 2] == self.grille[i][j + 3]):
                    if (self.grille[i][j] == 1):
                        return 1
                    if (self.grille[i][j] == 2):
                        return 2

        # verticale
        for i in range(self.hauteur - 3):
            for j in range(self.largeur):
                if (self.grille[i][j] == self.grille[i + 1][j] == self.grille[i + 2][j] == self.grille[i + 3][j]):
                    if (self.grille[i][j] == 1):
                        return 1
                    if (self.grille[i][j] == 2):
                        return 2

        # diago desc
        for i in range(self.hauteur - 3):
            for j in range(self.largeur - 3):
                if (self.grille[i][j] == self.grille[i + 1][j + 1] == self.grille[i + 2][j + 2] == self.grille[i + 3][
                    j + 3]):
                    if (self.grille[i][j] == 1):
                        return 1
                    if (self.grille[i][j] == 2):
                        return 2

        # diago mont
        for i in range(3, self.hauteur):
            for j in range(self.largeur - 3):
                if (self.grille[i][j] == self.grille[i - 1][j + 1] == self.grille[i - 2][j + 2] == self.grille[i - 3][
                    j + 3]):
                    if (self.grille[i][j] == 1):
                        return 1
                    if (self.grille[i][j] == 2):
                        return 2

        return 0

    def alignes(self, joueur, nb):  # retourne le nombre de possibilité d'alligner nb pion avec cette position
        ali = 0

        # test lignes
        for i in range(self.hauteur):
            cpt = 0
            for j in range(self.largeur):

                if (self.grille[i, j] != joueur):
                    cpt = -1

                cpt += 1

                if (cpt == nb):
                    ali += 1

        # test colonnes
        for j in range(self.largeur):

            cpt = 0

            for i in range(self.hauteur):

                if (self.grille[i, j] != joueur):
                    cpt = -1

                cpt += 1

                if (cpt == nb):
                    ali += 1

        # test diagonales

        # test diagonale gauche-droite descendante
        for j in range(self.largeur - 3):
            cpt = 0
            i = 0

            while i != self.hauteur and j != self.largeur:
                if (self.grille[i, j] != joueur):
                    cpt = -1

                cpt += 1

                if (cpt == nb):
                    ali += 1

                i += 1
                j += 1

        for i in range(1, self.hauteur - 3):

            cpt = 0
            j = 0
            while i != self.hauteur and j != self.largeur:
                if (self.grille[i, j] != joueur):
                    cpt = -1

                cpt += 1

                if (cpt == nb):
                    ali += 1

                i += 1
                j += 1

        # test diagonale gauche-droite montante
        for j in range(self.largeur - 3):

            cpt = 0
            i = self.hauteur - 1

            while i != -1 and j != self.largeur:
                if (self.grille[i, j] != joueur):
                    cpt = -1

                cpt += 1

                if (cpt == nb):
                    ali += 1

                i -= 1
                j += 1

        for i in range(self.hauteur - 2, 2, -1):

            cpt = 0
            j = 0
            while i != -1 and j != self.largeur:
                if (self.grille[i, j] != joueur):
                    cpt = -1

                cpt += 1

                if (cpt == nb):
                    ali += 1

                i -= 1
                j += 1
        return ali

        def terminalTest(self, dernierJoueur=False):
            if self.terminal:  # si on a déjà fait le test
                return True
            if self.nbCoups <= 6:  # impossible d'aligner 4 pions en 6 coups
                return False
            if self.nbCoups > 48:  # nb maximal de coups autorisé
                self.terminal = True
                return True
            gagne1 = self.gagneTest(1)
            gagne2 = self.gagneTest(2)
            if gagne1:
                self.gagnant = 1
            if gagne2:
                self.gagnant = 2
            if gagne1 or gagne1:
                self.terminal = True
                return True

    def aligne3(self, joueur):  # joueur = à 1 ou 2

        ali = 0
        # test lignes
        for i in range(self.hauteur):
            x = 0
            y = 0
            cpt = 0
            for j in range(self.largeur):

                if (self.grille[i, j] != joueur):
                    cpt = -1

                    if (self.grille[i, j] == 0):
                        x = i
                        y = j
                cpt += 1

                if (cpt == 3 and j < self.largeur - 1 and self.grille[i, j + 1] == 0):
                    ali += 1
                if (cpt == 3 and self.grille[x, y + 1] == joueur and self.grille[x, y + 2] == joueur and self.grille[
                    x, y + 3] == joueur):
                    ali += 1

        # test colonnes
        for j in range(self.largeur):
            x = 0
            y = 0
            cpt = 0

            for i in range(self.hauteur):

                if (self.grille[i, j] != joueur):
                    cpt = -1
                    if (self.grille[i, j] == 0):
                        x = i
                        y = j

                cpt += 1

                if (cpt == 3 and i < self.hauteur - 1 and self.grille[i + 1, j] == 0):
                    ali += 1
                if (cpt == 3 and self.grille[x + 1, y] == joueur and self.grille[x + 2, y] == joueur and self.grille[
                    x + 3, y] == joueur):
                    ali += 1

                    # test diagonales

        # test diagonale gauche-droite descendante
        for j in range(self.largeur - 3):
            x = 0
            y = 0
            cpt = 0
            i = 0

            while i != self.hauteur and j != self.largeur:
                if (self.grille[i, j] != joueur):
                    cpt = -1
                    if (self.grille[i, j] == 0):
                        x = i
                        y = j

                cpt += 1
                if (cpt == 3 and i < self.hauteur - 1 and j < self.largeur - 1 and self.grille[i + 1, j + 1] == 0):
                    ali += 1
                if (cpt == 3):
                    if (self.grille[x + 1, y + 1] == joueur and self.grille[x + 2, y + 2] == joueur and self.grille[
                        x + 3, y + 3] == joueur):
                        ali += 1
                i += 1
                j += 1

        for i in range(1, self.hauteur - 3):
            x = 0
            y = 0
            cpt = 0
            j = 0
            while i != self.hauteur and j != self.largeur:
                if (self.grille[i, j] != joueur):
                    cpt = -1
                    if (self.grille[i, j] == 0):
                        x = i
                        y = j
                cpt += 1

                if (cpt == 3 and i < self.hauteur - 1 and j < self.largeur - 1 and self.grille[i + 1, j + 1] == 0):
                    ali += 1
                if (cpt == 3):
                    if (self.grille[x + 1, y + 1] == joueur and self.grille[x + 2, y + 2] == joueur and self.grille[
                        x + 3, y + 3] == joueur):
                        ali += 1
                i += 1
                j += 1

        # test diagonale gauche-droite montante
        for j in range(self.largeur - 3):
            x = 0
            y = 0
            cpt = 0
            i = self.hauteur - 1

            while i != -1 and j != self.largeur:
                if (self.grille[i, j] != joueur):
                    cpt = -1
                    if (self.grille[i, j] == 0):
                        x = i
                        y = j
                cpt += 1
                if (cpt == 3 and i > 0 and j < self.largeur - 1 and self.grille[i - 1, j + 1] == 0):
                    ali += 1
                if (cpt == 3):
                    if (self.grille[x - 1, y + 1] == joueur and self.grille[x - 2, y + 2] == joueur and self.grille[
                        x - 3, y + 3] == joueur):
                        ali += 1
                i -= 1
                j += 1

        for i in range(self.hauteur - 2, 2, -1):
            x = 0
            y = 0
            cpt = 0
            j = 0
            while i != -1 and j != self.largeur:
                if (self.grille[i, j] != joueur):
                    cpt = -1
                    if (self.grille[i, j] == 0):
                        x = i
                        y = j
                cpt += 1
                if (cpt == 3 and i > 0 and j < self.largeur - 1 and self.grille[i - 1, j + 1] == 0):
                    ali += 1
                if (cpt == 3):
                    if (self.grille[x - 1, y + 1] == joueur and self.grille[x - 2, y + 2] == joueur and self.grille[
                        x - 3, y + 3] == joueur):
                        ali += 1
                i -= 1
                j += 1

        return ali

    def ali(self, joueurIA):
        score = 0
        # horrizontale
        for i in range(self.hauteur):
            for j in range(self.largeur - 3):
                rangee = [self.grille[i, j], self.grille[i, j + 1], self.grille[i, j + 2], self.grille[i, j + 3]]
                score += self.scoreRangee(rangee, joueurIA, score)

        # verticale
        for i in range(self.hauteur - 3):
            for j in range(self.largeur):
                rangee = [self.grille[i, j], self.grille[i + 1, j], self.grille[i + 2, j], self.grille[i + 3, j]]
                score += self.scoreRangee(rangee, joueurIA, score)

        # diagonale descandante
        for i in range(self.hauteur - 3):
            for j in range(self.largeur - 3):
                rangee = [self.grille[i, j], self.grille[i + 1, j + 1], self.grille[i + 2, j + 2],
                          self.grille[i + 3, j + 3]]
                score += self.scoreRangee(rangee, joueurIA, score)

        # diagonale montante
        for i in range(3, self.hauteur):
            for j in range(self.largeur - 3):
                rangee = [self.grille[i][j], self.grille[i - 1][j + 1], self.grille[i - 2][j + 2],
                          self.grille[i - 3][j + 3], ]
                score += self.scoreRangee(rangee, joueurIA, score)
        """
        if score < 10:
            for i in range(self.hauteur - 1, -1, -1):
                for j in range(self.largeur):
                    if self.grille[i, j] == joueurIA:
                        score += abs(self.largeur / 2 - j)
                    if score == 10:
                        break
                if score == 10:
                    break"""

        return score

    def scoreRangee(self, ligne, joueurIA, score):
        adv = 1
        if joueurIA == 1:
            adv = 2
        score = 0
        if ligne.count(joueurIA) == 3 and ligne.count(0) == 1:
            score += 150
        if ligne.count(adv) == 3 and ligne.count(0) == 1:
            score += -100
        if ligne.count(joueurIA) == 2 and ligne.count(0) == 2:
            score += 15
        if ligne.count(adv) == 2 and ligne.count(0) == 2:
            score += -10

        return score

    def utility(self, joueurIA, mode):
        adv = 1
        if joueurIA == 1:
            adv = 2
        val = 0
        if self.gagnant == 0:
            self.gagnant = self.gagneTest(1)

        if self.gagnant != 0:
            if self.gagnant == joueurIA:
                val = 1000 - self.nbCoups
                return val
            else:
                val = -1000 + self.nbCoups
                return val
        # si il n'y a pas de gagnant on retourne le nb de pions alignés suivant les différents modes
        if val == 0 and mode > 0:
            if mode == 5:
                val = self.ali(joueurIA)
            elif mode ==7:
                for j in range(self.largeur):
                    if self.grille[self.hauteur-1, j] == joueurIA:
                        val += -abs(self.largeur / 2 - j)
            elif mode == 1:
                val = self.alignes(joueurIA, 3) - self.alignes(adv, 3)
                if val == 0:
                    val = self.alignes(joueurIA, 2) - self.alignes(adv, 2)
            elif mode == 2:
                val = self.alignes(joueurIA, 3) - self.alignes(adv, 3)
            elif mode == 3:
                val = 10 * self.aligne3(joueurIA) - self.aligne3(adv)
            elif mode == 4:
                val = self.aligne3(joueurIA)
            elif mode == 6:
                val = 10 * self.aligne3(joueurIA)
                if val == 0:
                    val = -10 * self.aligne3(adv)
        return val

    # mode 0 : seulement test victoire
    # mode 1 : test victoire + profondeur 1 et 2
    def tourIA(self, profondeur, joueur, mode,profVar=False):
        vMax = -100000
        ListesActions = self.actions()
        actionMax = ListesActions[0]
        if profVar and self.nbCoups<2:
            profondeur=0
            mode=7

        for action in ListesActions:
            g = self.copy()
            g.resultat(action, joueur)
            v = g.alphaBeta(profondeur, -100000, 10000, False, joueur, mode)
            # g.printGrille()
            # print("AB : ", v, end="\n\n")
            if v > vMax:
                actionMax = action
                vMax = v
        print("L'IA joue en ", actionMax + 1)
        print("Heuristique : ", vMax)
        self.resultat(actionMax, joueur)

    def alphaBeta(grille, profondeur, a, b, maxi, joueurIA, mode):
        adv = 1
        if joueurIA == 1:
            adv = 2
        if profondeur == 0 or grille.terminalTest():
            ut = grille.utility(joueurIA, mode)
            return ut
        else:
            if maxi:
                vMax = -100000
                listeAction = grille.actions()
                for action in listeAction:
                    g = grille.copy()
                    g.resultat(action, joueurIA)
                    vMax = max(vMax, Puiss4.alphaBeta(g, profondeur - 1, a, b, False, joueurIA, mode))
                    a = max(a, vMax)
                    if b <= a:
                        break
                return vMax
            else:
                vMin = 100000
                listeAction = grille.actions()
                for action in listeAction:
                    g = grille.copy()
                    g.resultat(action, adv)
                    vMin = min(vMin, Puiss4.alphaBeta(g, profondeur - 1, a, b, True, joueurIA, mode))
                    b = min(b, vMin)
                    if b <= a:
                        break
                return vMin


def testIAvsIA():
    g = Puiss4()
    g.printGrille()
    t1 = 0
    t2 = 0
    p1 = 2
    print("lets go")
    while (True):
        print("\n\nJ1 : ")
        start_time = time.time()
        g.tourIA(profondeur=2, joueur=1, mode=5, profVar=True)
        tempsEx = (time.time() - start_time)
        print("Temps d execution : %s secondes ---" % tempsEx)
        # print("Pronfondeur : ", p1)
        t1 += tempsEx
        if tempsEx < 1:
            p1 += 1
        g.printGrille()
        if g.terminalTest():
            break

        print("\n\nJ2 : ")
        start_time = time.time()
        g.tourIA(profondeur=4, joueur=2, mode=4,profVar=True)
        tempsEx = (time.time() - start_time)
        t2 += tempsEx
        print("Temps d execution : %s secondes ---" % tempsEx)
        g.printGrille()
        if g.terminalTest():
            break



    print("\nle gagnant est : ", g.gagnant)
    print("temps j1 : ", t1, "s\ntemps j2 : ", t2,"s")
    print("nb coups : ", g.nbCoups)


def multiTestIAvsIA(profMin1, profMax1, profMin2, profMax2, modes1, modes2):
    for p1 in range(profMin1, profMax1 + 1):
        for p2 in range(profMin2, profMax2 + 1):
            for mode1 in modes1:
                for mode2 in modes2:
                    g = Puiss4()
                    t1 = 0
                    t2 = 0
                    while (True):
                        start_time = time.time()
                        g.tourIA(profondeur=p1, joueur=1, mode=mode1)
                        tempsEx = (time.time() - start_time)
                        t1 += tempsEx
                        if g.terminalTest():
                            break

                        start_time = time.time()
                        g.tourIA(profondeur=p2, joueur=2, mode=mode2)
                        tempsEx = (time.time() - start_time)
                        t2 += tempsEx
                        if g.terminalTest():
                            break

                    print("\nProfondeur 1 : ", p1, " ; Profondeur 2 : ", p2, " ; mode 1 : ", mode1, " ; mode 2 : ",
                          mode2, " : ")
                    print("Gagnant : ", g.gagnant, "nb coups : ", g.nbCoups, " ; T1 : ", t1, " ; T2 : ", t2)


def IAvs():
    while (True):
        entree = input("Taper A si l'IA commence sinon autre : ")
        joueurIA = False
        if entree == "A":
            joueurIA = True
        g = Puiss4()
        print("On commence !")
        g.printGrille()
        tpsExe = 0
        while (True):
            if joueurIA:
                start_time = time.time()
                g.tourIA(profondeur=3, joueur=2, mode=5,profVar=True)
                tpsExe += (time.time() - start_time)
                print("Temps d execution : %s secondes ---" % (time.time() - start_time))
            else:
                choix = 0
                while True:
                    try:
                        choix = int(input("entrez votre choix de case"))
                    except ValueError:
                        print("ce n'est pas un chiffre")
                        continue
                    if choix in range(1, 13):
                        break
                    else:
                        print("Entrez une valeur entre 1 et 12")
                g.resultat(choix - 1, 1)

            g.printGrille()
            if g.terminalTest():
                break
            joueurIA = not joueurIA

        print("Le gagnant est : ", g.gagnant, " en ", g.nbCoups, " coups")
        print("temps execution de l'IA : ", tpsExe)

        entree = input("\n tapez R pour rejouer sinon autre : ")
        if entree != "R":
            break

if __name__ == "__main__":
    #testIAvsIA()  # pour faire jouer les versions de l'IA en elle
    # multiTestIAvsIA(1,4,1,4,[1,2,3,4],[1,2,3,4])# test de multiples versions
    IAvs() #pour jouer contre l'IA









