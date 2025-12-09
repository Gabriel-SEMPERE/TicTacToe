import time
import random
import os

# Les combinaisons gagnantes
COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

def nettoyer_ecran():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_plateau(plateau):
    nettoyer_ecran()
    print("\n -- TicTacToe --\n")
    for row in range(3):
        offset = row * 3
        print(f" {plateau[offset]} | {plateau[offset+1]} | {plateau[offset+2]} ")
        if row < 2:
            print("---+---+---")
    print("\n" + "-"*15)

def verifier_victoire(plateau, symbole):
    return any(plateau[a] == plateau[b] == plateau[c] == symbole for a, b, c in COMBOS)

def grille_pleine(plateau):
    return " " not in plateau

def ordinateur(plateau, signe):
    time.sleep(0.8)
    adversaire = "X" if signe == "O" else "O"

    # Fonction pour trouver un coup gagnant ou bloquant
    def trouver_coup_critique(symbole_cible):
        for a, b, c in COMBOS:
            ligne = [plateau[a], plateau[b], plateau[c]]
            if ligne.count(symbole_cible) == 2 and ligne.count(" ") == 1:
                return [a, b, c][ligne.index(" ")]
        return None

    # 1. Attaque
    coup = trouver_coup_critique(signe)
    if coup is not None: return coup

    # 2. Défense
    coup = trouver_coup_critique(adversaire)
    if coup is not None: return coup

    # 3. Centre
    if plateau[4] == " ": return 4

    # 4. Coins
    coins = [0, 2, 6, 8]
    coins_dispos = [c for c in coins if plateau[c] == " "]
    if coins_dispos:
        return random.choice(coins_dispos)

    # 5. Reste random
    dispos = [i for i, x in enumerate(plateau) if x == " "]
    return random.choice(dispos) if dispos else None

def tour_humain(plateau, symbole):
    while True:
        try:
            choix = int(input(f"\nJoueur {symbole}, case (1-9) : "))
            if 1 <= choix <= 9:
                if plateau[choix-1] == " ":
                    plateau[choix-1] = symbole
                    break
                print("Case déjà prise.")
            else:
                print("Entre 1 et 9 svp.")
        except ValueError:
            print("Chiffre invalide.")

# Programme Principal
if __name__ == "__main__":
    while True:
        plateau = [" "] * 9
        jeu_en_cours = True
        
        nettoyer_ecran()
        choix = input("1. vs Ordi\n2. vs Humain\n> ")
        mode_ia = (choix == "1")

        joueurs = {"X": "Joueur 1", "O": "Ordinateur" if mode_ia else "Joueur 2"}
        tour = random.choice(["X", "O"])
        
        print(f"\n{joueurs[tour]} ({tour}) commence !")
        time.sleep(1.5)

        while jeu_en_cours:
            afficher_plateau(plateau)

            if mode_ia and tour == "O":
                coup = ordinateur(plateau, "O")
                if coup is not None:
                    plateau[coup] = "O"
                else:
                    jeu_en_cours = False
            else:
                tour_humain(plateau, tour)

            # Vérifications fin de partie
            if verifier_victoire(plateau, tour):
                afficher_plateau(plateau)
                print(f"\nBravo ! {joueurs[tour]} ({tour}) a gagné !")
                jeu_en_cours = False
            elif grille_pleine(plateau):
                afficher_plateau(plateau)
                print("\nMatch Nul !")
                jeu_en_cours = False
            else:
                tour = "O" if tour == "X" else "X"

        if input("\nRejouer ? (o/n) : ").lower() != 'o':
            break