import csv
import os
import random
import sys
from datetime import datetime

MAX_LEVEL = 100
ENDLESS_START = 101
SAVE_FILE = os.path.join(os.path.dirname(__file__), "spielerstand.csv")
ENDLESS_SAVE_FILE = os.path.join(os.path.dirname(__file__), "endless_run.csv")
LOG_FILE = os.path.join(os.path.dirname(__file__), "kampf_log.csv")
BOSS_LEVELS = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100}
CHECKPOINTS = {25, 50, 75}
BOSS_SPECIALS = {
    "boss": ["Knochensturm", "Dunkelkreis", "Blutiger Schrei"],
    "final": ["Sonnenfinsternis", "Nachtklinge", "Kaiserurteil"],
    "elite": ["Wolkenbruch", "Schattenzahn", "Kreuzflamme", "Todesschweif"],
    "legend": ["Abyssal Nova", "Ruf des Kaisers", "Sternenverderber", "Kaiserwunde"]
}
LEGENDARY_DECKS = [
    {"name": "Deck des Lichts", "buff": "crit", "value": 10, "desc": "Mehr kritische Treffer und purer Glanz."},
    {"name": "Deck der Flammen", "buff": "damage", "value": 12, "desc": "Mehr Schaden und brennende Wut."},
    {"name": "Deck der Stille", "buff": "hp", "value": 18, "desc": "Mehr Lebenspunkte und Ruhe im Sturm."},
    {"name": "Deck des Schattens", "buff": "evasion", "value": 8, "desc": "Mehr Überleben und subtile Gegenangriffe."},
    {"name": "Deck der Astralflut", "buff": "crit", "value": 14, "desc": "Astrale Treffer verzehnfachen den Druck."},
    {"name": "Deck des Krieges", "buff": "damage", "value": 16, "desc": "Die Wut des Schlachtfelds steigt ins Unendliche."},
    {"name": "Deck der Ewigkeit", "buff": "hp", "value": 24, "desc": "Das Reich der Nacht hält dich länger am Leben."}
]
BOSS_PATTERNS = [
    "Sonnenbeben", "Flammensog", "Mondschnitt", "Abyssale Rüstung", "Ewiges Blut",
    "Riss des Himmels", "Göttlicher Zorn", "Nachtwelle", "Kaisersturm", "Stille des Grabes"
]
ELITE_BOSSES = [
    "Der verfluchte Schlächter", "Mara, die Sternenjägerin", "Gorr, der Mondfresser",
    "Die Ascheprinzessin", "Auralon der Sternenbruch", "Der Flammenkönig", "Nox, Herr der Kälte"
]

STORY_TEXT = [
    "Seit Jahren liegt ein Fluch auf dem Reich von Aember. Die Sonne ist blass, die Straßen sind leer, und Geister wandern durch die Städte.",
    "Nur noch ein mutiger Held kann die Dunkelheit brechen. Der Legende nach ruht der Fluch im Inneren des hohen Turms, wo ein alter König angeblich die Nacht gebändigt hat.",
    "Du wirst durch Ruinen, Wälder, Felsspalten und Katakomben ziehen. Jeder Sieg macht dich stärker, jeder Kampf bringt dich dem Licht näher.",
    "Am Ende wartet der Nachtkaiser. Nur wer alle 100 Stufen übersteht, darf den Fluch endgültig brechen und das Reich retten."
]

CLASS_DATA = {
    "krieger": {"hp": 42, "attack": 13, "skill": "Eisenwall", "skills": ["Schildstoss", "Klingenchor", "Eiserner Schlag", "Götterwall", "Titanensturz"], "desc": "Ein robustes Schildkämpfer-Format mit viel Lebensenergie."},
    "bogenschütze": {"hp": 31, "attack": 16, "skill": "Sternenpfeil", "skills": ["Doppelbogen", "Himmelsraub", "Mondschneide", "Sturmsehne", "Phantompfeil"], "desc": "Schnell, präzise und stark im Fernkampf."},
    "magier": {"hp": 29, "attack": 19, "skill": "Flammensturm", "skills": ["Arkaner Schock", "Meteorfall", "Nova des Lichts", "Sonnenruß", "Aethernova"], "desc": "Verheerende Magie mit hohem Zerstörungspotenzial."},
    "dieb": {"hp": 33, "attack": 15, "skill": "Schattenstich", "skills": ["Nachtblitz", "Schädling", "Dornensprung", "Todesschritt", "Viperfang"], "desc": "Schnell, verletzlich, aber extrem effizient im Nahkampf."},
    "paladin": {"hp": 46, "attack": 15, "skill": "Lichtschild", "skills": ["Sonnenhammer", "Reiner Schwur", "Heiliger Stoß", "Aurora Schild", "Adlerwache"], "desc": "Ein schützender Krieger mit heiligem Zorn."},
    "hexer": {"hp": 30, "attack": 21, "skill": "Nachtfluch", "skills": ["Düsterklinge", "Seelenriss", "Schwarzer Sigil", "Mordendes Echo", "Schattengebet"], "desc": "Verursacht verheerenden Fluchschaden mit hoher Varianz."},
    "waldläufer": {"hp": 35, "attack": 17, "skill": "Wildfang", "skills": ["Waldschlag", "Blitzpfad", "Dornenfährte", "Rasender Äste", "Dschungelsturm"], "desc": "Scharf, schnell und stark bei langen Kämpfen."},
    "mönch": {"hp": 38, "attack": 14, "skill": "Innere Ruhe", "skills": ["Atem des Himmels", "Leerefäuste", "Sonnenkorde", "Stiller Kreis", "Mondschlag"], "desc": "Zäh, mystisch und durchdringend im Ausgleich."},
    "berserker": {"hp": 50, "attack": 20, "skill": "Blutrausch", "skills": ["Wutklinge", "Rasender Hieb", "Sturmbringer", "Knochenbrecher", "Kalkul des Blutes"], "desc": "Vollkommen auf Zerstörung und rohe Aggression ausgerichtet."},
    "wächter": {"hp": 44, "attack": 12, "skill": "Eisenbastion", "skills": ["Kettenwall", "Bergfest", "Schildstrom", "Turm der Treue", "Bastionfall"], "desc": "Ein defensiver Titan, der enorme Lasten auffängt."},
    "schamane": {"hp": 36, "attack": 18, "skill": "Donnersturm", "skills": ["Wurzelpakt", "Lavaflöte", "Erdbebenruf", "Sturmgeister", "Sonnentotem"], "desc": "Naturkräfte und Totemzauber in perfekter Symbiose."},
    "orakel": {"hp": 30, "attack": 22, "skill": "Prophezeiung", "skills": ["Sternenspruch", "Verlorene Vision", "Kronenschein", "Nachtspiegel", "Zeitbruch"], "desc": "Wahrsagung, Kontrolle und zerstörerische Präzision in einem."}
}

NORMAL_ENEMIES = {
    "Goblin": ["Stumpfe Axt", "Goblinohrring", "Leuchtkiesel"],
    "Skelett": ["Knochenbogen", "Skelettkiefer", "Knochensplitter"],
    "Schrat": ["Wurzelstab", "Düsterblatt", "Moosklinge"],
    "Wölfin": ["Wolfsfell", "Wolfszahn", "Wolfsklaue"],
    "Kobold": ["Spitzdolch", "Koboldstein", "Schlüssel der Mine"],
    "Räuber": ["Räuberknife", "Diebesmantel", "Lichtkette"],
    "Basilisk": ["Basiliskzahn", "Giftauge", "Lauernder Panzer"],
    "Waldgeist": ["Geisterfeder", "Mondsammet", "Umhang der Nacht"],
    "Blutkröte": ["Schwarze Haut", "Giftkapsel", "Leichenmoos"],
    "Dunkelritter": ["Dunkellanze", "Ritterhelm", "Nachtpanzer"],
    "Schwarzer Bär": ["Bärenfell", "Krallenbruch", "Felsknochen"],
    "Riesenratte": ["Zahnrad", "Schmutzklauen", "Stocklicht"],
    "Moorwisp": ["Sumpflicht", "Totenblüte", "Nebelkristall"],
    "Eisgolem": ["Frostplatte", "Blauer Kern", "Schneehorn"],
    "Würgekraut": ["Rauschblatt", "Giftstab", "Wurzelherz"],
    "Nachtjäger": ["Klingenfeder", "Stillemaske", "Monddolch"]
}

BOSS_NAMES = [
    "Der Knochendrache", "Mordwulf", "Der Totengräber", "Vespera, die Nachtwölfin",
    "Ragnar der Eisenfürst", "Abyssus, der Blutmagier", "Der Dornenfürst", "Morkel, der Rasenwolf",
    "Die Flammendiabolin", "Der Schattenlord", "Der Nachtkaiser"
]

SHOP_ITEMS = [
    {"name": "Kurzschwert", "kind": "weapon", "power": 6, "price": 30},
    {"name": "Knochenbogen", "kind": "weapon", "power": 9, "price": 50},
    {"name": "Flammenstab", "kind": "weapon", "power": 11, "price": 85},
    {"name": "Drachenschuppenbogen", "kind": "weapon", "power": 16, "price": 120},
    {"name": "Wolfsfellrüstung", "kind": "armor", "power": 8, "price": 55},
    {"name": "Eisenplatte", "kind": "armor", "power": 12, "price": 90},
    {"name": "Nachtpanzer", "kind": "armor", "power": 18, "price": 140},
    {"name": "Heiltrank", "kind": "potion", "power": 0, "price": 20},
    {"name": "Sonnenhieb", "kind": "skill", "power": 12, "price": 80},
    {"name": "Schattenstreich", "kind": "skill", "power": 14, "price": 100},
    {"name": "Katakombenfluch", "kind": "skill", "power": 18, "price": 140},
    {"name": "Nachtklinge", "kind": "boss_weapon", "power": 22, "price": 220},
    {"name": "Sonnenkronleuchter", "kind": "boss_armor", "power": 20, "price": 210},
    {"name": "Roter Elixier", "kind": "potion", "power": 25, "price": 35},
    {"name": "Ewiger Seelensplitter", "kind": "relic", "power": 10, "price": 90},
    {"name": "Schwert der Winde", "kind": "weapon", "power": 18, "price": 150},
    {"name": "Himmelswächter", "kind": "armor", "power": 22, "price": 170},
    {"name": "Ruf des Drachen", "kind": "skill", "power": 24, "price": 180}
]

RANDOM_SHOP_POOL = [
    "Kurzschwert", "Knochenbogen", "Flammenstab", "Drachenschuppenbogen", "Wolfsfellrüstung",
    "Eisenplatte", "Nachtpanzer", "Heiltrank", "Roter Elixier", "Sonnenhieb", "Schattenstreich",
    "Katakombenfluch", "Nachtklinge", "Sonnenkronleuchter", "Ruf des Drachen", "Schwert der Winde",
    "Himmelswächter", "Ewiger Seelensplitter"
]


class Player:
    def __init__(self, name, class_name="krieger", level=1, gold=60, hp=None, heal_potions=3):
        self.name = name
        self.class_name = class_name
        self.level = level
        self.gold = gold
        self.heal_potions = heal_potions
        self.weapon = "Kurzschwert"
        self.armor = "Lederrüstung"
        self.skills = [CLASS_DATA[class_name]["skill"]] + CLASS_DATA[class_name].get("skills", [])
        self.active_skill = self.skills[0]
        self.inventory = []
        self.effects = {}
        self.meta_upgrades = {"hp": 0, "attack": 0, "crit": 0}
        self.legendary_deck = None
        self.endless_run = False
        self.run_stats = {
            "bosses_killed": 0,
            "enemies_killed": 0,
            "gold_earned": 0,
            "damage_dealt": 0,
            "damage_taken": 0,
            "max_level": 1,
            "healing_used": 0,
            "relics": 0,
        }
        self.max_hp = CLASS_DATA[class_name]["hp"] + (level - 1) * 4
        self.hp = hp if hp is not None else self.max_hp
        self.attack = CLASS_DATA[class_name]["attack"] + (level - 1) * 2
        self.armor_bonus = 0
        self.weapon_bonus = 0
        self.update_stats()

    def update_stats(self):
        self.max_hp = CLASS_DATA[self.class_name]["hp"] + (self.level - 1) * 4 + self.armor_bonus + sum(v for k, v in self.effects.items() if k in ["Vigor", "Aegis", "Stärke", "Wut"])
        self.attack = CLASS_DATA[self.class_name]["attack"] + (self.level - 1) * 2 + self.weapon_bonus + sum(v for k, v in self.effects.items() if k in ["Stärke", "Wut", "Blitz"])
        self.hp = min(self.max_hp, self.hp) if self.hp is not None else self.max_hp

    def add_effect(self, name, amount):
        self.effects[name] = self.effects.get(name, 0) + amount
        self.update_stats()
        print(f"Effekt gestapelt: {name} +{amount}.")

    def add_meta_upgrade(self, kind, amount=1):
        self.meta_upgrades[kind] = self.meta_upgrades.get(kind, 0) + amount
        if kind == "hp":
            self.max_hp += 12 * amount
            self.hp += 12 * amount
        elif kind == "attack":
            self.attack += 5 * amount
        elif kind == "crit":
            self.attack += 2 * amount
        print(f"Meta-Upgrade aktiviert: {kind} +{amount}")

    def add_gold(self, amount):
        self.gold += amount

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        self.run_stats["damage_taken"] += amount
        print(f"{self.name} erleidet {amount} Schaden und bleibt bei {self.hp}/{self.max_hp} HP.")
        return self.hp

    def heal(self):
        if self.heal_potions <= 0:
            print("Du hast keine Heiltränke mehr.")
            return False
        potion_rank = random.randint(1, 6)
        amount = 12 + self.level * 2 + random.randint(5, 22) + potion_rank * 3
        self.hp = min(self.max_hp, self.hp + amount)
        self.heal_potions -= 1
        self.run_stats["healing_used"] += 1
        print(f"{self.name} trinkt einen zufälligen Trank der Stufe {potion_rank} und heilt {amount} HP. {self.hp}/{self.max_hp}")
        if random.random() < 0.28:
            self.add_effect("Vigor", random.randint(1, 3))
        return True

    def basic_attack(self, enemy):
        crit = random.random() < (0.18 + self.meta_upgrades.get("crit", 0) * 0.03)
        damage = random.randint(5, 12) + self.attack + random.randint(1, 6)
        if crit:
            damage += 8 + self.meta_upgrades.get("crit", 0) * 2
            print(f"Kritischer Treffer! {self.name} trifft {enemy.name} für {damage} Schaden.")
        else:
            print(f"{self.name} trifft {enemy.name} für {damage} Schaden.")
        enemy.hp -= damage
        self.run_stats["damage_dealt"] += damage
        return damage

    def set_active_skill(self, skill_name):
        if skill_name in self.skills:
            self.active_skill = skill_name
            print(f"Aktive Fähigkeit gesetzt: {skill_name}")
        else:
            print("Diese Fähigkeit hast du nicht gelernt.")

    def special_attack(self, enemy):
        skill = self.active_skill
        if skill == "Eisenwall":
            damage = random.randint(8, 18) + self.attack + 6
            enemy.hp -= damage
            print(f"{self.name} nutzt {skill} und verursacht {damage} Schaden!")
            self.run_stats["damage_dealt"] += damage
            return damage
        if skill == "Sternenpfeil":
            damage = random.randint(10, 22) + self.attack + 8
            enemy.hp -= damage
            print(f"{self.name} feuert {skill} ab und verursacht {damage} Schaden!")
            self.run_stats["damage_dealt"] += damage
            return damage
        if skill == "Flammensturm":
            damage = random.randint(12, 26) + self.attack + 10
            enemy.hp -= damage
            print(f"{self.name} entfesselt {skill} und verursacht {damage} Schaden!")
            self.run_stats["damage_dealt"] += damage
            return damage
        if skill == "Schattenstich":
            damage = random.randint(9, 20) + self.attack + 7
            enemy.hp -= damage
            print(f"{self.name} setzt {skill} ein und verursacht {damage} Schaden!")
            self.run_stats["damage_dealt"] += damage
            return damage
        if skill in ["Schildstoss", "Doppelbogen", "Arkaner Schock", "Nachtblitz", "Sonnenhammer", "Düsterklinge", "Waldschlag", "Atem des Himmels", "Klingenchor", "Himmelsraub", "Meteorfall", "Schädling", "Reiner Schwur", "Seelenriss", "Blitzpfad", "Leerefäuste"]:
            damage = random.randint(12, 32) + self.attack + 14
            enemy.hp -= damage
            print(f"{self.name} nutzt {skill} und verursacht {damage} Schaden!")
            self.run_stats["damage_dealt"] += damage
            return damage
        if skill in ["Sonnenhieb", "Schattenstreich", "Katakombenfluch", "Eiserner Schlag", "Blutige Klinge", "Nachtklinge", "Lichtschild", "Nachtfluch", "Wildfang", "Innere Ruhe"]:
            damage = random.randint(10, 28) + self.attack + 12
            enemy.hp -= damage
            print(f"{self.name} nutzt {skill} und verursacht {damage} Schaden!")
            self.run_stats["damage_dealt"] += damage
            return damage

        damage = random.randint(8, 18) + self.attack
        enemy.hp -= damage
        print(f"{self.name} nutzt Spezialangriff und verursacht {damage} Schaden.")
        self.run_stats["damage_dealt"] += damage
        return damage

    def add_inventory_item(self, item_name):
        self.inventory.append(item_name)

    def add_skill(self, skill_name):
        if skill_name not in self.skills:
            self.skills.append(skill_name)
            print(f"Neue Fähigkeit gelernt: {skill_name}")
        else:
            print(f"{skill_name} ist bereits gelernt.")

    def save_endless_state(self):
        with open(ENDLESS_SAVE_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "class_name", "level", "gold", "hp", "max_hp", "heal_potions", "weapon", "armor", "skills", "inventory", "active_skill", "endless_run", "timestamp"])
            writer.writerow([
                self.name,
                self.class_name,
                self.level,
                self.gold,
                self.hp,
                self.max_hp,
                self.heal_potions,
                self.weapon,
                self.armor,
                ";".join(self.skills),
                ";".join(self.inventory),
                self.active_skill,
                str(bool(self.endless_run)).lower(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])

    def save_state(self):
        with open(SAVE_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["name", "class_name", "level", "gold", "hp", "max_hp", "heal_potions", "weapon", "armor", "skills", "inventory", "active_skill", "endless_run", "timestamp"])
            writer.writerow([
                self.name,
                self.class_name,
                self.level,
                self.gold,
                self.hp,
                self.max_hp,
                self.heal_potions,
                self.weapon,
                self.armor,
                ";".join(self.skills),
                ";".join(self.inventory),
                self.active_skill,
                str(bool(self.endless_run)).lower(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])
            if self.endless_run:
                self.save_endless_state()

    def show_status(self):
        print("\n=== STATUS ===")
        print(f"Held: {self.name} ({self.class_name})")
        print(f"Level: {self.level}/{MAX_LEVEL}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Attacke: {self.attack}")
        print(f"Gold: {self.gold}")
        print(f"Waffe: {self.weapon}")
        print(f"Rüstung: {self.armor}")
        print(f"Heiltränke: {self.heal_potions}")
        print(f"Aktive Fähigkeit: {self.active_skill}")
        print(f"Fähigkeiten: {', '.join(self.skills)}")
        if self.effects:
            print(f"Effekte: {', '.join(f'{k} +{v}' for k, v in self.effects.items())}")
        if self.meta_upgrades and any(v > 0 for v in self.meta_upgrades.values()):
            print(f"Meta-Upgrades: {self.meta_upgrades}")
        print("=============")

    def show_run_summary(self):
        score = self.run_stats["damage_dealt"] + self.run_stats["bosses_killed"] * 400 + self.run_stats["gold_earned"] * 2 + self.run_stats["relics"] * 150
        if self.endless_run or self.level >= MAX_LEVEL:
            title = "LEGENDÄRER LAUF"
            if score >= 9000:
                rank = "S+ - Nachtwächter des Endes"
            elif score >= 7000:
                rank = "S - Erbe der Finsternis"
            elif score >= 5000:
                rank = "A+ - Kronenbrecher"
            elif score >= 3500:
                rank = "A - Flammenstürmer"
            else:
                rank = "B - Überlebender"
        else:
            title = "ERFOLGREICHER LAUF"
            if score >= 6000:
                rank = "S"
            elif score >= 4000:
                rank = "A"
            elif score >= 2500:
                rank = "B"
            else:
                rank = "C"

        print("\n=== RUN-STATISTIK ===")
        print(f"Held: {self.name} ({self.class_name})")
        print(f"Laufstatus: {title} ({rank})")
        print(f"Max Level: {self.run_stats['max_level']}")
        print(f"Gegner besiegt: {self.run_stats['enemies_killed']}")
        print(f"Bosse besiegt: {self.run_stats['bosses_killed']}")
        print(f"Gold verdient: {self.run_stats['gold_earned']}")
        print(f"Schaden verursacht: {self.run_stats['damage_dealt']}")
        print(f"Schaden erlitten: {self.run_stats['damage_taken']}")
        print(f"Heilungen: {self.run_stats['healing_used']}")
        print(f"Relikte: {self.run_stats['relics']}")
        print(f"Deck: {self.legendary_deck or 'Keines'}")
        print(f"Meta-Upgrades: {self.meta_upgrades}")
        print(f"Gesamtwertung: {score}")
        print("====================")


class Enemy:
    def __init__(self, name, hp, attack, kind="normal", drop_table=None, pattern=None):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.kind = kind
        self.drop_table = drop_table or []
        self.pattern = pattern or (random.choice(BOSS_PATTERNS) if kind in ["boss", "elite", "final", "legend"] else "")

    def strike(self, player):
        damage = random.randint(2, self.attack)
        player.take_damage(damage)
        print(f"{self.name} schlägt zu und macht {damage} Schaden.")
        return damage

    def use_special_move(self, player):
        if self.kind not in ["boss", "final", "elite", "legend"]:
            if random.random() < 0.15:
                damage = random.randint(5, 12) + self.attack // 2
                player.take_damage(damage)
                print(f"{self.name} setzt einen wilden Angriff ein und macht {damage} Schaden!")
                return damage
            return 0

        abilities = BOSS_SPECIALS.get(self.kind, ["Dunkler Schlag"])
        move = random.choice(abilities)
        pattern_bonus = 0
        if self.pattern:
            pattern_bonus += {"Sonnenbeben": 8, "Flammensog": 10, "Mondschnitt": 9, "Abyssale Rüstung": 12, "Ewiges Blut": 15, "Riss des Himmels": 18, "Göttlicher Zorn": 20, "Nachtwelle": 14, "Kaisersturm": 22, "Stille des Grabes": 17}.get(self.pattern, 0)
        damage = random.randint(12, 30) + self.attack // 2 + pattern_bonus + (15 if self.kind == "legend" else 8 if self.kind == "elite" else 0)
        player.take_damage(damage)
        print(f"{self.name} nutzt {move} [{self.pattern}]! Der Schlag trifft für {damage} Schaden.")
        return damage


def log_event(message):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message])


def show_story():
    print("====================================")
    print("      AEMBER – DAS VERFLUCHTE REICH")
    print("====================================")
    for line in STORY_TEXT:
        print(line)
    print("\nDie Nacht ist nicht nur dunkel – sie ist lebendig.")
    print("Du bist der letzte, der die Regeln des Reiches brechen kann.")


def class_menu():
    print("\nWähle deine Klasse:")
    keys = list(CLASS_DATA.keys())
    for index, key in enumerate(keys, start=1):
        print(f"{index}) {key.title()} - {CLASS_DATA[key]['desc']}")
    while True:
        choice = safe_input("Deine Wahl: ", default="1")
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            return keys[int(choice) - 1]
        print(f"Bitte wähle eine Zahl zwischen 1 und {len(keys)}.")


def safe_input(prompt, default=""):
    try:
        value = input(prompt)
    except EOFError:
        print()
        return default
    return value.strip().lower() if value.strip() else default


def create_enemy(level):
    if level >= MAX_LEVEL and level % 10 == 0:
        return Enemy("Der Nachtkaiser", 320 + level * 5, 35 + level, kind="final", pattern=random.choice(BOSS_PATTERNS), drop_table=["Nachtklinge", "Sonnenkronleuchter", "Kaiserwappen"])

    if level > MAX_LEVEL:
        endless_tier = level - MAX_LEVEL
        if endless_tier % 8 == 0:
            boss_name = random.choice(ELITE_BOSSES)
            hp = 280 + endless_tier * 18 + random.randint(40, 180)
            attack = 36 + endless_tier + random.randint(12, 28)
            return Enemy(f"Legend: {boss_name}", hp, attack, kind="legend", pattern=random.choice(BOSS_PATTERNS), drop_table=["Aetherkristall", "Götterklinge", "Ewiger Wurzelring", "Sonnenmantel", "Kaiserwappen"])
        elite_name = random.choice(ELITE_BOSSES)
        hp = 220 + endless_tier * 12 + random.randint(20, 100)
        attack = 28 + endless_tier + random.randint(8, 18)
        return Enemy(f"Elite: {elite_name}", hp, attack, kind="elite", pattern=random.choice(BOSS_PATTERNS), drop_table=["Aetherkristall", "Götterklinge", "Ewiger Wurzelring"])

    if level % 10 == 0:
        boss_name = random.choice(BOSS_NAMES)
        hp = 180 + level * 9 + random.randint(15, 60)
        attack = 18 + level + random.randint(6, 16)
        return Enemy(f"Boss: {boss_name}", hp, attack, kind="boss", pattern=random.choice(BOSS_PATTERNS), drop_table=["Drachenschuppe", "Eisenkralle", "Mondsichel", "Nachtklinge"])

    enemy_name = random.choice(list(NORMAL_ENEMIES.keys()))
    hp = 24 + level * 4 + random.randint(6, 18)
    attack = 8 + level + random.randint(2, 7)
    return Enemy(enemy_name, hp, attack, kind="normal", pattern=None, drop_table=NORMAL_ENEMIES[enemy_name])


def is_valid_save_row(row):
    if row is None:
        return False
    required_fields = ["name", "class_name", "level", "gold", "hp", "heal_potions", "weapon", "armor", "skills", "active_skill"]
    if any(field not in row or row[field] in (None, "") for field in required_fields):
        return False
    if row.get("class_name") not in CLASS_DATA:
        return False
    try:
        int(row["level"])
        int(row["gold"])
        int(row["hp"])
        int(row["heal_potions"])
    except (TypeError, ValueError):
        return False
    return True


def build_player_from_row(row):
    player = Player(
        name=row["name"],
        class_name=row["class_name"],
        level=int(row["level"]),
        gold=int(row["gold"]),
        hp=int(row["hp"]),
        heal_potions=int(row["heal_potions"]),
    )
    player.weapon = row["weapon"] or "Kurzschwert"
    player.armor = row["armor"] or "Lederrüstung"
    valid_skills = [CLASS_DATA[player.class_name]["skill"]] + CLASS_DATA[player.class_name].get("skills", [])
    saved_skills = row["skills"].split(";") if row["skills"] else []
    player.skills = []
    for skill in saved_skills:
        if skill in valid_skills and skill not in player.skills:
            player.skills.append(skill)
    if not player.skills:
        player.skills = valid_skills[:]
    player.active_skill = row.get("active_skill", player.skills[0])
    if player.active_skill not in player.skills:
        player.active_skill = player.skills[0]
    player.inventory = row["inventory"].split(";") if row["inventory"] else []
    player.endless_run = str(row.get("endless_run", "false")).lower() in {"1", "true", "yes"}
    player.update_stats()
    return player


def clear_endless_state():
    if os.path.exists(ENDLESS_SAVE_FILE):
        try:
            os.remove(ENDLESS_SAVE_FILE)
        except OSError:
            pass


def load_saved_game():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            row = next(reader, None)
            if row is None or not is_valid_save_row(row):
                return None
            player = build_player_from_row(row)
            if player.hp <= 0:
                return None
            print(f"Gespeicherter Stand gefunden: {player.name}, Level {player.level}")
            return player
    except Exception:
        return None


def load_endless_state():
    if not os.path.exists(ENDLESS_SAVE_FILE):
        return None
    try:
        with open(ENDLESS_SAVE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            row = next(reader, None)
            if row is None or not is_valid_save_row(row):
                clear_endless_state()
                return None
            player = build_player_from_row(row)
            player.endless_run = True
            if player.hp <= 0:
                clear_endless_state()
                return None
            print(f"Aktiver Endless-Lauf gefunden: {player.name}, Level {player.level}")
            return player
    except Exception:
        clear_endless_state()
        return None


def has_active_endless_run():
    return load_endless_state() is not None


def try_activate_endless_run(player):
    if player.endless_run:
        return True
    if has_active_endless_run():
        print("Das Portal der Ewigkeit öffnet sich nur einmal. Es ist noch ein aktiver Endless-Player im Reich. Das Portal öffnet erst wieder, wenn der Endless-Helden gefallen ist.")
        return False
    player.endless_run = True
    player.level = ENDLESS_START
    player.max_hp += 40
    player.hp = player.max_hp
    player.attack += 12
    player.save_endless_state()
    print("\n=== UNENDLICHER RUN AKTIVIERT ===")
    print("Der Fluch kehrt zurück – und mit ihm beginnt der ewige Zyklus der Prüfung.")
    print("Du stehst jetzt im Endless-Mode: immer stärkerer Mut, immer härtere Gegner, immer mehr Relikte.")
    return True


def reward_player(player, enemy):
    gold_gain = 12 + player.level * 3 + random.randint(5, 15)
    player.gold += gold_gain
    player.run_stats["gold_earned"] += gold_gain
    print(f"{enemy.name} wurde besiegt! Gold gewonnen: {gold_gain}")

    if enemy.kind in ["boss", "final", "elite", "legend"]:
        print("Bosskampf gewonnen! Du bekommst die Wahl zwischen Shop, Fähigkeiten und weiterem Fortschritt.")
        bonus_gold = 60 if enemy.kind == "boss" else 90 if enemy.kind == "elite" else 120 if enemy.kind == "legend" else 160
        player.gold += bonus_gold
        player.run_stats["gold_earned"] += bonus_gold
        print(f"Zusätzliche Bossbelohnung: {bonus_gold} Gold.")
        player.level += 1
        player.run_stats["max_level"] = max(player.run_stats["max_level"], player.level)
        player.max_hp += 8
        player.hp = min(player.max_hp, player.hp + 12)
        player.attack += 4
        if enemy.kind == "final":
            if random.random() < 0.8:
                rare_item = random.choice(enemy.drop_table)
                player.add_inventory_item(rare_item)
                player.run_stats["relics"] += 1
                print(f"Legendärer Gegenstand gefunden: {rare_item}")
        if enemy.kind in ["elite", "legend"]:
            relic_name = random.choice(["Aetherkristall", "Götterklinge", "Ewiger Wurzelring", "Sonnenmantel"])
            player.add_effect("Wut", random.randint(2, 5))
            player.add_inventory_item(relic_name)
            player.run_stats["relics"] += 1
            print(f"Elite-Relikt gewonnen: {relic_name}")
        if player.level >= MAX_LEVEL and not player.endless_run:
            if not try_activate_endless_run(player):
                print("Der Portal-Block bleibt aktiv. Du kannst erst wieder einen neuen Endless-Lauf starten, wenn der aktuelle Endless-Helden tot ist.")
                return True
        return True

    player.level += 1
    player.run_stats["max_level"] = max(player.run_stats["max_level"], player.level)
    player.max_hp += 3
    player.hp = min(player.max_hp, player.hp + 5)
    player.attack += 2

    drop = random.choice(enemy.drop_table) if enemy.drop_table else ""
    if drop and random.random() < 0.7:
        player.add_inventory_item(drop)
        print(f"Du hast einen Gegenstand gefunden: {drop}")

    return False


def buy_item(player, item_name):
    data = next((item for item in SHOP_ITEMS if item["name"].lower() == item_name.lower()), None)
    if data is None:
        print("Dieses Item gibt es im Shop nicht.")
        return False

    if player.gold < data["price"]:
        print("Du hast nicht genug Gold.")
        return False

    player.gold -= data["price"]
    if data["kind"] == "weapon":
        player.weapon = data["name"]
        player.weapon_bonus = data["power"]
    elif data["kind"] == "armor":
        player.armor = data["name"]
        player.armor_bonus = data["power"]
    elif data["kind"] == "potion":
        player.heal_potions += 1
        if random.random() < 0.35:
            player.add_effect("Vigor", random.randint(1, 3))
        print("Heiltrank hinzugefügt.")
    elif data["kind"] == "skill":
        player.add_skill(data["name"])
        player.active_skill = data["name"]
        player.skills = list(dict.fromkeys(player.skills))
    elif data["kind"] == "boss_weapon":
        player.weapon = data["name"]
        player.weapon_bonus = max(player.weapon_bonus, data["power"])
        player.add_effect("Stärke", 3)
    elif data["kind"] == "boss_armor":
        player.armor = data["name"]
        player.armor_bonus = max(player.armor_bonus, data["power"])
        player.add_effect("Aegis", 4)
    elif data["kind"] == "relic":
        player.add_effect("Blitz", random.randint(2, 5))
        player.add_effect("Wut", random.randint(1, 3))
    else:
        player.add_inventory_item(data["name"])
    player.update_stats()
    print(f"{data['name']} gekauft!")
    return True


def generate_random_shop():
    offers = random.sample(RANDOM_SHOP_POOL, 6)
    return [next(item for item in SHOP_ITEMS if item["name"] == name) for name in offers]


def shop_menu(player):
    inventory = generate_random_shop()
    while True:
        print("\n=== RANDOM SHOP ===")
        for index, item in enumerate(inventory, start=1):
            print(f"{index}) {item['name']} - {item['price']} Gold - {item['kind']}")
        print("0) Zurück")
        choice = safe_input("Deine Wahl: ", default="0")
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(inventory):
            item = inventory[int(choice) - 1]
            buy_item(player, item["name"])
        else:
            print("Ungültige Auswahl.")


def learn_skill_menu(player):
    skill_options = [
        "Sonnenhieb", "Schattenstreich", "Katakombenfluch", "Eiserner Schlag",
        "Blutige Klinge", "Nachtklinge"
    ]
    print("\n=== FÄHIGKEITSBUCH ===")
    for index, skill in enumerate(skill_options, start=1):
        print(f"{index}) {skill} - 70 Gold")
    print("0) Zurück")
    choice = safe_input("Wähle eine Fähigkeit: ", default="0")
    if choice == "0":
        return
    if choice.isdigit() and 1 <= int(choice) <= len(skill_options):
        skill = skill_options[int(choice) - 1]
        if player.gold < 70:
            print("Du hast nicht genug Gold.")
            return
        player.gold -= 70
        player.add_skill(skill)
        player.active_skill = skill
        print(f"Fähigkeit erlernt: {skill}")
    else:
        print("Ungültige Auswahl.")


def choose_active_skill(player):
    if len(player.skills) <= 1:
        print("Du hast noch keine weitere Fähigkeit gewählt.")
        return
    print("\n=== AKTIVE FÄHIGKEIT WÄHLEN ===")
    for index, skill in enumerate(player.skills, start=1):
        print(f"{index}) {skill}")
    choice = safe_input("Deine Wahl: ", default="1")
    if choice.isdigit() and 1 <= int(choice) <= len(player.skills):
        player.set_active_skill(player.skills[int(choice) - 1])
    else:
        print("Ungültige Auswahl.")


def meta_upgrade_menu(player):
    options = [
        ("Herzstärke", lambda: player.add_meta_upgrade("hp", 1)),
        ("Waffenkern", lambda: player.add_meta_upgrade("attack", 1)),
        ("Mondkrit", lambda: player.add_meta_upgrade("crit", 1)),
    ]
    print("\n=== META-UPGRADE ===")
    for index, (name, _) in enumerate(options, start=1):
        print(f"{index}) {name}")
    choice = safe_input("Deine Wahl: ", default="1")
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        options[int(choice) - 1][1]()
    else:
        print("Ungültige Auswahl.")


def choose_legendary_deck(player):
    print("\n=== LEGENDÄRES BOSS-DECK ===")
    for index, deck in enumerate(LEGENDARY_DECKS, start=1):
        print(f"{index}) {deck['name']} - {deck['desc']}")
    choice = safe_input("Dein Deck: ", default="1")
    if choice.isdigit() and 1 <= int(choice) <= len(LEGENDARY_DECKS):
        deck = LEGENDARY_DECKS[int(choice) - 1]
        player.legendary_deck = deck["name"]
        if deck["buff"] == "crit":
            player.add_meta_upgrade("crit", 2)
        elif deck["buff"] == "damage":
            player.add_meta_upgrade("attack", 2)
        elif deck["buff"] == "hp":
            player.add_meta_upgrade("hp", 2)
        else:
            player.add_effect("Aegis", deck["value"])
        print(f"Deck gewählt: {deck['name']} - {deck['desc']}")
    else:
        print("Unbekanntes Deck. Standard gewählt.")


def post_boss_menu(player):
    while True:
        print("\n=== BOSS-OPTIONEN ===")
        print("1) Shop")
        print("2) Fähigkeit lernen")
        print("3) Aktive Fähigkeit wählen")
        print("4) Meta-Upgrade")
        if player.endless_run:
            print("5) Legendäres Deck wählen")
            print("6) Weiter")
        else:
            print("5) Weiter")
        choice = safe_input("Deine Wahl: ", default="6" if player.endless_run else "5")
        if choice == "1":
            shop_menu(player)
        elif choice == "2":
            learn_skill_menu(player)
        elif choice == "3":
            choose_active_skill(player)
        elif choice == "4":
            meta_upgrade_menu(player)
        elif player.endless_run and choice == "5":
            choose_legendary_deck(player)
        elif (not player.endless_run and choice == "5") or (player.endless_run and choice == "6"):
            return
        else:
            print("Bitte gültige Auswahl wählen.")


def fight(player):
    enemy = create_enemy(player.level)
    if player.level in BOSS_LEVELS or player.level == MAX_LEVEL:
        print(f"\n=== BOSS-KAMPF ===")
        print(f"{enemy.name} erscheint! HP: {enemy.hp}, Angriff: {enemy.attack}")
    elif player.level > MAX_LEVEL:
        print(f"\n=== ELITE-ENDELOST ===")
        print(f"{enemy.name} erscheint! HP: {enemy.hp}, Angriff: {enemy.attack}")
    else:
        print(f"\nEin {enemy.name} erscheint! HP: {enemy.hp}, Angriff: {enemy.attack}")

    while player.hp > 0 and enemy.hp > 0:
        print("\n1) Angriff")
        print("2) Spezialangriff")
        print("3) Heiltrank")
        print("4) Speichern & Beenden")
        print("5) Fliehen")
        choice = safe_input("Deine Wahl: ", default="1")

        if choice in ["1", "angriff", "a"]:
            player.basic_attack(enemy)
        elif choice in ["2", "spezial", "special"]:
            player.special_attack(enemy)
        elif choice in ["3", "heil", "trank"]:
            player.heal()
        elif choice in ["4", "save", "speichern"]:
            player.save_state()
            print("Spiel gespeichert und beendet.")
            raise SystemExit
        elif choice in ["5", "fliehen", "run"]:
            if random.random() < 0.4:
                print("Du bist erfolgreich geflohen.")
                return False
            print("Flucht misslungen!")
        else:
            print("Unbekannte Auswahl. Bitte erneut wählen.")
            continue

        if enemy.hp <= 0:
            print(f"{enemy.name} wurde besiegt!")
            player.run_stats["max_level"] = max(player.run_stats["max_level"], player.level)
            if enemy.kind in ["normal", "boss", "final", "elite", "legend"]:
                player.run_stats["enemies_killed"] += 1
            if enemy.kind in ["boss", "final", "elite", "legend"]:
                player.run_stats["bosses_killed"] += 1
            boss_victory = reward_player(player, enemy)
            log_event(f"{player.name} gewinnt gegen {enemy.name} auf Level {player.level}")
            if boss_victory and enemy.kind in ["boss", "final", "elite", "legend"]:
                post_boss_menu(player)
            return True

        if enemy.kind in ["boss", "final", "elite", "legend"] and random.random() < 0.55:
            enemy.use_special_move(player)
        else:
            enemy.strike(player)
        log_event(f"{enemy.name} greift {player.name} an")

        if player.hp <= 0:
            print(f"{player.name} wurde besiegt! Game Over.")
            if player.endless_run:
                print("Das Portal der Ewigkeit schließt sich wieder. Ein neuer Endless-Run kann nun erneut geöffnet werden.")
                clear_endless_state()
            player.save_state()
            return False

    return True


def start_game():
    endless_loaded = load_endless_state()

    show_story()
    print("\nDie Türen der Vergangenheit öffnen sich. Wähle mit Bedacht.")

    if endless_loaded is not None:
        print("Ein aktiver Endless-Lauf wurde gefunden.")
        print("1) Neues normales Spiel starten")
        print("2) Normales Spiel laden")
        print("3) Endless-Lauf fortsetzen")
        print("4) Beenden")
        mode = safe_input("Deine Wahl: ", default="1")

        if mode == "4":
            print("Bis bald.")
            raise SystemExit
        if mode == "2":
            loaded = load_saved_game()
            if loaded is not None:
                print("Gespeicherten Charakter geladen.")
                return loaded
            print("Kein normaler Speicherstand gefunden. Neues normales Spiel startet.")
        elif mode == "3":
            print("Endless-Lauf wird fortgesetzt.")
            return endless_loaded
        # mode == 1 falls through to a normal new run
    else:
        mode = safe_input("1) Neues Spiel\n2) Spiel laden\n3) Beenden\nDeine Wahl: ", default="1")

        if mode == "3":
            print("Bis bald.")
            raise SystemExit

        if mode == "2":
            loaded = load_saved_game()
            if loaded is not None:
                print("Gespeicherten Charakter geladen.")
                return loaded
            print("Kein Speicherstand gefunden. Neues Spiel startet.")

    class_name = class_menu()
    name = safe_input("Wie heißt dein Held? ", default="Aric")
    return Player(name, class_name)


def main():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["zeit", "ereignis"])

    player = start_game()
    player.show_status()

    while player.hp > 0:
        if player.level in BOSS_LEVELS:
            print(f"\n=== Boss-Level {player.level} ===")
            print("Die Luft wird still. Ein mächtiger Gegner erwartet dich.")
        if player.level > MAX_LEVEL:
            endless_tier = player.level - MAX_LEVEL
            print(f"\n=== Endless Run – Stufe {player.level} ===")
            print(f"Der Fluch hat sich verdoppelt. Stufe {endless_tier} der Nacht beginnt jetzt ernsthaft.")
            if endless_tier % 8 == 0:
                print("Eine legendarische Bedrohung nähert sich – die Grenze zwischen Boss und Mythos beginnt zu brechen.")
        if player.level in CHECKPOINTS:
            print(f"\nCheckpoint erreicht: Level {player.level}.")
            player.save_state()
            print("Dein Fortschritt wurde gesichert.")

        player.show_status()
        action = safe_input("Möchtest du kämpfen? (j/n): ", default="j")
        if action in ["n", "nein"]:
            print("Du ruhst dich aus und speicherst den Fortschritt.")
            player.save_state()
            break

        if action not in ["j", "ja", "y", "yes"]:
            print("Bitte mit j oder n antworten.")
            continue

        if not fight(player):
            print("Du hast das Reich nicht retten können. Versuch es erneut.")
            player.show_run_summary()
            break

        if player.level >= MAX_LEVEL and player.endless_run:
            print("\n=== ENDLESS SIEG ===")
            print("Du bist in den ewigen Zyklus eingetreten. Die Nacht nennt dich ihren Erben.")
            print("Der Fluch ist nicht besiegt – er wurde nur in dir zu einer Waffe.")
            player.show_run_summary()
            player.save_state()
            print("Fortsetzung des Endless-Runs möglich – das Reich wartet auf den nächsten Durchgang.")
            continue

        if player.level >= MAX_LEVEL and not player.endless_run:
            print("\n=== SIEG ===")
            print("Du hast den Nachtkaiser besiegt und das Reich von Aember vor dem Fluch gerettet.")
            print("Die Legende lebt weiter – und dein Name wird in Stein gehauen.")
            player.show_run_summary()
            player.save_state()
            break

    print("\nDanke für das Spielen.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        print("Spielende.")
    except KeyboardInterrupt:
        print("\nDas Spiel wurde abgebrochen.")
