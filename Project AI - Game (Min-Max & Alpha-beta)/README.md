# Barem

Rezolvati problema urmatoare folosind algoritmii:

 - min-max
 - alpha-beta

Toate cerintele se rezolva **intr-un singur fisier python**.

### Linkuri utile

- https://repl.it/@IrinaCiocan/xsi0exemplu#main.py
- https://repl.it/@IrinaCiocan/x-si-0-interf-grafica#main.py
- https://replit.com/@IrinaCiocan/4inline-interfatagrafica (aici aveti exemplul cu butoanele de la inceput, cum trebuie sa faceti voi in tema)
- https://replit.com/@IrinaCiocan/interfata-joc-celule-ziduri
- https://replit.com/@IrinaCiocan/interfata-joc-graf
- Hint: pentru calcularea statisticilor legate de numarul de noduri si de timpi, veti face cate un vector pentru fiecare tip de date (un vector cu toti timpii, un vector cu toate numerele de noduri) Pentru calcularea medianei puteti folosi: https://docs.python.org/3/library/statistics.html#statistics.median

### **Mod de punctare** (punctajul e dat in procentaje din punctajul maxim al temei; procentajul maxim este 100%):

1. (5%) Să se păstreze următoare lucruri deja implementate în exemplu (sau să se implementeze daca cineva decide să refacă programul de la zero):
  - La inceputul programului utilizatorul va fi intrebat ce algoritm doreste sa foloseasca (minimax sau alpha-beta)
  - Utilizatorul va fi întrebat cu ce simbol sa joace (la jocurile unde are sens aceasta intrebare)
  - Se va încerca evitarea sau tratarea situației în care utilizatorul ar putea răspunde greșit (de exemplu, nu poate selecta decât opțiunile corecte dintre care sunt selectate valorile default; sau, unde nu se poate așa ceva, jocul nu pornește până nu se primește un răspuns corect).
  - Afisarea a cui este rândul să mute.
  - Indicarea, la finalul jocului, a câstigatorului sau a remizei daca este cazul.
2. (5%) Utilizatorul va fi întrebat care sa fie nivelul de dificultate a jocului (incepator, mediu, avansat). In functie de nivelul ales se va seta adancimea arborelui de mutari (cu cat nivelul ales e mai mare, cu atat adancimea trebuie sa fie mai mare ca sa fie mai precisa predictia jocului). Posibilitatea utilizatorului de a face eventuale alte setări cerute de enunț. Se va verifica dacă utilizatorul a oferit un input corect, iar dacă nu se va trata acest caz (i se poate reafișa ecranul cu setările afișând și un mesaj de atenționare cu privire la inputul greșit).
3. (5%) Generarea starii initiale
4. (10%) Desenarea tablei de joc (interfața grafică) si afișarea în consolă a tablei (pentru debug; în ce format vreți voi). Titlul ferestrei de joc va fi numele vostru + numele jocului.
5. (15%) Functia de generare a mutarilor (succesorilor) + eventuala functie de testare a validitatii unei mutari (care poate fi folosita si pentru a verifica mutarea utilizatorului)
6. (5%) Realizarea mutarii utilizatorului. Utilizatorul va realiza un eveniment în interfață pentru a muta (de exemplu, click). Va trebui verificata corectitudinea mutarilor utilizatorului: nu a facut o mutare invalida.
7. (10%) Functia de testare a starii finale, stabilirea castigatorului și, dacă e cazul conform cerinței, calcularea scorului. Se va marca în interfața grafică configurația câștigătoare (sau simbolurile câștigătoare, în funcție de regulile jocului). Marcarea se poate face colorând, de exemplu, simbolurile sau culoare de fundal a eventualelor căsuțe în care se află.
8. (20%=10+10) Doua moduri diferite de estimare a scorului (pentru stari care nu sunt inca finale)
9. (15% impărtit după cum urmează) Afisari (în consolă).<br>
  a. (5%) Afisarea timpului de gandire, dupa fiecare mutare, atat pentru calculator (deja implementat în exemplu) cat si pentru utilizator. Pentru timpul de găndire al calculatorului: afișarea la final a timpului minim, maxim, mediu și a medianei.<br>
  b. (2%) Afișarea scorurilor (dacă jocul e cu scor), atat pentru jucator cat si pentru calculator și a estimărilor date de minimax și alpha-beta (estimarea pentru rădacina arborelui; deci cât de favorabilă e configurația pentru calculator, în urma mutării sale - nu se va afișa estimarea și când mută utilizatorul).<br>
  c. (5%) Afișarea numărului de noduri generate (în arborele minimax, respectiv alpha-beta) la fiecare mutare. La final se va afișa numărul minim, maxim, mediu și mediana pentru numarul de noduri generat pentru fiecare mutare.<br>
  d. (3%) Afisarea timpului final de joc (cat a rulat programul) si a numarului total de mutari atat pentru jucator cat si pentru calculator (la unele jocuri se mai poate sari peste un rand și atunci să difere numărul de mutări).
10. (5%) La fiecare mutare utilizatorul sa poata si sa opreasca jocul daca vrea, caz in care se vor afisa toate informațiile cerute pentru finalul jocului ( scorul lui si al calculatorului,numărul minim, maxim, mediu și mediana pentru numarul de noduri generat pentru fiecare mutare, timpul final de joc și a numarului total de mutari atat pentru jucator cat si pentru calculator) Punctajul pentru calcularea efectivă a acestor date e cel de mai sus; aici se punctează strict afișarea lor în cazul cerut.
11. (5%) Comentarii. Explicarea algoritmului de generare a mutarilor, explicarea estimarii scorului si dovedirea faptului ca ordoneaza starile cu adevarat in functie de cat de prielnice ii sunt lui MAX (nu trebuie demonstratie matematica, doar explicat clar). Explicarea pe scurt a fiecarei functii si a parametrilor.
12. **Bonus (10%)**. Ordonarea succesorilor înainte de expandare (bazat pe estimare) astfel încât alpha-beta să taie cât mai mult din arbore.
13. **Bonus (20%)**. Opțiuni în meniu (cu butoane adăugate) cu:
  - Jucator vs jucător
  - Jucător vs calculator (selectată default)
  - Calculator (cu prima funcție de estimare) vs calculator (cu a doua funcție de estimare)
**Tema nu se puncteaza fara prezentare**. Se va da o nota pe prezentare de la 1 la 10 in functie de cat de bine a stiut studentul sa explice ce a facut. Punctajul temei se va inmulti cu nota_prezentare/10. Astfel, daca cineva stie sa explice doar jumatate din ce a facut, primeste jumatate din punctaj; daca nu stie nimic primeste 0.

**Temele copiate duc la anularea notei atat pentru cel care a dat tema cat si pentru cel care a copiat, iar numele studentilor cu aceasta problema vor fi comunicate profesorului titular de curs.**

------------

# Cerinta:

**Atentie! acest exercitiu necesita prezentare!**
- Se va implementa urmatorul joc:
- Jocul se desfasoara pe un grid NxN cu 5≤N≤10 (utilizatorul va fi întrebat în legătură cu dimensiunea tablei).
- Este turn based
- Un jucator foloseste simbolul x si celalalt 0 ( o sa ii numim pe scurt jucatorii x si 0)
- Jucatorul x pune simbolul primul pe tabla.
- Mutarile sunt de doua feluri:
  - punerea unui simbol intr-un loc gol
  - saltul peste un simbol (in stilul jocului dame). Un jucator poate sari peste simbolul unui alt jucator doar pe diagonala, daca pe acea diagonala, imediat dupa simbolul jucatorului e un loc liber. Totusi, la urmatoarea mutare jucatorul opus nu are voie sa puna simbolul in locul de unde a fost luat. De exemplu, pentru x-ul marcat cu verde din imaginea de mai jos sunt marcate cu o culoare gălbuie locurile posibile în care poate face salt pentru a captura un 0: ![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
  - Scopul jocului este sa se creeze o configuratie de 4 simboluri vecine toate intre ele doua cate doua (practic formand un "patrat" de simboluri). De exemplu: ![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
  - La afișarea gridului în consolă, se vor afișa în dreptul liniilor și coloanelor și numerele lor (indicii începând de la 0) ca să poată identifica utilizatorul mai ușor coordonatele locului în care vrea să mute.
