import time
import random
import os

def nettoyer_ecran():
    os.system('cls')

def afficher_plateau(plateau):
    nettoyer_ecran()
    print("\n--TICTACTOE--\n")
    # Affiche les 3 lignes
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
    return any(plateau[a] == plateau[b] == plateau[c] == symbole for a, b, c in combos)

def grille_pleine(plateau):
    return " " not in plateau

def ordinateur(board, signe):
    time.sleep(1)
    
    adversaire = "X" if signe == "O" else "O"

    combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    
    # Cherche le premier mouvement valide selon les priorités
    def ai_coup(symbole_cible):
        for a, b, c in combos:
            ligne = [board[a], board[b], board[c]]
            if ligne.count(symbole_cible) == 2 and ligne.count(" ") == 1:
                # Retourne l'index de la case vide dans la combinaison
                return [a, b, c][ligne.index(" ")]
        return None

    # 1. ESSAYER DE GAGNER (Priorité maximale)
    coup = ai_coup(signe)
    if coup is not None:
        return coup

    # 2. BLOQUER LE JOUEUR
    coup = ai_coup(adversaire)
    if coup is not None:
        return coup

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
    return random.choice(cases_vides) if cases_vides else False

def tour_humain(plateau, joueur_symbole):
    valide = False
    while not valide:
        try:
            # Demande la case (1-9)
            coup = int(input(f"\n({joueur_symbole}), choisissez une case (1-9) : "))
            
            if 1 <= coup <= 9:
                # Vérifie si la case est vide (index 0-8)
                if plateau[coup - 1] == " ":
                    plateau[coup - 1] = joueur_symbole
                    valide = True
                else:
                    print("Cette case est déjà occupée !")
            else:
                print("Saisissez un nombre entre 1 et 9.")
        except ValueError:
            print("Erreur : Veuillez entrer un chiffre.")

if __name__ == "__main__":
    while True:
        plateau = [" " for _ in range(9)]
        running = True
        
        nettoyer_ecran()
        print("1. Un Joueur (vs IA)")
        print("2. Deux Joueurs")
        choix_mode = input("\nVotre choix : ")
        
        mode_ia = (choix_mode == "1")
        
        # Simplification de la gestion des joueurs
        if mode_ia:
            joueurs = {"X": "Joueur 1", "O": "Ordinateur"}
        else:
            joueurs = {"X": "Joueur 1", "O": "Joueur 2"}
        
        # Le symbole qui commence (X ou O)
        symbole_actuel = random.choice(["X", "O"])
        
        print(f"\nLe sort a décidé : c'est {joueurs[symbole_actuel]} ({symbole_actuel}) qui commence !")
        time.sleep(2)
        
        # --- BOUCLE DE JEU PRINCIPALE ---
        while running:
            afficher_plateau(plateau)
            nom_joueur = joueurs[symbole_actuel]

            # 1. JEU
            if mode_ia and symbole_actuel == "O":
                # Tour de l'ordinateur
                coup_ia = ordinateur(plateau, "O")
                if coup_ia is not False:
                    plateau[coup_ia] = "O"
                else:
                    running = False 
            else:
                # Tour de l'humain (Joueur 1 ou Joueur 2)
                tour_humain(plateau, symbole_actuel)

            # 2. VÉRIFICATION
            if verifier_victoire(plateau, symbole_actuel):
                afficher_plateau(plateau)
                print(f"\n VICTOIRE ! {nom_joueur} ({symbole_actuel}) a gagné !")
                running = False
            
            elif grille_pleine(plateau):
                afficher_plateau(plateau)
                print("\n Match Nul ! Aucune case disponible.")
                running = False
            
            else:
                # 3. CHANGEMENT DE JOUEUR
                symbole_actuel = "O" if symbole_actuel == "X" else "X"
        
        # Rejouer
        replay = input("\nVoulez-vous rejouer ? (oui/non) : ").lower()
        if replay not in ["oui", "o", "yes", "y"]:
            print("Au revoir !")
            break