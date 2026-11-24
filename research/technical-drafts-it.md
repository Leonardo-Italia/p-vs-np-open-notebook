# Appunti tecnici di supporto

Questa appendice raccoglie le derivazioni estese dei [filoni sul conteggio](02-counting-and-parameters.md), [sui matchgate](03-matchgate-representations.md) e [sui limiti di circuito](04-fixed-weights-and-proofs.md). I riferimenti ai conteggi dei test nelle singole sezioni descrivono i controlli svolti durante l'indagine. Per i controlli ripetibili in questo rilascio si veda il [README](../README.md).

Le argomentazioni sono bozze di ricerca generate con ChatGPT/Codex. La revisione indipendente è da documentare.

## Contrarre cicli di scelte

Siano $s=2k$, $a=2s+1$ e $N=a^2-1$. Ogni addendo è $2^i+2^{f(i)}$ con $f(i)=ai+s\bmod N$. La permutazione soddisfa $f^2(i)=i+N/2\bmod N$, perciò le scelte formano cicli di quattro. Si possono contrarre tutte le scelte di ciascun ciclo e lasciare esposti soltanto i riporti.

Il grafo quoziente ha larghezza ad albero $\Theta(\sqrt N)$. Le orbite di $x+ay$, per $0\le x,y<s$, sono distinte. Infatti $f(x+ay)=y+ax+s\bmod N$, $f^2$ aggiunge $N/2$ e nessuna delle altre tre immagini torna nel quadrato iniziale. I passi di ampiezza $1$ sono riporti; quelli di ampiezza $a$ diventano riporti dopo aver applicato $f^{-1}$, perché $f(i+1)=f(i)+a$. Si ottiene una griglia $s\times s$ senza usare il riporto circolare da $N-1$ a $0$. Le croci formate da una riga e una colonna sono connesse, si intersecano a coppie e richiedono almeno $s$ vertici per essere tutte incontrate. La proprietà di Helly per sottoalberi implica che una borsa di una decomposizione deve contenerne almeno $s$.

Per il limite superiore, ciascuna orbita mantiene il resto modulo $s$, ogni strato contiene $s+1$ orbite e i riporti collegano strati successivi. Basta tenere il primo strato e due consecutivi in una decomposizione in cammino. Ne risulta un conteggio esatto in $2^{O(\sqrt N)}$ per questa famiglia: si enumerano le scelte entro ciascuno strato, si ricavano i due vettori di riporti e si raccordano gli strati. La costruzione della griglia è stata controllata per $k$ da 1 a 14. Il conteggio è stato confrontato con enumerazione per metà su 25 obiettivi a 24 colonne.

## Somme con cancellazione

Un blocco è qui la firma che si ottiene contraendo i riporti interni e lasciando esposti i fili di scelta. Ripeto il blocco di quattro colonne con bit obiettivo $(0,0,1,0)$ dal meno significativo. Fisso entrambe le scelte dell'ultima colonna a zero, così essa impone riporto entrante e uscente zero. Nelle prime tre colonne lascio attivi quattro ingressi di pesi $1,1,2,4$. Con gli estremi fissati a zero, la somma $4$ ha esattamente due configurazioni: si seleziona il solo $4$ oppure tutti gli altri. Invertendo il bit del $4$, il blocco si riduce a $M=|0000\rangle+|1111\rangle$. Con $r$ copie si ottiene $M^{\otimes r}$.

Fissare e invertire bit preserva le identità dei matchgate. Un limite sul rango gaussiano del vettore ridotto è quindi un limite sul numero di firme necessarie per il blocco aritmetico nella base originale e con un ordine dei fili comune. Con operatori di Clifford fino al grado $p$ della stessa parità, una firma singola genera uno spazio di dimensione al massimo $C_{4r,p}=\sum_{j\le p,\,j\equiv p\pmod 2}\binom{4r}{j}$. La somma di $h$ firme genera al massimo $hC_{4r,p}$.

Su ciascuna copia di $M$ si possono scegliere un vettore di grado zero, otto di grado uno e sette di grado due con appoggi distinti: identità, creazione o annichilazione su un modo, doppia creazione su una coppia e proiezione tramite l'operatore di numero. Per fili intercalati, gli operatori aggiungono segni ma non cambiano gli appoggi. Ogni combinazione di grado esattamente $p$ ha un pivot unico: nelle copie su cui si applica l'identità si sceglie $0000$ come pivot, mentre gli altri appoggi possono sostituirlo con $1111$, il cui pivot richiederebbe grado due in più. Si ottengono almeno $[z^p](1+8z+7z^2)^r$ vettori indipendenti. Per $p=\lfloor 8r/9\rfloor$ il rapporto è dell'ordine di $(343/243)^r$. Ciò conta anche somme con coefficienti negativi o complessi.

La riduzione dal blocco aritmetico è stata costruita nell'indagine. La caratterizzazione delle firme e l'asintotica del rapporto sono risultati esterni:
- [Cai e Gorenstein, Matchgates Revisited](https://theoryofcomputing.org/articles/v010a007/), §2 e §5, per identità e normalizzazione pfaffiana.
- [Wei, Wu, Liu e Liu, Robust exponential lower bounds for fermionic and bosonic Gaussian ranks](https://arxiv.org/abs/2610.02172), preliminare, proposizione 3 e appendice B.1, per il rango gaussiano e il rapporto asintotico.
- [Reardon-Smith, Exponential lower bounds on the fermionic Gaussian rank of magic states](https://arxiv.org/abs/2610.03699), preliminare indipendente, per la stessa barriera sul vettore fermionico.

## Cambi di base sui singoli fili

Una Hadamard su ciascuno dei quattro fili trasforma $M$ nella firma uniforme sulle stringhe di parità pari, che è un matchgate. Per verificare se questo vantaggio si conserva sulla catena, considero invece tre colonne attive con obiettivo $(0,0,1)$ e lascio aperti tutti e sei i fili, di pesi $1,1,2,2,4,4$. Indico con $S$ la somma selezionata in un blocco. L'ordine dei terminali è comune a tutti gli addendi e segue le colonne. I due fili di ogni colonna sono adiacenti.

Con la Hadamard uniforme, fisso i due fili di ogni colonna separatrice con obiettivo $0$ ai bit trasformati $0$ e $1$. Nelle coordinate originali applico dunque le righe $(1,1)$ e $(1,-1)$ ignorando la normalizzazione. La matrice dei riporti è $K=|0\rangle(\langle0|-\langle1|)$. Una separatrice prima e dopo ogni blocco, condivisa fra blocchi consecutivi, e i riporti esterni fissati a zero danno un prodotto tensoriale delle firme $\psi=H^{\otimes6}(\mathbf 1[S=4]-\mathbf 1[S=3])$, a meno di un fattore scalare non nullo. L'identità si può leggere come $S+c=4+8d$, con riporto destro $d=0$ e coefficienti di segno opposto per il riporto sinistro $c$.

Per basi invertibili arbitrarie sui singoli fili, esiste anche un separatore di quattro colonne con obiettivo $(0,0,1,1)$ che fissa a zero i riporti alle sue due estremità. Nelle coordinate originali, una contrazione sui due fili di scelta con coefficienti $q_{ab}$ induce le matrici
$$
K_0(q)=\begin{pmatrix}q_{00}&q_{11}\\0&q_{01}+q_{10}\end{pmatrix},
\qquad
K_1(q)=\begin{pmatrix}q_{01}+q_{10}&0\\q_{00}&q_{11}\end{pmatrix}.
$$
I due piani di parità nelle coordinate trasformate corrispondono a due piani complementari nelle coordinate originali. Per il primo $K_0$ impongo $q_{01}+q_{10}=0$ e per l'ultimo $K_1$ impongo $q_{11}=0$. Ogni condizione interseca ciascuno dei due piani in dimensione almeno uno. Il nucleo comune delle due mappe $K_t$ è una retta, perciò almeno una delle due intersezioni dà una matrice non nulla. Ottengo una prima matrice con la sola riga $0$ non nulla e un'ultima con la sola colonna $0$ non nulla. Nelle colonne centrali le quattro proiezioni computazionali generano, rispettivamente, tutte le matrici triangolari superiori e tutte le inferiori. I prodotti dei due spazi generano tutte le matrici $2\times2$. Almeno una coppia di proiezioni rende quindi non nullo il prodotto complessivo, che è un multiplo di $|0\rangle\langle0|$. Le contrazioni hanno parità definita nelle coordinate trasformate. Su due terminali adiacenti sono firme matchgate e la composizione planare preserva il numero di termini di una somma.

Il separatore di quattro colonne isola i blocchi nella forma $\psi=(G_1\otimes\cdots\otimes G_6)\mathbf 1[S=4]$. Un esempio con le dimensioni richieste sotto è la Hadamard non normalizzata sui fili $3,5,6$ e l'identità sugli altri, contando da $1$. È la scelta locale per un blocco attivo, indipendente dalle basi sulle colonne del separatore.

## Certificato di rango

Su un blocco a sei modi calcolo gli spazi generati dalle parole di Clifford di grado pari fino a $d=0,2,4$. Per la Hadamard uniforme con separatrici di una colonna e per la scelta d'esempio del separatore di quattro colonne, i ranghi calcolati modulo $1009$ sono rispettivamente $1,53,64$. Il calcolo parte da coefficienti interi senza normalizzare la Hadamard. Per riprodurlo, si enumerano tutte le parole con $0,2,4$ indici distinti in ordine crescente fra $0,\dots,11$ e si accumulano le colonne dei vettori ottenuti, riutilizzando le colonne di grado inferiore. Con $X,Z$ matrici di Pauli, si usano come generatori $(Z_0\cdots Z_{j-1})X_j$ e $(Z_0\cdots Z_j)X_j$, $j=0,\dots,5$. Il secondo differisce dal corrispondente operatore di Majorana per una fase. Eliminazione gaussiana modulo $1009$ certifica minori non nulli anche in caratteristica zero. Le $64$ componenti della firma del separatore uniforme sono state verificate con calcolo intero, e il separatore generale è stato controllato anche in cento esempi esatti con matrici invertibili intere.

Un matchgate a $n$ modi genera, con tutte le parole di Clifford di grado al massimo $d$, uno spazio di dimensione al massimo $\sum_{j\le d}\binom nj$. Infatti una trasformazione gaussiana lo porta al vuoto, per cui sono sufficienti le parole di soli operatori di creazione. Sommando $R$ matchgate la dimensione cresce al massimo di un fattore $R$. Nel prodotto di $r$ blocchi contigui posso scegliere indipendentemente $1$, $52$ e $11$ vettori di costo rispettivamente $0,2,4$. Le parole pari agiscono localmente sui blocchi, perché le stringhe di Jordan–Wigner precedenti al blocco si cancellano. Peso i limiti per ogni $d$ con $z^d$ e sommo per tutti i $d\ge0$. Cancellando il fattore $1/(1-z)$ risulta
$$
R\ge \left(\frac{1+52z^2+11z^4}{(1+z)^6}\right)^r
\qquad(0<z<1).
$$
Per $z=1/2$ il rapporto è $940/729$. Questo dimostra il limite esponenziale per la Hadamard uniforme. Nel secondo schema i minori dei gradi $2$ e $4$ usati nell'esempio sono polinomi nelle entrate delle sei basi. Poiché sono non nulli in quell'esempio, il limite vale anche per basi locali generiche, ossia fuori da un insieme algebrico proprio. Se solo $g$ blocchi soddisfano la condizione sui minori, gli altri possono essere fissati a una componente non nulla, e il limite diventa $(940/729)^g$. Il limite ammette segni e coefficienti complessi.

Come riferimenti si aggiungono [Bravyi, Contraction of matchgate tensor networks on non-planar graphs](https://arxiv.org/abs/0801.2989), per la composizione planare, e la proposizione 3 e il lemma 13 del preliminare di Wei et al. già citato, per la filtrazione di Majorana. I separatori, i blocchi e i relativi calcoli di rango appartengono all'indagine.

## Limite uniforme per tutte le basi locali

Per la stessa famiglia con separatori di quattro colonne, il limite resta esponenziale anche nelle basi eccezionali. Vale per matrici invertibili complesse arbitrarie sui singoli fili e per l'ordine naturale comune dei terminali, con i sei fili di ogni blocco contigui. Postselezionati i separatori, scrivo $\phi$ per la firma trasformata di un blocco.

### Un invariante del blocco

Taglio la matrice dei coefficienti di $\mathbf 1[S=4]$ dopo il terzo filo. A sinistra ho pesi $1,1,2$ e a destra $2,4,4$. I soli accoppiamenti di somme parziali sono $(0,4),(2,2),(4,0)$. Ognuno dà un addendo di rango uno con supporti disgiunti sia sulle righe sia sulle colonne. La matrice ha quindi rango esattamente tre. Le matrici locali invertibili diventano trasformazioni di riga e colonna invertibili, perciò il rango rimane tre per ogni $\phi$.

### Dal rango al primo grado di Majorana

Sia $D_1(\phi)=\dim\operatorname{span}\{\phi,\gamma_1\phi,\dots,\gamma_{2n}\phi\}$, con $n$ modi e con $\gamma_i$ operatori di Majorana. Indico con $K$ il nucleo della mappa $(a,v)\mapsto(aI+v)\phi$, dove $v$ è una combinazione lineare dei Majorana. Poiché $\{v,w\}\phi=2ab\phi$ per $(a,v),(b,w)\in K$, $K$ è isotropo per la forma bilineare $v\cdot w-ab$. Dunque $\dim K\le n$.

Se $\dim K=n$, posso invertire bit affinché il coefficiente del vuoto sia diverso da zero e normalizzarlo a $1$. Queste inversioni preservano $D_1$ e il rango della matrice attraverso il taglio. Nell'algebra esterna, con creazione $x_j\wedge$ e annichilazione $\partial_j$, la mappa che associa a un elemento di $K$ i coefficienti delle sole annichilazioni è iniettiva. Se questi sono zero, i gradi zero e uno dell'equazione applicata a $\phi$ impongono rispettivamente $a=0$ e l'annullamento dei coefficienti delle creazioni. La mappa è quindi un isomorfismo. Posso scrivere le equazioni di annullamento nella forma
$$
\left(a_i+\partial_i+\sum_j B_{ij}x_j\wedge\right)\phi=0,\qquad
B_{ij}+B_{ji}=2a_i a_j .
$$
La soluzione a coefficiente costante $1$ è $\phi=(1+\ell)\exp Q$, con $\ell=-\sum_i a_i x_i$ e matrice antisimmetrica di $Q$ data da $a_i a_j-B_{ij}$. Si verifica per derivazione esterna. Per l'unicità, il primo grado non nullo della differenza fra due soluzioni dovrebbe essere annullato da ogni $\partial_i$.

Il rango di questa forma è sempre una potenza di due attraverso un taglio contiguo. Elimino i termini interni di $Q$ moltiplicando a sinistra e a destra per esponenziali locali invertibili. Con cambi lineari nei due gruppi di variabili riduco la parte incrociata a $\sum_{i=1}^k x_i y_i$. Nei $k$ modi accoppiati per parte, la matrice di $\exp Q$ è diagonale invertibile, con segni $(-1)^{s(s-1)/2}$ sul sottospazio di grado $s$. Dividere per questa diagonale trasforma la matrice principale di $(1+\ell)\exp Q$ in $I+C$, dove $C$ è una combinazione lineare di creazioni e annichilazioni sui $k$ modi. Per la parte di $\ell$ a destra, il segno di parità delle variabili a sinistra si cancella con il rapporto dei segni diagonali fra due gradi consecutivi. Perciò i termini a destra diventano annichilazioni con i consueti segni fermionici. Vale $C^2=\lambda I$ e $\operatorname{tr}C=0$. Se $\lambda\ne1$ il blocco principale è invertibile, altrimenti ha rango $2^{k-1}$. Se $\ell$ coinvolge modi non accoppiati, posso concentrare la sua componente residua su un modo per lato mediante trasformazioni locali. Ogni lato con componente residua aggiunge un blocco fuori diagonale invertibile di taglia $2^k$. Con un solo blocco aggiuntivo il rango è $2^k$. Con due, la matrice a blocchi ha rango $2^{k+1}$, dato che il blocco nell'angolo opposto a $I+C$ è zero. Tutti i casi danno una potenza di due.

C'è inoltre un salto di almeno tre nella dimensione di $K$. Aggiungo un modo e uso lo stato di parità pari $\widetilde\phi=\phi_{\rm pari}\otimes|0\rangle+\phi_{\rm dispari}\otimes|1\rangle$. Una relazione $(aI+v)\phi=0$ equivale a $(v\otimes I-iaP\otimes Y)\widetilde\phi=0$, dove $P$ è la parità dei primi $n$ modi e $Y$ è la matrice di Pauli. Questi operatori costituiscono un iperpiano nello spazio dei Majorana del sistema esteso. Se $\dim K\ge n-2$, restano al massimo tre modi dopo aver portato gli annichilatori indipendenti di $K$ a quelli standard. Per vedere che questo cambio è possibile, si prende una base isotropa ortonormale nel prodotto hermitiano. Parti reali e immaginarie danno coppie reali ortogonali, alle quali si applica una rotazione dei Majorana. La parità residua è definita. Su al massimo tre modi, ogni vettore di parità definita, dopo inversione di bit per rendere non nullo il coefficiente del vuoto, è proporzionale a $1+Q=\exp Q$. Ha dunque tutti gli annichilatori di uno stato gaussiano. Lo spazio degli annichilatori di $\widetilde\phi$ avrebbe allora dimensione $n+1$, e la sua intersezione con l'iperpiano avrebbe dimensione almeno $n$. Ne seguirebbe $\dim K=n$.

Il rango di taglio tre esclude il caso $\dim K=n$. Quindi $\dim K\le n-3$, ossia $D_1(\phi)\ge n+4$. Nel blocco a sei modi il minimo $D_1=10$ è raggiunto, per esempio applicando la Hadamard soltanto al secondo filo. Il valore è stato controllato con eliminazione senza divisioni non esatte sugli interi. Nelle $64$ scelte di identità o Hadamard sui sei fili, l'eliminazione intera ha dato le frequenze $8,16,16,24$ per $D_1=10,11,12,13$. Questi esempi controllano la soglia del primo grado, mentre il limite universale segue dalla dimostrazione.

### Prodotto di blocchi

In ciascun blocco scelgo $\phi$ e nove vettori indipendenti di grado uno. L'indipendenza dei prodotti sopravvive ai segni di Jordan–Wigner. Applico le operazioni dei blocchi da sinistra a destra. Per ogni scelta sul blocco destro, il suo vettore locale seleziona un sottospazio indipendente, mentre sul prefisso l'operazione induce soltanto una potenza fissata della parità, che è invertibile. Per induzione ottengo almeno $\sum_{j\le d}[z^j](1+9z)^r$ vettori indipendenti fino al grado $d$. Il confronto con il limite gaussiano e la somma pesata danno
$$
R\ge\left(\frac{1+9z}{(1+z)^6}\right)^r
\quad(0<z<1),
\qquad
R\ge \left[\frac85\left(\frac{15}{16}\right)^6\right]^r
>1.086^r .
$$
Il secondo limite sceglie $z=1/15$. Per ogni $d$ il vincolo di rango è chiuso, perché è espresso dall'annullamento di minori. Il limite esclude anche che la firma sia limite di somme con meno termini, nella stessa rappresentazione.

Il formalismo dei gaussiani fermionici con termini lineari è trattato da [Lyu e Bu, Displaced Fermionic Gaussian States and their Classical Simulation](https://arxiv.org/abs/2411.18517). La filtrazione di Majorana per gli stati gaussiani è quella del lemma 13 di Wei et al. citato sopra. Il criterio via rango tre, il salto applicato a questi blocchi e il limite uniforme sono derivati qui.

## Cambi congiunti sui due fili di una colonna

La barriera precedente è superabile con un cambio invertibile $4\times4$ su ciascuna coppia di fili di scelta. Per una catena di lunghezza arbitraria con due scelte per colonna e riporti binari, l'intera firma aperta nella nuova base è una somma di al massimo due matchgate.

Ordino le variabili di una colonna come $a,x,y,d$, rispettivamente riporto entrante, primo e secondo filo di scelta, e riporto uscente. Considero il vettore a coefficienti esterni
$$
\Phi=(1+y)\exp(ax+xd)=1+y+ax+xd+axy-xyd ,
$$
dove le variabili anticommutano e i monomi sono nell'ordine indicato. Nei settori $(a,d)=(0,0),(1,0),(0,1),(1,1)$ i rispettivi vettori sui fili interni sono $1+y,x+xy,x-xy,0$. Nella base fisica $(00,10,01,11)$ uso le matrici intere
$$
A_0=\begin{pmatrix}
0&0&0&2\\
2&1&1&0\\
0&-1&1&2\\
-2&1&1&0
\end{pmatrix},
\qquad A_1=A_0 P_{00,11},
$$
dove $P_{00,11}$ scambia la prima e l'ultima coordinata. Per $t=0$, il tensore $T_t=\mathbf1[s_1+s_2+a=t+2d]$ trasformato da $A_0$ sui fili di scelta è $2\Phi$ con il bit $d$ invertito. Per $t=1$ è $2\Phi$ con il bit $a$ invertito. Il controllo direttamente sui coefficienti dà tutte le $32$ uguaglianze.

Per il prodotto delle colonne non invertite, in ordine naturale, ogni termine lineare $y_i$ ha quadrato zero e ogni commutatore ordinario $[y_i,y_j]=2y_i y_j$ commuta con tutti gli altri termini. La formula di Baker–Campbell–Hausdorff si arresta al commutatore, dunque
$$
\prod_i(1+y_i)\exp(a_i x_i+x_i d_i)
=(1+L)\exp Q,\qquad
L=\sum_i y_i,\quad Q=\sum_i(a_i x_i+x_i d_i)+\sum_{i<j}y_i y_j .
$$
Le due parti $\exp Q$ e $L\exp Q$ sono firme gaussiane di parità opposta. Per la seconda, un cambio lineare invertibile delle variabili porta $L$ sul primo modo, così i termini di $Q$ contenenti quel modo spariscono per moltiplicazione e rimane un prodotto gaussiano con il primo modo occupato. I bit dei riporti si invertono in entrambi i termini. Si contraggono poi soltanto coppie adiacenti, usando $\langle00|+\langle11|$, e si fissano i riporti ai confini. Queste operazioni preservano le firme matchgate. I primi quattro valori della lunghezza sono stati verificati per tutte le sequenze di obiettivi e tutti i coefficienti esposti ($4680$ confronti con il prodotto di matrici di riporto). Fino a tre colonne sono state verificate anche tutte le identità matchgate di entrambe le componenti di parità.

### Due termini sono necessari nella famiglia precedente

I separatori di quattro colonne della prova precedente funzionano anche con arbitrarie matrici invertibili $4\times4$ sulla coppia di fili. La dimostrazione usa soltanto il fatto che i due piani di parità restano complementari. Isolato il blocco con obiettivo $(0,0,1)$, il rango rispetto ai due fili della colonna centrale contro gli altri quattro è esattamente tre. In quella colonna compaiono tre vettori indipendenti, $|00\rangle$, $|01\rangle+|10\rangle$, $|11\rangle$, associati a coppie indipendenti di vettori delle colonne esterne. Il rango è invariante sotto i tre cambi di base congiunti.

Per un singolo matchgate, il rango attraverso una bipartizione fermionica è una potenza di due. Per applicarlo a questo intervallo interno, sposto la colonna centrale $B$ a sinistra con una permutazione fermionica. Il segno aggiunto è $(-1)^{p_Ap_B}$, dove $p_A,p_B,p_C$ sono le tre parità. Sulla firma di parità totale fissata $\delta$ si ha $p_B=\delta+p_A+p_C$ modulo due. Il segno è quindi una trasformazione diagonale invertibile sulla sola parte esterna $AC$ e preserva il rango ordinario. Per il rango fermionico si può usare la decomposizione in coppie di [Botero e Reznik, BCS-like Modewise Entanglement of Fermion Gaussian States](https://arxiv.org/abs/quant-ph/0404176). Il rango tre esclude così una singola firma, mentre la costruzione precedente ne fornisce due.

### Il costo nei vincoli che identificano le scelte

Per chiudere l'istanza, ogni scelta deve coincidere nei due punti in cui compare il suo addendo. Sia $E$ la firma di tali uguaglianze, e $A$ il prodotto delle basi di colonna. Il conteggio è l'accoppiamento bilineare fra la firma aritmetica trasformata e $A^{-T}E$. Il risultato sui due termini riguarda la prima firma.

Per le basi esplicite precedenti, anche istanze con gruppi indipendenti di tre colonne possono richiedere una somma esponenziale sul lato delle uguaglianze. In ogni gruppo uso tre addendi, uno per ciascun lato del triangolo fra le colonne. I tre bit di scelta sono $e_0,e_1,e_2$, e nella colonna $j$ i due fili leggono $e_j,e_{j-1}$ (indici modulo tre). Uso l'obiettivo $(1,1,0)$ nel gruppo. Pongo
$$
D_0=4A_0^{-T}=\begin{pmatrix}
0&2&-2&2\\
1&1&1&0\\
0&-2&2&0\\
-1&1&1&0
\end{pmatrix},
\qquad D_1=D_0P_{00,11}.
$$
La firma del triangolo ha, a meno di scala non nulla, coordinate
$$
\eta(b_0,b_1,b_2)
=\sum_{e_0,e_1,e_2}\prod_{j=0}^2
 D_{t_j}[b_j,e_j+2e_{j-1}] .
$$
Numerando i sei fili da sinistra a destra e gli indici di ogni coppia come $b_j=x_j+2y_j$, l'eliminazione modulo $1009$ sulle colonne $\gamma_{i_1}\cdots\gamma_{i_k}\eta$ per $k=0,1,2,3$ dà ranghi cumulativi $1,13,63,64$. Si usano le convenzioni dei Majorana sopra, con parole di indici distinti crescenti e in ordine lessicografico all'interno di ciascun grado. La somma dei quadrati dei coefficienti interi di $\eta$ è $2616$. I prodotti dei pivot in tale ordine, ridotti modulo $1009$, sono $985,743,969,516$. Questi ranghi sono limiti inferiori in caratteristica zero. Ripetendo $r$ triangoli, la stessa prova di indipendenza per blocchi contigui e il confronto gaussiano danno
$$
R_E\ge \left(\frac{1+12z+50z^2+z^3}{(1+z)^6}\right)^r > 1.89^r
\quad\text{per }z=3/10 .
$$
È un limite sulla rappresentazione separata delle uguaglianze con queste basi. In questa famiglia ogni gruppo, spostato opportunamente di bit, ha pesi $3,5,6$ e obiettivo $3$. L'istanza stessa ammette una soluzione immediata scegliendo il peso $3$ in ogni gruppo.

Il difetto del lato delle uguaglianze persiste genericamente nella famiglia di basi ottenute sostituendo nella colonna $\Phi$ con $(1+\lambda y)\exp(pax+qxd)$, per $\lambda,p,q\ne0$, e completando a piacere la base sul vettore antisimmetrico. Il prodotto aperto ha ancora al massimo due termini, anche con parametri diversi per colonna. I minori certificati sopra diventano funzioni razionali dei parametri e sono non nulli nell'esempio, dunque fuori dal loro luogo di annullamento. Questo argomento lascia aperte le scelte eccezionali di basi congiunte.

## Difficoltà parametrica del numero di tratti

Per Subset Sum sul ciclo semplice, con parametro $r$ pari al numero di tratti costanti dell'obiettivo, la decisione è W[1]-hard e il conteggio è #W[1]-hard. Sotto ETH è escluso anche un tempo $f(r)N^{o(r/\log(r+2))}$, per qualunque funzione computabile $f$. La riduzione qui costruita parte da un sistema di vincoli binari con domini finiti. Per ciascuna variabile $i$ si sceglie un indice $a_i\in[1,n_i]$. Per ciascuna coppia con vincolo è data la lista delle coppie di indici ammesse. Più vincoli sulla stessa coppia si possono intersecare prima della riduzione.

### Selezionare e leggere la posizione di un cambio

Un blocco di selezione è un tratto di zeri con riporto entrante zero, seguito da una colonna senza scelte con obiettivo uno. Quest'ultima impone riporto entrante uno e uscente zero. Nel tratto avviene perciò un solo passaggio da zero a uno.

Una colonna di lettura ha obiettivo zero e un arco fissato a zero. L'altro arco legge il riporto $c$ e questo non può cambiare nella colonna, poiché $x+c=2d$ impone $x=c=d$. Le estremità fisse a zero si realizzano con un'unica zona iniziale di colonne a bit zero, una per ogni arco da fissare, seguita da una colonna zero senza scelte. La zona inizia e finisce con riporto zero e la monotonia lo mantiene zero. Per uguagliare due letture si usa direttamente lo stesso arco. Per renderle complementari si collegano i loro due archi a una colonna con obiettivo uno nella zona iniziale, prima degli zeri. In questo tratto di uni il riporto iniziale è zero e resta zero, quindi esattamente uno dei due archi è scelto.

Ogni opzione $j$ ha una colonna marcatrice, con obiettivo zero e due archi. Uno porta il valore $d$ del riporto uscente, letto nella prima colonna dopo la marcatrice. L'altro porta $p_j$. L'equazione $d+p_j+c=2d$ dà $p_j=d-c$. L'arco $p_j$ è selezionato esattamente se la marcatrice accende il riporto. Indico con taglio $j$ la zona dopo la marcatrice $j$ e prima della successiva, con taglio zero prima di tutte e taglio $n_i$ dopo l'ultima. Se la scelta è $a_i$, il riporto al taglio $j$ è $C_i(j)=\mathbf1[a_i\le j]$.

### Confrontare la scelta con gli estremi di un vincolo

Uso sei blocchi per una variabile: due per la scelta principale, due lettori in ordine crescente e due in ordine inverso. I primi due accoppiano direttamente gli archi $p_j$, così indicano la stessa scelta. Nei lettori in ordine crescente uguaglio, per ogni taglio $j$, due letture distinte del blocco principale alle letture all'inizio e alla fine del sito di controllo del lettore. Le letture sono prima e dopo tutte le colonne di controllo del sito e non passano per una marcatrice. Nei lettori inversi impongo invece il complemento del riporto al taglio $n_i-j$ del blocco principale, ottenendo al taglio $j$ il valore $1-C_i(n_i-j)$. L'uguaglianza delle due letture di ogni sito, insieme alla monotonia, garantisce che il riporto sia costante durante i controlli. Anche i lettori possono quindi accendere il riporto soltanto su una marcatrice. Collegando fra loro i $p_j$ dei due lettori dello stesso verso si terminano questi archi senza nuove libertà.

Per un vincolo fra due variabili uso otto copie sincronizzate di un blocco la cui lista contiene tutte le coppie ammesse. Sincronizzo per uguaglianza delle letture a ogni taglio. Ogni coppia $(u,v)$ ha così otto copie del segnale $p$ che vale uno se e solo se quella coppia è scelta. Quattro coppie di copie servono rispettivamente a verificare $a_i\le u$, $a_i\ge u$, $a_j\le v$ e $a_j\ge v$, tutte condizionate a $p=1$.

Un controllo è una coppia di colonne, una in ciascuno dei due lettori dello stesso verso della variabile interessata. Metto nelle colonne le due copie di $p$ e un arco comune $q$ fra loro. Siccome il riporto del sito vale $C$ ed è costante, entrambe le equazioni sono $p+q=C$. Vi è una sola scelta di $q$ se $p\le C$, e nessuna altrimenti. Nel lettore crescente uso il taglio $u$, quindi $C=\mathbf1[a_i\le u]$. In quello inverso uso il taglio $n_i-u+1$, quindi $C=1-C_i(u-1)=\mathbf1[a_i\ge u]$. Si fa lo stesso per l'altro estremo. Ogni scelta delle variabili che soddisfa i vincoli seleziona un'unica coppia dichiarata in ciascuna lista e fissa tutti gli archi ausiliari. Ogni soluzione numerica determina a sua volta un'assegnazione soddisfacente.

### Un solo ciclo e numero di tratti

Ogni colonna incide su al massimo due archi. Il grafo degli addendi è una foresta di cammini corti. Le letture terminano sempre in una colonna di fissaggio. Un'uguaglianza, un complemento, un collegamento di marcatori o una coppia di controlli si trova in un cammino con queste estremità. Il cammino più lungo va da un fissaggio a una lettura, una marcatrice, due controlli, l'altra marcatrice, un'altra lettura e l'altro fissaggio. Le colonne vuote sono vertici isolati. Applico il completamento precedente con i collegamenti a due nuove posizioni e il blocco finale con obiettivo locale $29$. Tutti gli archi di completamento diversi dai due archi interni noti sono forzati a zero, e il conteggio rimane invariato. Si ottiene un solo ciclo semplice, con pesi distinti e strettamente minori dell'obiettivo.

Se il sistema ha $k$ variabili e $m$ coppie vincolate, uso $6k+8m$ blocchi di selezione. Ciascuno contribuisce al massimo due tratti. La zona per i complementi, la zona per i fissaggi e il completamento aggiungono al massimo sei tratti, perciò $r\le12k+16m+6$. Il numero di colonne è lineare nella somma delle dimensioni dei domini e delle liste delle coppie ammesse, più $k+m$. In particolare ogni lettura di sincronizzazione è creata un numero costante di volte per candidato e ogni coppia in una lista aggiunge un numero costante di controlli. La codifica esplicita dei pesi resta polinomiale.

Una Clique multicolore è il caso con una variabile per classe e una lista di adiacenze per ogni coppia di classi. La riduzione è parametrica perché $m=\binom{k}{2}$, ed è parsimoniosa. Ne seguono W[1]-hardness e #W[1]-hardness. Si veda [Jerrum e Meeks, Some hard families of parameterised counting problems](https://eprints.gla.ac.uk/97129/1/97129.pdf), §1.2, per la durezza del problema di partenza.

Per il limite ETH parto direttamente da Partitioned Subgraph Isomorphism. Ogni vertice del grafo modello è una variabile e ogni suo arco dà una lista di coppie. Basta la famiglia di modelli senza vertici isolati usata da [Marx, Can You Beat Treewidth?](https://toc.cs.uchicago.edu/articles/v006a005/v006a005.pdf), corollari 6.2 e 6.3. Se $m$ è il numero di archi del modello, allora $k\le2m$ e $r=O(m)$. Marx esclude un tempo $f(G)n^{o(m/\log m)}$ sotto ETH per il modello $G$ e il grafo ospite di taglia $n$. Poiché l'istanza numerica prodotta ha taglia polinomiale, un tempo $f(r)N^{o(r/\log(r+2))}$ violerebbe quel limite. I casi con dominio o lista vuoti si possono riconoscere prima e inviare a un'istanza negativa fissa, il ciclo con pesi $3,5,6$ e obiettivo $7$.

### Verifica

Un enumeratore di attribuzioni ai domini e un risolutore esatto delle equazioni di colonna danno gli stessi conteggi su 68 istanze di Clique multicolore, di cui 14 negative, e su altri 75 sistemi di vincoli, inclusi 60 con grafo dei vincoli a cammino. Nelle prime 68 prove si sono contate le soluzioni sia prima sia dopo il completamento, con fino a 6022 colonne. Per la versione completata si sono fissati gli archi ausiliari come imposto dal blocco finale. La condizione di quel blocco è stata ricontrollata indipendentemente su tutti i suoi $64$ sottoinsiemi locali: nessuno totalizza $28$ e soltanto $\{5,24\}$ totalizza $29$.

## Classificazione parametrica esatta per il ciclo unico

Per Subset Sum sul ciclo semplice, con parametro $r$ pari al numero di tratti costanti dell'obiettivo, la decisione è W[1]-completa e il conteggio esatto è #W[1]-completo. La sezione precedente prova la durezza. Per l'appartenenza costruisco una riduzione parsimoniosa nella direzione inversa, verso Clique multicolore con $O(r^2)$ classi.

Per ciascun tratto $i$ di lunghezza $\ell_i$, le opzioni locali sono i due riporti costanti e gli $\ell_i$ possibili punti in cui il riporto cambia nel verso consentito. Ogni opzione specifica tutti i gradi richiesti $s_v$ nel proprio tratto. Le opzioni di tratti consecutivi devono avere lo stesso riporto sul confine comune, e il primo e l'ultimo riporto devono essere zero. Questi sono vincoli unari o binari.

Siano $v_0,\ldots,v_{N-1}$ le colonne in ordine ciclico, e sia $b$ la scelta dell'arco prima di $v_0$. Dalle opzioni dei tratti determino interi $x_{-1}=b$, $x_j=s_{v_j}-x_{j-1}$. La chiusura del ciclo e l'appartenenza di tutti gli $x_j$ a $\{0,1\}$ equivalgono a
$$
F=\sum_{j=0}^{N-1}x_j(x_j-1)+(x_{N-1}-b)^2=0.
$$
Infatti ogni addendo è non negativo per argomenti interi. Ogni sottoinsieme valido determina un solo insieme di opzioni e un solo $b$, e viceversa.

Il vettore $x$ dipende additivamente dalle scelte. Per il tratto $i$ posso precalcolare, per ciascuna opzione $a$, il vettore $q_{i,a}$ ottenuto dalla ricorrenza con $b=0$ e con tutti i gradi degli altri tratti posti a zero. Completo il vettore con una coordinata uguale all'ultima, per rappresentare il contributo a $x_{N-1}-b$. Per $b$ includo il suo vettore di contributi, l'alternanza di segno nella ricorrenza e l'ulteriore $-b$ nell'ultima coordinata. La somma di questi vettori ha prime $N$ coordinate $x_j$ e ultima coordinata $x_{N-1}-b$. Quindi $F$ è la norma quadrata di questa somma meno la somma delle prime $N$ coordinate. Espandendo il quadrato, si ricava una costante più $O(r^2)$ termini tabulabili, ciascuno dipendente da al più due scelte. Ogni peso è di grandezza polinomiale in $N$.

Creo una variabile ausiliaria per ogni termine tabulato. Un valore del suo dominio è una tupla con gli indici delle scelte interessate, la somma parziale prima del termine e quella dopo. Mantengo soltanto le tuple in cui la differenza delle somme coincide con il termine. Tutte le somme appartengono a un intervallo intero di ampiezza polinomiale. I vincoli binari fanno coincidere gli indici con le variabili originali e le somme parziali fra termini adiacenti. Impongo somma iniziale zero e somma finale zero, includendo l'eventuale costante fra i termini. Ogni assegnazione valida determina univocamente tutte le tuple ausiliarie. Una classe per ogni variabile e un arco per ogni coppia di valori compatibili danno Clique multicolore, ancora con una soluzione per ogni sottoinsieme. Il problema di conteggio di arrivo è #W[1]-completo, si veda [Jerrum e Meeks, Some hard families of parameterised counting problems](https://eprints.gla.ac.uk/97129/1/97129.pdf), §1.2.

### Conteggio per mezzo di tre gruppi

La stessa identità dà un algoritmo diretto. Fisso $b\in\{0,1\}$ e divido i tratti in tre gruppi $A,B,C$. Un vertice del gruppo rappresenta una scelta di opzioni locali in tutti i suoi tratti. Elimino le scelte incompatibili interne a un gruppo e gli archi fra scelte con riporti incompatibili sui confini. Ogni arco fra due gruppi riceve la somma dei termini di $F$ che li collegano. Attribuisco il costo interno del gruppo sorgente al suo arco uscente nel giro $A\to B\to C\to A$, e attribuisco la costante a uno solo dei tre archi. Il risultato è che il peso totale di un triangolo è esattamente $F$.

Sommo una costante $H$ a ciascun peso per rendere non negativi tutti gli esponenti. Nelle tre matrici $P_{AB},P_{BC},P_{CA}$ sostituisco ogni arco di peso $w$ con $X^{w+H}$ e ogni arco vietato con zero. Il coefficiente di $X^{3H}$ nella traccia di $P_{AB}P_{BC}P_{CA}$ conta esattamente i triangoli validi. Il grado è polinomiale in $N$. Equivalentemente, si può valutare in una base intera potenza di due maggiore del numero di tutti i triangoli e poi estrarre la cifra in posizione $3H$. Le operazioni aritmetiche hanno costo polinomiale in $N$ per entrata dei prodotti, perché il grado è polinomiale e la lunghezza binaria della base è $O(r\log(N+2))$.

Con gruppi di al più $\lceil r/3\rceil$ tratti, la dimensione massima delle matrici è $(N+2)^{\lceil r/3\rceil}$. Usando [Strassen, Gaussian Elimination is not Optimal](https://deltadbu.github.io/UCAS_algorithm_course/Lectures/Lec5-Matrix-Multiplication-Strassen1969.pdf), il costo esatto è
$$
N^{(\log_2 7)r/3+O(1)}.
$$
Si può anche bilanciare il prodotto delle dimensioni dei domini, anziché il numero dei tratti. Assegnando ciascun tratto al gruppo con somma di logaritmi delle dimensioni al momento più piccola, la somma massima finale è al più un terzo del totale più due terzi del massimo logaritmo individuale. Di conseguenza il costo è al più $\operatorname{poly}(N)\bigl(\prod_i(\ell_i+2)\bigr)^{(\log_2 7)/3}$.

La verifica quadratica e il conteggio per triangoli hanno dato lo stesso conteggio dell'enumerazione diretta su 425 istanze, con 11412 coppie di configurazione dei riporti e bit iniziale esaminate. In 276 delle istanze è stata verificata anche la traccia codificata in un intero, mediante moltiplicazione esatta. Questi controlli attestano l'identità del conteggio. Il limite temporale deriva dalla sostituzione del prodotto matriciale con l'algoritmo di Strassen.

## Limite lineare nell'esponente se si ammettono più cicli

Se il grafo degli addendi può essere unione di cicli, sotto ETH è escluso un tempo $f(r)N^{o(r)}$. Qui il parametro della riduzione da Clique multicolore cresce solo linearmente nel numero delle classi, a differenza della riduzione che usa un blocco per ogni vincolo. La decisione e il conteggio su questa variante ammettono comunque $N^{O(r)}$ enumerando i riporti e propagando separatamente su ciascun ciclo. Si veda il lemma 13 in [Tight Bounds for Clique-Packing Parameterized by Clique-Width](https://drops.dagstuhl.de/storage/00lipics/lipics-vol388-esa2026/html/LIPIcs.ESA.2026.115/LIPIcs.ESA.2026.115.html) per il limite ETH di partenza.

Per ogni classe costruisco sei blocchi di selezione e lettura come nella sezione parametrica. Uso il blocco principale e la sua copia, due lettori crescenti e due lettori inversi. Per una scelta $a_i$ nella classe $i$, mantengo l'indicatore $C_i(u)=\mathbf1[a_i\le u]$ nei siti crescenti, e il complemento della lettura corrispondente nei siti inversi. Le letture prima e dopo i siti mantengono il riporto costante attraverso i controlli. Posso quindi aggiungere arbitrarie colonne con due scelte e grado richiesto $C_i(u)$ oppure $1-C_i(u)$ senza aggiungere un nuovo tratto. Posso anche aggiungere colonne con grado richiesto uno nella zona iniziale di uni a riporto zero.

Per ogni coppia vietata $(u,v)$ fra le classi $i,j$, uso un cammino di sei colonne con due fili terminali aperti. Chiamo $M_0,M_1$ le matrici dei gradi zero e uno della sezione precedente. Il cammino ha matrice di trasferimento
$$
P=M_{C_i(u-1)}\,M_{1-C_j(v-1)}\,M_1\,
M_{C_j(v)}\,M_{1-C_i(u)}\,M_1 .
$$
Ogni fattore condizionale è una colonna nel corrispondente sito di lettura. Sono colonne consecutive nel grafo degli addendi, attraverso gli archi del cammino, mentre ciascuna occupa la propria posizione nell'ordine binario. Calcolando i nove casi, con righe e colonne corrispondenti rispettivamente a $a_i<u,a_i=u,a_i>u$ e $a_j<v,a_j=v,a_j>v$, le matrici $P$ valgono
$$
\begin{pmatrix}
E_{11}&E_{01}&E_{11}\\
E_{01}&0&E_{01}\\
E_{00}&E_{01}&E_{00}
\end{pmatrix}.
$$
Qui $E_{ab}$ è la matrice $2\times2$ con un solo uno in posizione $(a,b)$, con indici da zero. Creo due copie identiche del cammino e unisco i loro terminali sinistri fra loro e i destri fra loro. Il controllo è un ciclo di dodici colonne e contribuisce $\operatorname{tr}(PP^{\mathsf T})$. Quindi esiste una sola configurazione degli addendi del controllo per ogni coppia ammessa, e nessuna per la coppia vietata.

I cicli di controllo sono già completi. Le altre componenti sono cammini, come per i blocchi di selezione e sincronizzazione precedenti. Completo soltanto questi ultimi in un ciclo aggiuntivo con la stessa costruzione finale di obiettivo locale $29$. Ne risultano pesi distinti, due bit a uno per addendo e due occorrenze per colonna. I bit dell'obiettivo sono costanti in tutti i siti di uno stesso tratto. Il numero di tratti è al più $12k+6$ per $k$ classi, anche con una quantità arbitraria di coppie vietate. Il numero di colonne è polinomiale nelle dimensioni delle classi. La riduzione conserva il numero di soluzioni e trasferisce il limite ETH $f(k)n^{o(k)}$ di Clique multicolore.

La tabella di nove casi e la costruzione completa sono state verificate. Su 85 istanze di Clique multicolore, 50 positive e 35 negative, il conteggio delle equazioni di colonna ha coinciso con quello diretto delle clique. Le istanze arrivano a 1530 colonne e 34 cicli di controllo.

## Limite al collegamento dei controlli di soglia

Le sole letture di soglia non permettono di collegare arbitrariamente i controlli del caso precedente. Il seguente limite riguarda il modello locale in cui, dopo aver fissato le scelte, ciascuna colonna ha grado richiesto $s\in\{0,1,2\}$ determinato da una sola variabile ordinata oppure costante. Se la funzione di una variabile assume due valori consecutivi, richiedo che non isoli una singola posizione interna del dominio come unica occorrenza di un valore. La condizione comprende tutte le soglie dirette o inverse dei blocchi precedenti. Comprende anche il grado in una colonna marcatrice interna, che assume tutti e tre i valori $0,1,2$.

### Un singolo controllo con un estremo fissato

Siano $a,b$ due variabili con posizioni interne $u,v$. Considero un cammino di colonne con filo iniziale fissato e filo finale libero o fissato. Un tale cammino non può accettare esattamente tutte le coppie salvo $(u,v)$.

Per un filo iniziale fissato, la ricorrenza $x_j=s_j-x_{j-1}$ determina ogni filo. Poiché ogni $s_j$ dipende al più da una variabile, ogni $x_j$ è della forma $f_j(a)+g_j(b)$ con $f_j,g_j$ interi. Una funzione di questa forma che è binaria sull'intero prodotto dei domini dipende da al più una variabile. Infatti, se entrambe le funzioni variano, il massimo meno il minimo dell'intera somma è almeno due.

Suppongo che il cammino accetti tutte le coppie diverse da $(u,v)$ e considero il primo filo che diventa non binario in $(u,v)$. Se il filo precedente e il grado della colonna dipendono dalla stessa variabile, o uno è costante, la violazione coinvolge anche una delle coppie che devono essere accettate. Rimane, a meno di scambiare le variabili, $x_{j-1}=f(a)$ e $s_j=g(b)$. Per un qualsiasi $a\ne u$, tutti i valori di $b$ devono dare un esito binario. Quindi $g$ può assumere soltanto uno o due valori consecutivi. Per l'ipotesi sui gradi, esiste $b'\ne v$ con $g(b')=g(v)$. La coppia $(u,b')$ subisce allora la stessa violazione. Se tutti i fili sono binari sull'intero prodotto, anche l'ultimo dipende da al più una variabile, e fissarlo non può escludere soltanto $(u,v)$.

### Quante componenti possono servire

Nel medesimo modello, per escludere $k$ coppie interne su $k$ coppie di variabili fra loro disgiunte, con tutte le altre combinazioni ammesse, servono almeno $k$ cicli nel grafo degli addendi. Questo vale anche quando il bit iniziale di ogni ciclo è libero.

Se un ciclo ha su un'assegnazione ammessa un vertice di grado zero o due, fisso ai valori di quell'assegnazione la coppia di variabili che contiene la variabile da cui dipende quel grado. Se il grado è costante, non serve fissare una coppia. Il vertice fissa entrambi i suoi fili e permette di trattare il resto del ciclo come un cammino. Su qualunque coppia di variabili ancora libera, fissate tutte le altre a valori ammessi, il cammino accetta tutte le combinazioni ammesse. Per il lemma accetta anche la coppia interna che si voleva escludere.

Ripeto per ogni ciclo ancora privo di un vertice fissato che possa avere grado zero o due su un'assegnazione ammessa delle coppie rimaste. Per ciascun ciclo si fissa al massimo una coppia. Se ci sono meno di $k$ cicli, alla fine rimane almeno una coppia libera. In ogni ciclo ancora privo di un vertice fissato tutte le colonne hanno grado uno su tutte le assegnazioni ammesse rimaste. Ogni variabile libera assume tutti i valori del proprio dominio su queste assegnazioni. Dato che il grado di una colonna dipende da al più una variabile, tali colonne mantengono grado uno anche sulla coppia interna esclusa. Si ottiene così una configurazione ammessa da ogni ciclo e proibita dalla relazione richiesta.

Questo risultato spiega perché la fusione diretta delle componenti mediante altri cammini di soglia non può dare in generale un unico ciclo. La conclusione riguarda la rappresentazione con gradi unari specificata sopra. Un meccanismo che accoppia i gradi a più scelte, oppure che introduce un diverso tipo di dipendenza unaria, è fuori dal lemma.

L'esplorazione esaustiva con due domini da tre elementi e le 23 funzioni unarie ammesse su ciascuno ha trovato 14 stati binari raggiungibili per ciascun bit iniziale, mantenendo valide le otto coppie ammesse. Nessuna transizione conserva quelle otto coppie e fa fallire soltanto la nona. La dimostrazione sopra vale indipendentemente dall'enumerazione.

## Classificazione parametrica quando il grafo ha più cicli

Per un'unione disgiunta di cicli, la decisione è W[1]-completa rispetto al numero $r$ di tratti. Anche il conteggio delle sole configurazioni dei riporti che ammettono almeno un sottoinsieme è #W[1]-completo con lo stesso parametro. La versione che conta tutti i sottoinsiemi ha una molteplicità per configurazione e va trattata a parte.

Per ogni ciclo $C$ e bit iniziale $b\in\{0,1\}$ uso la penalità $F_{C,b}$ della sezione sul ciclo unico, calcolata soltanto sui vertici di $C$. A riporti fissati, la penalità è un intero non negativo e si annulla esattamente se quel bit iniziale dà una scelta valida. Ogni ciclo ammette una scelta se e solo se
$$
\Phi=\sum_C F_{C,0}F_{C,1}=0 .
$$
I due fattori eliminano la necessità di indovinare separatamente il bit iniziale di ciascun ciclo. Ogni $F_{C,b}$ è una somma di termini tabulabili dipendenti da al più due opzioni di tratto. Il prodotto ha interazioni fra al massimo quattro opzioni. Posso aggregare le tabelle, sommando su tutti i cicli, per ciascun insieme di al più quattro tratti. Restano $O(r^4)$ tabelle con valori di grandezza polinomiale in $N$. Il procedimento con somme parziali e vincoli binari usato per il ciclo unico, applicato ora a termini con al massimo quattro indici, dà una riduzione parsimoniosa a Clique multicolore. Ogni configurazione dei riporti realizzabile corrisponde a una clique. Per la durezza del conteggio delle configurazioni, nella precedente riduzione sul ciclo unico il blocco finale contiene un vertice forzato a grado zero. Esiste quindi al massimo un sottoinsieme per configurazione dei riporti, e la riduzione precedente da Clique multicolore conserva anche il numero delle configurazioni. Per la definizione parsimoniosa delle classi di conteggio si veda [Jerrum e Meeks, Some hard families of parameterised counting problems](https://eprints.gla.ac.uk/97129/1/97129.pdf), §1.2.

Un ciclo con almeno un grado zero o due ha al massimo una soluzione per configurazione, perché quel vertice fissa entrambi i fili incidenti. Se tutti i gradi sono uno, le soluzioni sono due per un ciclo pari e zero per un ciclo dispari. Pertanto, date le sole configurazioni realizzabili $\mathbf c$, il conteggio di tutti i sottoinsiemi è
$$
\sum_{\mathbf c:\,\Phi(\mathbf c)=0}2^{g(\mathbf c)},
$$
dove $g$ conta i cicli pari con tutti i gradi uno. La molteplicità può essere esponenziale persino per $r=1$. Con obiettivo composto interamente da uni e un'unione di cicli di lunghezza quattro, i riporti restano tutti a zero e tutti i gradi valgono uno. Ci sono $2^{N/4}$ sottoinsiemi per la sola configurazione. Con parametro $r$ una riduzione parsimoniosa a Clique multicolore non può preservare tale conteggio. A parametro fissato la taglia dell'istanza prodotta sarebbe polinomiale e il numero di classi limitato, consentendo soltanto un conteggio polinomiale. Con parametro combinato $r+h$, dove $h$ è il numero di cicli, il conteggio di tutti i sottoinsiemi è invece #W[1]-completo. Si mantiene un bit iniziale per ciclo e si impone $\sum_C F_{C,b_C}=0$, conservando una sola scelta ausiliaria per ogni sottoinsieme.

Nella formula pesata, anche $g$ ha una descrizione geometrica. Indico con $\lambda_i=0$ l'opzione del tratto $i$ in cui tutti i gradi sono uno, con $\lambda_i=\ell_i+1$ quella in cui sono tutti fissati, e altrimenti con $\lambda_i$ la posizione del cambio, numerata da uno. Un ciclo pari contribuisce a $g$ esattamente se, in ogni tratto che incontra, $\lambda_i$ precede la sua prima colonna. Il conteggio dei cicli liberi è dunque un conteggio di punti dominanti in dimensione $r$. Questa osservazione descrive il peso di una configurazione data.

Ai fini del controllo, la penalità globale, le configurazioni realizzabili e la loro molteplicità sono state confrontate con l'enumerazione di tutti i sottoinsiemi su 377 istanze, di cui 207 con più cicli, per un totale di 6021 configurazioni aritmeticamente ammissibili. L'espansione in termini dipendenti da al più quattro scelte è stata ricontrollata in 311 casi.

## Derivazioni per i limiti di circuito

### Limiti booleani incondizionati

Fissare i bit costanti e rinominare gli altri preserva fan-in e profondità dei circuiti booleani. Compilare Parity, che ha un circuito lineare di XOR e quindi di AND e NOT di taglia lineare, realizza una famiglia con $N=\Theta(m)$ che richiede $2^{\Omega_d(N^{1/(d-1)})}$ porte a profondità fissa $d\ge2$ nel modello con AND e OR a fan-in illimitato e negazioni agli ingressi. È il trasferimento del [limite di Håstad per Parity](https://eccc.weizmann.ac.il/report/2019/073/), sulla restrizione ai bit obiettivo liberi.

Si ottiene anche una restrizione dell'obiettivo che è essa stessa monotona e difficile per circuiti booleani monotoni. Uso la funzione di Harnik–Raz su $m$ bit, per $m$ primo. Il verificatore riceve come testimone i coefficienti di un polinomio $P$ su $\mathbb F_m$, di grado minore di $c=\Theta(\sqrt m/\log m)$. Verifica che fra $P(1),\ldots,P(k)$, con $k=\lfloor\sqrt m\rfloor$, ci siano almeno $k/2$ valori distinti e che tutti i corrispondenti bit di ingresso siano uno. Uso i parametri di [Cavalar, Kumar e Rossman, Monotone Circuit Lower Bounds from Robust Sunflowers](https://eccc.weizmann.ac.il/report/2020/181/revision/2/download/), §2.2 e teorema 2.19.

C'è un verificatore con $O(m\log^3 m)$ porte. Con Horner si fanno $O(kc)$ operazioni modulari, ognuna in $O(\log^2 m)$ porte con aritmetica scolastica. Confronti fra tutte le coppie di valori calcolati e l'indicatore di prima occorrenza danno il numero di valori distinti in $O(k^2\log m)$ porte. Per leggere i bit di ingresso uso una rete di ordinamento bitonica di Batcher. Ordino insieme i $m$ record dati e i $k$ record che chiedono un bit. Ogni chiave è un indice di $O(\log m)$ bit, e a parità di chiave il dato precede la richiesta. Una scansione aggiorna il bit da controllare al passaggio di ciascun dato e lo verifica a ogni richiesta. La rete usa $O(m\log^2 m)$ comparatori e ogni comparatore costa $O(\log m)$ porte. I test dei coefficienti canonici e il conteggio delle prime occorrenze rientrano negli stessi limiti.

La taglia compilata è quindi $N=O(m\log^3 m)$. Il limite monotono $2^{\Omega(\sqrt m/\log m)}$ di Cavalar, Kumar e Rossman dà
$$
2^{\Omega(\sqrt N/\log^{5/2}N)}
$$
per la restrizione dell'obiettivo così ottenuta. La monotonia riguarda gli ingressi liberi dell'istanza compilata. I bit costanti possono essere cablati senza inserire negazioni.

### Limite esponenziale per il polinomio dei sottoinsiemi

Per un ciclo e un obiettivo entrambi fissi, considero il polinomio
$$
G(z)=\sum_{S:\,\sum_{e\in S}w_e=T}\prod_{e\in S}z_e .
$$
Esistono famiglie con $N$ colonne in cui qualsiasi circuito aritmetico con somma, prodotto e costanti non negative che calcoli $G$ ha taglia $2^{\Omega(N)}$. Il limite riguarda il polinomio simbolico. La sua valutazione in un punto, come il conteggio in cui tutti gli $z_e$ valgono uno, è un problema distinto.

Costruisco prima un codice lineare binario di lunghezza $m$ con almeno $2^{m/2}$ parole, distanza relativa positiva e verificatore a taglia lineare. Per $m$ multiplo di sei, collego $m$ variabili con quattro porte ciascuna a $m/2$ vincoli di parità con otto porte ciascuno, usando una permutazione casuale delle porte. Una parola non nulla con peso $t$ può essere valida soltanto se le sue $4t$ porte incontrano al massimo $2t$ vincoli, poiché ogni vincolo toccato deve ricevere un numero pari di porte dalla parola. L'unione su tutti i supporti di taglia $t$ dà un limite
$$
\binom{m}{t}\binom{m/2}{2t}(4t/m)^{4t}
\ \le\ (16e^3t/m)^t .
$$
La somma per $1\le t\le\delta m$ tende a zero per una costante $\delta>0$ abbastanza piccola. Per vederlo si separano i termini a $t=\sqrt m$. Le parole valide formano un sottospazio di dimensione almeno $m/2$. I vincoli usano un numero costante di ingressi, quindi la verifica usa $O(m)$ porte. La costruzione di esistenza consente porte multiple fra una variabile e un vincolo.

Amplifico poi la distanza usando, per ciascuna di $m$ posizioni nuove, una tupla ordinata di $L$ indici scelti in modo indipendente e uniforme, con $L$ costante e $(1-\delta)^L\le2^{-9}$. La posizione nuova contiene la tupla dei corrispondenti bit della parola originaria, ossia un simbolo su un alfabeto costante di $2^L$ simboli. Due parole distinte coincidono in una posizione nuova con probabilità al massimo $2^{-9}$. La probabilità che coincidano in almeno $m/3$ posizioni è al più $2^m(2^{-9})^{m/3}=2^{-2m}$. Per la linearità del codice binario basta fare l'unione sulle meno di $2^m$ differenze non nulle. Esiste quindi una scelta fissa delle tuple per cui il codice amplificato $C$ ha almeno $2^{m/2}$ parole e due parole distinte coincidono in al massimo $m/3-1$ coordinate. La mappa delle tuple è iniettiva. L'esistenza delle due strutture è garantita con un argomento probabilistico, senza richiedere un algoritmo uniforme efficiente che le trovi.

Per ciascuna posizione nuova $j$ e ciascun simbolo $a$ creo una variabile che vale uno esattamente se la tupla in quella posizione è $a$. Il costo booleano totale è $O(m)$, dato che $L$ e la dimensione dell'alfabeto sono costanti. Compilo il verificatore e tutti questi valori ausiliari in Subset Sum, con le parole binarie come testimoni e nessun bit obiettivo libero. Nel polinomio $G$ sostituisco con $X_{j,a}$ la variabile $z_e$ dell'arco $q$ che legge quella bandierina, e con uno tutte le altre indeterminate. Ottengo esattamente
$$
P_C(X)=\sum_{c\in C}\prod_{j=1}^m X_{j,c_j}.
$$
La corrispondenza fra parole originarie, parole amplificate e sottoinsiemi impedisce coefficienti multipli. Per il [teorema 7 di Cavalar, Kumar e Rossman](https://pmc.ncbi.nlm.nih.gov/articles/PMC9705498/), la distanza del codice impone taglia almeno $|C|$ a ogni circuito aritmetico monotono per $P_C$. La sostituzione conserva il modello e $N=\Theta(m)$, dando il limite dichiarato per $G$.
