# RED TEAM #2 — DEC-032

## Definiția frontului de flacără | GFL / B6

RED TEAM — Critical Review

DEC-032 nesemnat

5 noiembrie 2026

Rol: Scientific Advisor / Independent Red Team — Combustion Science, fizica flăcării, analiză radiometrică, procesare de imagini și statistică experimentală.

Nu coordonez proiectul, nu aprob decizii și nu înlocuiesc autoritatea Owner-ului. Rolul meu este să identific punctele în care o concluzie poate fi atacată științific, inclusiv atunci când concluzia pare convenabilă.

Voi respecta cele patru niveluri de evidență și voi separa observațiile, inferențele și propunerile noi.

# 0. Verdict preliminar

DEC-032: NU RECOMAND SEMNAREA ÎN FORMA ACTUALĂ

Nu pentru că propunerea este fundamental greșită, ci pentru că rezolvă o problemă — sensibilitatea la expunere — introducând o altă problemă care nu este încă suficient investigată: dependența frontului detectat de distribuția spațială a intensității flăcării.

Cele trei elemente ale DEC-032 trebuie evaluate separat:

| Element                                      | Evaluarea mea                                                                    |
| -------------------------------------------- | -------------------------------------------------------------------------------- |
| Prag relativ la maximul fiecărui cadru       | Promițător, dar vulnerabil la schimbarea formei flăcării                         |
| Rate separate pe intervale cu debit constant | Corect metodologic în principiu, condiționat de existența unor intervale stabile |
| Pragurile 0,05 / 0,1 / 0,2                   | Necesită justificare independentă și analiză de sensibilitate                    |

Observația cea mai importantă:

Avem acum dovezi că rezultatul depinde de definiția operațională a frontului. Nu avem încă dovezi că una dintre definiții identifică mai fidel frontul fizic al flăcării.

Această diferență este fundamentală.

O precizie numerică mai bună nu înseamnă automat o măsurare fizică mai bună.

# 1. Ce știm efectiv despre B6

Mai întâi, separăm proveniența informațiilor.

### 1.1. Situația probelor

| Afirmație                                             | Statut                                                     |
| ----------------------------------------------------- | ---------------------------------------------------------- |
| ISO 1000 și f/2 fixe                                  | [RAPORTAT DE SURSĂ: verificarea PM pe imaginile originale] |
| Expunere 1/60 → 1/400 s                               | [RAPORTAT DE SURSĂ: verificarea PM]                        |
| Creștere de 6,3× a radianței maxime normalizate       | [RAPORTAT DE SURSĂ: analiza PM]                            |
| Corelație cu timpul 0,93                              | [RAPORTAT DE SURSĂ: analiza PM]                            |
| Rate 2,21–2,42 mm/s cu prag fix                       | [RAPORTAT DE SURSĂ: analiza PM]                            |
| Rate 2,07–2,20 mm/s cu prag relativ per cadru         | [RAPORTAT DE SURSĂ: analiza PM]                            |
| Rate 2,17 și 1,97 mm/s pentru indicatorii alternativi | [RAPORTAT DE SURSĂ: analiza PM]                            |
| Corectitudinea fizică a noii definiții                | [NECUNOSCUT]                                               |

Nu am acces, în acest moment, la imaginile originale, matricele de pixeli, fișierul de analiză radiometrică și timestampurile brute pentru a reproduce independent calculele.

Prin urmare, nu voi transforma verificările PM în verificări experimentale independente ale mele.

### 1.2. O observație statistică importantă

Diferența dintre extremele raportate pentru pragul relativ per cadru este:

\\[ \Delta v=2.20-2.07=0.13\\;mm/s \\]

Raportată la valoarea minimă:

\\[ \frac{0.13}{2.07}\times100\approx6.28\\% \\]

[INFERENȚĂ] Sensibilitatea observată la alegerea pragului este de aproximativ 6,3% pe intervalul analizat.

Dar aceasta nu este o incertitudine totală de măsurare.

Nu include automat:

- incertitudinea scalei spațiale;
- incertitudinea timestampurilor;
- erorile de segmentare;
- dependența temporală dintre cadre;
- incertitudinea regresiei;
- erorile radiometrice.

Nu putem prezenta încă 2,07–2,20 mm/s ca interval de încredere.

# 2. Obiecția majoră: normalizarea per cadru poate ascunde modificarea formei flăcării

OBIECȚIA #1 — FUNDAMENTALĂ

Aceasta este problema pe care o consider cea mai importantă din DEC-032.

## 2.1. Ce face matematic propunerea

Definim intensitatea unui pixel:

\\[ I(x,y,t) \\]

Iar maximul cadrului:

\\[ I\_{\max}(t)=\max\_{x,y} I(x,y,t) \\]

Pragul relativ devine:

\\[ I(x,y,t)\geq\alpha I\_{\max}(t) \\]

unde:

\\[ \alpha\in\\{0.05,0.1,0.2\\} \\]

Poziția frontului este ultima coloană care satisface condiția.

Simplificat:

\\[ x_f(t,\alpha)= \max\left\\{ x:\max_y I(x,y,t)\geq\alpha I\_{\max}(t) \right\\} \\]

Avantajul este evident: dacă intensitatea întregii flăcări crește proporțional, pragul se adaptează.

Dar există o presupunere implicită:

Distribuția relativă a intensității în interiorul flăcării trebuie să rămână suficient de stabilă.

Nu avem încă demonstrația acestei presupuneri.

## 2.2. De ce schimbarea formei poate introduce o eroare

Să considerăm două situații.

Situația A — flacără cu formă relativ stabilă

Dacă forma și profilul relativ rămân stabile, pragurile relative pot urmări aceeași evoluție generală.

Situația B — flacăra își schimbă geometria și distribuția luminozității

Dacă profilul luminos se modifică, pozițiile pragurilor pot evolua diferit chiar dacă emisia totală crește.

[INFERENȚĂ] În al doilea caz, pragul relativ nu mai urmărește doar creșterea flăcării. Urmărește și schimbarea formei distribuției luminoase.

Mai există o problemă subtilă.

Normalizarea la maximul cadrului poate fi afectată de un punct luminos local, care nu reprezintă neapărat evoluția întregului corp al flăcării.

Dacă acel punct își schimbă intensitatea, toate pragurile se modifică simultan.

Asta înseamnă că denominatorul poate introduce o dependență artificială între zone diferite ale imaginii.

## 2.3. Este creșterea monotonă a ratei cu pragul un indiciu?

Avem:

| Prag | Rată raportată        |
| ---- | --------------------- |
| 0,05 | 2,07 mm/s             |
| 0,10 | În curs de verificare |
| 0,20 | În curs de verificare |
| 0,50 | 2,20 mm/s             |

[VERIFICAT MATEMATIC, condiționat de valorile raportate] Rata crește monoton între extremele furnizate.

[INFERENȚĂ] Acest comportament este compatibil cu o evoluție diferită a nucleului luminos față de anvelopa exterioară a flăcării.

Dar nu demonstrează că aceasta este cauza.

Alte explicații posibile:

- profilul luminos se deplasează;
- gradientul de intensitate se modifică;
- flacăra își schimbă lungimea;
- flacăra își schimbă lățimea;
- zona luminoasă maximă migrează;
- există o combinație între efectele radiometrice și cele geometrice.

Verdict: monotonicitatea este un semnal care justifică investigația, nu o demonstrație a unei erori.

## 2.4. Testul care poate tranșa problema

IDEA-032-A — Shape/Amplitude Decomposition

Aș introduce o analiză în două componente.

Pornim de la imaginea corectată de fundal:

\\[ I'(x,y,t)=I(x,y,t)-B(x,y,t) \\]

Apoi:

\\[ I'(x,y,t)=A(t)\cdot P(x,y,t) \\]

unde:

- \\(A(t)\\) reprezintă amplitudinea luminoasă;
- \\(P(x,y,t)\\) reprezintă distribuția spațială normalizată.

Nu pretind că această descompunere este automat o separare fizică perfectă. Este un instrument de diagnostic.

Testul 1 — Amplitude-only

Păstrăm forma distribuției spațiale și modificăm numai amplitudinea.

Dacă normalizarea per cadru funcționează așa cum presupunem, poziția frontului la un prag relativ trebuie să rămână neschimbată.

Testul 2 — Shape-only

Comparăm distribuțiile normalizate ale cadrelor succesive.

Măsurăm:

- lungimea anvelopei;
- lățimea flăcării;
- aria zonei luminoase;
- poziția centrului de intensitate;
- distribuția intensității de-a lungul axei;
- poziția frontului la fiecare prag.

Testul 3 — Interaction

Estimăm:

\\[ v_f=f(\alpha,Q,\alpha\times Q) \\]

unde \\(Q\\) este debitul aerului.

Dacă interacțiunea prag–debit este importantă, definiția frontului este dependentă de regimul de curgere.

Acesta ar fi un rezultat mult mai interesant decât simpla alegere a pragului care produce rata dorită.

# 3. Obiecția #2 — Creșterea de 6,3×: emisie reală sau artefact radiometric?

OBIECȚIA #2 — CRITICĂ

Aici avem un element care mă face să opresc orice concluzie prematură.

Camera a trecut de la:

\\[ t_1=1/60\\;s \\]

la:

\\[ t_2=1/400\\;s \\]

Raportul este:

\\[ \frac{t_1}{t_2}= \frac{400}{60}=6.667 \\]

Creșterea radianței normalizate raportată este 6,3×.

Observație importantă

Cele două valori sunt foarte apropiate.

Nu spun că aceasta demonstrează o eroare. Dar este o coincidență numerică suficient de importantă încât trebuie investigată înainte de a interpreta creșterea drept dovadă independentă a intensificării emisiei.

## 3.1. Ce ne spune fizica senzorului

Într-un senzor liniar, nesaturat, putem aproxima:

\\[ DN-DN_0 \propto L\cdot t_e\cdot G \\]

unde:

- \\(DN\\) = valoarea digitală a pixelului;
- \\(DN_0\\) = nivelul de negru;
- \\(L\\) = radianta optică incidentă;
- \\(t_e\\) = timpul de expunere;
- \\(G\\) = câștigul senzorului.

În condițiile ISO și diafragmei fixe, estimarea radiometrică simplificată ar fi:

\\[ \hat L\propto\frac{DN-DN_0}{t_e} \\]

Dar numai dacă răspunsul senzorului este liniar și procesarea imaginii nu introduce transformări neliniare.

Dacă valorile provin din JPEG, gamma, tone mapping și procesarea internă pot compromite această relație.

## 3.2. Ce trebuie să verificăm

Există trei scenarii diferite.

Scenariul A — emisia reală crește

Camera scurtează expunerea deoarece scena devine mai luminoasă.

După corecția expunerii, radianta estimată crește.

Aceasta este o interpretare fizic plauzibilă.

Scenariul B — normalizarea amplifică un artefact

Valorile pixelilor sunt deja afectate de procesarea camerei, iar împărțirea la timpul de expunere nu mai reprezintă o estimare liniară a radianței.

Creșterea calculată poate fi distorsionată.

Scenariul C — crește lumina în câmpul camerei, dar nu neapărat emisia proprie a flăcării

Pot interveni:

- reflexii;
- lumină împrăștiată;
- iluminare ambientală;
- reflexii de pe suprafețe;
- modificarea fundalului luminos.

Acestea pot produce o creștere a semnalului măsurat fără să reprezinte exclusiv creșterea emisiei proprii a flăcării.

## 3.3. Testele decisive pe imaginile existente

IDEA-032-B — Radiometric Consistency Audit

Aș face cinci verificări.

| Test                            | Ce căutăm                                                           |
| ------------------------------- | ------------------------------------------------------------------- |
| Histogramă RAW                  | Liniaritate, clipping, saturație                                    |
| Fundal în afara flăcării        | Creșterea iluminării generale                                       |
| Zone de reflexie                | Corelația reflexiilor cu intensitatea aparentă                      |
| Canale RGB separat              | Schimbarea distribuției spectrale aparente                          |
| Intensitate integrată vs maximă | Diferența dintre creșterea unui pixel și creșterea întregii flăcări |

În special, aș compara:

\\[ L\_{\max}(t) \\]

cu:

\\[ L\_{\mathrm{integrat}}(t)= \sum\_{(x,y)\in ROI} L(x,y,t) \\]

și cu:

\\[ A\_{\mathrm{flacără}}(t) \\]

unde \\(ROI\\) este regiunea de interes a flăcării.

Dacă maximul crește de 6,3 ori, dar aria și intensitatea integrată au alte evoluții, avem informații importante despre natura creșterii.

Mai vreau un test:

Comparăm fundalul din jurul flăcării în aceleași cadre.

Dacă fundalul crește sistematic împreună cu flacăra, trebuie investigată o componentă optică comună.

### Atenție la interpretare

[RAPORTAT DE SURSĂ] ISO și diafragma sunt fixe.

[INFERENȚĂ] Acest lucru elimină două surse importante de variație a expunerii.

[NECUNOSCUT] Nu demonstrează liniaritatea senzorului, absența clippingului sau lipsa procesării automate a imaginilor.

Concluzia mea: nu putem afirma încă faptul că flacăra emite de 6,3 ori mai multă energie radiativă. Putem afirma că analiza PM indică o creștere de aproximativ 6,3 ori a indicatorului de radianta normalizată.

Sunt două afirmații diferite.

# 4. Obiecția #3 — Fitul pe intervale cu debit constant

OBIECȚIE METODOLOGICĂ

Aici sunt mai favorabil propunerii DEC-032.

Dacă avem două regimuri de curgere distincte, o singură pantă peste întreaga perioadă poate combina două comportamente diferite.

Matematic, dacă:

\\[ x_f(t)=x_0+vt \\]

atunci această relație presupune o rată constantă pe întregul interval.

Dar dacă debitul se modifică, putem avea:

\\[ x_f(t)= \begin{cases} a_1+v_1t,&t\in T_1\\\ a_2+v_2t,&t\in T_2 \end{cases} \\]

Acest model este mai potrivit dacă există două regimuri stabile.

## 4.1. Ce câștigăm

1. Separăm comportamentele asociate unor condiții de curgere diferite.
2. Evităm ca o singură pantă să ascundă o schimbare de regim.
3. Putem observa dacă rata frontului se modifică odată cu debitul.
4. Putem investiga dacă există o relație între curgerea impusă și propagarea frontului.

## 4.2. Ce pierdem

Aici sunt patru probleme.

A. Pierdem continuitatea interpretării globale.

Nu mai avem o singură rată descriptivă pentru întregul experiment.

Nu este neapărat rău, dar trebuie explicat.

B. Crește incertitudinea regresiei.

Dacă împărțim un set mic de puncte în două sau mai multe intervale, fiecare regresie are mai puține observații.

C. Introducem riscul selecției intervalelor.

Dacă alegem limitele după ce vedem ce rezultate obținem, putem produce artificial rate convenabile.

D. Nu rezolvăm cauzalitatea.

Debitul crește de la 3 la 5 cm/s în același interval în care flacăra se intensifică.

Nu putem separa automat efectul debitului de efectul evoluției temporale a flăcării.

Mai mult, trebuie să știm dacă debitul raportat este debitul efectiv măsurat sau doar valoarea setată de echipaj.

## 4.3. Problema tranzițiilor

Nu aș include automat în regresie cadrele în care debitul trece de la un nivel la altul.

Pot exista:

- timpul de răspuns al ventilatorului;
- timpul de stabilizare a curgerii;
- efecte tranzitorii asupra flăcării;
- întârzieri între schimbarea comenzii și răspunsul fizic.

Dacă tranziția este inclusă într-unul dintre intervale, panta poate fi distorsionată.

IDEA-032-C — Piecewise Flow Regression

Propun următoarea abordare:

1. Stabilim intervalele pe baza overlay-ului original, independent de rezultatele regresiei.
2. Identificăm separat tranzițiile.
3. Verificăm existența unui platou real după fiecare schimbare.
4. Calculăm regresii separate.
5. Raportăm numărul de cadre și durata fiecărui interval.
6. Calculăm intervalele de încredere și reziduurile.
7. Comparăm rezultatul cu regresia globală, exclusiv ca analiză de sensibilitate.

Pentru cadre consecutive nu aș utiliza un bootstrap obișnuit al observațiilor independente. Aș prefera un block bootstrap, care păstrează parțial autocorelația temporală.

O precizare: două pante diferite nu demonstrează că debitul a cauzat diferența. Pentru aceasta ar trebui controlate și celelalte variabile.

Verdictul meu: păstrăm ideea fitului segmentat, dar nu declarăm încă ratele fizice ale celor două regimuri.

# 5. Obiecția #4 — Ce ar alege un jurat ostil?

Aici vreau să privim proiectul din perspectiva unui evaluator care nu are niciun interes să ne valideze metoda.

El nu va întreba dacă metoda noastră produce rezultate coerente.

Va întreba:

De ce aceasta este definiția corectă a frontului de flacără și nu una aleasă pentru a obține rezultatul dorit?

Aceasta este întrebarea dificilă.

## 5.1. Prima vulnerabilitate: ce măsurăm de fapt?

Există o distincție esențială între:

- frontul fizico-chimic al reacției;
- anvelopa vizibilă a flăcării;
- extremitatea luminoasă;
- regiunea de intensitate maximă.

Nu sunt sinonime.

În special, imaginile RGB obișnuite nu identifică automat suprafața reacției chimice.

Într-o flacără de difuzie, zona de reacție poate să nu coincidă cu zona de luminozitate maximă.

Prin urmare:

[INFERENȚĂ] Dacă metoda folosește intensitatea luminoasă pentru identificarea ultimei coloane, măsurăm în primul rând o extremitate a anvelopei luminoase.

Nu putem numi această măsurătoare front chimic fără dovezi suplimentare.

## 5.2. Ce definiție ar putea prefera un evaluator critic?

Eu aș anticipa următoarea alternativă:

Extremitatea anvelopei luminoase detectată printr-un prag absolut, corectat radiometric și definit față de nivelul de fond și zgomotul senzorului.

De exemplu:

\\[ I\_{\mathrm{corr}}(x,y,t)>B(x,y,t)+k\sigma_B \\]

unde:

- \\(B\\) este nivelul de fond;
- \\(\sigma_B\\) este deviația standard a zgomotului de fond;
- \\(k\\) este un factor stabilit înaintea analizei.

Această abordare are avantajul că pragul este raportat la un criteriu de detecție, nu la maximul variabil al flăcării.

Dar nici aceasta nu este automat perfectă.

Dacă radiometria nu este calibrată, pragul absolut poate deveni la rândul său dependent de expunere.

De aceea, juratul ar putea cere:

- calibrare radiometrică;
- corecția fundalului;
- verificarea saturației;
- segmentarea componentelor conectate;
- demonstrarea robusteții la prag;
- estimarea incertitudinii.

## 5.3. De ce ar respinge DEC-032?

Ar putea formula cinci obiecții:

1. Pragul este definit relativ la o mărime care se schimbă semnificativ în timp.
2. Flacăra își poate modifica forma și distribuția luminoasă.
3. Nu există demonstrația că pragul urmărește aceeași structură fizică în toate cadrele.
4. Alegerea fracțiilor 0,05 / 0,1 / 0,2 nu este încă justificată independent.
5. Ratele rezultate sunt apropiate de o valoare publicată anterior, dar nu este demonstrată independența alegerii metodologice față de acea valoare.

A cincea obiecție este deosebit de sensibilă.

Nu pentru că ar demonstra o manipulare, ci pentru că un rezultat care converge spre o valoare cunoscută va atrage automat suspiciunea unui evaluator exigent.

# 6. Obiecția #5 — Ne apropiem de Carmignani: coincidență sau calibrare retrospectivă?

RISC DE CONFIRMARE A IPOTEZEI

Avem următoarele rezultate raportate:

| Metodă                  | Rată                                 |
| ----------------------- | ------------------------------------ |
| Prag fix                | 2,21–2,42 mm/s                       |
| Prag relativ per cadru  | 2,07–2,20 mm/s                       |
| Punctul cel mai luminos | 2,17 mm/s                            |
| Centroid radiant        | 1,97 mm/s                            |
| Comparator Carmignani   | ≈2 mm/s, conform referinței invocate |

Observația este evidentă: toate valorile se concentrează într-o zonă relativ apropiată de 2 mm/s.

Dar avem o problemă.

Nu putem utiliza apropierea de rezultatul Carmignani drept criteriu de validare a metodei noastre.

Înainte de comparație trebuie stabilit dacă măsurătorile sunt comparabile.

În special, Red Team #1 identificase deja o vulnerabilitate: valoarea de aproximativ 2,0 mm/s ar putea proveni din condiții de gravitație normală, în timp ce B6 este un experiment în microgravitație.&#x20;

Nu consider această diferență verificată aici. Ea trebuie confruntată cu sursa originală Carmignani.

## 6.1. Cum demonstrăm independența metodologică?

Nu putem demonstra intenția psihologică printr-o analiză a imaginilor.

Putem însă demonstra că alegerea metodei nu depinde de rezultatul urmărit.

IDEA-032-D — Blind Method Selection

Aș propune următorul protocol:

1. Nu folosim valoarea Carmignani la alegerea pragului.
2. Stabilim criteriile de segmentare pe baza calității imaginii și a proprietăților fizice ale indicatorului.
3. Înregistrăm toate pragurile testate, nu doar cele selectate.
4. Raportăm toate ratele obținute.
5. Comparăm cu Carmignani numai după înghețarea metodologiei.
6. Documentăm explicit orice modificare ulterioară a metodei.

Aș păstra și o analiză de sensibilitate pentru fracțiile:

\\[ \alpha=0.05,\\;0.10,\\;0.20,\\;0.30,\\;0.40,\\;0.50 \\]

Nu văd un motiv suficient pentru a elimina din analiza de sensibilitate valorile 0,3–0,5.

Dacă acestea arată o schimbare sistematică a ratei, tocmai acea informație este importantă.

### O altă problemă

Centroidul radiant are o autocorelație extremă, conform raportului PM.

Acest lucru nu îl face automat invalid, dar îl face nepotrivit ca dovadă independentă de confirmare a ratei frontului.

Centroidul și frontul sunt extrase din aceeași distribuție luminoasă. Sunt indicatori matematic diferiți, dar nu observații experimentale independente.

La fel, punctul cel mai luminos și frontul nu sunt măsurători independente ale aceluiași fenomen.

Nu putem spune că trei metode independente confirmă rezultatul dacă toate trei folosesc aceeași imagine și aceeași structură radiometrică.

# 7. O problemă suplimentară: ce înseamnă exact ultima coloană?

Aici mai am o obiecție tehnică.

Dacă frontul este definit drept ultima coloană care conține cel puțin un pixel peste prag, avem:

\\[ x_f(t)=\max\\{x:\exists y,\ I(x,y,t)>T(t)\\} \\]

Această definiție este sensibilă la:

- pixeli izolați;
- zgomot;
- reflexii;
- particule luminoase;
- artefacte de compresie;
- componente care nu aparțin flăcării.

Un singur pixel îndepărtat poate muta frontul.

Propun să verificăm dacă ultima coloană detectată aparține unei componente conectate la corpul principal al flăcării.

Nu recomand eliminarea automată a componentelor secundare înainte să le examinăm. Trebuie să păstrăm imaginile originale și să documentăm orice operație de filtrare.

IDEA-032-E — Connected Flame Envelope

Testăm trei definiții alternative:

- ultima coloană cu cel puțin un pixel valid;
- ultima coloană aparținând componentei conectate la corpul principal;
- ultima coloană care îndeplinește un criteriu de persistență spațială și temporală.

Dacă rezultatele sunt apropiate, câștigăm robustețe.

Dacă diferă semnificativ, avem încă o sursă de incertitudine care trebuie raportată.

# 8. Ce verificăm în datele brute

Aceasta este lista pe care aș transmite-o PM pentru următoarea etapă.

Nu aș închide DEC-032 înainte de a rezolva punctele critice.

## 8.1. Radiometrie și cameră

Audit radiometric

0/10

Verificarea formatului original: RAW, TIFF, JPEG sau video comprimat

Critic

Verificarea valorilor pixelilor și a eventualei saturări

Critic

Verificarea nivelului de negru și a corecției de fundal

Critic

Recalcularea radianței folosind timpul exact de expunere al fiecărui cadru

Critic

Compararea evoluției maximei cu evoluția intensității integrate

Critic

Analiza fundalului și a zonelor cu reflexii

Critic

Compararea canalelor RGB separat

Important

Verificarea stabilității camerei, focalizării și geometriei optice

Important

Verificarea corecției gamma și a procesării automate

Critic

Compararea raportului de expunere 6,667 cu evoluția indicatorului 6,3

Critic

## 8.2. Geometria și segmentarea flăcării

- Reconstruirea profilului de intensitate pe axa principală.
- Compararea profilurilor normalizate pentru toate cadrele.
- Măsurarea lungimii și lățimii flăcării.
- Calcularea ariilor segmentate la toate pragurile.
- Compararea poziției maximei cu poziția frontului.
- Compararea centroidului cu anvelopa exterioară.
- Verificarea componentelor conectate.
- Recalcularea frontului cu pragurile 0,05–0,50.

## 8.3. Analiza temporală și debit

- Confirmarea timestampurilor originale.
- Identificarea exactă a momentelor de schimbare a debitului.
- Separarea debitului comandat de cel efectiv măsurat.
- Identificarea intervalelor de stabilizare.
- Numărul efectiv de cadre din fiecare interval.
- Autocorelația reziduurilor.
- Intervalele de încredere ale fiecărei pante.
- Compararea fitului global cu fiturile segmentate.

## 8.4. Incertitudinea măsurării

Trebuie să avem o estimare pentru:

\\[ u(v_f) \\]

care să includă, pe cât posibil:

- calibrarea mm/pixel;
- localizarea frontului;
- rezoluția temporală;
- incertitudinea regresiei;
- autocorelația;
- variația pragului.

Nu recomand să combinăm mecanic toate aceste surse într-o singură valoare fără să verificăm dependențele dintre ele.

# 9. Recomandarea mea pentru DEC-032

Aici este concluzia operațională a Red Team-ului.

Nu recomand abandonarea propunerii. Recomand separarea ei în trei decizii.

DEC-032-A — Definiția operațională a frontului

Necesită revizuire

Nu declarăm încă pragul relativ per cadru drept definiție fizică validată.

Îl păstrăm ca metodă de detecție experimentală și efectuăm testul de sensibilitate la schimbarea formei flăcării.

DEC-032-B — Segmentarea după debit

Susținută metodologic, condiționat

Adoptăm regresii separate numai dacă intervalele de debit constant și tranzițiile pot fi identificate independent și dacă există suficiente observații pentru estimări utile.

DEC-032-C — Validarea independentă a rezultatului

Deschis

Înghețăm metoda înaintea comparației cu Carmignani.

Păstrăm toate rezultatele alternative și documentăm incertitudinea.

## Ordinea pe care aș urma-o

1. Audit radiometric.
2. Audit morfologic.
3. Test de sensibilitate la prag.
4. Verificarea segmentării pe componente conectate.
5. Identificarea intervalelor stabile de debit.
6. Regresii segmentate și estimarea incertitudinii.
7. Comparația cu Carmignani.

Nu aș inversa această ordine.

Dacă începem prin a selecta rata care se apropie de Carmignani, riscăm să contaminăm întregul proces de validare.

# 10. Ce ar putea deveni contribuția științifică interesantă?

Vreau să subliniez un lucru.

În această etapă, cred că există o oportunitate care depășește simpla determinare a unei viteze de propagare.

Avem posibilitatea de a studia relația dintre trei fenomene:

1. Evoluția geometrică a flăcării.
2. Evoluția distribuției luminoase.
3. Evoluția frontului detectat algoritmic.

Acestea pot avea viteze diferite.

Putem defini:

\\[ v\_{\mathrm{tip}} \\]

viteza extremității flăcării;

\\[ v\_{\mathrm{centroid}} \\]

viteza centrului distribuției luminoase;

\\[ v\_{\mathrm{envelope}} \\]

viteza anvelopei luminoase;

\\[ v\_{\alpha} \\]

viteza frontului la un prag relativ dat.

Dacă aceste viteze diferă sistematic, nu înseamnă automat că una dintre ele este greșită.

Poate însemna că descriu proprietăți diferite ale fenomenului.

IDEA-032-F — Multi-Definition Flame Propagation Analysis

Propun să investigăm dacă dinamica flăcării poate fi descrisă printr-un set de indicatori cinematici, în loc să forțăm toate observațiile într-o singură definiție a frontului.

Ar fi o contribuție metodologică interesantă, cu condiția să nu prezentăm acești indicatori drept măsurători independente.

# 11. Verdict final Red Team #2

DEC-032 — HOLD / REVISION REQUIRED

| Întrebare                                                       | Verdict                                                  |
| --------------------------------------------------------------- | -------------------------------------------------------- |
| Este pragul relativ per cadru mai robust la variația expunerii? | [INFERENȚĂ] Probabil, în condițiile testate              |
| Este imun la modificarea formei flăcării?                       | [NECUNOSCUT]                                             |
| Monotonicitatea ratelor indică o problemă?                      | [INFERENȚĂ] Este un semnal de investigat                 |
| Este creșterea de 6,3× emisie reală?                            | [NECUNOSCUT]                                             |
| Sunt justificate regresiile pe intervale de debit?              | [INFERENȚĂ] Da, condiționat de stabilitatea intervalelor |
| Este ultima coloană peste prag un front chimic?                 | Nu este demonstrat                                       |
| Este rezultatul apropiat de Carmignani o validare?              | Nu                                                       |
| Putem semna DEC-032 acum?                                       | Nu recomand                                              |

### Cele trei obiecții pe care nu le-aș lăsa nerezolvate

1\. Endogenitatea pragului.

Maximul fiecărui cadru este o variabilă dinamică. Normalizarea poate elimina variația de amplitudine, dar nu și variația formei distribuției luminoase.

2\. Ambiguitatea radiometrică.

Creșterea de 6,3× este foarte apropiată de raportul expunerilor, 6,667. Trebuie să stabilim dacă estimarea radiometrică este validă și dacă semnalul reprezintă efectiv emisia flăcării.

3\. Ambiguitatea fizică a termenului front.

O extremitate luminoasă nu este automat frontul reacției chimice.

Acestea sunt vulnerabilitățile principale în fața unui evaluator specializat.

### Ce aș păstra ca idei noi

| ID         | Propunere                                   | Statut                 |
| ---------- | ------------------------------------------- | ---------------------- |
| IDEA-032-A | Shape/Amplitude Decomposition               | De evaluat             |
| IDEA-032-B | Radiometric Consistency Audit               | Prioritate critică     |
| IDEA-032-C | Piecewise Flow Regression                   | De evaluat             |
| IDEA-032-D | Blind Method Selection                      | Recomandată            |
| IDEA-032-E | Connected Flame Envelope                    | De evaluat             |
| IDEA-032-F | Multi-Definition Flame Propagation Analysis | Cercetare exploratorie |

Acestea sunt propuneri pentru PM, nu decizii implementate și nici decizii aprobate de Owner.

## Ultima observație

Vreau să atrag atenția asupra unei capcane intelectuale.

Am început cu o problemă de măsurare: cum identificăm frontul flăcării?

Am ajuns la o problemă mai interesantă: ce anume se propagă și ce anume măsurăm atunci când spunem că frontul se propagă?

Este posibil ca flacăra să aibă o extremitate geometrică, o extremitate luminoasă și o regiune de reacție care evoluează diferit.

Dacă imaginile ne permit să distingem aceste fenomene, putem obține mai mult decât o valoare de 2,1 mm/s.

Dar nu trebuie să anticipăm rezultatul.

Prefer o măsurătoare de 2,42 mm/s demonstrată riguros decât una de 2,00 mm/s obținută printr-o definiție convenabilă.

Și prefer să descoperim că metoda noastră inițială era greșită decât să construim o validare aparentă pe o presupunere neverificată.

Acesta este rolul Red Team.

Recomandarea mea: DEC-032 rămâne deschis. Următoarea etapă trebuie să fie auditul radiometric și morfologic, nu alegerea definitivă a pragului.