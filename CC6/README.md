# 🛡️ RPG Combat System — MVC Architecture (Python)

Questo progetto implementa un sistema di combattimento RPG in Python seguendo un approccio **MVC (Model–View–Controller)** ispirato alla guida di Marco Farina:

🔗 https://marcofarina.notion.site/Parte-5-implementare-l-MVC-2afaa73c260f80b084dac4ec169fc886

L’obiettivo è strutturare il codice in modo pulito, modulare e facilmente estendibile, separando chiaramente:

- **Model** → logica di gioco (Player, Weapon, Potion)
- **View** → visualizzazione dell’azione (HUD, log, messaggi)
- **Controller** → gestione del flusso del combattimento e input dell’utente

---

## 🎮 Funzionalità Principali

### ✔️ Sistema completo di combattimento
- Attacchi basati su **danni variabili dell’arma**
- Modificatori basati su **Forza** o **Destrezza**
- Gestione della vita e morte del personaggio
- Armi corpo a corpo (“melee”) e a distanza (“ranged”)

### ✔️ Sistema di pozioni con effetti
- Pozioni di cura (`heal`)
- Buff di forza (`buff_str`)
- Buff di destrezza (`buff_dex`)
- Applicazione degli effetti con durata e stack controllato

### ✔️ Inventario basilare
- Fino a **3 pozioni** trasportabili
- Equipaggiamento di 1 arma alla volta
- Gestione sicura tramite proprietà e validazione

### ✔️ Gestione eccezioni robusta
Tutte le classi implementano controlli rigorosi su:
- tipi non validi (`TypeError`)
- valori fuori range (`ValueError`)
- oggetti non utilizzabili
- settaggi non ammessi

Questo impedisce bug silenziosi e fornisce feedback immediato durante lo sviluppo.

---

# 🧩 Architettura del Progetto — MVC

Il codice è organizzato secondo il pattern **Model–View–Controller** come suggerito nella guida Notion.

---

## 🟦 MODEL — Logica di Gioco

### `Player`
- Nome, salute, statistiche
- Arma equipaggiata
- Pozioni e buff attivi
- Metodo `attack()` con calcolo danni
- Metodo `should_use_potion()` per IA basilare
- Serializzazione stato (`get_state_dict()`)

### `Weapon`
- Tipo arma (`melee` / `ranged`)
- Range danni (`min_damage`, `max_damage`)
- `get_damage()` ritorna un valore random nel range

### `Potion`
- Effetti disponibili: heal, buff_str, buff_dex
- Durata effetti
- Applicazione al personaggio (`apply_to`)
- Controllo buff già presenti

---

## 🟩 VIEW — Interfaccia e Output
Mostra informazioni a schermo senza modificare lo stato.

---

## 🟥 CONTROLLER — Gestione del Combattimento
Coordina Model e View (turni, logica battaglia, condizioni vittoria).

---

# 🔧 Installazione

```bash
git clone https://github.com/tuo-username/tuo-repo.git
cd tuo-repo
python3 main.py
```

---

# 📁 Struttura consigliata

```
📦 rpg-mvc
 ├── models/
 │   ├── player.py
 │   ├── weapon.py
 │   └── potion.py
 ├── controller/
 │   └── game_controller.py
 ├── view/
 │   └── console_view.py
 ├── data/
 │   └── weapon.json
 ├── main.py
 └── README.md
```

---

# 🙋‍♂️ Autore

**Daniele Porcaro**
