# -*- coding: utf-8 -*-
import os
import sys
import json
import random
import time
import textwrap

# --- NEW: ระบบนำทางสำหรับ .exe ---
def get_base_path():
    """ หา Path หลักของโปรแกรม ไม่ว่าจะรันจาก .py หรือ .exe """
    if getattr(sys, 'frozen', False):
        # รันจาก .exe ที่ถูก build แล้ว
        return os.path.dirname(sys.executable)
    else:
        # รันจาก .py ปกติ
        return os.path.dirname(os.path.abspath(__file__))

# --- นำเข้าข้อมูลและคลาสจากไฟล์อื่น ---
from game_classes import Card, Weapon, Armor, Player, Enemy
from npc_dialogue import get_dialogue
from quest_data import get_quests
from weapon_data import get_weapons
from skill_data import get_skills
from item_data import get_items
from location_data import get_regions, get_locations
from enemy_data import get_enemies, get_enemy_card_pools
from armor_data import get_armors

# --- ฟังก์ชันเสริม ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# --- ส่วนหลักของเกม ---
class Game:
    def __init__(self):
        self.player = None; self.game_state = 'MAIN_MENU'; self.is_running = True; self.cause_of_death = "ความเหนื่อยล้าจากการเดินทาง"; self.current_enemies = []
        self.base_path = get_base_path()
        self.setup_game_data()

    def setup_game_data(self):
        self.all_player_cards = [ Card("ฟันดาบ", "ATTACK", 5, "โจมตีปกติ"), Card("ตั้งรับ", "DEFEND", 5, "ป้องกันความเสียหาย"), Card("จู่โจมเร็ว", "ATTACK", 3, "โจมตีอย่างรวดเร็ว"), Card("แทง", "ATTACK", 7, "โจมตีจุดตาย"), Card("ปัดป้อง", "DEFEND", 7, "ป้องกันอย่างสมบูรณ์") ]; self.all_quests = get_quests(); self.all_weapons = get_weapons(); self.all_skills = get_skills(); self.all_items = get_items(); self.all_regions = get_regions(); self.all_locations = get_locations(); self.all_enemies_data = get_enemies(); self.enemy_card_pools = get_enemy_card_pools(); self.all_armors = get_armors()
        self.enemies_by_region_type = {}
        for e_id, e_data in self.all_enemies_data.items():
            for region_type in e_data["region_types"]:
                if region_type not in self.enemies_by_region_type: self.enemies_by_region_type[region_type] = []
                self.enemies_by_region_type[region_type].append(e_id)
        self.time = {"day": 1, "month": 1, "year": 1470, "segment": "เช้า"}; self.time_segments = ["เช้า", "กลางวัน", "เย็น", "กลางคืน"]; self.service_hours = {"โรงตีดาบ": ["เช้า", "กลางวัน"], "ตลาด": ["เช้า", "กลางวัน"], "ร้านค้าเล็กๆ": ["เช้า", "กลางวัน", "เย็น"], "โรงฝึก": ["เช้า", "กลางวัน"] }

    def advance_time(self, segments=1):
        for _ in range(segments):
            current_index = self.time_segments.index(self.time["segment"])
            if current_index == 3:
                self.time["segment"] = "เช้า"; self.time["day"] += 1
                if self.time["day"] > 30: self.time["day"] = 1; self.time["month"] += 1
                if self.time["month"] > 12: self.time["month"] = 1; self.time["year"] += 1
            else: self.time["segment"] = self.time_segments[current_index + 1]

    def new_game(self):
        self.player = Player("โรนิน"); plains_region_ids = [r_id for r_id, r_data in self.all_regions.items() if r_data["type"] == "plains"]; self.player.current_region_id = random.choice(plains_region_ids) if plains_region_ids else list(self.all_regions.keys())[0]; possible_start_locations = [l_id for l_id, l_data in self.all_locations.items() if l_data["region_id"] == self.player.current_region_id]; self.player.current_location_id = random.choice(possible_start_locations) if possible_start_locations else list(self.all_locations.keys())[0]; self.player.build_deck(self.all_player_cards, 10); self.time = {"day": random.randint(1,28), "month": random.randint(1,12), "year": 1470, "segment": "เช้า"}; self.game_state = 'LOCATION_HUB'; loc_name = self.all_locations[self.player.current_location_id]['name']; print(f"การเดินทางของคุณเริ่มต้นที่... {loc_name}"); time.sleep(2)

    def save_game(self):
        if not self.player: return
        save_data = {'player': self.player.to_dict(), 'time': self.time}
        save_file_path = os.path.join(self.base_path, 'savegame.json')
        with open(save_file_path, 'w', encoding='utf-8') as f: json.dump(save_data, f, ensure_ascii=False, indent=4)
        print("เกมถูกบันทึกเรียบร้อยแล้ว")

    def load_game(self):
        try:
            save_file_path = os.path.join(self.base_path, 'savegame.json')
            with open(save_file_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f); self.player = Player.from_dict(save_data['player']); self.time = save_data['time']; self.game_state = 'LOCATION_HUB'; print("โหลดเกมสำเร็จ!"); time.sleep(1.5); return True
        except (FileNotFoundError, json.JSONDecodeError): print("ไม่พบไฟล์เซฟ หรือไฟล์เสียหาย..."); time.sleep(1.5); return False

    def show_intro(self):
        clear_screen(); intro_text = [ "ปี ค.ศ. 1470... แผ่นดินญี่ปุ่นลุกเป็นไฟ", "สงครามโอนินแผดเผาเมืองหลวงจนมอดไหม้...", "ท่ามกลางยุคสมัยแห่งความโกลาหล... ตระกูลของคุณต้องพบกับจุดจบ", "คุณ... ผู้รอดชีวิตเพียงหนึ่งเดียว", "บัดนี้กลายเป็น 'โรนิน' ซามูไรพเนจรไร้นาย", "ตำนานของคุณ... เริ่มต้นขึ้นแล้ว ณ บัดนี้" ];
        for line in intro_text: typewriter_print(line); time.sleep(1.5)
        input("\nกด Enter เพื่อเริ่มต้นการเดินทาง...")

    def run(self):
        try:
            while self.is_running:
                if self.game_state == 'MAIN_MENU': self.main_menu_phase()
                elif self.game_state == 'LOCATION_HUB': self.location_hub_phase()
                elif self.game_state == 'TRAVELING': self.traveling_phase()
                elif self.game_state == 'COMBAT': self.combat_phase()
                elif self.game_state == 'GAME_OVER': self.game_over_phase(); self.is_running = False
        except Exception as e: print(f"\n\n---!!! เกิดข้อผิดพลาดที่ไม่คาดคิด !!!---\nข้อความ Error: {e}\nประเภท Error: {type(e).__name__}\nเกมจะปิดตัวลง กรุณาคัดลอกข้อความด้านบนนี้เพื่อแจ้งให้ผู้พัฒนาทราบ"); input("\nกด Enter เพื่อปิดโปรแกรม..."); self.is_running = False
    
    def main_menu_phase(self):
        clear_screen(); print("ยินดีต้อนรับสู่ MaiWa BETA 2.12 (PC)\n"); print("1. เริ่มเกมใหม่"); print("2. โหลดเกม")
        choice = input("เลือก: ")
        if choice == '1': self.show_intro(); self.new_game()
        elif choice == '2':
            if not self.load_game(): self.show_intro(); self.new_game()

    def location_hub_phase(self):
        clear_screen(); loc_id = self.player.current_location_id; loc_data = self.all_locations[loc_id]; loc_name = loc_data["name"]; loc_type = loc_data["type"]
        completed_this_turn = []
        for q_id, quest in list(self.player.active_quests.items()):
            if quest.get("progress", 0) >= quest.get("objective", {}).get("count", 1):
                print(f"--- ภารกิจสำเร็จ: {quest['title']} ---"); reward = quest.get("reward", {}); self.player.money += reward.get("money", 0); self.player.reputation[loc_name] = self.player.reputation.get(loc_name, 0) + reward.get("reputation", 0); print(f"ได้รับเงิน {reward.get('money', 0)} มง และชื่อเสียง {reward.get('reputation', 0)} แต้ม"); self.player.completed_quests.append(q_id); completed_this_turn.append(q_id); time.sleep(2)
        for q_id in completed_this_turn: del self.player.active_quests[q_id]
        print(f"--- {loc_name} ({loc_type}) ---"); print(f"วันที่ {self.time['day']}/{self.time['month']}/{self.time['year']} | เวลา: {self.time['segment']}")
        print(f"HP: {self.player.hp}/{self.player.max_hp} | ATK: {self.player.get_total_atk()} | DEF: {self.player.get_total_def()} | เงิน: {self.player.money} มง | ชื่อเสียง: {self.player.reputation.get(loc_name, 0)}")
        equipped_weapon_name = self.player.equipped_weapon.name if self.player.equipped_weapon else "มือเปล่า"; print(f"อาวุธที่ใช้: {equipped_weapon_name}"); print("-" * 30)
        options = ["ออกเดินทาง", "ดูภารกิจ", "จัดการยุทโธปกรณ์", "ดูไอเทมในย่าม"];
        for service in loc_data.get("services", []):
            if service not in options: is_open = self.time["segment"] in self.service_hours.get(service, self.time_segments); options.append(f"{service} {'(ปิด)' if not is_open else ''}")
        options.extend(["บันทึกเกม", "ออกจากเกม"]);
        for i, option in enumerate(options, 1): print(f"{i}. {option}")
        choice = input("เลือก: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            action = options[int(choice)-1].split(" ")[0]
            if "(ปิด)" in options[int(choice)-1]: print(f"'{action}' ปิดให้บริการในเวลานี้"); time.sleep(1.5); return
            if action == "ออกเดินทาง": self.game_state = 'TRAVELING'
            elif action == "พูดคุยกับชาวบ้าน": self.talk_to_npc_phase()
            elif action == "ดูภารกิจ": self.view_quests_phase()
            elif action == "ดูไอเทมในย่าม": self.inventory_phase()
            elif action == "จัดการยุทโธปกรณ์": self.equipment_phase()
            elif action == "โรงเตี๊ยม": self.inn_phase()
            elif action in ["ร้านค้าเล็กๆ", "โรงตีดาบ", "ตลาด"]: self.shop_phase(action)
            elif action == "โรงฝึก": self.dojo_phase()
            elif action == "บันทึกเกม": self.save_game(); time.sleep(1)
            elif action == "ออกจากเกม": self.is_running = False
            else: print(f"ยังไม่เปิดให้บริการ '{action}' ในตอนนี้"); time.sleep(1.5)

    def inventory_phase(self):
        clear_screen(); print("--- ไอเทมในย่าม ---")
        if not self.player.item_inventory: print("- ย่ามของคุณว่างเปล่า -")
        else:
            for item_name, quantity in self.player.item_inventory.items(): print(f"- {item_name} x{quantity}")
        input("\nกด Enter เพื่อกลับ...")

    def equipment_phase(self):
        while True:
            clear_screen(); print("--- จัดการยุทโธปกรณ์ ---"); wep = self.player.equipped_weapon; head = self.player.equipped_head; body = self.player.equipped_body; feet = self.player.equipped_feet
            print(f"1. อาวุธ: {wep.name if wep else 'มือเปล่า'} (ATK +{wep.bonus_atk if wep else 0})")
            print(f"2. ศีรษะ: {head.name if head else 'ว่าง'} (DEF +{head.bonus_def if head else 0})")
            print(f"3. ลำตัว: {body.name if body else 'ว่าง'} (DEF +{body.bonus_def if body else 0})")
            print(f"4. เท้า:   {feet.name if feet else 'ว่าง'} (DEF +{feet.bonus_def if feet else 0})")
            print("\n0. กลับ"); choice = input("เลือกส่วนที่จะจัดการ: ")
            if choice == '0': break
            elif choice == '1': self.manage_slot('weapon')
            elif choice == '2': self.manage_slot('head')
            elif choice == '3': self.manage_slot('body')
            elif choice == '4': self.manage_slot('feet')

    def manage_slot(self, slot_type):
        clear_screen(); print(f"--- เลือกอุปกรณ์สำหรับช่อง '{slot_type.capitalize()}' ---")
        if slot_type == 'weapon': inventory = self.player.weapon_inventory; item_list = [(item, f"ATK +{item.bonus_atk}") for item in inventory]
        else: inventory = self.player.armor_inventory; item_list = [(item, f"DEF +{item.bonus_def}") for item in inventory if item.slot == slot_type]
        
        if not item_list: print("- ไม่มีอุปกรณ์ประเภทนี้ในคลัง -")
        else:
            for i, (item, stat_text) in enumerate(item_list, 1): print(f"{i}. {item.name} ({stat_text})")
        
        print("\n99. ถอดอุปกรณ์"); print("0. กลับ"); choice = input("เลือก: ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 0: return
            elif choice == 99:
                if slot_type == 'weapon': self.player.equipped_weapon = None
                elif slot_type == 'head': self.player.equipped_head = None
                elif slot_type == 'body': self.player.equipped_body = None
                elif slot_type == 'feet': self.player.equipped_feet = None
                print("\nคุณถอดอุปกรณ์แล้ว"); time.sleep(1)
            elif 1 <= choice <= len(item_list):
                item_to_equip = item_list[choice-1][0]
                if slot_type == 'weapon': self.player.equipped_weapon = item_to_equip
                elif slot_type == 'head': self.player.equipped_head = item_to_equip
                elif slot_type == 'body': self.player.equipped_body = item_to_equip
                elif slot_type == 'feet': self.player.equipped_feet = item_to_equip
                print(f"\nคุณสวมใส่ {item_to_equip.name}"); time.sleep(1.5)

    def shop_phase(self, shop_type):
        clear_screen(); print(f"--- {shop_type} ---"); greetings = { "โรงตีดาบ": "ช่างตีดาบ: \"ดาบดีๆ ช่วยรักษาชีวิตเจ้านะ... สนใจเล่มไหนล่ะ?\"", "ร้านค้าเล็กๆ": "เจ้าของร้าน: \"ยินดีต้อนรับ! ของจำเป็นสำหรับนักเดินทางอยู่ที่นี่แล้ว\"", "ตลาด": "พ่อค้า: \"ของแปลกๆ หายากๆ เชิญดูทางนี้เลย!\"" }; print(greetings.get(shop_type, "พ่อค้า: \"ยินดีต้อนรับ!\""))
        for_sale = []
        for w_id, w_data in self.all_weapons.items():
            if shop_type in w_data.get("sale_locations", []): for_sale.append({'type': 'weapon', 'id': w_id, 'data': w_data})
        for a_id, a_data in self.all_armors.items():
            if shop_type in a_data.get("sale_locations", []): for_sale.append({'type': 'armor', 'id': a_id, 'data': a_data})
        for i_id, i_data in self.all_items.items():
            if shop_type in i_data.get("sale_locations", []): for_sale.append({'type': 'item', 'id': i_id, 'data': i_data})

        if not for_sale: print("\nดูเหมือนว่าวันนี้จะไม่มีอะไรวางขายเป็นพิเศษนะ"); input("\nกด Enter เพื่อออกจากร้าน..."); self.advance_time(); return
        while True:
            clear_screen(); print(f"--- {shop_type} ---"); print(f"เงินของคุณ: {self.player.money} มง"); print("-" * 30); print("\n--- สินค้า ---")
            for i, item in enumerate(for_sale, 1):
                data = item['data'];
                if item['type'] == 'weapon': print(f"{i}. [อาวุธ] {data['name']} (ATK +{data['bonus_atk']}) - ราคา {data['price']} มง")
                elif item['type'] == 'armor': print(f"{i}. [เกราะ] {data['name']} (DEF +{data['bonus_def']}) - ราคา {data['price']} มง")
                elif item['type'] == 'item': print(f"{i}. [ไอเทม] {data['name']} ({data['desc']}) - ราคา {data['price']} มง")
            print("0. ออกจากร้าน"); choice = input("เลือกสินค้าที่จะซื้อ: ")
            if not choice.isdigit(): continue
            choice = int(choice);
            if choice == 0: break
            if 1 <= choice <= len(for_sale):
                selected_item = for_sale[choice-1]; item_data = selected_item['data']
                if self.player.money >= item_data['price']:
                    self.player.money -= item_data['price']
                    if selected_item['type'] == 'weapon': new_weapon = Weapon(selected_item['id'], item_data['name'], item_data['bonus_atk'], item_data['price']); self.player.weapon_inventory.append(new_weapon); print(f"\nคุณได้ซื้อ {item_data['name']}!")
                    elif selected_item['type'] == 'armor': new_armor = Armor(selected_item['id'], item_data['name'], item_data['slot'], item_data['bonus_def'], item_data['price']); self.player.armor_inventory.append(new_armor); print(f"\nคุณได้ซื้อ {item_data['name']}!")
                    elif selected_item['type'] == 'item': item_name = item_data['name']; self.player.item_inventory[item_name] = self.player.item_inventory.get(item_name, 0) + 1; print(f"\nคุณได้ซื้อ {item_name}!")
                    time.sleep(1.5)
                else: print("\nเงินของคุณไม่พอ..."); time.sleep(1.5)
        self.advance_time()

    def dojo_phase(self):
        clear_screen(); print("--- โรงฝึก ---"); print("อาจารย์: \"วิชาดาบคือหนทางแห่งชีวิต... เจ้าสนใจจะขัดเกลาฝีมือของตนเองหรือไม่?\"")
        learned_card_names = [card.name for card in self.player.original_deck]; available_skills = [(s_id, s_data) for s_id, s_data in self.all_skills.items() if s_data["name"] not in learned_card_names]
        if not available_skills: print("\nอาจารย์: \"ดูเหมือนเจ้าจะเรียนรู้วิชาทั้งหมดของข้าไปแล้ว จงนำไปใช้ให้ดีเถิด\""); input("\nกด Enter เพื่อกลับ..."); self.advance_time(); return
        while True:
            print("\n--- วิชาที่มีให้เรียน ---")
            for i, (s_id, s_data) in enumerate(available_skills, 1): print(f"{i}. {s_data['name']} ({s_data['desc']}) - ค่าเล่าเรียน {s_data['price']} มง")
            print("0. ข้ายังไม่พร้อม"); choice = input("เลือกวิชาที่จะเรียน: ")
            if not choice.isdigit(): continue
            choice = int(choice)
            if choice == 0: break
            if 1 <= choice <= len(available_skills):
                s_id, s_data = available_skills[choice-1]
                if self.player.money >= s_data['price']:
                    self.player.money -= s_data['price']; new_card = Card(s_data['name'], s_data['type'], s_data['value'], s_data['desc']); self.player.original_deck.append(new_card); print(f"\nคุณได้เรียนรู้วิชา '{s_data['name']}'!"); print("การ์ดใบใหม่ได้ถูกเพิ่มเข้าไปในกองการ์ดของคุณแล้ว"); time.sleep(2.5); break
                else: print("\nเงินของคุณไม่พอสำหรับค่าเล่าเรียน..."); time.sleep(1.5)
        self.advance_time()

    def talk_to_npc_phase(self):
        clear_screen(); loc_type = self.all_locations[self.player.current_location_id]["type"]; dialogue = get_dialogue(loc_type); print("คุณเดินเข้าไปพูดคุยกับชาวบ้านคนหนึ่ง..."); time.sleep(1); typewriter_print(f"ชาวบ้าน: \"{dialogue}\""); self.advance_time()
        if random.random() < 0.3:
            available_quests = [ q_id for q_id, q_data in self.all_quests.items() if loc_type in q_data["giver_type"] and q_id not in self.player.active_quests and q_id not in self.player.completed_quests ]
            if available_quests:
                quest_id = random.choice(available_quests); quest = self.all_quests[quest_id]; print("\nดูเหมือนว่าเขามีเรื่องเดือดร้อน..."); time.sleep(1); typewriter_print(f"ชาวบ้าน: \"เอ่อ... ท่านซามูไร คือว่า... {quest['description']}\"")
                choice = input("\nคุณจะรับภารกิจนี้หรือไม่? (y/n): ").lower()
                if choice == 'y': self.player.active_quests[quest_id] = { "title": quest["title"], "objective": quest["objective"], "reward": quest["reward"], "progress": 0 }; print(f"\nคุณรับภารกิจ: {quest['title']}")
                else: print("\nคุณปฏิเสธความช่วยเหลือในครั้งนี้")
        input("\nกด Enter เพื่อกลับ...")

    def view_quests_phase(self):
        clear_screen(); print("--- ภารกิจที่กำลังทำ ---")
        if not self.player.active_quests: print("ยังไม่มีภารกิจที่รับไว้")
        else:
            for q_id, quest in self.player.active_quests.items():
                obj = quest.get('objective', {}); print(f"- {quest.get('title','N/A')} ({quest.get('progress',0)}/{obj.get('count',1)} {obj.get('target','N/A')})")
        input("\nกด Enter เพื่อกลับ...")

    def inn_phase(self):
        clear_screen(); print("--- โรงเตี๊ยม ---"); rep = self.player.reputation.get(self.all_locations[self.player.current_location_id]['name'], 0); cost = max(0, 10 - rep // 10); print(f"เจ้าของ: \"ยินดีต้อนรับท่านซามูไร ค่าที่พักคืนนี้ {cost} มง ท่านจะพักหรือไม่?\"")
        choice = input("(y/n): ").lower()
        if choice == 'y':
            if self.player.money >= cost:
                self.player.money -= cost; self.player.hp = self.player.max_hp; self.player.reputation[self.all_locations[self.player.current_location_id]['name']] = rep + 1
                while self.time["segment"] != "เช้า": self.advance_time()
                self.advance_time(); print("\nคุณได้พักผ่อนอย่างเต็มที่... เช้าวันใหม่ได้เริ่มขึ้นแล้ว")
            else: print("\nเงินของคุณไม่พอสำหรับค่าที่พัก...")
        time.sleep(2)
    
    def traveling_phase(self):
        clear_screen(); print("คุณกำลังเดินทางบนเส้นทางสายเปลี่ยว..."); self.advance_time(); time.sleep(2); roll = random.randint(1, 100); current_region_type = self.all_regions[self.player.current_region_id]['type']
        if roll <= 60 and current_region_type in self.enemies_by_region_type:
            enemy_id = random.choice(self.enemies_by_region_type[current_region_type]); enemy_base_data = self.all_enemies_data[enemy_id]; card_pool = self.enemy_card_pools[enemy_base_data["card_pool_tag"]]; num_enemies = random.randint(1, 2)
            self.current_enemies = []
            for _ in range(num_enemies):
                init_data = {k:v for k,v in enemy_base_data.items() if k not in ['name', 'region_types', 'card_pool_tag', 'drop_table']}; new_enemy = Enemy(enemy_id=enemy_id, name=enemy_base_data['name'], **init_data, card_pool=card_pool); self.current_enemies.append(new_enemy)
            print(f"\n!!! คุณถูกลอบโจมตีโดย {self.current_enemies[0].name} {num_enemies} ตัว !!!"); time.sleep(2); self.game_state = 'COMBAT'
        elif roll <= 65: self.meet_traveler_phase()
        elif roll <= 68: self.found_item_event_phase()
        elif roll <= 74: self.crossroads_event_phase()
        else: print("\nการเดินทางครั้งนี้ปลอดภัยดี"); time.sleep(2); self.safe_travel_to_random_location()

    def safe_travel_to_random_location(self):
        possible_locations = [l_id for l_id in self.all_locations if l_id != self.player.current_location_id]
        if possible_locations:
            new_location_id = random.choice(possible_locations); self.player.current_location_id = new_location_id; self.player.current_region_id = self.all_locations[new_location_id]['region_id']; loc_name = self.all_locations[self.player.current_location_id]['name']; print(f"คุณเดินทางมาถึง {loc_name}")
        else: print("ไม่มีที่อื่นให้ไปแล้ว...")
        time.sleep(2); self.game_state = 'LOCATION_HUB'

    def crossroads_event_phase(self):
        clear_screen(); print("คุณมาถึงทางแยกบนเส้นทาง..."); time.sleep(1); current_region_id = self.player.current_region_id; possible_destinations = [r_id for r_id in self.all_regions if r_id != current_region_id]
        if not possible_destinations: print("แต่ดูเหมือนทุกเส้นทางจะวนกลับไปที่เดิม..."); time.sleep(2); self.game_state = 'LOCATION_HUB'; return
        choices = random.sample(possible_destinations, min(2, len(possible_destinations))); print("เส้นทางข้างหน้าแยกออกเป็นสองทาง:");
        for i, region_id in enumerate(choices, 1): region_data = self.all_regions[region_id]; print(f"{i}. เส้นทางสู่ {region_data['name']} ({region_data['desc']})")
        print("0. ตั้งแคมป์พักที่นี่ก่อน"); choice = input("เลือกเส้นทาง: ")
        if choice.isdigit() and 1 <= int(choice) <= len(choices):
            chosen_region_id = choices[int(choice)-1]; self.player.current_region_id = chosen_region_id; print(f"\nคุณเลือกเดินทางเข้าสู่ {self.all_regions[chosen_region_id]['name']}..."); self.advance_time(); time.sleep(2)
            possible_locations = [l_id for l_id, l_data in self.all_locations.items() if l_data["region_id"] == chosen_region_id]
            if possible_locations:
                self.player.current_location_id = random.choice(possible_locations); loc_name = self.all_locations[self.player.current_location_id]['name']; print(f"การเดินทางปลอดภัยดี คุณมาถึง {loc_name}"); time.sleep(2)
            else: print("แต่กลับไม่พบสถานที่ใดๆ ในภูมิภาคนี้..."); time.sleep(2)
            self.game_state = 'LOCATION_HUB'
        else: print("คุณตัดสินใจตั้งแคมป์เพื่อพักเอาแรง..."); heal_amount = random.randint(5, 15); self.player.hp = min(self.player.max_hp, self.player.hp + heal_amount); print(f"คุณฟื้นฟู HP {heal_amount} หน่วย"); self.advance_time(2); time.sleep(2); self.game_state = 'LOCATION_HUB'
        
    def meet_traveler_phase(self):
        clear_screen(); traveler_types = ["พ่อค้าเร่", "นักบวชพเนจร", "ทหารส่งสาส์น", "โรนินอีกคน"]; traveler = random.choice(traveler_types); print(f"ระหว่างทาง คุณได้พบกับ{traveler}คนหนึ่ง..."); time.sleep(1)
        print("\nคุณจะทำอย่างไร?"); print("1. เข้าไปทักทาย"); print("2. เดินทางต่อไปอย่างระมัดระวัง"); choice = input("เลือก: ")
        if choice == '1': dialogue = get_dialogue("general"); print(f"\n{traveler}: \"{dialogue}\""); time.sleep(2)
        else: print("\nคุณเลือกที่จะไม่เข้าไปยุ่งและเดินทางต่อไป"); time.sleep(2)
        self.safe_travel_to_random_location()

    def found_item_event_phase(self):
        clear_screen(); descriptions = ["คุณสังเกตเห็นถุงผ้าเก่าๆ ตกอยู่ข้างทาง...", "มีบางอย่างสะท้อนแสงอยู่ใต้พุ่มไม้...", "คุณเห็นหีบไม้เล็กๆ ใบหนึ่งถูกทิ้งไว้ใต้ต้นไม้..."]; print(random.choice(descriptions)); time.sleep(1)
        print("\nคุณจะทำอย่างไร?"); print("1. เข้าไปตรวจสอบ"); print("2. ไม่สนใจและเดินทางต่อไป"); choice = input("เลือก: ")
        if choice == '1':
            if random.random() < (2/3):
                damage = random.randint(5, 15); print(f"\nกับดัก! คุณได้รับบาดเจ็บ เสีย HP ไป {damage} หน่วย!"); self.player.take_damage(damage); time.sleep(2)
                if not self.player.is_alive(): self.cause_of_death = "เสียชีวิตเพราะกับดักข้างทาง"; self.game_state = 'GAME_OVER'; return
            else: money_found = random.randint(10, 30); print(f"\nโชคดี! คุณพบเงิน {money_found} มง!"); self.player.money += money_found; time.sleep(2)
        else: print("\nคุณตัดสินใจที่จะไม่เสี่ยงและเดินทางต่อไป"); time.sleep(2)
        self.safe_travel_to_random_location()
        
    def combat_phase(self):
        self.player.deck = list(self.player.original_deck); random.shuffle(self.player.deck); self.player.discard = []; self.player.hand = []; self.player.draw_hand()
        for enemy in self.current_enemies: enemy.draw_hand()
        turn = 1
        while any(e.is_alive() for e in self.current_enemies) and self.player.is_alive():
            clear_screen(); print(f"--- การต่อสู้ | เทิร์นที่ {turn} ---")
            for i, enemy in enumerate(self.current_enemies): status = "HP: " + str(enemy.hp) if enemy.is_alive() else "ตายแล้ว"; print(f"{i+1}. {enemy.name} ({status})")
            print(f"\nคุณ: HP {self.player.hp}/{self.player.max_hp}");
            if self.player.defense_bonus > 0: print(f"   └ ตั้งรับ: {self.player.defense_bonus}")
            self.player_turn()
            if not any(e.is_alive() for e in self.current_enemies): break
            for enemy in self.current_enemies:
                if enemy.is_alive() and self.player.is_alive():
                    self.enemy_turn(enemy)
                    if not self.player.is_alive(): self.cause_of_death = f"พ่ายแพ้ในคมดาบของ {enemy.name}"; break
            turn += 1; input("\nกด Enter เพื่อเข้าสู่เทิร์นถัดไป...")
        clear_screen()
        if self.player.is_alive():
            print("\n--- คุณได้รับชัยชนะ! ---"); money_gain = sum(random.randint(5, 15) for _ in self.current_enemies); self.player.money += money_gain; print(f"ได้รับเงิน {money_gain} มง")
            print("\n--- ไอเทมที่ได้รับ ---"); item_dropped = False
            for enemy in self.current_enemies:
                enemy_data = self.all_enemies_data.get(enemy.enemy_id)
                if not enemy_data or "drop_table" not in enemy_data: continue
                for drop in enemy_data["drop_table"]:
                    if random.random() < drop["chance"]:
                        item_id = drop["item_id"]; item_info = self.all_items.get(item_id)
                        if not item_info: continue
                        quantity = random.randint(drop["quantity"][0], drop["quantity"][1]); item_name = item_info["name"]
                        self.player.item_inventory[item_name] = self.player.item_inventory.get(item_name, 0) + quantity
                        print(f"{enemy.name} ดรอป {item_name} x{quantity}!"); item_dropped = True
            if not item_dropped: print("- ไม่ได้รับไอเทมใดๆ -")
            killed_enemies = [e.name for e in self.current_enemies]
            for q_id, quest in list(self.player.active_quests.items()):
                if quest.get("objective", {}).get("type") == "kill":
                    target_name = quest["objective"]["target"]
                    kill_count = sum(1 for name in killed_enemies if name == target_name)
                    if kill_count > 0: quest["progress"] += kill_count; print(f"ความคืบหน้าภารกิจ '{quest['title']}': {quest['progress']}/{quest['objective']['count']}")
            self.game_state = 'LOCATION_HUB'
        else: print("\nคุณพ่ายแพ้..."); self.game_state = 'GAME_OVER'
        input("กด Enter เพื่อดำเนินการต่อ...")

    def player_turn(self):
        print("\n--- ตาของคุณ ---"); used_cards_this_turn = 0
        while used_cards_this_turn < 2 and self.player.is_alive() and any(e.is_alive() for e in self.current_enemies):
            print("\nการ์ดในมือ:"); [print(f"  {i+1}. [{card.type}] {card.name} ({card.value}) - {card.desc}") for i, card in enumerate(self.player.hand)]; print("  0. จบเทิร์น")
            choice = input("เลือกการ์ด (หรือ 0 เพื่อจบเทิร์น): ")
            if not choice.isdigit(): continue
            choice = int(choice)
            if choice == 0: break
            if not (1 <= choice <= len(self.player.hand)): print("เลือกไม่ถูกต้อง"); continue
            card = self.player.hand.pop(choice - 1)
            if card.type == "ATTACK":
                target_choice = input(f"เลือกเป้าหมาย (1-{len(self.current_enemies)}): ")
                if target_choice.isdigit():
                    target_idx = int(target_choice) - 1
                    if 0 <= target_idx < len(self.current_enemies) and self.current_enemies[target_idx].is_alive():
                        target = self.current_enemies[target_idx]; damage = self.player.get_total_atk() + card.value; actual_damage = target.take_damage(damage); print(f"คุณใช้ '{card.name}' โจมตี {target.name} ทำความเสียหาย {actual_damage}!")
                    else: print("เป้าหมายไม่ถูกต้อง"); self.player.hand.insert(choice - 1, card); continue
                else: print("เลือกเป้าหมายไม่ถูกต้อง"); self.player.hand.insert(choice - 1, card); continue
            elif card.type == "DEFEND": self.player.defense_bonus += card.value; print(f"คุณใช้ '{card.name}' ตั้งรับ {card.value} แต้ม!")
            self.player.discard.append(card); used_cards_this_turn += 1; time.sleep(1)
        self.player.draw_hand()

    def enemy_turn(self, enemy):
        print(f"\n--- ตาของ {enemy.name} ---"); time.sleep(1); damage = enemy.atk + random.randint(0, 3); actual_damage = self.player.take_damage(damage); print(f"{enemy.name} โจมตี! คุณได้รับความเสียหาย {actual_damage} แต้ม!"); time.sleep(1)

    def game_over_phase(self):
        clear_screen(); print("--- ตำนานของคุณได้จบสิ้นลงแล้ว ---"); time.sleep(2); death_by_enemy_type = "Unknown"
        if "โจรป่า" in self.cause_of_death: death_by_enemy_type = "Bandit"
        elif "หมาป่า" in self.cause_of_death: death_by_enemy_type = "Wolf"
        elif "โรนิน" in self.cause_of_death: death_by_enemy_type = "Ronin"
        elif "กับดัก" in self.cause_of_death: death_by_enemy_type = "Trap"
        end_stories = { "Bandit": [f"สาเหตุ: {self.cause_of_death}", "ร่างกายของคุณถูกทิ้งไว้ข้างทางอย่างไร้ค่า", "ข้าวของทุกชิ้นถูกปล้นไปจนหมดสิ้น", "ชื่อของคุณ... ถูกลืมเลือนไปกับสายลม ราวกับไม่เคยมีตัวตน"], "Wolf": [f"สาเหตุ: {self.cause_of_death}", "คุณพ่ายแพ้ให้แก่สัญชาตญาณดิบของสัตว์ร้าย", "ร่างกายของคุณกลายเป็นอาหารให้กับฝูงของมัน", "ไม่มีใครรู้ถึงชะตากรรมของคุณ มีเพียงเสียงหอนอันเยือกเย็นในยามค่ำคืน"], "Ronin": [f"สาเหตุ: {self.cause_of_death}", "เป็นการดวลที่สมศักดิ์ศรี... แต่คุณคือผู้ที่ช้ากว่าเพียงก้าวเดียว", "ดาบของคุณถูกปักไว้บนพื้นดินเพื่อเป็นเกียรติแก่นักสู้", "เรื่องราวของคุณกลายเป็นข่าวลือในโรงเตี๊ยมอยู่พักหนึ่ง... ก่อนจะเลือนหายไป"], "Trap": [f"สาเหตุ: {self.cause_of_death}", "ความประมาทเพียงชั่วครู่ได้นำมาซึ่งจุดจบ", "ร่างกายของคุณนอนแน่นิ่งอยู่ข้างทางจนกระทั่งมีคนมาพบในอีกหลายวันต่อมา", "เป็นอีกหนึ่งบทเรียนที่ธรรมชาติสอนให้กับนักเดินทางผู้ไม่ระวังตัว"] }
        story_lines = end_stories.get(death_by_enemy_type, [f"สาเหตุ: {self.cause_of_death}", "คุณล้มลงกลางทาง...", "ไม่มีใครบันทึกเรื่องราว ไม่มีใครจดจำการเดินทางครั้งนี้"])
        for line in story_lines: typewriter_print(f"\n{line}"); time.sleep(2)
        print("\n\nGAME OVER")

if __name__ == "__main__":
    game = Game()
    game.run()

