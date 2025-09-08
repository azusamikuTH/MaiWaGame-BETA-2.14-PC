# -*- coding: utf-8 -*-
import os
import sys
import json
import random
import time
import textwrap

# --- นำเข้าข้อมูลจากไฟล์อื่น ---
from npc_dialogue import get_dialogue
from quest_data import get_quests

# --- ฟังก์ชันเสริม ---
def clear_screen():
    """ล้างหน้าจอ Terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter_print(text, delay=0.03):
    """พิมพ์ข้อความเหมือนเครื่องพิมพ์ดีด"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# --- คลาสข้อมูล ---
class Card:
    def __init__(self, name, card_type, value, desc):
        self.name = name
        self.type = card_type # ATTACK, DEFEND, SKILL, ITEM
        self.value = value
        self.desc = desc

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['type'], data['value'], data['desc'])

class Character:
    def __init__(self, name, max_hp, atk, defense, spd, luck):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk = atk
        self.defense = defense
        self.spd = spd
        self.luck = luck
        self.deck = []
        self.hand = []
        self.discard = []
        self.defense_bonus = 0

    def is_alive(self):
        return self.hp > 0

    def draw_hand(self, num_cards=4):
        self.discard.extend(self.hand)
        self.hand = []
        for _ in range(num_cards):
            if not self.deck:
                if not self.discard:
                    break 
                self.deck = self.discard
                self.discard = []
                random.shuffle(self.deck)
            if self.deck:
                self.hand.append(self.deck.pop())
    
    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense_bonus)
        self.hp = max(0, self.hp - actual_damage)
        self.defense_bonus = 0 # Reset defense bonus after taking a hit
        return actual_damage

class Player(Character):
    def __init__(self, name):
        super().__init__(name, 100, 10, 5, 7, 5)
        self.money = 50
        self.current_location = "หมู่บ้านฮาจิมัง"
        self.reputation = {} # {"เมือง A": 10, "เมือง B": 5}
        self.active_quests = {}
        self.completed_quests = []
        self.original_deck = []
    
    def build_deck(self, card_pool, size=10):
        # --- FIX: ป้องกันข้อผิดพลาด Sample larger than population ---
        # ตรวจสอบว่าจำนวนการ์ดที่ต้องการ (size) ไม่มากกว่าจำนวนการ์ดที่มีทั้งหมด (len(card_pool))
        safe_size = min(len(card_pool), size)
        self.original_deck = random.sample(card_pool, safe_size)
        # ---------------------------------------------------------
        self.deck = list(self.original_deck)
        random.shuffle(self.deck)

    def to_dict(self):
        return {
            'name': self.name, 'max_hp': self.max_hp, 'hp': self.hp, 'atk': self.atk,
            'defense': self.defense, 'spd': self.spd, 'luck': self.luck, 'money': self.money,
            'current_location': self.current_location, 'reputation': self.reputation,
            'active_quests': self.active_quests, 'completed_quests': self.completed_quests,
            'original_deck': [card.to_dict() for card in self.original_deck]
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(data['name'])
        player.max_hp = data['max_hp']; player.hp = data['hp']; player.atk = data['atk']
        player.defense = data['defense']; player.spd = data['spd']; player.luck = data['luck']
        player.money = data['money']; player.current_location = data['current_location']
        player.reputation = data['reputation']; player.active_quests = data['active_quests']
        player.completed_quests = data['completed_quests']
        player.original_deck = [Card.from_dict(c_data) for c_data in data['original_deck']]
        player.deck = list(player.original_deck)
        random.shuffle(player.deck)
        return player

class Enemy(Character):
    def __init__(self, name, max_hp, atk, defense, spd, luck, card_pool):
        super().__init__(name, max_hp, atk, defense, spd, luck)
        self.deck = random.sample(card_pool, min(len(card_pool), 10))


# --- ส่วนหลักของเกม ---
class Game:
    def __init__(self):
        self.player = None
        self.game_state = 'MAIN_MENU'
        self.is_running = True
        self.cause_of_death = "ความเหนื่อยล้าจากการเดินทาง"
        self.current_enemies = []
        self.setup_game_data()

    def setup_game_data(self):
        # Setup Cards
        self.all_player_cards = [ Card("ฟันดาบ", "ATTACK", 5, "โจมตีปกติ"), Card("ตั้งรับ", "DEFEND", 5, "ป้องกันความเสียหาย"), Card("จู่โจมเร็ว", "ATTACK", 3, "โจมตีอย่างรวดเร็ว"), Card("แทง", "ATTACK", 7, "โจมตีจุดตาย"), Card("ปัดป้อง", "DEFEND", 7, "ป้องกันอย่างสมบูรณ์"), Card("ไหวพริบ", "SKILL", 0, "จั่วการ์ดเพิ่ม 1 ใบ"), Card("ข่มขวัญ", "SKILL", 0, "ลดพลังป้องกันศัตรู"), Card("รวบรวมสมาธิ", "SKILL", 0, "เพิ่มพลังโจมตีในเทิร์นถัดไป"), Card("ยาฟื้นฟู", "ITEM", 10, "ฟื้นฟู HP เล็กน้อย") ]
        bandit_cards = [Card("ฟัน", "ATTACK", 4, ""), Card("ปาหิน", "ATTACK", 2, ""), Card("ป้องกันตัว", "DEFEND", 3, "")]
        
        # Setup Enemies
        self.enemies_pool = {
            "โจรป่า": lambda: Enemy("โจรป่า", 80, 8, 3, 5, 3, bandit_cards),
            "หมาป่า": lambda: Enemy("หมาป่า", 60, 10, 1, 8, 5, [Card("กัด", "ATTACK", 5, "")]*10),
            "โรนินตกอับ": lambda: Enemy("โรนินตกอับ", 90, 12, 4, 6, 4, self.all_player_cards[:5])
        }

        # Setup Locations
        self.locations = { "เมืองหลวงเคียว": {"type": "เมืองหลวง", "services": ["โรงเตี๊ยม", "โรงตีดาบ", "ตลาด", "โรงฝึก"]}, "หมู่บ้านฮาจิมัง": {"type": "เมืองบ้านนอก", "services": ["โรงเตี๊ยม", "ร้านค้าเล็กๆ"]}, "หมู่บ้านชาวประมงอิเสะ": {"type": "เมืองบ้านนอก", "services": ["โรงเตี๊ยม"]},"ป้อมปราการโอวาริ": {"type": "เมืองบ้านนอก", "services": ["โรงเตี๊ยม", "โรงตีดาบ"]},"ป่าไผ่ซากาโนะ": {"type": "สถานที่ห่างไกล", "services": []},"ทุ่งหญ้าเซกิงาฮาระ": {"type": "สถานที่ห่างไกล", "services": []},"ศาลเจ้าฟูชิมิอินาริ": {"type": "สถานที่ห่างไกล", "services": []},"วัดคิโยมิสุ": {"type": "สถานที่ห่างไกล", "services": []} }

        # Setup Time
        self.time = {"day": 1, "month": 1, "year": 1470, "segment": "เช้า"}
        self.time_segments = ["เช้า", "กลางวัน", "เย็น", "กลางคืน"]

        # Setup Business Hours
        self.service_hours = {"โรงตีดาบ": ["เช้า", "กลางวัน"], "ตลาด": ["เช้า", "กลางวัน"], "ร้านค้าเล็กๆ": ["เช้า", "กลางวัน", "เย็น"], "โรงฝึก": ["เช้า", "กลางวัน"] }

        # Setup Quests
        self.all_quests = get_quests()

    def advance_time(self, segments=1):
        for _ in range(segments):
            current_index = self.time_segments.index(self.time["segment"])
            if current_index == 3:
                self.time["segment"] = "เช้า"
                self.time["day"] += 1
                if self.time["day"] > 30:
                    self.time["day"] = 1
                    self.time["month"] += 1
                    if self.time["month"] > 12:
                        self.time["month"] = 1
                        self.time["year"] += 1
            else:
                self.time["segment"] = self.time_segments[current_index + 1]

    def new_game(self):
        self.player = Player("โรนิน")
        self.player.build_deck(self.all_player_cards, 10)
        self.time = {"day": random.randint(1,28), "month": random.randint(1,12), "year": 1470, "segment": "เช้า"}
        self.game_state = 'LOCATION_HUB'
        print("เริ่มต้นการเดินทางครั้งใหม่!")
        time.sleep(1.5)

    def save_game(self):
        if not self.player: return
        save_data = {'player': self.player.to_dict(), 'time': self.time}
        with open('savegame.json', 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=4)
        print("เกมถูกบันทึกเรียบร้อยแล้ว")

    def load_game(self):
        try:
            with open('savegame.json', 'r', encoding='utf-8') as f:
                save_data = json.load(f)
                self.player = Player.from_dict(save_data['player'])
                self.time = save_data['time']
                self.game_state = 'LOCATION_HUB'
                print("โหลดเกมสำเร็จ!")
                time.sleep(1.5)
                return True
        except FileNotFoundError:
            print("ไม่พบไฟล์เซฟ...")
            time.sleep(1.5)
            return False

    def show_intro(self):
        clear_screen()
        intro_text = [ "ปี ค.ศ. 1470... แผ่นดินญี่ปุ่นลุกเป็นไฟ", "สงครามโอนินแผดเผาเมืองหลวงจนมอดไหม้...", "ท่ามกลางยุคสมัยแห่งความโกลาหล... ตระกูลของคุณต้องพบกับจุดจบ", "คุณ... ผู้รอดชีวิตเพียงหนึ่งเดียว", "บัดนี้กลายเป็น 'โรนิน' ซามูไรพเนจรไร้นาย", "ตำนานของคุณ... เริ่มต้นขึ้นแล้ว ณ บัดนี้" ]
        for line in intro_text:
            typewriter_print(line)
            time.sleep(1.5)
        input("\nกด Enter เพื่อเริ่มต้นการเดินทาง...")

    def run(self):
        try:
            while self.is_running:
                if self.game_state == 'MAIN_MENU': self.main_menu_phase()
                elif self.game_state == 'LOCATION_HUB': self.location_hub_phase()
                elif self.game_state == 'TRAVELING': self.traveling_phase()
                elif self.game_state == 'COMBAT': self.combat_phase()
                elif self.game_state == 'GAME_OVER':
                    self.game_over_phase()
                    self.is_running = False
        except Exception as e:
            # กล่องดำดักจับข้อผิดพลาด
            print("\n\n---!!! เกิดข้อผิดพลาดที่ไม่คาดคิด !!!---")
            print(f"ข้อความ Error: {e}")
            print("\nเกมจะปิดตัวลง กรุณาคัดลอกข้อความด้านบนนี้เพื่อแจ้งให้ผู้พัฒนาทราบ")
            input("\nกด Enter เพื่อปิดโปรแกรม...")
            self.is_running = False
    
    # --- PHASES ---
    def main_menu_phase(self):
        clear_screen()
        print("ยินดีต้อนรับสู่ MaiWa V1.7 (PC)\n")
        print("1. เริ่มเกมใหม่")
        print("2. โหลดเกม")
        choice = input("เลือก: ")
        if choice == '1':
            self.show_intro()
            self.new_game()
        elif choice == '2':
            if not self.load_game(): 
                self.show_intro()
                self.new_game()

    def location_hub_phase(self):
        clear_screen()
        loc_name = self.player.current_location
        loc_type = self.locations[loc_name]["type"]
        
        # Check for completed quests
        completed_this_turn = []
        for q_id, quest in self.player.active_quests.items():
            if quest["progress"] >= quest["objective"]["count"]:
                print(f"--- ภารกิจสำเร็จ: {quest['title']} ---")
                self.player.money += quest["reward"]["money"]
                self.player.reputation[loc_name] = self.player.reputation.get(loc_name, 0) + quest["reward"]["reputation"]
                print(f"ได้รับเงิน {quest['reward']['money']} มง และชื่อเสียง {quest['reward']['reputation']} แต้ม")
                self.player.completed_quests.append(q_id)
                completed_this_turn.append(q_id)
                time.sleep(2)
        
        for q_id in completed_this_turn:
            del self.player.active_quests[q_id]

        print(f"--- {loc_name} ({loc_type}) ---")
        print(f"วันที่ {self.time['day']}/{self.time['month']}/{self.time['year']} | เวลา: {self.time['segment']}")
        print(f"HP: {self.player.hp}/{self.player.max_hp} | เงิน: {self.player.money} มง | ชื่อเสียง: {self.player.reputation.get(loc_name, 0)}")
        print("-" * 30)

        options = ["ออกเดินทาง", "พูดคุยกับชาวบ้าน", "ดูภารกิจ"]
        
        # Add location-specific services
        for service in self.locations[loc_name].get("services", []):
            if service not in options:
                is_open = self.time["segment"] in self.service_hours.get(service, self.time_segments)
                options.append(f"{service} {'(ปิด)' if not is_open else ''}")

        options.extend(["บันทึกเกม", "ออกจากเกม"])

        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        choice = input("เลือก: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            action = options[int(choice)-1].split(" ")[0]
            
            if action == "ออกเดินทาง": self.game_state = 'TRAVELING'
            elif action == "พูดคุยกับชาวบ้าน": self.talk_to_npc_phase()
            elif action == "ดูภารกิจ": self.view_quests_phase()
            elif action == "โรงเตี๊ยม": self.inn_phase()
            elif action == "บันทึกเกม": self.save_game(); time.sleep(1)
            elif action == "ออกจากเกม": self.is_running = False
            else:
                if "(ปิด)" not in options[int(choice)-1]:
                    print(f"ยังไม่เปิดให้บริการ '{action}'")
                    time.sleep(1.5)
                else:
                    print(f"'{action}' ปิดให้บริการในเวลานี้")
                    time.sleep(1.5)

    def talk_to_npc_phase(self):
        clear_screen()
        loc_type = self.locations[self.player.current_location]["type"]
        dialogue = get_dialogue(loc_type)
        print("คุณเดินเข้าไปพูดคุยกับชาวบ้านคนหนึ่ง...")
        time.sleep(1)
        typewriter_print(f"ชาวบ้าน: \"{dialogue}\"")
        self.advance_time()

        # Quest Chance
        if random.random() < 0.3: # 30% chance to get a quest offer
            available_quests = [ q_id for q_id, q_data in self.all_quests.items() 
                                 if loc_type in q_data["giver_type"] and 
                                 q_id not in self.player.active_quests and 
                                 q_id not in self.player.completed_quests ]
            if available_quests:
                quest_id = random.choice(available_quests)
                quest = self.all_quests[quest_id]
                print("\nดูเหมือนว่าเขามีเรื่องเดือดร้อน...")
                time.sleep(1)
                typewriter_print(f"ชาวบ้าน: \"เอ่อ... ท่านซามูไร คือว่า... {quest['description']}\"")
                
                choice = input("\nคุณจะรับภารกิจนี้หรือไม่? (y/n): ").lower()
                if choice == 'y':
                    self.player.active_quests[quest_id] = {
                        "title": quest["title"], "objective": quest["objective"],
                        "reward": quest["reward"], "progress": 0
                    }
                    print(f"\nคุณรับภารกิจ: {quest['title']}")
                else:
                    print("\nคุณปฏิเสธความช่วยเหลือในครั้งนี้")
        
        input("\nกด Enter เพื่อกลับ...")

    def view_quests_phase(self):
        clear_screen()
        print("--- ภารกิจที่กำลังทำ ---")
        if not self.player.active_quests:
            print("ยังไม่มีภารกิจที่รับไว้")
        else:
            for q_id, quest in self.player.active_quests.items():
                obj = quest['objective']
                print(f"- {quest['title']} ({quest['progress']}/{obj['count']} {obj['target']})")
        input("\nกด Enter เพื่อกลับ...")

    def inn_phase(self):
        clear_screen()
        print("--- โรงเตี๊ยม ---")
        rep = self.player.reputation.get(self.player.current_location, 0)
        cost = max(0, 10 - rep // 10)
        print(f"เจ้าของ: \"ยินดีต้อนรับท่านซามูไร ค่าที่พักคืนนี้ {cost} มง ท่านจะพักหรือไม่?\"")
        
        choice = input("(y/n): ").lower()
        if choice == 'y':
            if self.player.money >= cost:
                self.player.money -= cost
                self.player.hp = self.player.max_hp
                self.player.reputation[self.player.current_location] = rep + 1 # gain reputation
                # Advance time to next morning
                while self.time["segment"] != "เช้า":
                    self.advance_time()
                self.advance_time()
                print("\nคุณได้พักผ่อนอย่างเต็มที่... เช้าวันใหม่ได้เริ่มขึ้นแล้ว")
            else:
                print("\nเงินของคุณไม่พอสำหรับค่าที่พัก...")
        time.sleep(2)

    def traveling_phase(self):
        clear_screen()
        print("คุณกำลังเดินทางบนเส้นทางสายเปลี่ยว...")
        self.advance_time()
        time.sleep(2)

        # Random Encounter
        if random.random() < 0.6: # 60% chance of encounter
            enemy_type = random.choice(list(self.enemies_pool.keys()))
            num_enemies = random.randint(1, 3)
            self.current_enemies = [self.enemies_pool[enemy_type]() for _ in range(num_enemies)]
            print(f"\n!!! คุณถูกลอบโจมตีโดย {enemy_type} {num_enemies} ตัว !!!")
            time.sleep(2)
            self.game_state = 'COMBAT'
        else:
            print("\nการเดินทางครั้งนี้ปลอดภัยดี")
            time.sleep(2)
            # Find a new location (simple for now)
            new_location = random.choice([loc for loc in self.locations if loc != self.player.current_location])
            self.player.current_location = new_location
            print(f"คุณเดินทางมาถึง {new_location}")
            time.sleep(2)
            self.game_state = 'LOCATION_HUB'

    def combat_phase(self):
        # Reset decks and draw initial hands
        self.player.deck = list(self.player.original_deck)
        random.shuffle(self.player.deck)
        self.player.discard = []
        self.player.hand = []
        self.player.draw_hand()
        
        for enemy in self.current_enemies:
            enemy.draw_hand()

        turn = 1
        while any(e.is_alive() for e in self.current_enemies) and self.player.is_alive():
            clear_screen()
            print(f"--- การต่อสู้ | เทิร์นที่ {turn} ---")
            
            # Display enemies
            for i, enemy in enumerate(self.current_enemies):
                status = "HP: " + str(enemy.hp) if enemy.is_alive() else "ตายแล้ว"
                print(f"{i+1}. {enemy.name} ({status})")

            # Display player
            print(f"\nคุณ: HP {self.player.hp}/{self.player.max_hp}")
            if self.player.defense_bonus > 0:
                print(f"   └ ตั้งรับ: {self.player.defense_bonus}")
            
            # Player's Turn
            self.player_turn()
            if not any(e.is_alive() for e in self.current_enemies): break

            # Enemies' Turn
            for enemy in self.current_enemies:
                if enemy.is_alive() and self.player.is_alive():
                    self.enemy_turn(enemy)
                    if not self.player.is_alive():
                        self.cause_of_death = f"พ่ายแพ้ในคมดาบของ {enemy.name}"
                        break
            
            turn += 1
            input("\nกด Enter เพื่อเข้าสู่เทิร์นถัดไป...")
        
        # End of combat
        clear_screen()
        if self.player.is_alive():
            print("\n--- คุณได้รับชัยชนะ! ---")
            money_gain = sum(random.randint(5, 15) for _ in self.current_enemies)
            self.player.money += money_gain
            print(f"ได้รับเงิน {money_gain} มง")
            
            # Update Quests
            killed_enemies = [e.name for e in self.current_enemies]
            for q_id, quest in self.player.active_quests.items():
                if quest["objective"]["type"] == "kill":
                    target_name = quest["objective"]["target"]
                    kill_count = sum(1 for name in killed_enemies if name == target_name)
                    if kill_count > 0:
                        quest["progress"] += kill_count
                        print(f"ความคืบหน้าภารกิจ '{quest['title']}': {quest['progress']}/{quest['objective']['count']}")

            self.game_state = 'LOCATION_HUB'
        else:
            print("\nคุณพ่ายแพ้...")
            self.game_state = 'GAME_OVER'
        
        input("กด Enter เพื่อดำเนินการต่อ...")

    def player_turn(self):
        print("\n--- ตาของคุณ ---")
        used_cards_this_turn = 0
        while used_cards_this_turn < 2 and self.player.is_alive() and any(e.is_alive() for e in self.current_enemies):
            print("\nการ์ดในมือ:")
            for i, card in enumerate(self.player.hand):
                print(f"  {i+1}. [{card.type}] {card.name} ({card.value}) - {card.desc}")
            print("  0. จบเทิร์น")

            choice = input("เลือกการ์ด (หรือ 0 เพื่อจบเทิร์น): ")
            if not choice.isdigit(): continue
            choice = int(choice)

            if choice == 0: break
            if not (1 <= choice <= len(self.player.hand)):
                print("เลือกไม่ถูกต้อง")
                continue

            card = self.player.hand.pop(choice - 1)
            
            if card.type == "ATTACK":
                target_choice = input(f"เลือกเป้าหมาย (1-{len(self.current_enemies)}): ")
                if target_choice.isdigit():
                    target_idx = int(target_choice) - 1
                    if 0 <= target_idx < len(self.current_enemies) and self.current_enemies[target_idx].is_alive():
                        target = self.current_enemies[target_idx]
                        damage = self.player.atk + card.value
                        actual_damage = target.take_damage(damage)
                        print(f"คุณใช้ '{card.name}' โจมตี {target.name} ทำความเสียหาย {actual_damage}!")
                    else:
                        print("เป้าหมายไม่ถูกต้อง")
                        self.player.hand.insert(choice - 1, card) # Return card to hand
                        continue
                else:
                    print("เลือกเป้าหมายไม่ถูกต้อง")
                    self.player.hand.insert(choice - 1, card) # Return card to hand
                    continue

            elif card.type == "DEFEND":
                self.player.defense_bonus += card.value
                print(f"คุณใช้ '{card.name}' ตั้งรับ {card.value} แต้ม!")
            
            # Other card types can be added here
            
            self.player.discard.append(card)
            used_cards_this_turn += 1
            time.sleep(1)

        self.player.draw_hand() # Draw for next turn

    def enemy_turn(self, enemy):
        print(f"\n--- ตาของ {enemy.name} ---")
        time.sleep(1)
        # Simple AI: just attack
        damage = enemy.atk + random.randint(0, 3)
        actual_damage = self.player.take_damage(damage)
        print(f"{enemy.name} โจมตี! คุณได้รับความเสียหาย {actual_damage} แต้ม!")
        time.sleep(1)

    def game_over_phase(self):
        clear_screen()
        print("--- ตำนานของคุณได้จบสิ้นลงแล้ว ---")
        time.sleep(2)
        
        death_by_enemy_type = "Unknown"
        if "โจรป่า" in self.cause_of_death: death_by_enemy_type = "Bandit"
        elif "หมาป่า" in self.cause_of_death: death_by_enemy_type = "Wolf"
        elif "โรนิน" in self.cause_of_death: death_by_enemy_type = "Ronin"

        end_stories = {
            "Bandit": [f"สาเหตุ: {self.cause_of_death}", "ร่างกายของคุณถูกทิ้งไว้ข้างทางอย่างไร้ค่า", "ข้าวของทุกชิ้นถูกปล้นไปจนหมดสิ้น", "ชื่อของคุณ... ถูกลืมเลือนไปกับสายลม ราวกับไม่เคยมีตัวตน"],
            "Wolf": [f"สาเหตุ: {self.cause_of_death}", "คุณพ่ายแพ้ให้แก่สัญชาตญาณดิบของสัตว์ร้าย", "ร่างกายของคุณกลายเป็นอาหารให้กับฝูงของมัน", "ไม่มีใครรู้ถึงชะตากรรมของคุณ มีเพียงเสียงหอนอันเยือกเย็นในยามค่ำคืน"],
            "Ronin": [f"สาเหตุ: {self.cause_of_death}", "เป็นการดวลที่สมศักดิ์ศรี... แต่คุณคือผู้ที่ช้ากว่าเพียงก้าวเดียว", "ดาบของคุณถูกปักไว้บนพื้นดินเพื่อเป็นเกียรติแก่นักสู้", "เรื่องราวของคุณกลายเป็นข่าวลือในโรงเตี๊ยมอยู่พักหนึ่ง... ก่อนจะเลือนหายไป"]
        }
        
        story_lines = end_stories.get(death_by_enemy_type, [f"สาเหตุ: {self.cause_of_death}", "คุณล้มลงกลางทาง...", "ไม่มีใครบันทึกเรื่องราว ไม่มีใครจดจำการเดินทางครั้งนี้"])
        
        for line in story_lines:
            typewriter_print(f"\n{line}")
            time.sleep(2)
            
        print("\n\nGAME OVER")

# --- Main Execution ---
if __name__ == "__main__":
    game = Game()
    game.run()

