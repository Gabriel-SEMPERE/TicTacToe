def afficher_plateau(self):
        self.nettoyer_ecran()
        print("\n--- TIC TAC TOE ---\n")
        for row in range(3):
            offset = row * 3
            ligne = f" {self.board[offset]} | {self.board[offset+1]} | {self.board[offset+2]} "
            print(ligne)
            if row < 2:
                print("---+---+---")
        print("\n-------------------")