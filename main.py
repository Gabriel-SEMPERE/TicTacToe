import time
import random
import os

def nettoyer_ecran():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_plateau(plateau):
    nettoyer_ecran()
    print("\n--- TIC TAC TOE ---\n")
    for row in range(3):
        offset = row * 3
        ligne = f" {plateau[offset]} | {plateau[offset+1]} | {plateau[offset+2]} "
        print(ligne)
        if row < 2:
            print("---+---+---")
    print("\n-------------------")

def verifier_victoire(plateau, symbole):
    combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in combos:
        if plateau[a] == plateau[b] == plateau[c] == symbole:
            return True
    return False

def grille_pleine(plateau):
    return " " not in plateau

def ordinateur(board, signe):
    print("\nL'ordinateur réfléchit...")
    time.sleep(1)
    
    adversaire = "X" if signe == "O" else "O"

    combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    # 1. ESSAYER DE GAGNER
    for a, b, c in combos:
        ligne = [board[a], board[b], board[c]]
        if ligne.count(signe) == 2 and ligne.count(" ") == 1:
            return [a, b, c][ligne.index(" ")]

    # 2. BLOQUER LE JOUEUR
    for a, b, c in combos:
        ligne = [board[a], board[b], board[c]]
        if ligne.count(adversaire) == 2 and ligne.count(" ") == 1:
            return [a, b, c][ligne.index(" ")]

    # 3. PRENDRE LE CENTRE
    if board[4] == " ":
        return 4

    # 4. PRENDRE UN COIN
    coins = [0, 2, 6, 8]
    coins_libres = [c for c in coins if board[c] == " "]
    if coins_libres:
        return random.choice(coins_libres)

    # 5. SINON, JOUER AU HASARD
    cases_vides = [i for i, x in enumerate(board) if x == " "]
    if cases_vides:
        return random.choice(cases_vides)
    
    return False

def tour_humain(plateau, joueur_actuel):
    valide = False
    while not valide:
        try:
            coup = int(input(f"\n{joueur_actuel}, choisissez une case (1-9) : "))
            if 1 <= coup <= 9:
                if plateau[coup - 1] == " ":
                    symbole = "X" if joueur_actuel == "Joueur 1" else "O"
                    plateau[coup - 1] = symbole
                    valide = True
                else:
                    print(">> Cette case est déjà occupée !")
            else:
                print(">> Saisissez un nombre entre 1 et 9.")
        except ValueError:
            print(">> Erreur : Veuillez entrer un chiffre.")

if __name__ == "__main__":
    while True:
        plateau = [" " for _ in range(9)]
        running = True
        
        nettoyer_ecran()
        print("1. Un Joueur (vs IA)")
        print("2. Deux Joueurs")
        choix = input("\nVotre choix : ")
        
        mode_ia = (choix == "1")
        adversaire = "Ordinateur" if mode_ia else "Joueur 2"
        joueur_actuel = random.choice(["Joueur 1", adversaire])
        
        print(f"\nLe sort a décidé : c'est {joueur_actuel} qui commence !")
        time.sleep(2)
        
        while running:
            afficher_plateau(plateau)

            if mode_ia and joueur_actuel == "Ordinateur":
                coup_ia = ordinateur(plateau, "O")
                if coup_ia is not False:
                    plateau[coup_ia] = "O"
                else:
                    running = False 
            else:
                tour_humain(plateau, joueur_actuel)

            symbole_actuel = "O" if joueur_actuel == "Ordinateur" or joueur_actuel == "Joueur 2" else "X"
            
            if verifier_victoire(plateau, symbole_actuel):
                afficher_plateau(plateau)
                print(f"\n>>> VICTOIRE ! {joueur_actuel} a gagné ! <<<")
                running = False
            
            elif grille_pleine(plateau):
                afficher_plateau(plateau)
                print("\n>>> Match Nul ! Aucune case disponible. <<<")
                running = False
            
            else:
                if mode_ia:
                    joueur_actuel = "Ordinateur" if joueur_actuel == "Joueur 1" else "Joueur 1"
                else:
                    joueur_actuel = "Joueur 2" if joueur_actuel == "Joueur 1" else "Joueur 1"
        
        replay = input("\nVoulez-vous rejouer ? (oui/non) : ").lower()
        if replay not in ["oui", "o", "yes", "y"]:
            print("Au revoir !")
            break