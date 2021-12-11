#############################################################
#                                                           #
#            PROJET IA PUISSANCE 4 - ESILV A3 S6            #
#                                                           #
#            Groupe TD F : Lightning Strike                 #
#                                                           #
#                          Morgane                          #
#                          Alban                            #
#                          Stephane                         #
#                          Dimitri                          #
#                                                           #
#############################################################
#pour calculer le temps d'exécution de notre IA
import time

#Fonction pour afficher la grille
def Affichage(grille):
    string = " __1__ __2__ __3__ __4__ __5__ __6__ __7__ __8__ __9__ __10____11___12__\n"
    for i in range(len(grille)):
        string=string+"|_"
        for j in range(len(grille[0])):
            if (j != 0):
                string = string + "_|_"

            if grille[i][j]==0:
                string=string+ "___"
            elif grille[i][j]==1:
                string=string+ " X "
            elif grille[i][j]==-1:
                string=string+ " O "
        string = string + "_|"
        string=string+"\n"
    print(string)

#Fonction pour cloner une grille
def Clone(grille):
    clone=[[0] * 12 for i in range(6)]
    for i in range(len(grille)):
        for j in range (len(grille[0])):
            clone[i][j]=grille[i][j]
    return clone

#True si il y a une place de libre dans la colonne j, False sinon
def PositionCorrecte(grille, j):
    positionLibre=False
    for i in range(len(grille)):
        if grille[i][j]==0:
            positionLibre=True
            break
    return positionLibre

#Change le joueur actuel
def ChangementJoueur(joueur):
    if joueur == 1:
        return -1
    elif joueur == -1:
        return 1

#Liste les actions possibles (les colonnes qui contiennent au moins une place vide)
def Actions(grille):
    listeActions=[]
    for j in range (len(grille[0])):
        for i in range (len(grille)):
            if grille[i][j]==0:
                #s'il y a un 0 dans une des lignes de la colonne, cela signifie que la colonne j est une position acceptable
                listeActions.append(j)
                break
    return listeActions

#Applique l'action dans un clone du grille (pour ne pas modifier notre grille actuelle)
def Result(grille, j, joueur): #joueur=1 : X    joueur=-1 : O
    grille2=Clone(grille) #on clone la grille pour ne pas modifier la grille actuelle.
    i=5
    while(grille2[i][j]!=0):
        i=i-1
    if joueur==1:
        grille2[i][j]=1
    else: #joueur==-1
        grille2[i][j]=-1
    return grille2

# Attribue une valeur à notre état (utilité)
def Utility(grille):
    utility = JoueurGagnant(grille)*1000
    return utility

# Teste si notre grille est terminale : si un joueur a gagné ou si tous les pions ont été joués (42)
def TerminalTest(grille):
    partieFinie = False

    # Test grille terminée
    grilleTerminee = False
    nombreDe0=0
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] == 0:
                nombreDe0+=1
    #s'il y a 30 0 dans la grille, cela signifie que les 42 pions ont été joués donc la grille est "remplie"
    if (nombreDe0==30):
        grilleTerminee=True

    # Test partie finie : si la grille est "remplie" ou qu'un joueur a gagné
    if (grilleTerminee or JoueurGagnant(grille)==1 or JoueurGagnant(grille)==-1):
        partieFinie = True

    return partieFinie

#retourne 0 si personne ne gagne, 1 si c'est le joueur 1, -1 si c'est le joueur -1
def JoueurGagnant(grille):
    #On regarde s'il y a 4 pions d'un même joueur alignés sur des lignes
    for i in range(6):
        for j in range(9):
            if grille[i][j] != 0 and all(grille[i][j + k] == grille[i][j] for k in range(4)):
                return grille[i][j]
    #On regarde s'il y a 4 pions d'un même joueur alignés sur des colonnes
    for i in range(3):
        for j in range(12):
            if grille[i][j] != 0 and all(grille[i + k][j] == grille[i][j] for k in range(4)):
                return grille[i][j]
    #On regarde s'il y a 4 pions d'un même joueur alignés sur des diagonales "droites" (=les diagonales qui partent du coin en bas à gauche jusqu'au coin en haut à droite)
    for i in range(3):
        for j in range(9):
            if grille[i][j] != 0 and all(grille[i + k][j + k] == grille[i][j] for k in range(4)):
                return grille[i][j]
    #On regarde s'il y a 4 pions d'un même joueur alignés sur des diagonales "gauches" (=les diagonales qui partent du coin en haut à gauche jusqu'au coin en bas à droite)
    for i in range(3):
        for j in range(3, 12):
            if grille[i][j] != 0 and all(grille[i + k][j - k] == grille[i][j] for k in range(4)):
                return grille[i][j]
    #Si on n'a trouvé aucun alignement de 4 mêmes pions
    return 0



infini=10000

# MINIMAX
def maxValue(grille, n, depth, joueur):
    v = -infini
    if TerminalTest(grille):
        return Utility(grille)
    elif (n > depth):
        return 0
    else:
        for a in Actions(grille):
            v = max(v, minValue(Result(grille, a, joueur), n + 1, depth, ChangementJoueur(joueur)))
        return v

def minValue(grille, n, depth, joueur):
    v = infini
    if TerminalTest(grille):
        return Utility(grille)
    elif (n > depth):
        return 0
    else:
        nb = 0
        for a in Actions(grille):
            nb = nb + 1
            v = min(v, maxValue(Result(grille, a, joueur), n + 1, depth, ChangementJoueur(joueur)))
        return v

def minimaxDecision(grille, depth, joueur):
    ListeActions, ListeUtility = [], []
    for a in Actions(grille):
        ListeActions.append(a)
        if TerminalTest(Result(grille, a, joueur)):
            ListeUtility.append(Utility(Result(grille, a, joueur)))
        else:
            ListeUtility.append(minValue(Result(grille, a, joueur), 1, depth, ChangementJoueur(joueur)))
    print(ListeUtility)
    for i in range(len(ListeActions)):
        if ListeUtility[i] == max(ListeUtility):
            #on retourne l'action dont l'utility est maximale
            return ListeActions[i]



# ALPHA-BETA
def maxValue2(grille, alpha, beta, n, depth, joueur):
    v = -infini
    #si la grille est terminale
    if TerminalTest(grille):
        #à la profondeur 1 = le joueur gagne au prochain coup
        if n==1:
            v = Utility(grille)*3
        #à la profondeur 2 = le joueur gagne dans 2 coups
        elif n==2:
            v= Utility(grille)*2
        else:
            v=Utility(grille)

    #si la profondeur max est dépassée
    elif (n > depth):
        return 0
    else:
        for a in Actions(grille):
            v = max(v, minValue2(Result(grille, a, joueur), alpha, beta, n + 1, depth, ChangementJoueur(joueur)))
            if v >= beta:
                break
            alpha = max(alpha, v)

    return v

def minValue2(grille, alpha, beta, n, depth, joueur):
    v = infini
    # si la grille est terminale
    if TerminalTest(grille):
        # à la profondeur 1 = le joueur gagne au prochain coup
        if n==1:
            v = Utility(grille)*3
        # à la profondeur 2 = le joueur gagne dans 2 coups
        elif n==2:
            v= Utility(grille)*2
        else:
            v=Utility(grille)
    elif (n > depth):
        return 0
    else:
        for a in Actions(grille):
            v = min(v, maxValue2(Result(grille, a, joueur), alpha, beta, n + 1, depth, ChangementJoueur(joueur)))
            if v <= alpha:
                break
            beta = min(beta, v)
    return v

def AlphaBetaDecision(grille, depth, joueur):
    ListeActions, ListeUtility = [], []
    for a in Actions(grille):
        ListeActions.append(a)
        mini=minValue2(Result(grille, a, joueur), -infini, infini, 1, depth, ChangementJoueur(joueur))
        #si la profondeur max est atteinte
        if mini==0:
            #on remplace le 0 : on appelle notre heuristique ScoreQuadruplet
            mini=ScoreQuadruplet(grille,a,joueur)
        ListeUtility.append(mini)
    #print(ListeUtility)

    for i in range(len(ListeActions)):
        if ListeUtility[i] == max(ListeUtility):
            # on retourne l'action dont l'utility est maximale
            return ListeActions[i]


# NOTRE HEURISTIQUE
#Pour une action donnée, renvoie le score de la case. Cette fonction n'est appelée que lorsque la profondeur max est atteinte
def ScoreQuadruplet(grille, action, j1):
    j=action
    #on cherche le i correspondant à notre action
    for k in range (5,-1,-1):
        if (grille[k][j]==0):
            i=k
            break
    j2=ChangementJoueur(j1)

    '''Un quadruplet est un alignement possible de 4 pions'''
    #score des quadruplets situés sur des lignes
    scoreQuadrupletLigne=0
    #score des quadruplets situés sur des colonnes
    scoreQuadrupletColonne=0
    #score des quadruplets situés sur des diagonales "gauches"
    scoreQuadrupletDiagGauche=0
    #score des quadruplets situés sur des diagonales "droites"
    scoreQuadrupletDiagDroite=0
    #nombre total de quadruplets
    scoreNombreQuadruplet=0

    #intervalle à regarder pour les quadruplets "lignes"
    m,n=ScoreQuadrupletLigne(grille,j)
    for a in range (m,n):
        # si on ne rencontre pas de pions adverses dans le quadruplet
        if all(grille[i][a+k]!=j2 for k in range(0,4)):
            #on parcourt les 4 cases du quadruplet
            for k in range(4):
                #on ajoute la valeur de la case regardée à notre score
                scoreQuadrupletLigne+=grille[i][a+k]
            #le score est d'autant plus élevé qu'on rencontre des pions identiques dans le quadruplet
            scoreQuadrupletLigne=abs(scoreQuadrupletLigne*2)

            #on incrémente le nombre de quadruplets
            scoreNombreQuadruplet+=1

    # intervalle à regarder pour les quadruplets "colonnes"
    o,p=ScoreQuadrupletColonne(grille,i)
    for a in range(o,p):
        #si on ne rencontre pas de pions adverses dans le quadruplet
        if all(grille[a+k][j]!=j2 for k in range(0,4)):
            # on parcourt les 4 cases du quadruplet
            for k in range(4):
                # on ajoute la valeur de la case regardée à notre score
                scoreQuadrupletColonne+=grille[a+k][j]
            # le score est d'autant plus élevé qu'on rencontre des pions identiques dans le quadruplet
            scoreQuadrupletColonne=abs(scoreQuadrupletColonne*2)

            # on incrémente le nombre de quadruplets
            scoreNombreQuadruplet+=1

    # intervalle à regarder pour les quadruplets "diagonales gauches"
    q,r=ScoreQuadrupletDiagGauche(grille,i,j)
    for k in range(q,r):
        # si on ne rencontre pas de pions adverses dans le quadruplet
        if all(grille[i-k+l][j-k+l]!=j2 for l in range(4)):
            # on parcourt les 4 cases du quadruplet
            for l in range(4):
                # on ajoute la valeur de la case regardée à notre score
                scoreQuadrupletDiagGauche+=grille[i-k+l][j-k+l]
            # le score est d'autant plus élevé qu'on rencontre des pions identiques dans le quadruplet
            scoreQuadrupletDiagGauche=abs(scoreQuadrupletDiagGauche*2)

            # on incrémente le nombre de quadruplets
            scoreNombreQuadruplet+=1

    # intervalle à regarder pour les quadruplets "diagonales droites"
    s,t=ScoreQuadrupletDiagDroite(grille,i,j)
    for k in range(s,t):
        # si on ne rencontre pas de pions adverses dans le quadruplet
        if all(grille[i+k-l][j-k+l]!=j2 for l in range(4)):
            # on parcourt les 4 cases du quadruplet
            for l in range(4):
                # on ajoute la valeur de la case regardée à notre score
                scoreQuadrupletDiagDroite+=grille[i+k-l][j-k+l]
            # le score est d'autant plus élevé qu'on rencontre des pions identiques dans le quadruplet
            scoreQuadrupletDiagDroite=abs(scoreQuadrupletDiagDroite*2)

            # on incrémente le nombre de quadruplets
            scoreNombreQuadruplet+=1

    #on somme tous les scores calculés précédemment
    sommeScoreQuadruplet=scoreQuadrupletLigne+scoreQuadrupletColonne+scoreQuadrupletDiagGauche+scoreQuadrupletDiagDroite+scoreNombreQuadruplet
    return sommeScoreQuadruplet

#renvoie l'intervalle à parcourir pour le score des quadruplets "lignes"
def ScoreQuadrupletLigne(grille,j):
    #selon la colonne de la case dont on veut calculer le score, l'intervalle à étudier diffère
    intervalle=(0,0)
    if j==0:
        intervalle=(j,j+1)
    elif j==1:
        intervalle=(j-1,j+1)
    elif j==2:
        intervalle=(j-2,j+1)
    elif j==11:
        intervalle=(j-3,j-2)
    elif j==10:
        intervalle=(j-3, j-1)
    elif j==9:
        intervalle=(j-3,j)
    else:
        intervalle=(j-3,j+1)
    return intervalle

#renvoie l'intervalle à parcourir pour le score des quadruplets "colonnes"
def ScoreQuadrupletColonne(grille,i):
    # selon la ligne de la case dont on veut calculer le score, l'intervalle à étudier diffère
    intervalle=(0,0)
    if i==0:
        intervalle=(i,i+1)
    elif i==1:
        intervalle=(i-1,i+1)
    elif i==2:
        intervalle=(i-2,i+1)
    elif i==3:
        intervalle=(i-3,i)
    elif i==4:
        intervalle=(i-3, i-1)
    elif i==5:
        intervalle=(i-3,i-2)
    return intervalle

#renvoie l'intervalle à parcourir pour le score des quadruplets "diagonales gauches"
def ScoreQuadrupletDiagGauche(grille,i,j):
    # selon la colonne et la ligne de la case dont on veut calculer le score, l'intervalle à étudier diffère
    q,r=0,0
    if (i==0 and j<9):
        q,r=0,1
    elif (i==1 and j<10):
        if (j==0):
            q,r=0,1
        elif (j==9):
            q,r=1,2
        else:
            q,r=0,2
    elif (i==2 and j<11):
        if (j==0):
            q,r=0,1
        elif (j==1):
            q, r = 0, 2
        elif (j==10):
            q,r=2,3
        elif (j==9):
            q,r=1,3
        else:
            q,r=0,3

    elif(i==3 and j>0):
        if (j==1):
            q,r=1,2
        elif (j==2):
            q,r=1,3
        elif (j==10):
            q,r=2,4
        elif (j==11):
            q,r=3,4
        else:
            q,r=1,4

    elif (i==4 and j>1):
        if j==2:
            q,r=2,3
        elif j==11:
            q,r=3,4
        else:
            q,r=2,4

    elif (i==5 and j>2):
        q,r=3,4

    return q,r

#renvoie l'intervalle à parcourir pour le score des quadruplets "diagonales droites"
def ScoreQuadrupletDiagDroite(grille,i,j):
    # selon la colonne et la ligne de la case dont on veut calculer le score, l'intervalle à étudier diffère
    q,r=0,0
    if (i==0 and j>2):
        q,r=3,4
    elif (i==1 and j>1):
        if (j==2):
            q,r=2,3
        elif(j==11):
            q,r=3,4
        else:
            q,r=2,4

    elif (i==2 and j>0):
        if (j==1):
            q,r=1,2
        elif (j==2):
            q,r = 1,3
        elif (j==10):
            q,r=2,4
        elif (j==11):
            q,r=3,4
        else:
            q,r=1,4

    elif(i==3 and j<11):
        if (j==0):
            q,r=0,1
        elif (j==1):
            q,r=0,2
        elif (j==9):
            q,r=1,3
        elif (j==10):
            q,r=2,3
        else:
            q,r=0,3

    elif (i==4 and j<10):
        if j==0:
            q,r=0,1
        elif j==9:
            q,r=1,2
        else:
            q,r=0,2

    elif (i==5 and j<9):
        q,r=0,1

    return q,r



#Nous utilisons la fonction AlphaBetaDecision pour faire jouer notre IA
def Jeu_Du_Puissance4(profondeur):
    joueurQuiCommence = eval(input("Qui veut commencer ? Taper 1 si c'est l'IA qui commence (joueurIA: X) ou taper 2 si c'est l'adversaire qui commence (joueurAdv: O) :"))
    while (joueurQuiCommence!=1 and joueurQuiCommence!=2):
        joueurQuiCommence = eval(input("Veuillez taper 1 si l'IA commence ou 2 si c'est l'adversaire qui commence !\n"))
    #notre IA aura toujours les pions "X"
    joueurIA= 1
    #le joueur adverse aura toujours les pions "O"
    joueurAdv = -1
    joueurActuel=""

    if (joueurQuiCommence==1):
        joueur=joueurIA #Notre IA commence
        joueurActuel="joueurIA (X)"
    else:
        joueur=joueurAdv
        joueurActuel="joueurAdv (O)"

    grille=[[0] * 12 for i in range(6)]
    Affichage(grille)
    #tant que la partie n'est pas finie (=tous les pions n'ont pas été joués et il n'y a pas encore de gagnant)
    while (TerminalTest(grille) == False):
        print("C'est au tour du joueur : ", joueurActuel)
        if (joueur == joueurAdv):
            j=eval(input("A quelle position voulez-vous jouer ?"))
            #on décrémente j car la 1ère colonne correspond à j=0 dans nos calculs et non pas à j=1
            j = j - 1
            while (PositionCorrecte(grille,j) == False):
                j = eval(input("La position choisie est déjà occupée, veuillez donner une autre position :\n"))
                j=j-1
            # on cherche la première ligne disponible pour jouer dans la colonne j (respecter la gravité)
            for k in range(5, -1, -1):
                if (grille[k][j] == 0):
                    i = k
                    break
            #on n'applique pas notre fonction Result car celle-ci applique l'action dans un clone de la grille actuelle
            grille[i][j] = joueur
            #on change de joueur
            joueur = joueurIA
            joueurActuel="joueurIA (X)"
            Affichage(grille)
        else:  # joueur==joueurIA
            depth = profondeur
            t1 = time.time()
            j=AlphaBetaDecision(grille,depth,joueur)
            t2 = time.time()
            # on cherche la première ligne disponible pour jouer dans la colonne j (respecter la gravité)
            for k in range(5, -1, -1):
                if (grille[k][j] == 0):
                    i = k
                    break
            #on n'applique pas notre fonction Result car celle-ci applique l'action dans un clone de la grille actuelle
            grille[i][j] = joueur
            # on change de joueur
            joueur = joueurAdv
            joueurActuel="joueurAdv (O)"
            Affichage(grille)
            print("L'IA a joué en position ",j+1," en ",round((t2 - t1),3)," sec")
    print("La partie est finie !")
    if JoueurGagnant(grille)==1:
        print("L'IA a gagné (joueurIA : X)!")
    elif JoueurGagnant(grille)==-1:
        print("Le joueur adverse a gagné (joueurAdv : O)!")
    else:
        print("Personne n'a gagné")

#on utilise une profondeur max égale à 4 pour notre AlphaBetaDecision : cela correspond au paramètre "depth"
profondeur=4
#Lancement du jeu
Jeu_Du_Puissance4(profondeur)
