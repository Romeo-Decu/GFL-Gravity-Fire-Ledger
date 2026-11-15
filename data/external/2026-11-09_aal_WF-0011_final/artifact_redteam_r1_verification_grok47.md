VERDICT: FAIL
ALIGNMENT: PARTIAL
SEVERITY: MAJOR
RESPONSIBLE: ADVERSARIAL_AUDIT
CAUSE: ERROR

## Constatări
- [AUDIT_COVERAGE_GAP] [CONFIRMED] Acceptance for ADVERSARIAL_AUDIT requires per-script defects with line references for time handling, direction, thresholds, window and statistics. The audit gives line refs for direction guards, a fixed 10% threshold and a partial window/MAD note only. Time-delta handling and the regression statistics (OLS vs robust, R², gap treatment) have no line-referenced defects.
- [EXPOSURE_RANGE_ERROR] [CONFIRMED] Against DATA_SCHEMA_AND_SAMPLE.md the audit states a 67× exposure range of 0.005–0.333 s. The same sample already contains 0.002 s (and the first frames are 0.333333 s), so the cited range is wrong without needing the full files.
- [NUMPY_PANDAS_OVERCLAIM] [CONFIRMED] The audit certifies that both scripts stay on numpy+pandas. [REPORTED] The founder/Validator record says deepseek_v4 imports scipy. [UNVERIFIABLE] The import line itself is not in this packet, so the miss is charged on the founder report, not on a line I opened.
- [DIRECTION_OVERCLAIM_AND_BAD_FALLBACK] [CONFIRMED] The audit says the two direction methods “yield consistent interpretations” while marking execution UNVERIFIABLE, and it recommends a fallback that hardcodes DECREASING_COLUMNS because the flow is opposed. [REPORTED] Validator execution shows the opposite: kimi26 INCREASING, deepseek_v4 cross-correlation DECREASING with its own front slope positive. Upstream is not a column direction in the task text.
- [RATE_GAP_IS_WINDOW_AND_THRESHOLD] [REPORTED] kimi26 full-series OLS is 0.43 mm/s (R² 0.19) and Theil–Sen 0.78, but 5–10×MAD Theil–Sen is 2.11–2.12; thirds are 3.21 / 0.98 / ~0; max frame gap 106 s. deepseek_v4 stays at 0.60–0.63 mm/s across 5–30% thresholds with R² 0.46 and a sign contradiction. GFL’s in-window absolute thresholds are 2.21–2.34 and relative thresholds 2.07–2.20. [INFERENCE] 0.4–0.8 is not the same estimand as 2.1–2.3.
- [GFL_PRECISION_NOT_REGISTERABLE] [REPORTED] GFL quotes 2.274 ± 0.094 mm/s on 13–53 s while residual autocorrelation ≈ 0.8, radiance ×6.3, opposed flow 3→5 cm/s, ramp 8.8→4.0 mm, and clipping at 13–17 s and 52.6 s. [INFERENCE] ±0.094 is a formal fit SE, not the uncertainty budget the brief requires. [UNKNOWN] Whether 13–53 s was fixed before the slope was seen.

## Conținut
CONTEXT: PKT-4a49aaa53d
CONFIDENCE: 0.74

# WF-0011 INTEGRATION_REVIEW — Red Team (B6)

## 1. Verificare — ADVERSARIAL_AUDIT față de task_brief

VERDICT: FAIL
ALIGNMENT: PARTIAL
RESPONSIBLE: ADVERSARIAL_AUDIT
CAUSE: ERROR

Criteriul de acceptare din brief: defecte de cod pe fiecare script, cu referință de linie, pentru time handling, direction, thresholds, window și statistics. [CONFIRMED] Auditul atinge parțial direction, thresholds și window (deepseek linii citate 42–45, 102–104, 120; kimi 89–91, 112) și discută calitatea datelor. [CONFIRMED] Nu există defecte cu linie pentru tratarea lui Δt și nici pentru statistică (OLS, Theil–Sen, R², perechi peste gap). Două din cinci clase cerute lipsesc. ALIGNMENT rămâne PARTIAL, nu NO: direcția-înaintea-frontului, bugetul de incertitudine și sensibilitatea la prag sunt în subiect.

- [CONFIRMED] Eroare factuală pe datele din pachet: auditul scrie „67x range (0.005s–0.333s)”. Eșantionul din `DATA_SCHEMA_AND_SAMPLE.md` conține deja `exposure_s` = 0.002 și patru cadre la 0.333333. Raportul 0.333/0.002 ≈ 167, nu 67, și limita de jos citată nu este minimul eșantionului.
- [CONFIRMED] Auditul afirmă respectarea constrângerii numpy+pandas și „consistent interpretations” ale direcției, deși tot el marchează execuția [UNVERIFIABLE]. Afirmația de consistență nu avea ce să confirme.
- [REPORTED] Validatorul, divulgat de Founder pentru această fază: deepseek_v4 importă scipy; cross-corelația dă DECREASING (lag mediu −14.8) în timp ce panta frontului propriu este +0.61 mm/s; kimi26 dă INCREASING. Certificarea „numpy/pandas only” și consistența de direcție sunt, pe această raportare, false.
- [UNVERIFIABLE] Linia de `import` scipy și atribuirea `np.array_split` către deepseek la liniile 102–104. Nu am scriptul în acest pachet; nu confirm numerotarea.
- [CONFIRMED] Recomandarea de refactorizare `if direction == 'AMBIGUOUS': direction = 'DECREASING_COLUMNS'` injectează direcția din propoziția „spre amonte”. Task-ul spune explicit că direcția se determină din date; textul experimental nu spune care sens de coloană este amonte. Recomandarea încalcă regula pe care auditul pretindea că o verifică.
- [REPORTED] „>20% across thresholds (per kimi26’s sensitivity outputs)” tratează ca output măsurat un script care, la data auditului, nu fusese rulat. Brief-ul interzice numere necalculate. După Validator, sensibilitatea kimi nu este „>20%”: este 0.01–2.12 mm/s, adică schimbă ordinul de mărime.

Nu este FABRICATION integrală: o parte din riscuri (prag fix, MAD contaminat de flacără, lipsa de gardă pe corelație plată, autocorelarea expunerii) sunt reale și utile. Este ERROR față de criteriul de acceptare și față de fapte din eșantion.

Nu am căutat și nu folosesc valori publicate pentru B6.

## 2. De ce orbii dau 0.4–0.8 mm/s și GFL 2.1–2.3 mm/s

Etichete de fază: [REPORTED BY SOURCE] = Founder DIR-001 / Validator; [VERIFIED] = citit direct în fișierele din pachet; [INFERENCE]; [UNKNOWN].

Fapte [REPORTED BY SOURCE]:
- kimi26: direcție INCREASING; OLS primar 0.43 mm/s, R² 0.19; Theil–Sen 0.78; 69/77 cadre; sensibilitate de prag 0.01–2.12 mm/s; Theil–Sen la 5–10×MAD = 2.11–2.12; treimi 3.21 / 0.98 / ≈0 mm/s; gap maxim între cadre 106 s; expuneri 0.0008–0.333 s.
- deepseek_v4: cross-corelație DECREASING (lag mediu −14.8) dar pantă de front +0.61 mm/s, R² 0.46; praguri 5–30% → 0.60–0.63 mm/s; import scipy.
- GFL: direcție INCREASING; fereastră 13–53 s, 40 cadre; 2.274 ± 0.094 mm/s; praguri absolute 2e5/5e5/1e6 → 2.21/2.27/2.34; prag relativ la peak 0.05–0.5 → 2.07–2.20; peak 2.17; centroid 1.97; pe start 8–25 s și end 40–60 s, pragul de referință dă 2.20–2.30; radiație ×6.3; debit 3→5 cm/s; rampă 8.8→4.0 mm; clipping 13–17 s și 52.6 s; autocorelație reziduală ≈ 0.8.
- [VERIFIED] Task: doar numpy+pandas; direcția înainte de orice front; rânduri 655–1016; scală 14.7 coloane/mm ±3%, riglă în spatele planului, fără corecție; fereastra și metoda se decid înainte de pante.

[INFERENCE] Discrepanța nu este „două fizici”. Este un alt estimand.

1. Fereastra și gap-ul domină la deepseek și la OLS-ul primar kimi. R² 0.19 înseamnă că o dreaptă pe seria lungă nu descrie datele. Treimile 3.21 / 0.98 / ≈0 arată trei regimuri; media lor, strivită de un gap de 106 s (Δx/Δt cu Δt uriaș), cade în 0.4–0.8. deepseek rămâne la 0.60–0.63 pe toate pragurile relative 5–30%, deci la el pragul nu mută rezultatul. GFL, pe același tip de definiție relativă, dar numai în 13–53 s, stă la 2.07–2.20. Aceeași clasă de front, alt interval de timp → altă pantă. [UNKNOWN] câte cadre și ce gap intră efectiv în fit-ul deepseek; mecanismul de fereastră este inferența cea mai economică, nu un fapt măsurat de mine.
2. Pragul explică intervalul intern kimi, nu neapărat cifra deepseek. 0.01 mm/s la prag lax este compatibil cu urmărirea unui umăr slab, a zgomotului sau a unei reflexii aproape staționare; 2.11–2.12 la 5–10×MAD Theil–Sen cade în banda GFL. Rezultatul „primar” 0.43 ascunde singura estimare kimi care concordă cu GFL.
3. Semnul. kimi și frontul deepseek și GFL sunt toți spre coloane crescătoare. Singura excepție este lag-ul de cross-corelație. [INFERENCE] Un lag mediu de −14.8 coloane/pas la ~1 s și 14.7 px/mm ar fi ~1 mm/s spre descreștere — nici măcar nu se potrivește cu |0.61|. Cauze plauzibile, neconfirmate: convenția de semn a `correlate`, blocarea corelației pe corpul care crește (radiație ×6.3), nu pe muchia de atac. Centroidul GFL este 1.97, nu 0.6, deci „au urmărit centroidul” nu explică rata oarbă.
4. Expunerea nu explică diferența de ~1.5 mm/s. [INFERENCE] La 2.3 mm/s, un shutter de 0.333 s mută flacăra ~0.8 mm în timpul integrării; diferența de smear între cadrele lungi și cele de 0.0008 s, întinsă pe zeci de secunde, este de ordinul 0.01 mm/s pe pantă, nu 1 mm/s. Poate părtini marginea; nu reconciliază cele două tabere.

## 3. Fereastra GFL 13–53 s: justificată sau aleasă?

[REPORTED BY SOURCE] Limitele cad peste clipping (start în 13–17 s, final lângă 52.6 s). [UNKNOWN] Nu există în pachet jurnalul GFL „metodă și fereastră înainte de pantă”, deși regula din task cere exact asta. Coincidența cu defectele de date este compatibilă și cu o regulă de calitate („taie transientele de clipping”), și cu o alegere după ce panta a fost văzută. Nu pot distinge.

[REPORTED BY SOURCE] Familia de 300+ ferestre dă 2.20–2.30, dar numai pentru start 8–25 s și end 40–60 s. [INFERENCE] Asta arată că 13–53 s nu este un vârf izolat în interiorul intervalului activ. Nu arată că intervalul activ a fost delimitat independent de pantă, și nu contrazice treimile 3.21/0.98/0: acele treimi sunt pe recordul lung, familia de 300 pe recordul scurt. Stabilitatea internă nu este o pre-înregistrare.

Înăuntrul ferestrei procesul nu este staționar: debitul echipajului se schimbă 3→5 cm/s, radiația ×6.3, rampa se ascute 8.8→4.0 mm. [INFERENCE] 2.274 mm/s este panta medie a unei muchii luminoase pe un proces care se schimbă, nu o constantă de test și nu rata frontului de piroliză. Offsetul muchie luminoasă–piroliză rămâne [UNKNOWN] pentru toate cele trei analize.

±0.094 mm/s nu este bugetul. [INFERENCE] Cu autocorelație reziduală ≈ 0.8, N efectiv pe 40 de cadre este mult mai mic decât 40; SE-ul OLS iid este optimist. Plaja de definiție deja raportată (centroid 1.97, relativ 2.07–2.20, peak 2.17, absolut 2.21–2.34) are lățime ~0.4 mm/s, de câteva ori ±0.094. Scala ±3% este ~0.07 mm/s și nu include paralaxa riglei din spatele filmului [UNKNOWN]. Pragul absolut fix urmărește fracții diferite din peak când peak-ul crește ×6.3; banda relativă GFL arată că efectul, în fereastra lor, este zecimi, nu factorul 3–5 față de orbi.

[VERIFIED] Off-by-one de bandă: task 655–1016, GFL 655–1017. Neglijabil pentru pantă; este totuși alt profil decât cel descris analiștilor.

## 4. Ce ar accepta un judecător NASA ostil

[INFERENCE] Nu ar accepta în registru nici 0.43, nici 0.78, nici 0.61, nici 2.274 ± 0.094 ca „rata B6”.

- Respinge deepseek: semn autocontradictoriu, R² 0.46, constrângere de stack încălcată, nicio dovadă că 0.6 supraviețuiește aceleiași ferestre ca GFL.
- Respinge OLS-ul primar kimi: R² 0.19, 69/77 cadre, gap 106 s, treimi incompatibile. Propria sensibilitate 2.11–2.12 îl contrazice pe 0.43 ca estimare robustă.
- Tratează 2.1–2.3 mm/s spre coloane crescătoare doar ca viteză a muchiei luminoase în intervalul în care frontul este continuu urmăribile, și doar pentru că definiții independente (prag absolut GFL, prag relativ GFL, peak GFL, Theil–Sen kimi la prag înalt) se întâlnesc acolo. Ar cere reexecutarea încrucișată, pe aceleași cadre, înainte de orice număr de registru.
- Ar impune raportarea ca interval condiționat de definiție și de debit, cu incertitudine de câteva zecimi de mm/s, nu ca scalar ±0.094, și fără echivalare cu rata de piroliză.

Enunțul maxim pe care evidența de față îl suportă [INFERENCE], nu [VERIFIED]: în porțiunea activă, muchia luminoasă se deplasează spre coloane crescătoare cu circa 2.1–2.3 mm/s; 0.4–0.8 mm/s este panta unei serii lungi, nestaționare, cu gap de 106 s și, la kimi, cu prag care poate urmări altceva decât flacăra.

## 5. Obiecții

OBIECȚIE: deepseek_v4 nu are o direcție utilizabilă: cross-corelația raportează DECREASING (lag mediu −14.8), iar panta propriului front este +0.61 mm/s (R² 0.46); magnitudinile nu se potrivesc nici ele. Un estimator cu semn autocontradictoriu nu se pune în registru. [REPORTED BY SOURCE] [INFERENCE] | MIZA: 5 | IREVERSIBIL: nu | VETO: da
OBIECȚIE: Scriptul deepseek_v4 importă scipy, împotriva regulii numpy+pandas din task. Livrabilul REALITY nu este conform; output-ul Validatorului poate fi discutat, dar nu ca analiză acceptată. [REPORTED BY SOURCE] [VERIFIED] | MIZA: 4 | IREVERSIBIL: nu | VETO: da
OBIECȚIE: OLS-ul primar kimi26, 0.43 mm/s la R² 0.19 pe 69/77 cadre cu gap maxim 106 s, nu este o rată de propagare. Este panta unei serii care amestecă regimuri și timp mort. Înregistrarea lui ca rata B6 ar fi ireversibil greșită. [REPORTED BY SOURCE] [INFERENCE] | MIZA: 5 | IREVERSIBIL: da | VETO: da
OBIECȚIE: Aceeași rulare kimi26 dă Theil–Sen 2.11–2.12 mm/s la 5–10×MAD, în banda GFL, și 0.01 mm/s la capătul lax. Citatul 0.43 sau 0.78 fără acest interval fabrică o discrepanță fizică dintr-o alegere de prag și de estimator. [REPORTED BY SOURCE] [INFERENCE] | MIZA: 5 | IREVERSIBIL: nu | VETO: da
OBIECȚIE: Treimile kimi26, 3.21 / 0.98 / ≈0 mm/s, fac ilegitim orice scalar unic „rata testului” pe recordul întreg, inclusiv Theil–Sen 0.78. [REPORTED BY SOURCE] [INFERENCE] | MIZA: 4 | IREVERSIBIL: nu | VETO: da
OBIECȚIE: Fereastra GFL 13–53 s începe în clippingul 13–17 s și se termină lângă clippingul de la 52.6 s. Nu există dovadă că regula a fost înghețată înainte de pantă. Veto pe pretenția că fereastra este justificată, nu pe existența pantei. [REPORTED BY SOURCE] [UNKNOWN] | MIZA: 4 | IREVERSIBIL: nu | VETO: da
OBIECȚIE: Banda 2.20–2.30 pe 300+ ferestre acoperă doar start 8–25 s și end 40–60 s. Nu reconciliază treimile recordului lung și nu demonstrează că delimitarea intervalului activ nu a fost aleasă. [REPORTED BY SOURCE] [INFERENCE] | MIZA: 4 | IREVERSIBIL: nu | VETO: da
OBIECȚIE: 2.274 ± 0.094 mm/s nu este un buget de incertitudine. Autocorelația reziduală ≈ 0.8 subminează SE-ul iid; definițiile deja calculate acoperă ~1.97–2.34; debitul, radiația ×6.3 și rampa 8.8→4.0 mm variază în fereastră; ±3% de scală nu include paralaxa. Veto pe înscrierea preciziei ±0.094. [REPORTED BY SOURCE] [INFERENCE] [UNKNOWN] | MIZA: 5 | IREVERSIBIL: da | VETO: da
OBIECȚIE: Nici GFL, nici analizele oarbe nu măsoară frontul de piroliză. Toate urmăresc o muchie luminoasă sau un corp de emisie. Offsetul față de piroliză este neconstrâns; echivalarea cu „flame-spread rate” de material, la debit care se schimbă 3→5 cm/s, este o afirmație în plus față de date. [REPORTED BY SOURCE] [INFERENCE] [UNKNOWN] | MIZA: 4 | IREVERSIBIL: da | VETO: da
OBIECȚIE: Pragurile absolute fixe schimbă fracția din peak când radiația crește ×6.3. Efectul, în fereastra GFL, este în zecimi de mm/s (2.07–2.20 relativ vs 2.21–2.34 absolut) și nu explică singur 0.4–0.8; trebuie raportat în buget, nu înghițit de ±0.094. [REPORTED BY SOURCE] [INFERENCE] | MIZA: 3 | IREVERSIBIL: nu
OBIECȚIE: Auditul nu poate sta la baza registrului: a certificat numpy+pandas, a declarat direcțiile consistente, a greșit intervalul de expunere față de eșantionul din brief și a propus fallback hardcodat DECREASING_COLUMNS. [CONFIRMED] [REPORTED] | MIZA: 4 | IREVERSIBIL: nu | VETO: da
OBIECȚIE: Banda de rânduri GFL 655–1017 nu este banda din task 655–1016. Efect așteptat mic, identitatea profilului nu este aceeași. [VERIFIED] [REPORTED BY SOURCE] | MIZA: 1 | IREVERSIBIL: nu

## Riscuri
- Înscrierea în registrul GFL a unui singur număr B6 (0.43, 0.61 sau 2.274±0.094) înainte de reexecutarea încrucișată pe aceleași cadre.
- Citirea acordului 2.11–2.12 (kimi, prag înalt) cu 2.2 (GFL) ca validare independentă, deși ambele pot urmări același vârf luminos în același film, nu frontul de piroliză.
- Fallback-ul de direcție „spre descreștere pentru că opposed flow” poate fi reluat în CONCEPT și poate răsturna semnul corect (INCREASING), singurul pe care două trackere de front și GFL concordă.
- Gap-ul de 106 s, dacă este pauză de cameră în afara propagării, condamnă doar OLS-ul pe tot recordul; dacă este în mijlocul propagării, și ferestrele „active” sunt suspecte. Locul lui nu este în pachet.

## Alternative
- Înainte de orice număr de registru: tabel 2×2 pe aceleași cadre — definiția de front kimi și definiția GFL, fiecare pe (a) toate cele 77 de cadre cu gap-ul lăsat înăuntru și (b) doar t0+13…53 s. Dacă ratele se mută împreună spre ~2.2 în (b) și spre ~0.5 în (a), discrepanța este fereastra.
- Înlocuiți OLS-ul global cu Theil–Sen rulant (fereastră ~15 s) și raportați rata în funcție de timp; dacă momentul schimbării de debit 3→5 cm/s poate fi aliniat la EXIF, împărțiți seria acolo în loc de o pantă unică.
- Declarați fereastra printr-o regulă de calitate înghețată înainte de fit: Δt sub un plafon (de ex. 2 s), peak peste un planșeu, cadrele cu clipping excluse, apoi fit. Nu folosiți 13 s și 53 s doar pentru că coincid cu clippingul.
- Incertitudine: eroare HAC sau bootstrap pe blocuri, dată fiind autocorelația ≈ 0.8, plus componente separate pentru definiția de front, scala ±3% și un termen de bias de paralaxă marcat [UNKNOWN], fără a le aduna în cuadratură ca și cum ar fi zgomot aleator.
- Anulați direcția deepseek până la un test de semn pe un profil sintetic deplasat cu +N coloane; nu hardcodați DECREASING. Dacă lag-ul își schimbă semnul pe sintetic, corelația se aruncă și se păstrează doar tracker-ul de front.

## Unde sunt cel mai puțin sigur
Unde stă gap-ul de 106 s (pauză în afara propagării sau gaură în mijlocul ei) și dacă GFL a fixat 13–53 s înainte de a vedea panta. Ambele decid cât din 0.4–0.8 vs 2.1–2.3 este contaminare de fereastră și cât este selecție. Nu am văzut linia de import scipy, doar raportul Validatorului.

## Ce aș verifica întâi
Reexecuție încrucișată, scripturi nemodificate altfel decât prin tăietura de timp: tracker-ele oarbe restrânse la 13–53 s și la familia 8–60 s, și pragul de referință GFL pe toate cele 77 de cadre cu gap-ul de 106 s inclus. Dacă ratele se adună la 2.1–2.3 în fereastra activă și la ~0.5 pe seria lungă, ipoteza de fereastră este confirmată și registrul poate discuta doar intervalul activ, cu incertitudine lărgită.
