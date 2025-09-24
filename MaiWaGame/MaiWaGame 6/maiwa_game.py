# -*- coding: utf-8 -*-
import os
import sys
import json
import random
import time
import textwrap

# --- คาถาแก้ตัวหนังสือสี่เหลี่ยม ---
# บรรทัดนี้อาจทำให้เกิดปัญหาในบางระบบ จะย้ายไปอยู่ใน main แทน
# sys.stdout.reconfigure(encoding='utf-8')

# --- ระบบนำทางสำหรับ .exe ---
def get_base_path():
    """ หา Path หลักของโปรแกรม ไม่ว่าจะรันจาก .py หรือ .exe """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# --- นำเข้าข้อมูลและคลาสจากไฟล์อื่น ---
try:
    from game_classes import Card, Weapon, Armor, Player, Enemy
    from npc_dialogue import get_random_npc_dialogue
    from quest_data import get_quests
    from weapon_data import get_weapons
    from skill_data import get_skills
    from item_data import get_items
    from location_data import get_regions, get_locations
    from enemy_data import get_enemies
    from armor_data import get_armors
    from boss_data import get_bosses
    from crafting_data import get_recipes
except ImportError as e:
    print("="*50)
    print("!!! เกิดข้อผิดพลาดในการโหลดไฟล์เกม !!!")
    print(f"ไม่พบไฟล์ที่จำเป็น: {e.name}")
    print("กรุณาตรวจสอบให้แน่ใจว่าไฟล์ .py ทั้งหมดอยู่ในโฟลเดอร์เดียวกันกับเกม")
    print("="*50)
    input("กด Enter เพื่อปิดโปรแกรม...")
    sys.exit()


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
        self.player = None
        self.game_state = 'MAIN_MENU'
        self.is_running = True
        self.cause_of_death = "ความเหนื่อยล้าจากการเดินทาง"
        self.current_enemies = []
        self.base_path = get_base_path()
        self.boss_encounter_cooldown = 0
        self.setup_game_data()

    def setup_game_data(self):
        self.all_player_cards = [ Card("ฟันดาบ", "ATTACK", 5, "โจมตีปกติ"), Card("ตั้งรับ", "DEFEND", 5, "ป้องกันความเสียหาย"), Card("จู่โจมเร็ว", "ATTACK", 3, "โจมตีอย่างรวดเร็ว"), Card("แทง", "ATTACK", 7, "โจมตีจุดตาย"), Card("ปัดป้อง", "DEFEND", 7, "ป้องกันอย่างสมบูรณ์") ]
        self.all_quests = get_quests()
        self.all_weapons = get_weapons()
        self.all_skills = get_skills()
        self.all_items = get_items()
        self.all_regions = get_regions()
        self.all_locations = get_locations()
        self.all_enemies_data = get_enemies()
        self.all_armors = get_armors()
        self.all_bosses = get_bosses()
        self.all_recipes = get_recipes()
        self.bosses_by_region = {}
        for b_id, b_data in self.all_bosses.items():
            for region_type in b_data.get("region_types", []):
                if region_type not in self.bosses_by_region:
                    self.bosses_by_region[region_type] = []
                self.bosses_by_region[region_type].append(b_id)
        self.enemies_by_region_type = {}
        for e_id, e_data in self.all_enemies_data.items():
            for region_type in e_data["region_types"]:
                if region_type not in self.enemies_by_region_type:
                    self.enemies_by_region_type[region_type] = []
                self.enemies_by_region_type[region_type].append(e_id)
        self.time = {"day": 1, "month": 1, "year": 1470, "segment": "เช้า"}
        self.time_segments = ["เช้า", "กลางวัน", "เย็น", "กลางคืน"]
        self.service_hours = {"โรงตีดาบ": ["เช้า", "กลางวัน"], "ตลาด": ["เช้า", "กลางวัน"], "ร้านค้าเล็กๆ": ["เช้า", "กลางวัน", "เย็น"], "โรงฝึก": ["เช้า", "กลางวัน"], "สร้างของ": ["เช้า", "กลางวัน", "เย็น"]}

    def advance_time(self, segments=1):
        for _ in range(segments):
            day_changed = False
            current_index = self.time_segments.index(self.time["segment"])
            if current_index == 3:
                self.time["segment"] = "เช้า"
                self.time["day"] += 1
                day_changed = True
                if self.time["day"] > 30:
                    self.time["day"] = 1
                    self.time["month"] += 1
                    if self.time["month"] > 12:
                        self.time["month"] = 1
                        self.time["year"] += 1
            else:
                self.time["segment"] = self.time_segments[current_index + 1]
            if day_changed and self.boss_encounter_cooldown > 0:
                self.boss_encounter_cooldown -= 1


    def new_game(self):
        self.player = Player("โรนิน")
        plains_region_ids = [r_id for r_id, r_data in self.all_regions.items() if r_data["type"] == "plains"]
        self.player.current_region_id = random.choice(plains_region_ids) if plains_region_ids else list(self.all_regions.keys())[0]
        possible_start_locations = [l_id for l_id, l_data in self.all_locations.items() if l_data["region_id"] == self.player.current_region_id]
        self.player.current_location_id = random.choice(possible_start_locations) if possible_start_locations else list(self.all_locations.keys())[0]
        self.player.build_deck(self.all_player_cards, 10)
        self.player.known_recipes = ["C001", "C011", "C021"] # Start with some basic recipes
        self.time = {"day": random.randint(1,28), "month": random.randint(1,12), "year": 1470, "segment": "เช้า"}
        self.game_state = 'LOCATION_HUB'
        loc_name = self.all_locations[self.player.current_location_id]['name']
        print(f"การเดินทางของคุณเริ่มต้นที่... {loc_name}")
        time.sleep(2)

    def save_game(self):
        if not self.player: return
        save_data = {'player': self.player.to_dict(), 'time': self.time, 'boss_encounter_cooldown': self.boss_encounter_cooldown}
        save_file_path = os.path.join(self.base_path, 'savegame.json')
        with open(save_file_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=4)
        print("เกมถูกบันทึกเรียบร้อยแล้ว")

    def load_game(self):
        try:
            save_file_path = os.path.join(self.base_path, 'savegame.json')
            with open(save_file_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
                self.player = Player.from_dict(save_data['player'])
                self.time = save_data['time']
                self.boss_encounter_cooldown = save_data.get('boss_encounter_cooldown', 0)
                self.game_state = 'LOCATION_HUB'
                print("โหลดเกมสำเร็จ!")
                time.sleep(1.5)
                return True
        except (FileNotFoundError, json.JSONDecodeError):
            print("ไม่พบไฟล์เซฟ หรือไฟล์เสียหาย...")
            input("\nกด Enter เพื่อดำเนินการต่อ...")
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
                elif self.game_state == 'GAME_OVER': self.game_over_phase(); # Don't stop running, go back to menu
        except Exception as e:
            clear_screen()
            print(f"\n\n---!!! เกิดข้อผิดพลาดที่ไม่คาดคิด !!!---\n")
            print(f"ประเภท Error: {type(e).__name__}")
            print(f"ข้อความ Error: {e}")
            print("\nเกมจะปิดตัวลง กรุณาคัดลอกข้อความด้านบนนี้เพื่อแจ้งให้ผู้พัฒนาทราบ")
            import traceback
            traceback.print_exc()
            input("\nกด Enter เพื่อปิดโปรแกรม...")
            self.is_running = False
    
    def main_menu_phase(self):
        clear_screen()
        print("ยินดีต้อนรับสู่ MaiWa v6.0 BETA (PC)\n")
        print("1. เริ่มเกมใหม่")
        print("2. โหลดเกม")
        print("3. ออกจากเกม")
        choice = input("เลือก: ")
        if choice == '1': self.show_intro(); self.new_game()
        elif choice == '2':
            if not self.load_game(): self.main_menu_phase()
        elif choice == '3': self.is_running = False

    def location_hub_phase(self):
        clear_screen()
        loc_id = self.player.current_location_id
        loc_data = self.all_locations[loc_id]
        loc_name = loc_data["name"]
        loc_type = loc_data["type"]
        
        # --- Quest Completion ---
        completed_this_turn = []
        for q_id, quest in list(self.player.active_quests.items()):
            if quest.get("progress", 0) >= quest.get("objective", {}).get("count", 1):
                print(f"--- ภารกิจสำเร็จ: {quest['title']} ---")
                reward = quest.get("reward", {})
                self.player.money += reward.get("money", 0)
                self.player.reputation[loc_name] = self.player.reputation.get(loc_name, 0) + reward.get("reputation", 0)
                print(f"ได้รับเงิน {reward.get('money', 0)} มง และชื่อเสียง {reward.get('reputation', 0)} แต้ม")
                
                # Item Reward
                if "item" in reward:
                    item_id = reward["item"]["id"]
                    item_qty = reward["item"]["quantity"]
                    item_info = self.all_items.get(item_id)
                    if item_info:
                        self.player.add_item(item_info["name"], item_qty, item_id)
                        print(f"ได้รับไอเทม: {item_info['name']} x{item_qty}")

                self.player.completed_quests.append(q_id)
                completed_this_turn.append(q_id)
                time.sleep(2.5)

        for q_id in completed_this_turn:
            del self.player.active_quests[q_id]

        print(f"--- {loc_name} ({loc_type}) ---")
        print(f"วันที่ {self.time['day']}/{self.time['month']}/{self.time['year']} | เวลา: {self.time['segment']}")
        print(f"Lvl: {self.player.level} | XP: {self.player.xp}/{self.player.xp_to_next_level}")
        print(f"HP: {self.player.hp}/{self.player.max_hp} | ATK: {self.player.get_total_atk()} | DEF: {self.player.get_total_def()} | เงิน: {self.player.money} มง")
        equipped_weapon_name = self.player.equipped_weapon.name if self.player.equipped_weapon else "มือเปล่า"
        print(f"อาวุธที่ใช้: {equipped_weapon_name}")
        print("-" * 30)
        options = ["ออกเดินทาง", "ดูสถานะและอัปเกรด", "ดูภารกิจ", "จัดการยุทโธปกรณ์", "ดูไอเทมในย่าม"]
        
        if any(service in loc_data.get("services", []) for service in ["โรงตีดาบ", "ตลาด", "ร้านค้าเล็กๆ"]):
            options.append("สร้างของ")
            
        for service in loc_data.get("services", []):
            if service not in options:
                is_open = self.time["segment"] in self.service_hours.get(service, self.time_segments)
                options.append(f"{service} {'(ปิด)' if not is_open else ''}")

        options.extend(["บันทึกเกม", "กลับสู่เมนูหลัก"])
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        choice = input("เลือก: ")

        if choice == '456': # Cheat Code
            self.cheat_menu_phase()
            return

        if choice.isdigit() and 1 <= int(choice) <= len(options):
            action_full = options[int(choice)-1]
            action = action_full.split(" ")[0]
            
            if "(ปิด)" in action_full:
                print(f"'{action}' ปิดให้บริการในเวลานี้")
                input("\nกด Enter เพื่อดำเนินการต่อ...")
                return

            if action == "ออกเดินทาง": self.game_state = 'TRAVELING'
            elif action == "ดูสถานะและอัปเกรด": self.status_phase()
            elif action == "พูดคุยกับชาวบ้าน": self.talk_to_npc_phase()
            elif action == "ดูภารกิจ": self.view_quests_phase()
            elif action == "ดูไอเทมในย่าม": self.inventory_phase()
            elif action == "จัดการยุทโธปกรณ์": self.equipment_phase()
            elif action == "โรงเตี๊ยม": self.inn_phase()
            elif action == "สร้างของ": self.crafting_phase()
            elif action in ["ร้านค้าเล็กๆ", "โรงตีดาบ", "ตลาด"]: self.shop_phase(action)
            elif action == "โรงฝึก": self.dojo_phase()
            elif action == "บันทึกเกม": self.save_game(); time.sleep(1)
            elif action == "กลับสู่เมนูหลัก": self.game_state = 'MAIN_MENU'
            else:
                print(f"ยังไม่เปิดให้บริการ '{action}' ในตอนนี้")
                input("\nกด Enter เพื่อดำเนินการต่อ...")

    def inventory_phase(self):
        while True:
            clear_screen(); print("--- ไอเทมในย่าม ---")
            if not self.player.item_inventory:
                print("- ย่ามของคุณว่างเปล่า -")
                input("\nกด Enter เพื่อกลับ...")
                break
            
            item_list = sorted(list(self.player.item_inventory.items()))
            
            for i, (item_name, data) in enumerate(item_list, 1):
                item_desc = self.all_items.get(data['id'], {}).get('desc', 'ไม่มีข้อมูล')
                print(f"{i}. {item_name} x{data['quantity']} - {item_desc}")

            print("\n0. กลับ"); choice = input("เลือกไอเทมที่จะใช้ (หรือ 0 เพื่อกลับ): ")
            if choice == '0': break
            if choice.isdigit() and 1 <= int(choice) <= len(item_list):
                item_name_to_use = item_list[int(choice)-1][0]
                self.use_item(item_name_to_use) # This now only handles out-of-combat items
                input("\nกด Enter เพื่อดำเนินการต่อ...")

    def use_item(self, item_name, in_combat=False):
        item_id = self.player.item_inventory.get(item_name, {}).get('id')
        if not item_id: return False
        item_data = self.all_items.get(item_id, {})
        
        item_type = item_data.get("type")
        item_value = item_data.get("value", 0)

        if in_combat:
            return self.use_item_in_combat(item_data)
        else: # Out of combat
            if item_type == "HEAL":
                self.player.hp = min(self.player.max_hp, self.player.hp + item_value)
                print(f"\nคุณใช้ {item_name} และฟื้นฟู HP {item_value} หน่วย!")
            elif item_type == "CURE":
                 self.player.status_effects = {}
                 print(f"\nคุณใช้ {item_name} และรักษาอาการผิดปกติทั้งหมด!")
            elif item_type in ["BUFF_ATK", "BUFF_DEF", "UTILITY"]:
                if 'atk' in item_data.get('name', '').lower(): self.player.next_fight_buffs['atk'] += item_value
                elif 'def' in item_data.get('name', '').lower(): self.player.next_fight_buffs['def'] += item_value
                else: self.player.next_fight_buffs['luck'] += item_value # Assuming UTILITY buffs luck
                print(f"\nคุณใช้ {item_name}! การต่อสู้ครั้งต่อไปจะได้รับบัฟ!")
            else:
                print(f"\nไม่สามารถใช้ '{item_name}' นอกการต่อสู้ได้")
                return False

        self.player.remove_item(item_name)
        return True

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
        while True:
            clear_screen(); print(f"--- เลือกอุปกรณ์สำหรับช่อง '{slot_type.capitalize()}' ---")
            if slot_type == 'weapon': inventory = self.player.weapon_inventory; item_list = [(item, f"ATK +{item.bonus_atk}") for item in inventory]
            else: inventory = self.player.armor_inventory; item_list = [(item, f"DEF +{item.bonus_def}") for item in inventory if item.slot == slot_type]
            
            if not item_list:
                print("- ไม่มีอุปกรณ์ประเภทนี้ในคลัง -")
                input("\nกด Enter เพื่อกลับ...")
                break

            for i, (item, stat_text) in enumerate(item_list, 1): print(f"{i}. {item.name} ({stat_text})")
            print("\n99. ถอดอุปกรณ์"); print("0. กลับ"); choice = input("เลือก: ")
            
            if choice.isdigit():
                choice = int(choice)
                if choice == 0: break
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
        potential_weapons = [item for item_id, item in self.all_weapons.items() if shop_type in item.get("sale_locations", [])]
        potential_armors = [item for item_id, item in self.all_armors.items() if shop_type in item.get("sale_locations", [])]
        potential_items = [item for item_id, item in self.all_items.items() if shop_type in item.get("sale_locations", [])]
        daily_stock = {'อาวุธ': random.sample(potential_weapons, min(5, len(potential_weapons))), 'ชุดเกราะ': random.sample(potential_armors, min(5, len(potential_armors))), 'ไอเทม': random.sample(potential_items, min(5, len(potential_items)))}
        while True:
            clear_screen(); print(f"--- {shop_type} ---"); print(f"เงินของคุณ: {self.player.money} มง"); print("-" * 30); print("\nพ่อค้า: \"สนใจดูสินค้าประเภทไหนดี?\"")
            categories = ["อาวุธ", "ชุดเกราะ", "ไอเทม"]
            for i, cat in enumerate(categories, 1):
                if daily_stock[cat]: print(f"{i}. ดูสินค้าประเภท{cat} ({len(daily_stock[cat])} ชิ้น)")
            print("0. ออกจากร้าน"); cat_choice = input("เลือก: ")
            if cat_choice == '0': break
            if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
                chosen_category = categories[int(cat_choice)-1]; self.browse_and_buy(chosen_category, daily_stock[chosen_category])
        self.advance_time()

    def browse_and_buy(self, category_name, stock):
        item_id_map = {v['name']: k for k, v in list(self.all_weapons.items()) + list(self.all_armors.items()) + list(self.all_items.items())}
        while True:
            clear_screen(); print(f"--- สินค้าประเภท{category_name} ---"); print(f"เงินของคุณ: {self.player.money} มง"); print("-" * 30)
            if not stock:
                print("\n- ไม่มีสินค้าประเภทนี้วางขายในวันนี้ -")
                input("\nกด Enter เพื่อกลับ...")
                break
            for i, item_data in enumerate(stock, 1):
                if category_name == 'อาวุธ': print(f"{i}. {item_data['name']} (ATK +{item_data['bonus_atk']}) - ราคา {item_data['price']} มง")
                elif category_name == 'ชุดเกราะ': print(f"{i}. {item_data['name']} (DEF +{item_data['bonus_def']}) - ราคา {item_data['price']} มง")
                elif category_name == 'ไอเทม': print(f"{i}. {item_data['name']} ({item_data['desc']}) - ราคา {item_data['price']} มง")
            print("0. กลับไปหน้าร้าน"); choice = input("เลือกสินค้าที่จะซื้อ: ")
            if not choice.isdigit(): continue
            choice = int(choice)
            if choice == 0: break
            if 1 <= choice <= len(stock):
                item_data = stock[choice-1]
                if self.player.money >= item_data['price']:
                    self.player.money -= item_data['price']
                    item_id = item_id_map.get(item_data['name'])
                    if category_name == 'อาวุธ': new_weapon = Weapon(item_id, item_data['name'], item_data['bonus_atk'], item_data['price']); self.player.weapon_inventory.append(new_weapon)
                    elif category_name == 'ชุดเกราะ': new_armor = Armor(item_id, item_data['name'], item_data['slot'], item_data['bonus_def'], item_data['price']); self.player.armor_inventory.append(new_armor)
                    elif category_name == 'ไอเทม': self.player.add_item(item_data['name'], 1, item_id)
                    print(f"\nคุณได้ซื้อ {item_data['name']}!"); time.sleep(1.5); break
                else:
                    print("\nเงินของคุณไม่พอ...")
                    input("\nกด Enter เพื่อดำเนินการต่อ...")

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
                else:
                    print("\nเงินของคุณไม่พอสำหรับค่าเล่าเรียน...")
                    input("\nกด Enter เพื่อดำเนินการต่อ...")
        self.advance_time()

    def crafting_phase(self):
        while True:
            clear_screen()
            print("--- โต๊ะสร้างของ ---")
            print("พิมพ์เขียวที่คุณรู้จัก:")
            
            known_recipes = sorted(self.player.known_recipes, key=lambda r_id: self.all_recipes.get(r_id, {}).get('name', ''))

            if not known_recipes:
                print("- คุณยังไม่รู้จักพิมพ์เขียวใดๆ -")
            else:
                for i, recipe_id in enumerate(known_recipes, 1):
                    recipe = self.all_recipes.get(recipe_id)
                    if not recipe: continue
                    
                    can_craft = True
                    material_str_parts = []
                    for mat_id, qty_needed in recipe['materials'].items():
                        mat_info = self.all_items.get(mat_id)
                        if not mat_info: 
                            can_craft = False; break
                        mat_name = mat_info['name']
                        qty_owned = self.player.item_inventory.get(mat_name, {}).get('quantity', 0)
                        if qty_owned < qty_needed:
                            can_craft = False
                        material_str_parts.append(f"{mat_name} ({qty_owned}/{qty_needed})")
                    
                    material_str = ", ".join(material_str_parts)
                    availability = "" if can_craft else "(วัตถุดิบไม่พอ)"
                    
                    print(f"{i}. {recipe['name']} -> {self.get_item_name_from_id(recipe['result'])} - ต้องการ: {material_str} {availability}")

            print("\n0. กลับ")
            choice = input("เลือกพิมพ์เขียวที่จะสร้าง: ")
            if not choice.isdigit() or choice == '0':
                break
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(known_recipes):
                recipe_id = known_recipes[choice_idx]
                recipe = self.all_recipes[recipe_id]
                
                can_craft = True
                materials_to_consume = []
                for mat_id, qty_needed in recipe['materials'].items():
                    mat_name = self.all_items[mat_id]['name']
                    if self.player.item_inventory.get(mat_name, {}).get('quantity', 0) < qty_needed:
                        can_craft = False; break
                    materials_to_consume.append((mat_name, qty_needed))

                if can_craft:
                    for mat_name, qty_needed in materials_to_consume:
                        self.player.remove_item(mat_name, qty_needed)
                    
                    result_id = recipe['result']
                    result_type = recipe['type']
                    if result_type == 'weapon':
                        w_data = self.all_weapons[result_id]
                        new_w = Weapon(result_id, w_data['name'], w_data['bonus_atk'], w_data['price'])
                        self.player.weapon_inventory.append(new_w)
                        print(f"\nคุณสร้าง {w_data['name']} สำเร็จ!")
                    elif result_type == 'armor':
                        a_data = self.all_armors[result_id]
                        new_a = Armor(result_id, a_data['name'], a_data['slot'], a_data['bonus_def'], a_data['price'])
                        self.player.armor_inventory.append(new_a)
                        print(f"\nคุณสร้าง {a_data['name']} สำเร็จ!")
                    elif result_type == 'item':
                        i_data = self.all_items[result_id]
                        self.player.add_item(i_data['name'], 1, result_id)
                        print(f"\nคุณสร้าง {i_data['name']} สำเร็จ!")
                    
                    input("\nกด Enter เพื่อดำเนินการต่อ...")
                else:
                    print("\nวัตถุดิบไม่เพียงพอ...")
                    input("\nกด Enter เพื่อดำเนินการต่อ...")
        self.advance_time()
    
    def get_item_name_from_id(self, item_id):
        if item_id.startswith('W'): return self.all_weapons.get(item_id, {}).get('name', '???')
        if item_id.startswith('AR'): return self.all_armors.get(item_id, {}).get('name', '???')
        if item_id.startswith('I'): return self.all_items.get(item_id, {}).get('name', '???')
        return '???'

    def talk_to_npc_phase(self):
        clear_screen()
        loc_type = self.all_locations[self.player.current_location_id]["type"]
        npc_type, dialogue = get_random_npc_dialogue(loc_type)
        print(f"คุณเดินเข้าไปพูดคุยกับ{npc_type}คนหนึ่ง...")
        time.sleep(1)
        typewriter_print(f"{npc_type}: \"{dialogue}\"")
        self.advance_time()
        
        if random.random() < 0.4:
            available_quests = [ q_id for q_id, q_data in self.all_quests.items() if loc_type in q_data["giver_type"] and q_id not in self.player.active_quests and q_id not in self.player.completed_quests ]
            if available_quests:
                quest_id = random.choice(available_quests)
                quest = self.all_quests[quest_id]
                print("\nดูเหมือนว่าเขามีเรื่องเดือดร้อน...")
                time.sleep(1)
                typewriter_print(f"{npc_type}: \"เอ่อ... ท่านซามูไร คือว่า... {quest['description']}\"")
                choice = input("\nคุณจะรับภารกิจนี้หรือไม่? (y/n): ").lower()
                if choice == 'y':
                    self.player.active_quests[quest_id] = { "title": quest["title"], "objective": quest["objective"], "reward": quest["reward"], "progress": 0 }
                    print(f"\nคุณรับภารกิจ: {quest['title']}")
                else:
                    print("\nคุณปฏิเสธความช่วยเหลือในครั้งนี้")
        input("\nกด Enter เพื่อกลับ...")

    def view_quests_phase(self):
        clear_screen(); print("--- ภารกิจที่กำลังทำ ---")
        if not self.player.active_quests: print("ยังไม่มีภารกิจที่รับไว้")
        else:
            for q_id, quest in self.player.active_quests.items():
                obj = quest.get('objective', {}); print(f"- {quest.get('title','N/A')} ({quest.get('progress',0)}/{obj.get('count',1)} {obj.get('target','N/A')})")
        
        print("\n--- ภารกิจที่สำเร็จแล้ว ---")
        if not self.player.completed_quests: print("ยังไม่มี")
        else:
            for q_id in self.player.completed_quests:
                quest_title = self.all_quests.get(q_id, {}).get('title', 'N/A')
                print(f"- {quest_title} (สำเร็จ)")
        
        input("\nกด Enter เพื่อกลับ...")
    
    def status_phase(self):
        while True:
            clear_screen()
            print("--- สถานะตัวละคร ---")
            print(f"เลเวล: {self.player.level}")
            print(f"ค่าประสบการณ์ (XP): {self.player.xp} / {self.player.xp_to_next_level}")
            print(f"\nพลังชีวิต (HP): {self.player.hp} / {self.player.max_hp}")
            print(f"พลังโจมตีพื้นฐาน (ATK): {self.player.atk}")
            print(f"พลังป้องกันพื้นฐาน (DEF): {self.player.defense_stat}")
            print(f"ความเร็ว (SPD): {self.player.spd}")
            print(f"โชค (LUCK): {self.player.luck}")
            print("\n" + "-"*20)
            print(f"แต้มสถานะคงเหลือ: {self.player.stat_points}")
            print("-" * 20)
            
            if self.player.stat_points > 0:
                print("\nคุณต้องการอัปเกรดสถานะใด? (ใช้ 1 แต้ม)")
                print("1. พลังโจมตี (ATK) +1")
                print("2. พลังป้องกัน (DEF) +1")
                print("3. ความเร็ว (SPD) +1")
                print("4. โชค (LUCK) +1")
                print("5. พลังชีวิตสูงสุด (HP) +5")
            
            print("\n0. กลับ")
            choice = input("เลือก: ")

            if choice == '0':
                break
            
            if self.player.stat_points > 0 and choice in ['1', '2', '3', '4', '5']:
                self.player.stat_points -= 1
                if choice == '1':
                    self.player.atk += 1
                    print("\nอัปเกรด ATK สำเร็จ!")
                elif choice == '2':
                    self.player.defense_stat += 1
                    print("\nอัปเกรด DEF สำเร็จ!")
                elif choice == '3':
                    self.player.spd += 1
                    print("\nอัปเกรด SPD สำเร็จ!")
                elif choice == '4':
                    self.player.luck += 1
                    print("\nอัปเกรด LUCK สำเร็จ!")
                elif choice == '5':
                    self.player.max_hp += 5
                    self.player.hp += 5 # เพิ่มเลือดปัจจุบันด้วย
                    print("\nอัปเกรด HP สูงสุดสำเร็จ!")
                
                time.sleep(1.5)
                # Loop back to show updated stats

    def inn_phase(self):
        clear_screen(); print("--- โรงเตี๊ยม ---"); rep = self.player.reputation.get(self.all_locations[self.player.current_location_id]['name'], 0); cost = max(0, 10 - rep // 10); print(f"เจ้าของ: \"ยินดีต้อนรับท่านซามูไร ค่าที่พักคืนนี้ {cost} มง ท่านจะพักหรือไม่?\"")
        choice = input("(y/n): ").lower()
        if choice == 'y':
            if self.player.money >= cost:
                self.player.money -= cost; self.player.hp = self.player.max_hp; self.player.reputation[self.all_locations[self.player.current_location_id]['name']] = rep + 1; self.player.status_effects = {}
                while self.time["segment"] != "เช้า": self.advance_time()
                self.advance_time(); print("\nคุณได้พักผ่อนอย่างเต็มที่... เช้าวันใหม่ได้เริ่มขึ้นแล้ว")
            else:
                print("\nเงินของคุณไม่พอสำหรับค่าที่พัก...")
        input("\nกด Enter เพื่อดำเนินการต่อ...")
    
    def traveling_phase(self):
        clear_screen(); print("คุณกำลังเดินทางบนเส้นทางสายเปลี่ยว..."); self.advance_time(); time.sleep(2);
        
        roll = random.random()
        current_region_type = self.all_regions[self.player.current_region_id]['type']
        
        can_spawn_boss = self.boss_encounter_cooldown == 0 and current_region_type in self.bosses_by_region
        if can_spawn_boss and roll < 0.10: # 10% chance to meet a boss
            possible_bosses = self.bosses_by_region[current_region_type]
            boss_id = random.choice(possible_bosses)
            boss_base_data = self.all_bosses[boss_id].copy()
            
            self.current_enemies = [Enemy.from_dict(boss_id, boss_base_data, is_boss=True)]
            
            self.apply_difficulty_scaling(self.current_enemies)

            print(f"\n!!! คุณได้เผชิญหน้ากับภัยคุกคามอันใหญ่หลวง... {self.current_enemies[0].name} !!!"); time.sleep(2.5)
            self.game_state = 'COMBAT'
            self.boss_encounter_cooldown = 5
        
        elif roll < 0.70: # 60% chance for normal enemies
            if current_region_type in self.enemies_by_region_type:
                max_enemies = 3 if self.player.level >= 8 else 2
                num_enemies = random.randint(1, max_enemies)
                self.current_enemies = []
                
                for _ in range(num_enemies):
                    enemy_id = random.choice(self.enemies_by_region_type[current_region_type])
                    enemy_base_data = self.all_enemies_data[enemy_id].copy()
                    new_enemy = Enemy.from_dict(enemy_id, enemy_base_data)
                    self.current_enemies.append(new_enemy)
                
                self.apply_difficulty_scaling(self.current_enemies)

                print(f"\n!!! คุณถูกลอบโจมตีโดย {self.current_enemies[0].name} {len(self.current_enemies)} ตัว !!!"); time.sleep(2);
                self.game_state = 'COMBAT'
            else:
                 print("\nเส้นทางนี้ดูเงียบสงบเป็นพิเศษ..."); time.sleep(2); self.safe_travel_to_random_location()
        
        elif roll < 0.95: # 25% chance for an event
            self.meet_traveler_phase()
        
        else: # 5% safe travel
            print("\nการเดินทางครั้งนี้ปลอดภัยดี"); time.sleep(2);
            self.safe_travel_to_random_location()

    def apply_difficulty_scaling(self, enemies_list):
        level_tier = self.player.level // 5
        if level_tier == 0: return

        for enemy in enemies_list:
            scale_multiplier = 0.15 if enemy.is_boss else 0.20
            
            hp_bonus = int(enemy.base_max_hp * (level_tier * scale_multiplier))
            atk_bonus = int(enemy.base_atk * (level_tier * scale_multiplier))
            def_bonus = int(enemy.base_def * (level_tier * scale_multiplier))
            
            enemy.max_hp += hp_bonus
            enemy.hp = enemy.max_hp
            enemy.atk += atk_bonus
            enemy.defense_stat += def_bonus

    def safe_travel_to_random_location(self):
        possible_locations = [l_id for l_id in self.all_locations if l_id != self.player.current_location_id]
        if possible_locations:
            new_location_id = random.choice(possible_locations)
            self.player.current_location_id = new_location_id
            self.player.current_region_id = self.all_locations[new_location_id]['region_id']
            loc_name = self.all_locations[self.player.current_location_id]['name']
            print(f"คุณเดินทางมาถึง {loc_name}")
        else: print("ไม่มีที่อื่นให้ไปแล้ว...")
        time.sleep(2)
        self.game_state = 'LOCATION_HUB'

    def meet_traveler_phase(self):
        clear_screen();
        events = [ "พ่อค้าเร่", "นักบวชพเนจร", "โรนินท้าดวล", "โจรปลอมตัว", "นักต้มตุ๋น" ]
        event = random.choice(events)
        print(f"ระหว่างทาง คุณได้พบกับคนผู้หนึ่ง...")
        time.sleep(1.5)

        if event == "พ่อค้าเร่":
            print("ดูเหมือนเขาจะเป็นพ่อค้าเร่ ที่มีของหายากมาเสนอขาย...")
            print("พ่อค้า: \"สนใจดูของหน่อยไหมล่ะ ท่านนักเดินทาง? ของดีๆ ทั้งนั้น!\""); input("กด Enter...")
            self.shop_phase("ตลาด") 
        elif event == "นักบวชพเนจร":
            print("เขาคือนักบวชพเนจร ผู้มีเมตตา...")
            print("นักบวช: \"การเดินทางของท่านคงจะเหนื่อยล้านัก ให้ข้าช่วยบรรเทาความเจ็บปวดให้เถิด\"")
            heal_amount = self.player.max_hp // 2
            self.player.hp = min(self.player.max_hp, self.player.hp + heal_amount)
            self.player.status_effects = {}
            print(f"คุณได้รับพร! ฟื้นฟู HP {heal_amount} หน่วย และรักษาอาการผิดปกติทั้งหมด!")
            time.sleep(2)
        elif event == "โรนินท้าดวล":
            print("เขาคือโรนินผู้กระหายการต่อสู้! เขาจ้องมาที่คุณและชักดาบออกมา!")
            print("โรนิน: \"เจ้าก็ใช้ดาบสินะ... มาพิสูจน์กันหน่อยว่าใครกันแน่ที่แกร่งกว่า!\"")
            input("กด Enter เพื่อเริ่มการต่อสู้...")
            enemy_id = "E005" 
            enemy_base_data = self.all_enemies_data[enemy_id].copy()
            self.current_enemies = [Enemy.from_dict(enemy_id, enemy_base_data)]
            self.apply_difficulty_scaling(self.current_enemies)
            self.game_state = 'COMBAT'
            return 
        elif event == "โจรปลอมตัว":
            print("เขาดูเหมือนชาวบ้านธรรมดาที่กำลังเดือดร้อน...")
            print("ชาวบ้าน(?): \"ท่านซามูไร ได้โปรดช่วยข้าด้วย! ข้าโดนโจรปล้นมา...\"")
            choice = input("คุณจะช่วยเขาหรือไม่? (y/n): ").lower()
            if choice == 'y':
                print("ทันใดนั้น รอยยิ้มของเขาก็เปลี่ยนไป! \"ฮ่าๆๆ โง่จริง! ส่งของมีค่ามาให้หมด!\"")
                input("มันคือกับดัก! กด Enter เพื่อเริ่มการต่อสู้...")
                enemy_id = "E004"
                enemy_base_data = self.all_enemies_data[enemy_id].copy()
                self.current_enemies = [Enemy.from_dict(enemy_id, enemy_base_data)]
                self.apply_difficulty_scaling(self.current_enemies)
                self.game_state = 'COMBAT'
                return
            else:
                print("คุณรู้สึกไม่ชอบมาพากลและเดินจากไป... เป็นการตัดสินใจที่ถูกต้อง")
                time.sleep(2)
        elif event == "นักต้มตุ๋น":
            print("เขาเป็นชายท่าทางน่าเชื่อถือ เข้ามาเสนอขาย 'ยาอายุวัฒนะ' ให้คุณ")
            print("นักต้มตุ๋น: \"ท่านดูสิ! ยาอายุวัฒนะในตำนาน! เพียง 500 มง ท่านก็จะเป็นอมตะ!\"")
            choice = input("คุณจะซื้อมันหรือไม่? (y/n): ").lower()
            if choice == 'y':
                if self.player.money >= 500:
                    self.player.money -= 500
                    print("คุณจ่ายเงินและดื่มยา... รสชาติมันเหมือนน้ำเปล่า...")
                    print("ชายคนนั้นรีบเดินจากไปอย่างรวดเร็ว... ดูเหมือนคุณจะโดนหลอกเสียแล้ว")
                else:
                    print("คุณไม่มีเงินพอ และชายคนนั้นก็เดินจากไปอย่างหัวเสีย")
            else:
                print("คุณปฏิเสธข้อเสนอ และชายคนนั้นก็รีบเดินจากไปหาเหยื่อรายต่อไป")
            time.sleep(3)

        self.safe_travel_to_random_location()
        
    def combat_phase(self):
        self.player.combat_buffs = self.player.next_fight_buffs.copy()
        self.player.next_fight_buffs = {'atk': 0, 'def': 0, 'luck': 0}
        
        self.player.deck = list(self.player.original_deck)
        random.shuffle(self.player.deck)
        self.player.discard = []
        self.player.hand = []
        self.player.draw_hand()
        
        turn = 1
        
        for enemy in self.current_enemies:
            enemy.trigger_passive('start_of_combat', self)
            
        combat_result = None

        while any(e.is_alive() for e in self.current_enemies) and self.player.is_alive():
            clear_screen()
            print(f"--- การต่อสู้ | เทิร์นที่ {turn} ---")
            
            for i, enemy in enumerate(self.current_enemies):
                status_line = f"HP: {enemy.hp}/{enemy.max_hp}"
                if enemy.status_effects:
                    effects = ", ".join([f"{k.capitalize()}({v})" for k, v in enemy.status_effects.items()])
                    status_line += f" | สถานะ: {effects}"
                alive_status = "" if enemy.is_alive() else " (ตายแล้ว)"
                print(f"{i+1}. {enemy.name}{alive_status} ({status_line})")

            player_status_line = f"HP: {self.player.hp}/{self.player.max_hp}"
            if self.player.defense_bonus > 0: player_status_line += f" | ตั้งรับ: {self.player.defense_bonus}"
            if self.player.status_effects:
                effects = ", ".join([f"{k.capitalize()}({v})" for k, v in self.player.status_effects.items()])
                player_status_line += f" | สถานะ: {effects}"
            print(f"\nคุณ: {player_status_line}")
            
            print("\n--- ตาของคุณ ---")
            self.player.defense_bonus = 0
            self.player.tick_status_effects()
            if not self.player.is_alive(): break
            
            if 'stun' in self.player.status_effects or 'charm' in self.player.status_effects:
                print(f"คุณติดสถานะ {list(self.player.status_effects.keys())[0]} และไม่สามารถทำอะไรได้!")
            else:
                player_action_result = self.player_turn()
                if player_action_result == 'FLED':
                    combat_result = 'fled'
                    break

            if not any(e.is_alive() for e in self.current_enemies): break

            for enemy in self.current_enemies:
                if enemy.is_alive() and self.player.is_alive():
                    print(f"\n--- ตาของ {enemy.name} ---")
                    enemy.tick_status_effects(self)
                    if not enemy.is_alive():
                        print(f"{enemy.name} ทนพิษบาดแผลไม่ไหวและล้มลง!")
                        continue
                    
                    if 'stun' in enemy.status_effects:
                        print(f"{enemy.name} ติดสถานะมึนงงและขยับไม่ได้!")
                    else:
                        self.enemy_turn(enemy)
                    
                    if not self.player.is_alive():
                        self.cause_of_death = f"พ่ายแพ้ในคมดาบของ {enemy.name}"
                        break
            
            turn += 1
            if self.player.is_alive() and any(e.is_alive() for e in self.current_enemies):
                input("\nกด Enter เพื่อเข้าสู่เทิร์นถัดไป...")
        
        if combat_result is None:
            if self.player.is_alive():
                combat_result = 'win'
            else:
                combat_result = 'loss'

        self.player.combat_buffs = {'atk': 0, 'def': 0, 'luck': 0}
        self.player.status_effects = {}
        if combat_result in ['win', 'loss']:
            self.player.temp_skill_cards = [] 
        
        clear_screen()
        
        if combat_result == 'win':
            print("\n--- คุณได้รับชัยชนะ! ---")
            money_gain_total = 0; total_xp_gain = 0
            
            for enemy in self.current_enemies:
                base_data = self.all_enemies_data.get(enemy.enemy_id) or self.all_bosses.get(enemy.enemy_id)
                if not base_data: continue
                total_xp_gain += base_data.get("xp_reward", 0)
                money_gain_total += random.randint(base_data.get("xp_reward", 10)//2, base_data.get("xp_reward", 10))

            self.player.money += money_gain_total
            print(f"ได้รับเงิน {money_gain_total} มง")
            self.player.add_xp(total_xp_gain)
            
            print("\n--- ไอเทมที่ได้รับ ---"); item_dropped = False
            for enemy in self.current_enemies:
                base_data = self.all_enemies_data.get(enemy.enemy_id) or self.all_bosses.get(enemy.enemy_id)
                if not base_data or "drop_table" not in base_data: continue
                
                for drop in base_data["drop_table"]:
                    if random.random() < drop["chance"]:
                        item_id = drop["item_id"]; item_info = self.all_items.get(item_id)
                        if not item_info: continue
                        quantity = random.randint(drop["quantity"][0], drop["quantity"][1]); item_name = item_info["name"]
                        self.player.add_item(item_name, quantity, item_id)
                        print(f"{enemy.name} ดรอป {item_name} x{quantity}!"); item_dropped = True
                
                if not enemy.is_boss and random.random() < 0.04:
                    move = random.choice(enemy.moveset)
                    if move['type'] != 'passive':
                        new_card = Card(move['name'], move['type'].upper(), 10, move['desc'], temporary=True, uses=2)
                        self.player.add_temp_card(new_card)
                        print(f"คุณเรียนรู้ท่า '{move['name']}' จาก {enemy.name} มาชั่วคราว (ใช้ได้ 2 ครั้ง)!")
                        item_dropped = True


            if not item_dropped: print("- ไม่ได้รับไอเทมใดๆ -")
            
            killed_enemies = [e.name for e in self.current_enemies]
            for q_id, quest in list(self.player.active_quests.items()):
                if quest.get("objective", {}).get("type") == "kill":
                    target_name = quest["objective"]["target"]
                    kill_count = sum(1 for name in killed_enemies if name == target_name)
                    if kill_count > 0: quest["progress"] += kill_count; print(f"ความคืบหน้าภารกิจ '{quest['title']}': {quest['progress']}/{quest['objective']['count']}")
            
            self.game_state = 'LOCATION_HUB'
        
        elif combat_result == 'loss':
            print("\nคุณพ่ายแพ้...")
            self.game_state = 'GAME_OVER'
        
        elif combat_result == 'fled':
            print("\nคุณหนีออกมาได้ และเดินทางต่อไปยังที่อื่น...")

        input("กด Enter เพื่อดำเนินการต่อ...")

    def player_turn(self):
        actions_this_turn = 0
        max_actions = 1
        
        while actions_this_turn < max_actions and self.player.is_alive() and any(e.is_alive() for e in self.current_enemies):
            print("\nการ์ดในมือ:")
            for i, card in enumerate(self.player.hand):
                uses_left = f" ({card.uses} ครั้ง)" if card.temporary else ""
                print(f"  {i+1}. [{card.type}] {card.name}{uses_left} ({card.value}) - {card.desc}")
            
            print("\nตัวเลือกเพิ่มเติม:")
            print("  8. ใช้ไอเทม")
            print("  9. พยายามหลบหนี")
            print("  0. จบเทิร์น")
            choice = input("เลือกการ์ด (หรือตัวเลือกอื่น): ")
            
            if not choice.isdigit(): continue
            choice = int(choice)
            
            if choice == 0: break
            if choice == 9:
                if self.attempt_flee():
                    return 'FLED'
                else: 
                    break 
            if choice == 8:
                if self.inventory_turn_action():
                    actions_this_turn += 1
                continue

            if not (1 <= choice <= len(self.player.hand)): print("เลือกไม่ถูกต้อง"); continue
            
            card_index = choice -1
            card = self.player.hand[card_index]
            
            if card.type == "ATTACK":
                target = self.choose_enemy_target()
                if target:
                    
                    damage = self.player.get_total_atk() + card.value
                    
                    crit_chance = (self.player.luck / 200) + (0.05 if target.is_boss else 0)
                    is_crit = random.random() < crit_chance
                    if is_crit:
                        damage = int(damage * 1.5)
                        print(" *** คริติคอล! *** ")

                    actual_damage = target.take_damage(damage)
                    print(f"คุณใช้ '{card.name}' โจมตี {target.name} ทำความเสียหาย {actual_damage}!")
                    target.trigger_passive('on_hit', self, source=self.player)
                    self.player.hand.pop(card_index)
                else:
                    continue
            
            elif card.type == "DEFEND":
                self.player.defense_bonus += card.value + self.player.get_total_def() // 2
                print(f"คุณใช้ '{card.name}' ตั้งรับ {self.player.defense_bonus} แต้ม!")
                self.player.hand.pop(card_index)
            
            elif card.type == "SKILL":
                print("ยังไม่รองรับการ์ดสกิลของผู้เล่น")
                self.player.hand.pop(card_index)
            
            if card.temporary:
                card.uses -= 1
                if card.uses > 0:
                    pass # Card stays in hand implicitly because we didn't discard
                else:
                    self.player.remove_temp_card(card.name)
                    print(f"การ์ด '{card.name}' ถูกใช้จนหมดแล้ว!")
            else:
                self.player.discard.append(card)

            actions_this_turn += 1
            time.sleep(1.5)
            if not any(e.is_alive() for e in self.current_enemies): break
        
        self.player.draw_hand()
        return None
        
    def inventory_turn_action(self):
        clear_screen(); print("--- เลือกไอเทมที่จะใช้ในการต่อสู้ ---")
        combat_items = {name: data for name, data in self.player.item_inventory.items() if self.all_items.get(data['id'], {}).get('type') in ['ATTACK', 'UTILITY', 'HEAL', 'CURE', 'BUFF_ATK', 'BUFF_DEF']}
        
        if not combat_items:
            print("- ไม่มีไอเทมที่ใช้ในการต่อสู้ได้ -")
            input("\nกด Enter เพื่อดำเนินการต่อ...")
            return False
        
        item_list = sorted(list(combat_items.items()))
        for i, (name, data) in enumerate(item_list, 1):
            print(f"{i}. {name} x{data['quantity']}")
        print("0. ยกเลิก")
        
        choice = input("เลือก: ")
        if choice.isdigit() and 1 <= int(choice) <= len(item_list):
            item_name = item_list[int(choice)-1][0]
            item_id = self.player.item_inventory[item_name]['id']
            item_data = self.all_items[item_id]
            
            if self.use_item_in_combat(item_data):
                self.player.remove_item(item_name)
                time.sleep(1.5)
                return True
        return False

    def use_item_in_combat(self, item_data):
        item_type = item_data['type']
        item_value = item_data['value']
        print(f"\nคุณใช้ {item_data['name']}!")
        
        if item_type == 'HEAL':
            self.player.hp = min(self.player.max_hp, self.player.hp + item_value)
            print(f"ฟื้นฟู HP {item_value} หน่วย!")
        elif item_type == 'CURE':
            self.player.status_effects = {}
            print("รักษาอาการผิดปกติทั้งหมด!")
        elif item_type == 'ATTACK':
            target = self.choose_enemy_target()
            if not target: return False
            actual_damage = target.take_damage(item_value)
            print(f"{target.name} ได้รับความเสียหาย {actual_damage} หน่วย!")
        elif item_type == 'UTILITY':
            if "ระเบิดควัน" in item_data['name']:
                print("คุณเตรียมขว้างระเบิดควัน...")
                return True 
            elif "พิษ" in item_data['name']:
                 target = self.choose_enemy_target()
                 if not target: return False
                 target.apply_status_effect('poison', 3)
                 print(f"{target.name} ติดสถานะพิษ!")
        elif item_type == 'BUFF_ATK':
            self.player.combat_buffs['atk'] += item_value
            print(f"พลังโจมตีของคุณเพิ่มขึ้น {item_value}!")
        elif item_type == 'BUFF_DEF':
            self.player.combat_buffs['def'] += item_value
            print(f"พลังป้องกันของคุณเพิ่มขึ้น {item_value}!")
        else:
            print("ไม่สามารถใช้ไอเทมนี้ในการต่อสู้ได้")
            input("\nกด Enter เพื่อดำเนินการต่อ...")
            return False

        return True


    def choose_enemy_target(self):
        alive_enemies = [e for e in self.current_enemies if e.is_alive()]
        if not alive_enemies: return None
        if len(alive_enemies) == 1: return alive_enemies[0]
        
        while True:
            print("\nเลือกเป้าหมาย:")
            for i, enemy in enumerate(alive_enemies, 1):
                print(f"  {i}. {enemy.name} (HP: {enemy.hp})")
            print("  0. ยกเลิก")
            target_choice = input("เลือก: ")
            if target_choice.isdigit():
                target_idx = int(target_choice) - 1
                if target_idx == -1: return None
                if 0 <= target_idx < len(alive_enemies):
                    return alive_enemies[target_idx]
            print("เลือกไม่ถูกต้อง")


    def attempt_flee(self):
        clear_screen(); print("คุณพยายามหาช่องทางหลบหนี..."); time.sleep(1.5);
        if any(e.is_boss for e in self.current_enemies):
            print("ไม่สามารถหลบหนีจากบอสได้!")
            input("\nกด Enter เพื่อดำเนินการต่อ...")
            return False

        avg_enemy_spd = sum(e.get_total_spd() for e in self.current_enemies) / len(self.current_enemies)
        base_chance = 0.50
        speed_diff = self.player.get_total_spd() - avg_enemy_spd
        speed_modifier = (speed_diff * 0.05)
        luck_modifier = (self.player.luck * 0.01)
        escape_chance = max(0.1, min(0.9, base_chance + speed_modifier + luck_modifier))
        print(f"โอกาสหนีสำเร็จ: {int(escape_chance * 100)}%"); time.sleep(1)
        if random.random() < escape_chance:
            print("\nคุณหนีรอดมาได้อย่างหวุดหวิด!")
            time.sleep(2)
            self.safe_travel_to_random_location()
            self.game_state = 'LOCATION_HUB'
            return True
        else:
            print("\nการหลบหนีล้มเหลว! ศัตรูขวางทางไว้!")
            input("\nกด Enter เพื่อดำเนินการต่อ...")
            return False

    def enemy_turn(self, enemy):
        time.sleep(1)
        player_hp_percent = self.player.hp / self.player.max_hp
        move = enemy.choose_move(player_hp_percent)
        
        if not move:
            print(f"{enemy.name} กำลังรวบรวมพลัง..."); return

        move_desc = move.get('desc', 'มันโจมตี!')
        print(f"{enemy.name} ใช้ท่า '{move['name']}'! ({move_desc})")
        time.sleep(1.5)
        
        move_type = move.get('type')
        if move_type == 'attack':
            damage = int(enemy.get_total_atk() * move.get('power', 1.0))
            actual_damage = self.player.take_damage(damage)
            print(f"คุณได้รับความเสียหาย {actual_damage} แต้ม!")
            if 'effect' in move and random.random() < move.get('chance', 1.0):
                self.player.apply_status_effect(move['effect'], move.get('duration', 3))

        elif move_type == 'skill':
            effect = move.get('effect')
            power = move.get('power', 0)
            if 'buff' in effect:
                stat_to_buff = effect.split('_')[1]
                enemy.combat_buffs[stat_to_buff] += power
                print(f"พลัง{stat_to_buff.upper()}ของ {enemy.name} เพิ่มขึ้น!")
            elif 'debuff' in effect:
                stat_to_debuff = effect.split('_')[1]
                self.player.combat_buffs[stat_to_debuff] -= power
                print(f"พลัง{stat_to_debuff.upper()}ของคุณลดลง!")
            elif effect == 'heal':
                enemy.hp = min(enemy.max_hp, enemy.hp + power)
                print(f"{enemy.name} ฟื้นฟูพลังชีวิต!")
            elif effect == 'summon':
                print(f"{enemy.name} พยายามจะเรียกพวก แต่ยังไม่มีใครมา!")
                
        elif move_type == 'charge':
            pass


    def game_over_phase(self):
        clear_screen(); print("--- ตำนานของคุณได้จบสิ้นลงแล้ว ---"); time.sleep(2);
        
        story_lines = [f"สาเหตุ: {self.cause_of_death}", "คุณล้มลงกลางทาง...", "ไม่มีใครบันทึกเรื่องราว ไม่มีใครจดจำการเดินทางครั้งนี้"]
        for line in story_lines:
            typewriter_print(f"\n{line}")
            time.sleep(2)
        
        print("\n\nGAME OVER")
        input("\nกด Enter เพื่อกลับสู่เมนูหลัก...")
        self.game_state = 'MAIN_MENU'

    def cheat_menu_phase(self):
        clear_screen(); print("--- CHEAT MENU ACTIVATED ---")
        cheats = {
            "1": ("GODMODE", "HP สูงสุด, ไม่โดนดาเมจ"),
            "2": ("CASHMONEY", "เพิ่มเงิน 10,000 มง"),
            "3": ("LEVELUP", "เพิ่ม 5 เลเวล"),
            "4": ("GIMMEALL", "ได้รับไอเทมและวัตถุดิบทั้งหมดอย่างละ 10 ชิ้น"),
            "5": ("GEARUP", "ได้รับอาวุธและชุดเกราะทั้งหมด"),
            "6": ("INSTAWIN", "ชนะการต่อสู้ทันที (ใช้ตอนสู้)"),
            "7": ("TELEPORT", "วาปไปสถานที่อื่น"),
            "8": ("MAXSTATS", "เพิ่มค่าสถานะพื้นฐานทั้งหมด +10"),
        }
        for key, (name, desc) in cheats.items():
            print(f"{key}. {name} - {desc}")
        print("0. กลับ")
        
        choice = input("Enter Cheat Code Number: ")

        if choice == '1':
            self.player.max_hp = 9999
            self.player.hp = 9999
            self.player.god_mode = True 
            print("GOD MODE ACTIVATED")
        elif choice == '2':
            self.player.money += 10000
            print("ได้รับ 10,000 มง!")
        elif choice == '3':
            for _ in range(5):
                self.player.add_xp(self.player.xp_to_next_level - self.player.xp + 1)
            print("ได้รับ 5 เลเวล!")
        elif choice == '4':
            for item_id, item_data in self.all_items.items():
                self.player.add_item(item_data['name'], 10, item_id)
            print("ได้รับไอเทมทั้งหมด!")
        elif choice == '5':
            for w_id, w_data in self.all_weapons.items():
                self.player.weapon_inventory.append(Weapon(w_id, w_data['name'], w_data['bonus_atk'], w_data['price']))
            for a_id, a_data in self.all_armors.items():
                 self.player.armor_inventory.append(Armor(a_id, a_data['name'], a_data['slot'], a_data['bonus_def'], a_data['price']))
            print("ได้รับยุทโธปกรณ์ทั้งหมด!")
        elif choice == '6':
            if self.game_state == 'COMBAT':
                for e in self.current_enemies: e.hp = 0
                print("Enemies defeated.")
            else:
                print("ต้องอยู่ในการต่อสู้เท่านั้น")
        elif choice == '7':
            print("เลือกสถานที่:")
            locations = list(self.all_locations.items())
            for i, (l_id, l_data) in enumerate(locations):
                print(f"{i+1}. {l_data['name']}")
            tp_choice = input("ไปที่: ")
            if tp_choice.isdigit() and 1 <= int(tp_choice) <= len(locations):
                l_id, l_data = locations[int(tp_choice)-1]
                self.player.current_location_id = l_id
                self.player.current_region_id = l_data['region_id']
                print(f"เดินทางไปยัง {l_data['name']} สำเร็จ!")
        elif choice == '8':
            self.player.atk += 10
            self.player.defense_stat += 10
            self.player.spd += 10
            self.player.luck += 10
            print("ค่าสถานะเพิ่มขึ้น!")
        
        input("\nกด Enter เพื่อดำเนินการต่อ...")


if __name__ == "__main__":
    # ตั้งค่า encoding สำหรับ Windows console
    if os.name == 'nt':
        os.system('chcp 65001 > nul')

    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except TypeError:
        # fallback for older python versions
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

    game = Game()
    game.run()

