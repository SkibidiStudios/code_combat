# view.py
from colorama import Fore, Style, init

# Inizializza Colorama
init(autoreset=True)

class ConsoleView:
    """View del gioco: si occupa SOLO della presentazione (MVC: livello View).
    Nessuna logica, nessuna decisione: solo stampa ed estetica.
    """

   
    # TITOLI

    def show_welcome(self):
        banner = (
            f"{Fore.CYAN}{Style.BRIGHT}"
            + "=" * 50 + "\n"
            + "        🛡️  SIMULAZIONE COMBATTIMENTO  ⚔️\n"
            + "=" * 50 + f"{Style.RESET_ALL}"
        )
        print(banner + "\n")

   
    #  ERRORI DI VALIDAZIONE
   
    def show_validation_error(self, component, message):
        print(
            f"{Fore.MAGENTA}{Style.BRIGHT}❌ Errore in '{component}': "
            f"{Fore.WHITE}{message}\n"
        )

   
    #  ARMA DI DEFAULT
   
    def show_default_weapon(self, player_name, default_weapon_name):
        print(
            f"{Fore.YELLOW}⚠️ "
            f"{Fore.GREEN}{Style.BRIGHT}{player_name}"
            f"{Fore.WHITE} usa l’arma di default: "
            f"{Fore.CYAN}{default_weapon_name}{Fore.RESET}\n"
        )

    def show_weapon_equip(self, player_name, weapon):
        print(
            f"🗡️  {Fore.GREEN}{Style.BRIGHT}{player_name}{Fore.WHITE} equipaggia: "
            f"{Fore.CYAN}{weapon}{Fore.RESET}"
        )

   
    #  STATISTICHE INIZIALI
   

    def _format_player_box(self, name, hp, max_hp, strength, dexterity, weapon_name):
        """Crea una box ASCII colorata per un singolo giocatore."""
        lines = [
            f"| Nome : {name}",
            f"| HP   : {hp} / {max_hp}",
            f"| STR  : {strength}",
            f"| DEX  : {dexterity}",
            f"| Arma : {weapon_name}",
        ]
        width = max(len(line) for line in lines)
        top = "+" + "-" * (width - 1) + "+"
        bottom = top

        box = (
            f"{Fore.GREEN}{Style.BRIGHT}{top}\n"
            + "\n".join(
                f"{Fore.GREEN}{Style.BRIGHT}{line.ljust(width)}{Fore.GREEN}{Style.BRIGHT}|"
                for line in lines
            )
            + f"\n{bottom}{Style.RESET_ALL}"
        )
        return box

    def show_initial_stats(self, player1: dict, player2: dict):
        print(f"{Fore.CYAN}{Style.BRIGHT}📊 STATISTICHE INIZIALI\n")
        for player_name, attributes in {"Player 1": player1, "Player 2": player2}.items():
            print(f"{Fore.YELLOW}{Style.BRIGHT}{player_name}{Style.RESET_ALL}")
            lines = [f"| {key.capitalize()} : {value}" for key, value in attributes.items()]
            width = max(len(line) for line in lines)
            top = "+" + "-" * (width - 1) + "+"
            bottom = top

            box = (
                f"{Fore.GREEN}{Style.BRIGHT}{top}\n"
                + "\n".join(
                    f"{Fore.GREEN}{Style.BRIGHT}{line.ljust(width)}{Fore.GREEN}{Style.BRIGHT}|"
                    for line in lines
                )
                + f"\n{bottom}{Style.RESET_ALL}"
            )
            print(box)
            print()
   
    #  TURNO
   

    def show_turn_header(self, turn_number: int):
        print(
            f"{Fore.CYAN}{Style.BRIGHT}"
            + "-" * 40
            + f"\n           🔄  TURNO {turn_number}\n"
            + "-" * 40
            + f"{Style.RESET_ALL}\n"
        )

   
    #  POZIONI
   
    def show_potion_decision(self, player_name, potion_name):
        print(
            f"🧪  {Fore.GREEN}{Style.BRIGHT}{player_name}{Fore.WHITE} decide di usare "
            f"{Fore.CYAN}“{potion_name}”{Fore.RESET}\n"
        )

    def show_action_failure(self, player_name, action_name, reason):
        print(
            f"{Fore.MAGENTA}{Style.BRIGHT}❌ Azione {action_name} fallita per "
            f"{Fore.GREEN}{player_name}{Fore.MAGENTA}: "
            f"{Fore.WHITE}{reason}\n"
        )

    def show_potion_success(self, player_name, effect_desc, current_hp_msg):
        print(
            f"✨ {Fore.GREEN}{Style.BRIGHT}{player_name}{Fore.WHITE} usa una pozione: "
            f"{Fore.YELLOW}{effect_desc}{Fore.WHITE} "
            f"-> {Fore.GREEN}{current_hp_msg}{Fore.RESET}\n"
        )

   
    #  ATTACCHI
   
    def show_attack_result(self, attacker_name, defender_name, damage,stat, eff_stat):
        print(
            f"{Fore.GREEN}{attacker_name}{Fore.WHITE} attacca "
            f"{Fore.GREEN}{defender_name}{Fore.WHITE}"
            f" ({stat} eff={eff_stat})\n"
            f"{Fore.RED}{Style.BRIGHT}🔥 Danni inflitti: {damage}{Fore.RESET}\n"
        )

   
    #  VINCITORE
   
    def show_winner(self, winner_name):
        print(
            f"{Fore.YELLOW}{Style.BRIGHT}"
            + "=" * 50 + "\n"
            + f"        🏆  VINCITORE: {winner_name}  🏆\n"
            + "=" * 50
            + f"{Style.RESET_ALL}\n"
        )

   
    #  INPUT

    def get_user_input(self, prompt: str):
        return input(f"{Fore.WHITE}{prompt}{Style.RESET_ALL}")