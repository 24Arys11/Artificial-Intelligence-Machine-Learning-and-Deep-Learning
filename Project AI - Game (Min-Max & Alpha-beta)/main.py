"""Tema 2 - Dima Darius, Gr.311."""
import copy
import time
import pygame
import statistics
import sys


class GameMechanics:
    """
    Clasa specifica jocului ce pune la dispozitie urmatoarele metode:
        * start_position: defineste pozitia initiala
        * is_legal: verifica daca o mutare e valida
        * is_final: verifica daca o pozitie este finala
        * is_victory: verifica daca o pozitie este o victorie
        * is_draw: verifica daca o pozitie este o remiza
        * rate_e1: estimeaza valoarea unei pozitii pentru jucatorul cerut
        * rate_e2: alta estimare a pozitiei pentru jucatorul cerut
        * min_max: algoritmul Min-Max
        * alpha_beta: algoritmul Alpha-beta
    """
    @staticmethod
    def start_position(board_size, c="#"):
        """
        Defineste pozitia initiala
        :param board_size: (int) - reprezinta dimensiunea tablei
        :param c: (char) - caracterul ce reprezinta spatiul liber
        :return: pos (lista de liste(randuri) de char) - pozitia de inceput
        """
        pos = []
        for i in range(board_size):
            row = []
            for j in range(board_size):
                row.append(c)
            pos.append(row)
        return pos

    @staticmethod
    def is_legal(pos, new_pos, sign):
        """
        Verifica daca o mutare e valida
        :param pos: (lista de liste(randuri) de char) - pozitia curenta a tablei
        :param new_pos: (lista de liste(randuri) de char) - pozitia la care se va ajunge
        :param sign: (char) - jucatorul curent ("x" sau "0")
        :return: bool - True daca mutarea este valida, altfel False
        """
        state = State(pos, sign, 1)
        new_state = State(new_pos, GameMechanics.other_sign(sign), 0)
        if new_state in state.branch():
            return True
        return False

    @classmethod
    def is_final(cls, pos):
        """
        Verifica daca o pozitie este finala
        :param pos: (lista de liste(randuri) de char) - pozitia curenta a tablei
        :return: bool - True daca pozitia este finala, altfel False
        """
        return cls.is_victory(pos) or cls.is_draw(pos)

    @staticmethod
    def is_victory(pos):
        """
        Verifica daca o pozitie este victorioasa
        :param pos: (lista de liste(randuri) de char) - pozitia curenta a tablei
        :return: bool - True daca pozitia este victorioasa, altfel False
        """
        board_size = len(pos)     # position e lista de liste rows*elements. len returneaza nr de randuri, deci marimea tablei
        for i in range(board_size - 1):
            for j in range(board_size - 1):
                if pos[i][j] != "#" and pos[i][j] == pos[i][j + 1] == pos[i + 1][j] == pos[i + 1][j + 1]:    # am gasit un patratel victorios
                    # marcam victoria
                    if pos[i][j] == "x":
                        pos[i][j] = pos[i][j + 1] = pos[i + 1][j] = pos[i + 1][j + 1] = "X"
                    elif pos[i][j] == "0":  # Nu punem else, deoarece daca verificam iar daca pozitia e victorie, "X" s-ar face "Q".
                        pos[i][j] = pos[i][j + 1] = pos[i + 1][j] = pos[i + 1][j + 1] = "Q"
                    return True
        return False

    @staticmethod
    def is_draw(pos):
        """
        Verifica daca o pozitie este remiza
        :param pos: (lista de liste(randuri) de char) - pozitia curenta a tablei
        :return: bool - True daca pozitia este remiza, altfel False
        """
        for row in pos:
            for item in row:
                if item == "#":
                    return False    # Daca mai e loc pe tabla, NU e remiza.
        if GameMechanics.is_victory(pos):  # Ne asiguram ca ultimul simbol care a umplut tabla nu aduce victoria
            return False
        return True

    @staticmethod
    def other_sign(sign):
        """
        Arata celalalt simbol
        :param sign: (char) - "x" sau "0"
        :return: char - "0" sau "x"
        """
        if sign == "x":
            return "0"
        return "x"

    @staticmethod
    def other_thing(current, thing1, thing2):
        """
        Celalalt obiect
        :param current: un obiect egal cu primul sau al doilea obiect
        :param thing1: primul obiect
        :param thing2: al doilea obiect
        :return: "al doilea obiect", daca "current" este "primul obiect", altfel "primul obiect".
        """
        if current == thing1:
            return thing2
        return thing1

    @staticmethod
    def rate_e1(pos, sign):
        """
        O estimare (E1) a pozitiei din punctul de vedere a jucatorului cu semnul sign.

        Estimarea E1 este simpla. Cu cat avem mai multe oportunitati de victorie, scorul
        pozitiei creste, iar cu cat adversarul se apropie de victorie scorul pozitiei scade.
        Cu aceasta estimare, computerul va juca foarte slab, intrcat ne va lasa sa obtinem
        victoria daca avem o singura oportunitate, iar el va cauta sa faca rost de mai multe
        oportunitati, cu alte cuvinte, aduce mingea in fata portii si dupa rateaza !

        :param pos: (lista de liste(randuri) de char) - pozitia curenta a tablei
        :param sign: (char) - "x" sau "0"
        :return: int - valoarea estimarii
        """
        score = 0
        board_size = len(pos)     # position e lista de liste rows*elements. len returneaza nr de randuri, deci marimea tablei
        for i in range(board_size - 1):
            for j in range(board_size - 1):
                square = pos[i][j] + pos[i][j + 1] + pos[i + 1][j] + pos[i + 1][j + 1]   # daca in acest patratel:
                if square == "QQQQ":    # victorie pentru "0"
                    if sign == "0":
                        score += 10
                    else:
                        score -= 10
                if square == "XXXX":    # victorie pentru "x"
                    if sign == "x":
                        score += 10
                    else:
                        score -= 10
                elif square == "####":    # sunt doar spatii goale
                    continue            # nu influenteaza scorul
                elif sign in square and GameMechanics.other_sign(sign) in square:  # se gasesc ambele simboluri
                    continue                                                    # nu influenteaza scorul
                else:
                    # daca patratelul nu e gol, nici mixt, ori contine semne adverse ori semnele noastre si spatii libere
                    score += square.count(sign)     # atunci primim 1, 2 sau 3 puncte in functie de cate simboluri avem in patratel
                    score -= square.count(GameMechanics.other_sign(sign))      # si pierdem 1, 2 sau 3 puncte in functie de cate simboluri detine adversarul
        return score

    @staticmethod
    def rate_e2(pos, sign):
        """
        Alta estimare (E2) a pozitiei din punctul de vedere a jucatorului cu semnul sign.

        Estimarea E2 este cea mai buna. Asemenea estimarii E1, este necesara pastrarea
        echilibrului dintre dezvoltarea propriei pozitii si impiedicarea adversarului
        de a ajunge la victorie. Diferenta este ca pentru E2, un patratel completat
        in proportie mai mare este semnificativ mai valoros decat mai multe patratele
        completate in proportie mai mica, iar pozitia finala influenteaza scorul masiv.

        :param pos: (lista de liste(randuri) de char) - pozitia curenta a tablei
        :param sign: (char) - "x" sau "0"
        :return: int - valoarea estimarii
        """
        score = 0
        board_size = len(pos)     # position e lista de liste rows*elements. len returneaza nr de randuri, deci marimea tablei
        for i in range(board_size - 1):
            for j in range(board_size - 1):
                square = pos[i][j] + pos[i][j + 1] + pos[i + 1][j] + pos[i + 1][j + 1]   # daca in acest patratel:
                if square == "QQQQ":    # victorie pentru "0"
                    if sign == "0":
                        score += 999
                    else:
                        score -= 999
                if square == "XXXX":    # victorie pentru "x"
                    if sign == "x":
                        score += 999
                    else:
                        score -= 999
                elif square == "####":    # sunt doar spatii goale
                    continue            # nu influenteaza scorul
                elif sign in square and GameMechanics.other_sign(sign) in square:  # se gasesc ambele simboluri
                    continue                                                    # nu influenteaza scorul
                else:
                    # daca patratelul nu e gol, nici mixt, ori contine semne adverse ori semnele noastre si spatii libere
                    score += square.count(sign)**2     # atunci primim 1, 4 sau 9 puncte in functie de cate simboluri avem in patratel
                    score -= square.count(GameMechanics.other_sign(sign))**3      # si pierdem 1, 8 sau 27 puncte in functie de cate simboluri detine adversarul
        return score

    @staticmethod
    def statistics(player_1, player_2, thinking_times, depths):
        """
        Afiseaza statisticile jucatorilor la finalul jocului
        :param player_1: Jucatorul cu simbolul "x"
        :param player_2: Jucatorul cu simbolul "0"
        :param thinking_times: lista de timpi de gandire - pozitiile impare pentru jucatorul 1, cele pare pentru jucatorul 2
        :param depths: lista de noduri parcurse - pozitiile impare pentru jucatorul 1, cele pare pentru jucatorul 2
        :return: No return
        """
        p1_thinking_time = thinking_times[::2]
        p2_thinking_time = thinking_times[1::2]
        p1_depths = depths[::2]
        p2_depths = depths[1::2]

        if len(p1_thinking_time) != 0:
            print(f"{player_1} a executat {len(p1_thinking_time)} mutari. Cel mai repede a mutat in {min(p1_thinking_time)}\n"
                  f"Cel mai incet a mutat in {max(p1_thinking_time)}, in medie a mutat in {statistics.mean(p1_thinking_time)}, iar mediana\n"
                  f"mutarilor este {statistics.median(p1_thinking_time)}.")

        if len(p1_depths) != 0:
            if player_1 != "human":
                print(f"{player_1} a generat, cel mai putin la o mutare {min(p1_depths)} noduri, cel mai mult{max(p1_depths)}.\n"
                      f"In medie a generat {statistics.mean(p1_depths)}, iar mediana este {statistics.median(p1_depths)}.")

        if len(p2_thinking_time) != 0:
            print(f"{player_2} a executat {len(p2_thinking_time)} mutari. Cel mai repede a mutat in {min(p2_thinking_time)}\n"
                  f"Cel mai incet a mutat in {max(p2_thinking_time)}, in medie a mutat in {statistics.mean(p2_thinking_time)}, iar mediana\n"
                  f"mutarilor este {statistics.median(p2_thinking_time)}.")

        if len(p2_depths) != 0 and player_2 != "human":
            print(f"{player_2} a generat, cel mai putin la o mutare {min(p2_depths)} noduri, cel mai mult{max(p2_depths)}.\n"
                  f"In medie a generat {statistics.mean(p2_depths)}, iar mediana este {statistics.median(p2_depths)}.")

    @staticmethod
    def min_max(state, estimation, max_sign):
        """
        Algoritmul Min-Max, asa cum l-am invatat la laborator, usor modificat
        pentru a returna si numarul de noduri vizitate.

        :param state: (stare) - nod in arbore
        :param estimation: (str) - metoda de estimare a valorii starii
        :param max_sign: (char) - semnul lui Max ("x" sau "0")

        :return state: (obiect al clasei State) - nod in arbore, modificat astfel:
                * ratingul (valoarea) a fost modificata luand in calcul si succesorii
                * in favourite child s-a adaugat mutarea considerata optima
        :return no_visited: (int) - numarul de stari posibile parcurse
        """
        # daca sunt la o frunza in arborele minimax sau la o stare finala
        no_visited = 1   # pentru a numara cate noduri am generat
        # Daca adancimea este 0 sau avem stare finala returnam starea
        if state.depth == 0 or GameMechanics.is_final(state.position):
            state.compute_rating(estimation)
            return state, no_visited

        # calculez toate mutarile posibile din starea curenta
        state.kids = state.branch()

        # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
        considered_moves = []
        for child in state.kids:    # expandez(constr subarb) fiecare nod x din mutari posibile
            possible_move, more_visited = GameMechanics.min_max(child, estimation, max_sign)
            considered_moves.append(possible_move)
            no_visited += more_visited

        if state.sign == max_sign:      # Daca joaca MAX
            # aleg starea-fiica cu estimarea maxima
            state.favourite_child = max(considered_moves, key=lambda x: x.rating)
        else:   # Daca joaca MIN
            # aleg starea-fiica cu estimarea minima
            state.favourite_child = min(considered_moves, key=lambda x: x.rating)

        state.rating = state.favourite_child.rating
        return state, no_visited

    @staticmethod
    def alpha_beta(alpha, beta, state, estimation, max_sign):
        """
        Algoritmul Alpha-beta, asa cum l-am invatat la laborator, usor modificat
        pentru a returna si numarul de noduri vizitate. Reprezinta o optimizare
        a algoritmului Min-Max

        :param alpha: (int) - limita inferioara
        :param beta: (int) - limita superioara
        :param state: (stare) - nod in arbore
        :param estimation: (str) - metoda de estimare a valorii starii
        :param max_sign: (char) - semnul lui Max ("x" sau "0")

        :return state: (obiect al clasei State) - nod in arbore, modificat astfel:
                * ratingul (valoarea) a fost modificata luand in calcul si succesorii
                * in favourite child s-a adaugat mutarea considerata optima
        :return no_visited: (int) - numarul de stari posibile parcurse
        """
        # daca sunt la o frunza in arborele minimax sau la o stare finala
        no_visited = 1   # pentru a numara cate noduri am generat
        # Daca adancimea este 0 sau avem stare finala returnam starea
        if state.depth == 0 or GameMechanics.is_final(state.position):
            state.compute_rating(estimation)
            return state, no_visited

        if alpha > beta:
            return state, no_visited    # este intr-un interval invalid deci nu o mai procesez

        # calculez toate mutarile posibile din starea curenta
        state.kids = state.branch()

        if state.sign == max_sign:      # Daca joaca Max
            current_rating = float('-inf')  # in aceasta variabila calculam maximul

            for child in state.kids:
                # calculeaza estimarea pentru starea noua, realizand subarborele
                new_state, more_visited = GameMechanics.alpha_beta(alpha, beta, child, estimation, max_sign)
                no_visited += more_visited

                if current_rating < new_state.rating:
                    state.favourite_child = new_state
                    current_rating = new_state.rating
                if alpha < new_state.rating:
                    alpha = new_state.rating
                    if alpha >= beta:
                        break

        else:       # Daca joaca Min
            current_rating = float('inf')
            for child in state.kids:
                # calculeaza estimarea
                new_state, more_visited = GameMechanics.alpha_beta(alpha, beta, child, estimation, max_sign)
                no_visited += more_visited

                if current_rating > new_state.rating:
                    state.favourite_child = new_state
                    current_rating = new_state.rating
                if beta > new_state.rating:
                    beta = new_state.rating
                    if alpha >= beta:
                        break

        state.rating = state.favourite_child.rating
        return state, no_visited


class State:
    """
    Nod ce reprezinta starea curenta a jocului (pozitia tablei, cine este la mutare,
     parametrii pt AI: adancimea in arbore, starea precedenta, estimarea)
    
    Metode:
        * branch: genereaza si returneaza succesorii (toate mutarile posibile din starea curenta)
        * compute_rating: calculeaza estimarea propriei pozitii, in functie de estimarea primita ca parametru
    """
    def __init__(self, position, sign, depth, parent=None, rating=None):
        """
        Initializeaza starea cu parametrii dati.
        :param position (lista de liste(randuri) de char): pozitia tablei "#" - gol, "x". "0"
        :param sign (char): semnul jucatorului la mutare, "x" sau "0"
        :param depth (int): adancimea, un parametru esential pentru algoritmii AI
        :param parent (referinta): arata catre nodul (obiect State) parinte
        :param rating (int): estimarea starii, un parametru important pentru algoritmii AI
        """
        self.position = copy.deepcopy(position)
        self.sign = sign
        self.depth = depth
        self.parent = parent
        self.rating = rating
        self.kids = []
        self.favourite_child = None

    def branch(self):
        """
        Genereaza o lista de succesori (toate mutarile posibile din starea curenta)

        NO ARGS - se foloseste de variabilele din clasa Stare
                    * position: pozitia tablei
                    * sign - cine este la mutare ("x" sau "0")
                    * depth - adancimea starii. (scade la succesori)
                    * parent - fiecare succesor isi "tine minte" parintele
                    * rating - estimarea starii curente
                    
        :return kids []: lista de obiecte din clasa State ce reprezinta succesorii acesteia.
        """
        kids = []
        board_size = len(self.position)     # position e lista de liste rows*elements. len returneaza nr de randuri, deci marimea tablei
        # oriunde e loc gol "#" avem voie sa punem semnul nostru
        for i, _ in enumerate(self.position):
            for j, _ in enumerate(self.position[i]):
                if self.position[i][j] == "#":
                    child = State(self.position, GameMechanics.other_sign(self.sign), self.depth - 1, parent=self)
                    child.position[i][j] = self.sign
                    kids.append(child)
        # oriunde e un semn de-al nostru, daca la distanta 1 pe diagonala este un semn opus si la
        # distanta 2 pe diagonala este liber, putem muta semnul nostru si captura semnul adversar
        for i, _ in enumerate(self.position):
            for j, _ in enumerate(self.position[i]):
                if self.position[i][j] == self.sign:
                    # VERIFICAM DIAGONALA STANGA-SUS
                    if (i - 2) >= 0 and (j - 2) >= 0:   # daca destinatia nu e in afara tablei
                        # si pe diagonala cautata, la distanta 1 se afla semnul oponentului
                        if self.position[i - 1][j - 1] == GameMechanics.other_sign(self.sign):
                            # si daca pe diagonala cautata, la distanta 2 e loc liber
                            if self.position[i - 2][j - 2] == "#":
                                child = State(self.position, GameMechanics.other_sign(self.sign), self.depth - 1, parent=self)
                                child.position[i][j] = "#"
                                child.position[i - 1][j - 1] = "#"
                                child.position[i - 2][j - 2] = self.sign
                                kids.append(child)
                    # VERIFICAM DIAGONALA STANGA-JOS
                    if (i + 2) < board_size and (j - 2) >= 0:   # daca destinatia nu e in afara tablei
                        # si pe diagonala cautata, la distanta 1 se afla semnul oponentului
                        if self.position[i + 1][j - 1] == GameMechanics.other_sign(self.sign):
                            # si daca pe diagonala cautata, la distanta 2 e loc liber
                            if self.position[i + 2][j - 2] == "#":
                                child = State(self.position, GameMechanics.other_sign(self.sign), self.depth - 1, parent=self)
                                child.position[i][j] = "#"
                                child.position[i + 1][j - 1] = "#"
                                child.position[i + 2][j - 2] = self.sign
                                kids.append(child)
                    # VERIFICAM DIAGONALA DREAPTA-SUS
                    if (i - 2) >= 0 and (j + 2) < board_size:   # daca destinatia nu e in afara tablei
                        # si pe diagonala cautata, la distanta 1 se afla semnul oponentului
                        if self.position[i - 1][j + 1] == GameMechanics.other_sign(self.sign):
                            # si daca pe diagonala cautata, la distanta 2 e loc liber
                            if self.position[i - 2][j + 2] == "#":
                                child = State(self.position, GameMechanics.other_sign(self.sign), self.depth - 1, parent=self)
                                child.position[i][j] = "#"
                                child.position[i - 1][j + 1] = "#"
                                child.position[i - 2][j + 2] = self.sign
                                kids.append(child)
                    # VERIFICAM DIAGONALA DREAPTA-JOS
                    if (i + 2) < board_size and (j + 2) < board_size:   # daca destinatia nu e in afara tablei
                        # si pe diagonala cautata, la distanta 1 se afla semnul oponentului
                        if self.position[i + 1][j + 1] == GameMechanics.other_sign(self.sign):
                            # si daca pe diagonala cautata, la distanta 2 e loc liber
                            if self.position[i + 2][j + 2] == "#":
                                child = State(self.position, GameMechanics.other_sign(self.sign), self.depth - 1, parent=self)
                                child.position[i][j] = "#"
                                child.position[i + 1][j + 1] = "#"
                                child.position[i + 2][j + 2] = self.sign
                                kids.append(child)
        return kids

    def compute_rating(self, estimation):
        """
        Calculeaza ratingul (scorul) in functie de estimarea folosita
        :param estimation: (str) - "E1" sau "E2"
        :returns: No return
        """
        if estimation == "E1":
            self.rating = GameMechanics.rate_e1(self.position, self.sign)
        else:
            self.rating = GameMechanics.rate_e2(self.position, self.sign)

    def __eq__(self, other):
        """
        Doua stari sunt echivalente daca pozitia tablei este identica

        Args: other(State)

        Returns: bool - True - pozitia tablei identica, altfel False
        """
        for i, _ in enumerate(self.position):
            for j, _ in enumerate(self.position[i]):
                if self.position[i][j] != other.position[i][j]:
                    return False
        return True


def store_input(text):
    """
    Verifica si memoreaza un input ce se doreste a fi integer pozitiv
    :param text: (str) - inputul utilizatorului
    :return: int - integerul pozitiv introdus, sau "-1" daca utilizatorul nu a introdus un input valid
    """
    for c in text:
        if c not in "0123456789":
            return -1
    return int(text)


def launcher_exe():
    """
    Lanseaza jocul in varianta dorita !
    Meniu in consola cu 3 optiuni:
        * Launch GUI
        * Play in console
        * EXIT !!!
    """
    given_input = -1
    
    while given_input != 0:
        
        print("01. Launch GUI")
        print("02. Play in console")
        print("00. EXIT !!!")
        
        given_input = store_input(input(">>> "))
        while given_input == -1:
            print("Invalid input ! Please provide a positive integer !")
            given_input = store_input(input(">>> "))

        if given_input == 0:
            break

        elif given_input == 1:
            GUI = RunGUI()
            GUI.main_menu()
            
        elif given_input == 2:
            RunConsole.main_menu()

        else:
            print("Not an option !")


class RunConsole:
    """
    Varianta de consola a jocului
    """
    user = "Irina"
    BOARD_SIZE = 5
    sign = "x"
    opponent = "Min-Max"
    difficulty1 = "Easy"
    difficulty2 = "Easy"
    estimation = "E1"

    @staticmethod
    def display_pos(pos):
        """
        Afiseaza in consola pozitia curenta
        :param pos: lista de liste(randuri) de char

        :return: No return
        """
        print(" ", end=" ")
        for i, _ in enumerate(pos):
            print(i + 1, end=" ")
        print()
        for i, _ in enumerate(pos):
            print(i + 1, end=" ")
            for j, _ in enumerate(pos):
                print(pos[i][j], end=" ")
            print()

    @classmethod
    def _human_move(cls, pos, sign):
        """
        Jucatorul uman executa mutarea
        :param pos: lista de liste(randuri) de char
        :param sign: (char) - semnul jucatorul care muta("x" sau "0")
        :return: pos - noua pozitie, dupa efectuarea mutarii
                 int - numarul de noduri parcurse pt AI, 0 pt human
        """
        # simulam un do{code}while{condition} in python pt ca am cautat si am vazut ca nu exista.
        while True:
            new_pos = copy.deepcopy(pos)        # Saracul Garbage Collector are ceva treaba :))))
            print("row = 0, if you want to quit !")
            row = store_input(input("row: "))
            while row < 0 or row > cls.BOARD_SIZE:
                print("Please provide a valid coordonate, or 0 to quit !")
                row = store_input(input("row: "))
            if row == 0:
                pos = GameMechanics.start_position(cls.BOARD_SIZE, c="@")
                return pos, 0
            col = store_input(input("col: "))
            while col < 1 or col > cls.BOARD_SIZE:
                print("Please provide a valid coordonate")
                col = store_input(input("col: "))
            new_pos[row - 1][col - 1] = sign

            # pozitia rezultata poate fi egala cu pozitia initiala numai daca la
            if new_pos == pos:  # coordonatele alese se afla un simbol de-al nostru
                new_pos[row - 1][col - 1] = "#"     # stergem simbolul nostru
                print(f"Moving {sign} from row: {row}, col: {col} to:")
                target_row = store_input(input("row: "))
                while target_row < 1 or target_row > cls.BOARD_SIZE:
                    print("Please provide a valid coordonate")
                    target_row = store_input(input("row: "))
                target_col = store_input(input("col: "))
                while target_col < 1 or target_col > cls.BOARD_SIZE:
                    print("Please provide a valid coordonate")
                    target_col = store_input(input("col: "))
                new_pos[target_row - 1][target_col - 1] = sign  # punem semnul nostru la destinatie
                # capturam semnul adversarului
                new_pos[(row + target_row) // 2 - 1][(col + target_col) // 2 - 1] = "#"

            if GameMechanics.is_legal(pos, new_pos, sign):
                return new_pos, 0
            else:
                print("Illegal move !")

    @classmethod
    def _min_max_move(cls, pos, depth, sign):
        """
        Jucatorul Min-Max executa mutarea
        :param pos: lista de liste(randuri) de char
        :param sign: (char) - semnul jucatorul care muta("x" sau "0")
        :return: pos - noua pozitie, dupa efectuarea mutarii
                 int - numarul de noduri parcurse pt AI, 0 pt human
        """
        state = State(pos, sign, depth)
        state, visited_nodes = GameMechanics.min_max(state, cls.estimation, sign)
        print(f"Scorul pozitiei este: {state.favourite_child.rating} !")
        return state.favourite_child.position, visited_nodes

    @classmethod
    def _alpha_beta_move(cls, pos, depth, sign):
        """
        Jucatorul Alpha-beta executa mutarea
        :param pos: lista de liste(randuri) de char
        :param sign: (char) - semnul jucatorul care muta("x" sau "0")
        :return: pos - noua pozitie, dupa efectuarea mutarii
                 int - numarul de noduri parcurse pt AI, 0 pt human
        """
        state = State(pos, sign, depth)
        state, visited_nodes = GameMechanics.alpha_beta(-500, 500, state, cls.estimation, sign)
        print(f"Scorul pozitiei este: {state.favourite_child.rating} !")
        return state.favourite_child.position, visited_nodes

    @classmethod
    def make_move(cls, player, level, pos, sign):
        """
        Executa mutarea
        :param player: jucatorul care executa mutarea
        :param level: nivelul (pentru AI) de dificultate a jucatorului
        :param pos: lista de liste(randuri) de char
        :param sign: (char) - semnul jucatorul care muta("x" sau "0")
        :return: pos - noua pozitie, dupa efectuarea mutarii
                 int - numarul de noduri parcurse pt AI, 0 pt human
        """
        depth = 3
        if level == "medium":
            depth = 4
        elif level == "hard":
            depth = 5

        if player == "human":
            return cls._human_move(pos, sign)
        elif player == "Min-Max":
            return cls._min_max_move(pos, depth, sign)
        return cls._alpha_beta_move(pos, depth, sign)

    @classmethod
    def game(cls, player_1, player_2, p1_level="human", p2_level="human"):
        """
        Jocul efectiv in consola, dupa ce optiunile au fost alese.
        :param player_1: jucatorul cu semnul "x"
        :param player_2: jucatorul cu semnul "0"
        :param p1_level: nivelul de dificultate a jucatorului cu semnul "x" (pentru AI)
        :param p2_level: nivelul de dificultate a jucatorului cu semnul "0" (pentru AI)

        :return: NO RETURN ! We've passed the point of singularity...
        """
        print("Now playing...")

        # generam pozitia initiala (tabla goala)
        pos = GameMechanics.start_position(cls.BOARD_SIZE)
        cls.display_pos(pos)

        player = player_1
        level = p1_level
        sign = "x"

        thinking_times = []
        depths = []

        while True:

            print(f"Este randul lui {sign} !")
            start_time = int(round(time.time() * 1000))
            pos, depth = cls.make_move(player, level, pos, sign)
            stop_time = int(round(time.time() * 1000))

            cls.display_pos(pos)

            print(f"Jucatorul {player} a \"gandit\" timp de {stop_time - start_time} milisecunde.")
            thinking_times.append(stop_time - start_time)
            if player != "human":
                print(f"In acest timp, a luat in calcul {depth} situatii posibile")
            depths.append(depth)

            if pos[0][0] == "@":
                GameMechanics.statistics(player_1, player_2, thinking_times, depths)
                print("Game aborted !")
                break

            if GameMechanics.is_final(pos):
                GameMechanics.statistics(player_1, player_2, thinking_times, depths)
                if GameMechanics.is_victory(pos):
                    # Daca is_victory(pos) intoarce True, se evidentiaza configuratia castigatoare si trebuie sa reafisam pozitia
                    cls.display_pos(pos)
                    print(f"Player {sign} won the match !")
                elif GameMechanics.is_draw(pos):
                    print("The game is a draw !")
                break

            player = GameMechanics.other_thing(player, player_1, player_2)
            level = GameMechanics.other_thing(level, p1_level, p2_level)
            sign = GameMechanics.other_sign(sign)

    @classmethod
    def main_menu(cls):
        """
        Meniul principal al jocului in consola
        :return: No return
        """
        given_input = 1
        
        while given_input != 0:
            
            print(f"\nHello, {cls.user} !")
            print("\n----------PLAY----------")
            print("01. Player vs AI")
            print("02. Player vs Player")
            print("03. AI vs AI")
            print("--------SETTINGS--------")
            print(f"04. Set username: {cls.user}")
            print(f"05. Set board size: {cls.BOARD_SIZE}*{cls.BOARD_SIZE}")
            print("00. EXIT !!!")
            
            given_input = store_input(input(cls.user + ": "))
            while given_input == -1:
                print("Invalid input ! Please provide a positive integer !")
                given_input = store_input(input(cls.user + ": "))
    
            if given_input == 0:
                break
    
            elif given_input == 1:
                cls.PvAI_menu()
                
            elif given_input == 2:
                cls.PvP_menu()
                
            elif given_input == 3:
                cls.AIvAI_menu()
                
            elif given_input == 4:
                cls.user = input("New username: ")
    
            elif given_input == 5:
                cls.board_menu()
    
            else:
                print("Not an option !")

    @classmethod
    def PvAI_menu(cls):
        """
        Submeniul "Player vs AI" al jocului in consola
        :return: No return
        """
        given_input = 1
        
        while given_input != 0:
            
            print("01. Play !")
            print("---------OPTIONS--------")
            print("02. Sign: " + cls.sign)
            print("03. Opponent: " + cls.opponent)
            print("04. Difficulty: " + cls.difficulty1)
            print("05. Score estimation: " + cls.estimation)
            print("00. Back")
            
            given_input = store_input(input(cls.user + ": "))
            while given_input == -1:
                print("Invalid input ! Please provide a positive integer !")
                given_input = store_input(input(cls.user + ": "))
    
            if given_input == 0:
                break
    
            elif given_input == 1:
                if cls.sign == "x":
                    cls.game("human", cls.opponent, p2_level=cls.difficulty1)
                else:
                    cls.game(cls.opponent, "human", p1_level=cls.difficulty1)
                
            elif given_input == 2:
                cls.sign_menu()
                
            elif given_input == 3:
                cls.opponent_menu()
                
            elif given_input == 4:
                cls.difficulty1_menu()
    
            elif given_input == 5:
                cls.estimation_menu()
    
            else:
                print("Not an option !")
     
    @classmethod
    def PvP_menu(cls):
        """
        Submeniul "Player vs Player" al jocului in consola
        :return: No return
        """
        given_input = 1
        
        while given_input != 0:
            
            print("01. Play !")
            print("00. Back")
            
            given_input = store_input(input(cls.user + ": "))
            while given_input == -1:
                print("Invalid input ! Please provide a positive integer !")
                given_input = store_input(input(cls.user + ": "))
    
            if given_input == 0:
                break
    
            elif given_input == 1:
                cls.game("human", "human")
                
            else:
                print("Not an option !")
    
    @classmethod
    def AIvAI_menu(cls):
        """
        Submeniul "AI vs AI" al jocului in consola
        :return: No return
        """
        given_input = 1
        
        while given_input != 0:
            
            print("01. Play !")
            print("------------------------")
            print(f"Min-Max: {cls.sign}")
            print(f"Alpha-beta: {GameMechanics.other_sign(cls.sign)}")
            print("---------OPTIONS--------")
            print("02. Switch signs")
            print("03. Min-Max: " + cls.difficulty1)
            print("04. Alpha-beta: " + cls.difficulty2)
            print("05. Score estimation: " + cls.estimation)
            print("00. Back")
            
            given_input = store_input(input(cls.user + ": "))
            while given_input == -1:
                print("Invalid input ! Please provide a positive integer !")
                given_input = store_input(input(cls.user + ": "))
    
            if given_input == 0:
                break
            
            elif given_input == 1:
                if cls.sign == "x":
                    cls.game("Min-Max", "Alpha-beta", p1_level=cls.difficulty1, p2_level=cls.difficulty2)
                else:
                    cls.game("Alpha-beta", "Min-Max", p1_level=cls.difficulty2, p2_level=cls.difficulty1)
                
            elif given_input == 2:
                cls.sign = GameMechanics.other_sign(cls.sign)
                
            elif given_input == 3:
                cls.difficulty1_menu()
                
            elif given_input == 4:
                cls.difficulty2_menu()
                
            elif given_input == 5:
                cls.estimation_menu()
    
            else:
                print("Not an option !")

    @classmethod
    def sign_menu(cls):
        """
        Submeniul optiunii de alegere a simbolului ("x" sau "0") jocului in consola
        :return: No return
        """
        given_input = 1
        
        while given_input != 0:
            
            print("01. x")
            print("02. 0")
            print("00. Back")
            
            given_input = store_input(input(cls.user + ": "))
            while given_input == -1:
                print("Invalid input ! Please provide a positive integer !")
                given_input = store_input(input(cls.user + ": "))
    
            if given_input == 0:
                break
    
            elif given_input == 1:
                cls.sign = "x"
                break
                
            elif given_input == 2:
                cls.sign = "0"
                break
                
            else:
                print("Not an option !")
    
    @classmethod
    def opponent_menu(cls):
        """
        Submeniul optiunii de alegere a oponentului (Min-Max sau Alpha-beta) jocului in consola
        :return: No return
        """
        given_input = 1
        
        while given_input != 0:
            
            print("01. Min-Max")
            print("02. Alpha-beta")
            print("00. Back")
            
            given_input = store_input(input(cls.user + ": "))
            while given_input == -1:
                print("Invalid input ! Please provide a positive integer !")
                given_input = store_input(input(cls.user + ": "))
    
            if given_input == 0:
                break
    
            elif given_input == 1:
                cls.opponent = "Min-Max"
                break
                
            elif given_input == 2:
                cls.opponent = "Alpha-beta"
                break
                
            else:
                print("Not an option !")

    @classmethod
    def difficulty1_menu(cls):
        """
        Submeniul optiunii de alegere a dificultatii oponentului (la Player vs AI)
         sau dificultatii lui Min-Max (la AI vs AI) a jocului in consola
        :return: No return
        """
        given_input = 1
        
        while given_input != 0:
            
            print("01. Easy")
            print("02. Medium")
            print("03. Hard")
            print("00. Back")
            
            given_input = store_input(input(cls.user + ": "))
            while given_input == -1:
                print("Invalid input ! Please provide a positive integer !")
                given_input = store_input(input(cls.user + ": "))
    
            if given_input == 0:
                break
    
            elif given_input == 1:
                cls.difficulty1 = "Easy"
                break
                
            elif given_input == 2:
                cls.difficulty1 = "Medium"
                break
                
            elif given_input == 3:
                cls.difficulty1 = "Hard"
                break
                
            else:
                print("Not an option !")

    @classmethod
    def difficulty2_menu(cls):
        """
        Submeniul optiunii de alegere a dificultatii lui Alpha-beta (la AI vs AI) a jocului in consola
        :return: No return
        """
        given_input = 1
        
        while given_input != 0:
            
            print("01. Easy")
            print("02. Medium")
            print("03. Hard")
            print("00. Back")
            
            given_input = store_input(input(cls.user + ": "))
            while given_input == -1:
                print("Invalid input ! Please provide a positive integer !")
                given_input = store_input(input(cls.user + ": "))
    
            if given_input == 0:
                break
    
            elif given_input == 1:
                cls.difficulty2 = "Easy"
                break
                
            elif given_input == 2:
                cls.difficulty2 = "Medium"
                break
                
            elif given_input == 3:
                cls.difficulty2 = "Hard"
                break
                
            else:
                print("Not an option !")

    @classmethod
    def estimation_menu(cls):
        """
        Submeniul optiunii de alegere a estimarii folosite de AI a jocului in consola
        :return: No return
        """
        given_input = 1
        
        while given_input != 0:
            
            print("01. E1")
            print("02. E2")
            print("00. Back")
            
            given_input = store_input(input(cls.user + ": "))
            while given_input == -1:
                print("Invalid input ! Please provide a positive integer !")
                given_input = store_input(input(cls.user + ": "))
    
            if given_input == 0:
                break
    
            elif given_input == 1:
                cls.estimation = "E1"
                break
                
            elif given_input == 2:
                cls.estimation = "E2"
                break
                
            else:
                print("Not an option !")

    @classmethod
    def board_menu(cls):
        """
        Submeniul optiunii de alegere a dimensiunii tablei a jocului in consola
        :return: No return
        """
        given_input = 1
        
        while given_input != 0:
            
            print("01.  5*5")
            print("02.  6*6")
            print("03.  7*7")
            print("04.  8*8")
            print("05.  9*9")
            print("06. 10*10")
            print("00. Back")
            
            given_input = store_input(input(cls.user + ": "))
            while given_input == -1:
                print("Invalid input ! Please provide a positive integer !")
                given_input = store_input(input(cls.user + ": "))
    
            if given_input == 0:
                break
    
            elif given_input == 1:
                cls.BOARD_SIZE = 5
                break
                
            elif given_input == 2:
                cls.BOARD_SIZE = 6
                break
                
            elif given_input == 3:
                cls.BOARD_SIZE = 7
                break
                
            elif given_input == 4:
                cls.BOARD_SIZE = 8
                break
    
            elif given_input == 5:
                cls.BOARD_SIZE = 9
                break
    
            elif given_input == 6:
                cls.BOARD_SIZE = 10
                break
    
            else:
                print("Not an option !")


class RunGUI:
    """
    Varianta GUI a jocului folosind modulul "pygame".
    """

    def __init__(self):
        """
        Initializeaza jocul GUI.
        """
        self.BOARD_SIZE = 5
        self.sign = "x"
        self.opponent = "Min-Max"
        self.difficulty1 = "Easy"
        self.difficulty2 = "Easy"
        self.estimation = "E1"
        
        self.WIDTH, self.HEIGHT = 500, 500
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.VIOLET = (255, 0, 255)
        self.AQUA = (0, 255, 255)
        
        self.BTN_BG_COLOR = self.YELLOW
        self.BTN_HVR_COLOR = self.AQUA
        self.BTN_ALT_COLOR = self.VIOLET
        
        self.BTN_WIDTH = 250
        self.BTN_HEIGHT = 50
        
        pygame.font.init()
        pygame.mixer.init()
        pygame.display.set_caption("Dima Darius, Gr.311 - Tema 2 (4_signs_square)")
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        # pygame.mouse.set_cursor('cursor.ani')
        
        self.FPS = 60
        self.clock = pygame.time.Clock()
    
    class button:
        """
        Clasa cu ajutorul careia putem crea butoane cu usurinta.
        """
        def __init__(self, color, x, y, width, height, text="", info=None):
            """
            Initializeaza butonul cu parametrii dati.
            :param color: (tuplu de 3) - culoarea de fundal in RBG.
            :param x: (int) - coordonata latime a butonului
            :param y: (int) - coordonata inaltime a butonului
            :param width: (int) - latimea butonului
            :param height: (int) - inaltimea butonului
            :param text: (str) - eticheta afisata pe buton - optional
            :param info: (any) - util daca dorim sa salvam informatie specifica butonului
            """
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.info = info
            
        def update_text(self, text):
            """
            Schimba eticheta afisata pe buton
            :param text: (str) - eticheta noua
            :return: No return
            """
            self.text = text
        
        def draw(self, win, outline=None):
            """
            "Deseneaza" butonul in fereastra
            :param win: fereastra pygame
            :param outline: (tuplu de 3) - culoarea marginii in RGB, daca dorim margine (optional)
            :return: No return
            """
            if outline:
                pygame.draw.rect(win, outline, (self.x, self.y, self.width, self.height), 0)
            pygame.draw.rect(win, self.color, (self.x+2, self.y+2, self.width-4, self.height-4), 0)
            
            font = pygame.font.SysFont('timesnewroman', 20)
            text = font.render(self.text, True, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))
        
        def is_over(self, pos):
            """
            Verifica daca un obiect (exemplu: cursorul mouse-ului) se afla pe buton
            :param pos: (tuplu de 2 coordonate x, y) - pozitia obiectului de verificat
            :return: bool - True daca obiectul este pe buton, altfel False.
            """
            if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
                return True
            return False

    def _human_double_move(self, pos, row, col, sign):
        """
        Functie ajutatoare pentru mutarile realizate din 2 pasi (pe diagonala)

        :param pos: lista de liste(randuri) de char - pozitia inainte de mutare
        :param row: (int) - randul pe care se afla semnul selectat pt a fi mutat
        :param col: (int) - coloana pe care se afla semnul selectat pt a fi mutat
        :param sign: (char) - "x" sau "0"

        :return new_pos: lista de liste(randuri) de char - pozitia dupa mutare
        """
        new_pos = copy.deepcopy(pos)

        GRID_WIDTH = self.WIDTH // (self.BOARD_SIZE + 1)    # avem nevoie de o coloana pentru margine
        GRID_HEIGHT = self.HEIGHT // (self.BOARD_SIZE + 1)  # avem nevoie de un rand pentru margine
        x, y = 0, 0

        margin = []
        buttons = []
        back_button = self.button(self.BTN_BG_COLOR, x, y, GRID_WIDTH, GRID_HEIGHT, "<-")

        # Generam butoanele pentru fiecare pozitie si pentru margine
        for i in range(self.BOARD_SIZE):
            x += GRID_WIDTH
            margin.append(self.button(self.BTN_ALT_COLOR, x, y, GRID_WIDTH, GRID_HEIGHT, str(i + 1)))
        y += GRID_HEIGHT
        x = 0
        for i in range(self.BOARD_SIZE):
            margin.append(self.button(self.BTN_ALT_COLOR, x, y, GRID_WIDTH, GRID_HEIGHT, str(i + 1)))
            x += GRID_WIDTH
            for j, _ in enumerate(pos):
                buttons.append(self.button(self.BTN_BG_COLOR, x, y, GRID_WIDTH, GRID_HEIGHT, info=(str(i) + "/" + str(j))))
                x += GRID_WIDTH
            y += GRID_HEIGHT
            x = 0

        while True:
            # VISUALS:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.BLACK)

            mouse_pos = pygame.mouse.get_pos()

            back_button.draw(self.WIN, self.BLACK)
            for button in margin:
                button.draw(self.WIN, self.BLACK)

            for button in buttons:
                i, j = button.info.split("/")
                if pos[int(i)][int(j)] != "#":
                    button.update_text(pos[int(i)][int(j)])
                else:
                    button.update_text("")
                button.draw(self.WIN, self.BLACK)
                if int(i) == row and int(j) == col:
                    button.draw(self.WIN, self.GREEN)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.is_over(mouse_pos):
                            i, j = button.info.split("/")
                            target_x, target_y = int(i), int(j)
                            new_pos[row][col] = "#"
                            new_pos[target_x][target_y] = sign
                            new_pos[(row + target_x) // 2][(col + target_y) // 2] = "#"
                            return new_pos

                if event.type == pygame.MOUSEMOTION:
                    for button in buttons:
                        if button.is_over(mouse_pos):
                            button.color = self.BTN_HVR_COLOR
                        else:
                            button.color = self.BTN_BG_COLOR

    def _min_max_move(self, pos, depth, sign):
        """
        Jucatorul Min-Max executa mutarea
        :param pos: lista de liste(randuri) de char
        :param sign: (char) - semnul jucatorul care muta("x" sau "0")
        :return: pos - noua pozitie, dupa efectuarea mutarii
                 int - numarul de noduri parcurse pt AI, 0 pt human
        """
        state = State(pos, sign, depth)
        state, visited_nodes = GameMechanics.min_max(state, self.estimation, sign)
        print(f"Scorul pozitiei este: {state.favourite_child.rating} !")
        return state.favourite_child.position, visited_nodes

    def _alpha_beta_move(self, pos, depth, sign):
        """
        Jucatorul Alpha-beta executa mutarea
        :param pos: lista de liste(randuri) de char
        :param sign: (char) - semnul jucatorul care muta("x" sau "0")
        :return: pos - noua pozitie, dupa efectuarea mutarii
                 int - numarul de noduri parcurse pt AI, 0 pt human
        """
        state = State(pos, sign, depth)
        state, visited_nodes = GameMechanics.alpha_beta(-500, 500, state, self.estimation, sign)
        print(f"Scorul pozitiei este: {state.favourite_child.rating} !")
        return state.favourite_child.position, visited_nodes

    def make_move(self, player, level, pos, sign):
        """
        Executa mutarea
        :param player: jucatorul care executa mutarea
        :param level: nivelul (pentru AI) de dificultate a jucatorului
        :param pos: lista de liste(randuri) de char
        :param sign: (char) - semnul jucatorul care muta("x" sau "0")
        :return: pos - noua pozitie, dupa efectuarea mutarii
                 int - numarul de noduri parcurse pt AI, 0 pt human
        """
        depth = 3
        if level == "medium":
            depth = 4
        elif level == "hard":
            depth = 5

        if player == "Min-Max":
            return self._min_max_move(pos, depth, sign)
        return self._alpha_beta_move(pos, depth, sign)

    def game(self, player_1, player_2, p1_level="human", p2_level="human"):
        """
        Jocul efectiv in GUI, cu pygame, dupa ce optiunile au fost alese.
        :param player_1: jucatorul cu semnul "x"
        :param player_2: jucatorul cu semnul "0"
        :param p1_level: nivelul de dificultate a jucatorului cu semnul "x" (pentru AI)
        :param p2_level: nivelul de dificultate a jucatorului cu semnul "0" (pentru AI)

        :return: NO RETURN ! We've passed the point of singularity...
        """
        GRID_WIDTH = self.WIDTH // (self.BOARD_SIZE + 1)    # avem nevoie de o coloana pentru margine
        GRID_HEIGHT = self.HEIGHT // (self.BOARD_SIZE + 1)  # avem nevoie de un rand pentru margine
        x, y = 0, 0

        margin = []
        buttons = []
        back_button = self.button(self.BTN_BG_COLOR, x, y, GRID_WIDTH, GRID_HEIGHT, "<-")

        # generam pozitia initiala (tabla goala)
        pos = GameMechanics.start_position(self.BOARD_SIZE)

        # Generam butoanele pentru fiecare pozitie si pentru margine
        for i in range(self.BOARD_SIZE):
            x += GRID_WIDTH
            margin.append(self.button(self.BTN_ALT_COLOR, x, y, GRID_WIDTH, GRID_HEIGHT, str(i + 1)))
        y += GRID_HEIGHT
        x = 0
        for i in range(self.BOARD_SIZE):
            margin.append(self.button(self.BTN_ALT_COLOR, x, y, GRID_WIDTH, GRID_HEIGHT, str(i + 1)))
            x += GRID_WIDTH
            for j, _ in enumerate(pos):
                buttons.append(self.button(self.BTN_BG_COLOR, x, y, GRID_WIDTH, GRID_HEIGHT, info=(str(i) + "/" + str(j))))
                x += GRID_WIDTH
            y += GRID_HEIGHT
            x = 0

        # variabile pentru joc
        player = player_1
        level = p1_level
        sign = "x"

        # variabile pentru statistici
        thinking_times = []
        depths = []

        game_over = False

        print("Este randul lui x !")

        run = True
        while run:
            # VISUALS:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.BLACK)

            mouse_pos = pygame.mouse.get_pos()

            back_button.draw(self.WIN, self.BLACK)
            for button in margin:
                button.draw(self.WIN, self.BLACK)

            for button in buttons:
                i, j = button.info.split("/")
                if pos[int(i)][int(j)] != "#":
                    button.update_text(pos[int(i)][int(j)])
                else:
                    button.update_text("")
                if button.text == "X" or button.text == "Q":
                    button.draw(self.WIN, self.RED)
                else:
                    button.draw(self.WIN, self.BLACK)

            pygame.display.update()

            # I. Player is AI
            if player != "human" and not game_over:
                start_time = int(round(time.time() * 1000))
                pos, depth = self.make_move(player, level, pos, sign)
                stop_time = int(round(time.time() * 1000))
                print(f"Jucatorul {player} a \"gandit\" timp de {stop_time - start_time} milisecunde.")
                thinking_times.append(stop_time - start_time)
                print(f"In acest timp, a luat in calcul {depth} situatii posibile")
                depths.append(depth)
                player = GameMechanics.other_thing(player, player_1, player_2)
                level = GameMechanics.other_thing(level, p1_level, p2_level)
                sign = GameMechanics.other_sign(sign)
                print(f"Este randul lui {sign} !")
            # II. Player is human
            else:
                start_time = int(round(time.time() * 1000))
                player_is_thinking = True
                while player_is_thinking:     # intram in alt loop cat timp muta jucatorul, pentru a nu reseta timerul !
                    # REMAKE VISUALS:
                    self.clock.tick(self.FPS)
                    self.WIN.fill(self.BLACK)

                    mouse_pos = pygame.mouse.get_pos()

                    back_button.draw(self.WIN, self.BLACK)
                    for button in margin:
                        button.draw(self.WIN, self.BLACK)

                    for button in buttons:
                        i, j = button.info.split("/")
                        if pos[int(i)][int(j)] != "#":
                            button.update_text(pos[int(i)][int(j)])
                        if button.text == "X" or button.text == "Q":
                            button.draw(self.WIN, self.RED)
                        else:
                            button.draw(self.WIN, self.BLACK)

                    pygame.display.update()

                    for event in pygame.event.get():

                        # Ne ocupam de Quit
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        # Facem sa mearge hover-ul
                        if event.type == pygame.MOUSEMOTION:
                            if back_button.is_over(mouse_pos):
                                back_button.color = self.BTN_HVR_COLOR
                            else:
                                back_button.color = self.BTN_BG_COLOR

                            for button in buttons:
                                if button.is_over(mouse_pos):
                                    button.color = self.BTN_HVR_COLOR
                                else:
                                    button.color = self.BTN_BG_COLOR

                        # FUNCTIONALITATEA BUTOANELOR
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # Click pe back => parasim jocul si ne intoarcem in meniu
                            if back_button.is_over(mouse_pos):
                                run = False
                                player_is_thinking = False
                                if not game_over:
                                    game_over = True
                                    print("Game aborted !")
                                    GameMechanics.statistics(player_1, player_2, thinking_times, depths)
                            # Celelalte butoane nu functioneaza daca jocul s-a terminat, astfel nu poti da click pe pozitii ca sa faci o mutare.
                            if not game_over:
                                for button in buttons:
                                    # Executarea unei mutari
                                    if button.is_over(mouse_pos):   # Cand dam click pe un buton din grid
                                        i, j = button.info.split("/")   # Salvam pozitia caruia ii corespunde acesta
                                        pos_x, pos_y = int(i), int(j)
                                        new_pos = copy.deepcopy(pos)
                                        new_pos[pos_x][pos_y] = sign
                                        # pozitia rezultata poate fi egala cu pozitia initiala numai daca la
                                        if new_pos == pos:  # coordonatele alese se afla un simbol de-al nostru
                                            new_pos = self._human_double_move(pos, pos_x, pos_y, sign)
                                            RunConsole.display_pos(pos)
                                            RunConsole.display_pos(new_pos)
                                        # Am terminat mutarea, acum ramane sa verificam daca e valida !
                                        if GameMechanics.is_legal(pos, new_pos, sign):
                                            pos = new_pos
                                            stop_time = int(round(time.time() * 1000))
                                            button.update_text(sign)
                                            print(f"Jucatorul {player} a \"gandit\" timp de {stop_time - start_time} milisecunde.")
                                            thinking_times.append(stop_time - start_time)
                                            depths.append(0)
                                            # Jucatorul uman a mutat, deci i s-a terminat randul
                                            player = GameMechanics.other_thing(player, player_1, player_2)
                                            level = GameMechanics.other_thing(level, p1_level, p2_level)
                                            sign = GameMechanics.other_sign(sign)
                                            print(f"Este randul lui {sign} !")
                                            player_is_thinking = False
                                        else:
                                            print("Illegal move !")

            # III. Jocul s-a terminat
            if GameMechanics.is_final(pos):
                game_over = True
                GameMechanics.statistics(player_1, player_2, thinking_times, depths)
                if GameMechanics.is_victory(pos):
                    # Schimbam semnul la sfarsit, dupa mutare, iar la final trebuie sa il schimbam inapoi.
                    print(f"Player {GameMechanics.other_sign(sign)} won the match !")
                elif GameMechanics.is_draw(pos):
                    print("The game is a draw !")

            # Facem interactiunea pentru Quit si hover, si butonul de back
            for event in pygame.event.get():

                # Ne ocupam de Quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Facem sa mearge hover-ul
                if event.type == pygame.MOUSEMOTION:
                    if back_button.is_over(mouse_pos):
                        back_button.color = self.BTN_HVR_COLOR
                    else:
                        back_button.color = self.BTN_BG_COLOR

                    for button in buttons:
                        if button.is_over(mouse_pos):
                            button.color = self.BTN_HVR_COLOR
                        else:
                            button.color = self.BTN_BG_COLOR

                # FUNCTIONALITATEA BUTOANELOR
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Click pe back => parasim jocul si ne intoarcem in meniu
                    if back_button.is_over(mouse_pos):
                        run = False

    def main_menu(self):
        """
        Meniul principal al jocului in fereastra pygame
        :return: No return
        """
        PvAI_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//7 * 2 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Player vs AI")
        PvP_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//7 * 3 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Player vs Player")
        AIvAI_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//7 * 4 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "AI vs AI")
        board_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//7 * 5 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT,
                                   "Set board size: " + str(self.BOARD_SIZE) + "*" + str(self.BOARD_SIZE))
        exit_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//7 * 6 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Exit")
        
        while True:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.BLACK)
            board_button.update_text("Set board size: " +
                                     str(self.BOARD_SIZE) + "*" + str(self.BOARD_SIZE))
            mouse_pos = pygame.mouse.get_pos()
            
            PvAI_button.draw(self.WIN)
            PvP_button.draw(self.WIN)
            AIvAI_button.draw(self.WIN)
            board_button.draw(self.WIN)
            exit_button.draw(self.WIN)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PvAI_button.is_over(mouse_pos):
                        self.PvAI_menu()
                        
                    if PvP_button.is_over(mouse_pos):
                        self.PvP_menu()
                        
                    if AIvAI_button.is_over(mouse_pos):
                        self.AIvAI_menu()
                        
                    if board_button.is_over(mouse_pos):
                        self.board_menu()
                        
                    if exit_button.is_over(mouse_pos):
                        pygame.quit()
                        sys.exit()
                
                if event.type == pygame.MOUSEMOTION:
                    if PvAI_button.is_over(mouse_pos):
                        PvAI_button.color = self.BTN_HVR_COLOR
                    else:
                        PvAI_button.color = self.BTN_BG_COLOR
                    
                    if PvP_button.is_over(mouse_pos):
                        PvP_button.color = self.BTN_HVR_COLOR
                    else:
                        PvP_button.color = self.BTN_BG_COLOR
                        
                    if AIvAI_button.is_over(mouse_pos):
                        AIvAI_button.color = self.BTN_HVR_COLOR
                    else:
                        AIvAI_button.color = self.BTN_BG_COLOR
                        
                    if board_button.is_over(mouse_pos):
                        board_button.color = self.BTN_HVR_COLOR
                    else:
                        board_button.color = self.BTN_BG_COLOR
                        
                    if exit_button.is_over(mouse_pos):
                        exit_button.color = self.BTN_HVR_COLOR
                    else:
                        exit_button.color = self.BTN_BG_COLOR

    def PvAI_menu(self):
        """
        Submeniul "Player vs AI" al jocului in fereastra pygame
        :return: No return
        """
        play_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//8 * 2 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Play !")
        set_sign_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//8 * 3 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Sign: " + self.sign)
        opponent_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//8 * 4 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Opponent: " + self.opponent)
        difficulty_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//8 * 5 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Difficulty: " + self.difficulty1)
        estimation_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//8 * 6 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Score estimation: " + self.estimation)
        back_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//8 * 7 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Back")
        
        run = True
        while run:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.BLACK)
            set_sign_button.update_text("Sign: " + self.sign)
            opponent_button.update_text("Opponent: " + self.opponent)
            difficulty_button.update_text("Difficulty: " + self.difficulty1)
            estimation_button.update_text("Score estimation: " + self.estimation)
            mouse_pos = pygame.mouse.get_pos()
            
            play_button.draw(self.WIN)
            set_sign_button.draw(self.WIN)
            opponent_button.draw(self.WIN)
            difficulty_button.draw(self.WIN)
            estimation_button.draw(self.WIN)
            back_button.draw(self.WIN)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_over(mouse_pos):
                        if self.sign == "x":
                            self.game("human", self.opponent, p2_level=self.difficulty1)
                        else:
                            self.game(self.opponent, "human", p1_level=self.difficulty1)

                    if set_sign_button.is_over(mouse_pos):
                        self.sign_menu()
                        
                    if opponent_button.is_over(mouse_pos):
                        self.opponent_menu()
                        
                    if difficulty_button.is_over(mouse_pos):
                        self.difficulty1_menu()
                        
                    if estimation_button.is_over(mouse_pos):
                        self.estimation_menu()
                        
                    if back_button.is_over(mouse_pos):
                        run = False
                
                if event.type == pygame.MOUSEMOTION:
                    if play_button.is_over(mouse_pos):
                        play_button.color = self.BTN_HVR_COLOR
                    else:
                        play_button.color = self.BTN_BG_COLOR
                    
                    if set_sign_button.is_over(mouse_pos):
                        set_sign_button.color = self.BTN_HVR_COLOR
                    else:
                        set_sign_button.color = self.BTN_BG_COLOR
                        
                    if opponent_button.is_over(mouse_pos):
                        opponent_button.color = self.BTN_HVR_COLOR
                    else:
                        opponent_button.color = self.BTN_BG_COLOR
                        
                    if difficulty_button.is_over(mouse_pos):
                        difficulty_button.color = self.BTN_HVR_COLOR
                    else:
                        difficulty_button.color = self.BTN_BG_COLOR
                        
                    if estimation_button.is_over(mouse_pos):
                        estimation_button.color = self.BTN_HVR_COLOR
                    else:
                        estimation_button.color = self.BTN_BG_COLOR
                        
                    if back_button.is_over(mouse_pos):
                        back_button.color = self.BTN_HVR_COLOR
                    else:
                        back_button.color = self.BTN_BG_COLOR

    def PvP_menu(self):
        """
        Submeniul "Player vs Player" al jocului in fereastra pygame
        :return: No return
        """
        play_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//4 * 2 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Play !")
        back_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//4 * 3 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Back")
        
        run = True
        while run:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.BLACK)
            
            mouse_pos = pygame.mouse.get_pos()
            
            play_button.draw(self.WIN)
            back_button.draw(self.WIN)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_over(mouse_pos):
                        self.game("human", "human")
                        
                    if back_button.is_over(mouse_pos):
                        run = False
                
                if event.type == pygame.MOUSEMOTION:
                    if play_button.is_over(mouse_pos):
                        play_button.color = self.BTN_HVR_COLOR
                    else:
                        play_button.color = self.BTN_BG_COLOR
                        
                    if back_button.is_over(mouse_pos):
                        back_button.color = self.BTN_HVR_COLOR
                    else:
                        back_button.color = self.BTN_BG_COLOR

    def AIvAI_menu(self):
        """
        Submeniul "AI vs AI" al jocului in fereastra pygame
        :return: No return
        """
        play_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 2 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Play !")
        details_button = self.button(self.BTN_ALT_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 3 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT,
                                     "Min-Max: " + self.sign + " Alpha-beta: " + GameMechanics.other_sign(self.sign))
        set_sign_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 4 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Switch signs")
        difficulty1_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 5 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Min-Max: " + self.difficulty1)
        difficulty2_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 6 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Alpha-beta: " + self.difficulty2)
        estimation_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 7 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Score estimation: " + self.estimation)
        back_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 8 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Back")
        
        run = True
        while run:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.BLACK)
            details_button.update_text("Min-Max: " + self.sign + " Alpha-beta: " + GameMechanics.other_sign(self.sign))
            difficulty1_button.update_text("Min-Max: " + self.difficulty1)
            difficulty2_button.update_text("Alpha-beta: " + self.difficulty2)
            estimation_button.update_text("Score estimation: " + self.estimation)
            mouse_pos = pygame.mouse.get_pos()
            
            play_button.draw(self.WIN)
            details_button.draw(self.WIN)
            set_sign_button.draw(self.WIN)
            difficulty1_button.draw(self.WIN)
            difficulty2_button.draw(self.WIN)
            estimation_button.draw(self.WIN)
            back_button.draw(self.WIN)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_over(mouse_pos):
                        if self.sign == "x":
                            self.game("Min-Max", "Alpha-beta", p1_level=self.difficulty1, p2_level=self.difficulty2)
                        else:
                            self.game("Alpha-beta", "Min-Max", p1_level=self.difficulty2, p2_level=self.difficulty1)
                        
                    if set_sign_button.is_over(mouse_pos):
                        self.sign = GameMechanics.other_sign(self.sign)
                        
                    if difficulty1_button.is_over(mouse_pos):
                        self.difficulty1_menu()
                        
                    if difficulty2_button.is_over(mouse_pos):
                        self.difficulty2_menu()
                        
                    if estimation_button.is_over(mouse_pos):
                        self.estimation_menu()
                        
                    if back_button.is_over(mouse_pos):
                        run = False
                
                if event.type == pygame.MOUSEMOTION:
                    if play_button.is_over(mouse_pos):
                        play_button.color = self.BTN_HVR_COLOR
                    else:
                        play_button.color = self.BTN_BG_COLOR
                    
                    if set_sign_button.is_over(mouse_pos):
                        set_sign_button.color = self.BTN_HVR_COLOR
                    else:
                        set_sign_button.color = self.BTN_BG_COLOR
                        
                    if difficulty1_button.is_over(mouse_pos):
                        difficulty1_button.color = self.BTN_HVR_COLOR
                    else:
                        difficulty1_button.color = self.BTN_BG_COLOR
                        
                    if difficulty2_button.is_over(mouse_pos):
                        difficulty2_button.color = self.BTN_HVR_COLOR
                    else:
                        difficulty2_button.color = self.BTN_BG_COLOR
                        
                    if estimation_button.is_over(mouse_pos):
                        estimation_button.color = self.BTN_HVR_COLOR
                    else:
                        estimation_button.color = self.BTN_BG_COLOR
                        
                    if back_button.is_over(mouse_pos):
                        back_button.color = self.BTN_HVR_COLOR
                    else:
                        back_button.color = self.BTN_BG_COLOR

    def sign_menu(self):
        """
        Submeniul optiunii de alegere a simbolului ("x" sau "0") jocului in fereastra pygame
        :return: No return
        """
        x_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//5 * 2 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "x")
        zero_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//5 * 3 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "0")
        back_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//5 * 4 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Back")
        
        run = True
        while run:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.BLACK)
            
            mouse_pos = pygame.mouse.get_pos()
            
            x_button.draw(self.WIN)
            zero_button.draw(self.WIN)
            back_button.draw(self.WIN)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if x_button.is_over(mouse_pos):
                        self.sign = "x"
                        run = False
                        
                    if zero_button.is_over(mouse_pos):
                        self.sign = "0"
                        run = False
                        
                    if back_button.is_over(mouse_pos):
                        run = False
                
                if event.type == pygame.MOUSEMOTION:
                    if x_button.is_over(mouse_pos):
                        x_button.color = self.BTN_HVR_COLOR
                    else:
                        x_button.color = self.BTN_BG_COLOR
                    
                    if zero_button.is_over(mouse_pos):
                        zero_button.color = self.BTN_HVR_COLOR
                    else:
                        zero_button.color = self.BTN_BG_COLOR
                        
                    if back_button.is_over(mouse_pos):
                        back_button.color = self.BTN_HVR_COLOR
                    else:
                        back_button.color = self.BTN_BG_COLOR

    def opponent_menu(self):
        """
        Submeniul optiunii de alegere a oponentului (Min-Max sau Alpha-beta) jocului in fereastra pygame
        :return: No return
        """
        Min_Max_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//5 * 2 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Min-Max")
        Alpha_beta_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//5 * 3 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Alpha-beta")
        back_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//5 * 4 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Back")
        
        run = True
        while run:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.BLACK)
            
            mouse_pos = pygame.mouse.get_pos()
            
            Min_Max_button.draw(self.WIN)
            Alpha_beta_button.draw(self.WIN)
            back_button.draw(self.WIN)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Min_Max_button.is_over(mouse_pos):
                        self.opponent = "Min-Max"
                        run = False
                        
                    if Alpha_beta_button.is_over(mouse_pos):
                        self.opponent = "Alpha-beta"
                        run = False
                        
                    if back_button.is_over(mouse_pos):
                        run = False
                
                if event.type == pygame.MOUSEMOTION:
                    if Min_Max_button.is_over(mouse_pos):
                        Min_Max_button.color = self.BTN_HVR_COLOR
                    else:
                        Min_Max_button.color = self.BTN_BG_COLOR
                    
                    if Alpha_beta_button.is_over(mouse_pos):
                        Alpha_beta_button.color = self.BTN_HVR_COLOR
                    else:
                        Alpha_beta_button.color = self.BTN_BG_COLOR
                        
                    if back_button.is_over(mouse_pos):
                        back_button.color = self.BTN_HVR_COLOR
                    else:
                        back_button.color = self.BTN_BG_COLOR

    def difficulty1_menu(self):
        """
        Submeniul optiunii de alegere a dificultatii oponentului (la Player vs AI)
         sau dificultatii lui Min-Max (la AI vs AI) a jocului in fereastra pygame
        :return: No return
        """
        easy_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//6 * 2 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Easy")
        medium_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//6 * 3 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Medium")
        hard_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//6 * 4 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Hard")
        back_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//6 * 5 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Back")
        
        run = True
        while run:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.BLACK)
            
            mouse_pos = pygame.mouse.get_pos()
            
            easy_button.draw(self.WIN)
            medium_button.draw(self.WIN)
            hard_button.draw(self.WIN)
            back_button.draw(self.WIN)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.is_over(mouse_pos):
                        self.difficulty1 = "Easy"
                        run = False
                        
                    if medium_button.is_over(mouse_pos):
                        self.difficulty1 = "Medium"
                        run = False
                        
                    if hard_button.is_over(mouse_pos):
                        self.difficulty1 = "Hard"
                        run = False
                        
                    if back_button.is_over(mouse_pos):
                        run = False
                
                if event.type == pygame.MOUSEMOTION:
                    if easy_button.is_over(mouse_pos):
                        easy_button.color = self.BTN_HVR_COLOR
                    else:
                        easy_button.color = self.BTN_BG_COLOR
                    
                    if medium_button.is_over(mouse_pos):
                        medium_button.color = self.BTN_HVR_COLOR
                    else:
                        medium_button.color = self.BTN_BG_COLOR
                    
                    if hard_button.is_over(mouse_pos):
                        hard_button.color = self.BTN_HVR_COLOR
                    else:
                        hard_button.color = self.BTN_BG_COLOR
                        
                    if back_button.is_over(mouse_pos):
                        back_button.color = self.BTN_HVR_COLOR
                    else:
                        back_button.color = self.BTN_BG_COLOR

    def difficulty2_menu(self):
        """
        Submeniul optiunii de alegere a dificultatii lui Alpha-beta (la AI vs AI) a jocului in fereastra pygame
        :return: No return
        """
        easy_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//6 * 2 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Easy")
        medium_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//6 * 3 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Medium")
        hard_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//6 * 4 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Hard")
        back_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//6 * 5 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Back")
        
        run = True
        while run:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.BLACK)
            
            mouse_pos = pygame.mouse.get_pos()
            
            easy_button.draw(self.WIN)
            medium_button.draw(self.WIN)
            hard_button.draw(self.WIN)
            back_button.draw(self.WIN)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.is_over(mouse_pos):
                        self.difficulty2 = "Easy"
                        run = False
                        
                    if medium_button.is_over(mouse_pos):
                        self.difficulty2 = "Medium"
                        run = False
                        
                    if hard_button.is_over(mouse_pos):
                        self.difficulty2 = "Hard"
                        run = False
                        
                    if back_button.is_over(mouse_pos):
                        run = False
                
                if event.type == pygame.MOUSEMOTION:
                    if easy_button.is_over(mouse_pos):
                        easy_button.color = self.BTN_HVR_COLOR
                    else:
                        easy_button.color = self.BTN_BG_COLOR
                    
                    if medium_button.is_over(mouse_pos):
                        medium_button.color = self.BTN_HVR_COLOR
                    else:
                        medium_button.color = self.BTN_BG_COLOR
                    
                    if hard_button.is_over(mouse_pos):
                        hard_button.color = self.BTN_HVR_COLOR
                    else:
                        hard_button.color = self.BTN_BG_COLOR
                        
                    if back_button.is_over(mouse_pos):
                        back_button.color = self.BTN_HVR_COLOR
                    else:
                        back_button.color = self.BTN_BG_COLOR

    def estimation_menu(self):
        """
        Submeniul optiunii de alegere a estimarii folosite de AI a jocului in fereastra pygame
        :return: No return
        """
        E1_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//5 * 2 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "E1")
        E2_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//5 * 3 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "E2")
        back_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//5 * 4 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Back")
        
        run = True
        while run:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.BLACK)
            
            mouse_pos = pygame.mouse.get_pos()
            
            E1_button.draw(self.WIN)
            E2_button.draw(self.WIN)
            back_button.draw(self.WIN)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if E1_button.is_over(mouse_pos):
                        self.estimation = "E1"
                        run = False
                        
                    if E2_button.is_over(mouse_pos):
                        self.estimation = "E2"
                        run = False
                        
                    if back_button.is_over(mouse_pos):
                        run = False
                
                if event.type == pygame.MOUSEMOTION:
                    if E1_button.is_over(mouse_pos):
                        E1_button.color = self.BTN_HVR_COLOR
                    else:
                        E1_button.color = self.BTN_BG_COLOR
                    
                    if E2_button.is_over(mouse_pos):
                        E2_button.color = self.BTN_HVR_COLOR
                    else:
                        E2_button.color = self.BTN_BG_COLOR
                        
                    if back_button.is_over(mouse_pos):
                        back_button.color = self.BTN_HVR_COLOR
                    else:
                        back_button.color = self.BTN_BG_COLOR

    def board_menu(self):
        """
        Submeniul optiunii de alegere a dimensiunii tablei a jocului in fereastra pygame
        :return: No return
        """
        five_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 2 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "5*5")
        six_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 3 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "6*6")
        seven_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 4 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "7*7")
        eight_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 5 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "8*8")
        nine_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 6 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "9*9")
        ten_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 7 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "10*10")
        back_button = self.button(self.BTN_BG_COLOR, (self.WIDTH - self.BTN_WIDTH) // 2, (self.HEIGHT//9 * 8 - self.BTN_HEIGHT), self.BTN_WIDTH, self.BTN_HEIGHT, "Back")
        
        run = True
        while run:
            self.clock.tick(self.FPS)
            self.WIN.fill(self.BLACK)
            
            mouse_pos = pygame.mouse.get_pos()
            
            five_button.draw(self.WIN)
            six_button.draw(self.WIN)
            seven_button.draw(self.WIN)
            eight_button.draw(self.WIN)
            nine_button.draw(self.WIN)
            ten_button.draw(self.WIN)
            back_button.draw(self.WIN)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if five_button.is_over(mouse_pos):
                        self.BOARD_SIZE = 5
                        run = False
                        
                    if six_button.is_over(mouse_pos):
                        self.BOARD_SIZE = 6
                        run = False
                        
                    if seven_button.is_over(mouse_pos):
                        self.BOARD_SIZE = 7
                        run = False
                        
                    if eight_button.is_over(mouse_pos):
                        self.BOARD_SIZE = 8
                        run = False
                        
                    if nine_button.is_over(mouse_pos):
                        self.BOARD_SIZE = 9
                        run = False
                        
                    if ten_button.is_over(mouse_pos):
                        self.BOARD_SIZE = 10
                        run = False
                        
                    if back_button.is_over(mouse_pos):
                        run = False
                
                if event.type == pygame.MOUSEMOTION:
                    if five_button.is_over(mouse_pos):
                        five_button.color = self.BTN_HVR_COLOR
                    else:
                        five_button.color = self.BTN_BG_COLOR
                    
                    if six_button.is_over(mouse_pos):
                        six_button.color = self.BTN_HVR_COLOR
                    else:
                        six_button.color = self.BTN_BG_COLOR
                    
                    if seven_button.is_over(mouse_pos):
                        seven_button.color = self.BTN_HVR_COLOR
                    else:
                        seven_button.color = self.BTN_BG_COLOR
                    
                    if eight_button.is_over(mouse_pos):
                        eight_button.color = self.BTN_HVR_COLOR
                    else:
                        eight_button.color = self.BTN_BG_COLOR
                    
                    if nine_button.is_over(mouse_pos):
                        nine_button.color = self.BTN_HVR_COLOR
                    else:
                        nine_button.color = self.BTN_BG_COLOR
                    
                    if ten_button.is_over(mouse_pos):
                        ten_button.color = self.BTN_HVR_COLOR
                    else:
                        ten_button.color = self.BTN_BG_COLOR
                        
                    if back_button.is_over(mouse_pos):
                        back_button.color = self.BTN_HVR_COLOR
                    else:
                        back_button.color = self.BTN_BG_COLOR


def main():
    launcher_exe()


if __name__ == "__main__":
    main()
