# -*- coding: utf-8 -*-
from game_classes import Card # Import Card class to create card pools

def get_enemies():
    """
    คืน Dictionary ของศัตรูและปีศาจทั้งหมด
    region_types: ประเภทของภูมิภาคที่ศัตรูจะปรากฏตัว
    drop_table: รายการไอเทมที่มีโอกาสดรอป
      - item_id: รหัสไอเทมจาก item_data.py
      - chance: โอกาสดรอป (0.0 - 1.0)
      - quantity: จำนวนที่ดรอป [ต่ำสุด, สูงสุด]
    """
    enemies = {
        # --- มนุษย์ ---
        "E001": { "name": "โจรป่า", "max_hp": 50, "atk": 6, "def": 3, "spd": 5, "luck": 3, "card_pool_tag": "human_basic", "region_types": ["plains", "forest"],
                  "drop_table": [ {"item_id": "I002", "chance": 0.5, "quantity": [1, 1]}, {"item_id": "I001", "chance": 0.2, "quantity": [1, 1]} ] },
        "E002": { "name": "โรนินตกอับ", "max_hp": 65, "atk": 10, "def": 4, "spd": 6, "luck": 4, "card_pool_tag": "ronin_basic", "region_types": ["plains"],
                  "drop_table": [ {"item_id": "I005", "chance": 0.3, "quantity": [1, 1]}, {"item_id": "W006", "chance": 0.05, "quantity": [1, 1]} ] },
        "E003": { "name": "นักรบภูเขา (ยามะบูชิ)", "max_hp": 80, "atk": 9, "def": 6, "spd": 5, "luck": 5, "card_pool_tag": "human_strong", "region_types": ["mountain"],
                  "drop_table": [ {"item_id": "I010", "chance": 0.4, "quantity": [1, 2]}, {"item_id": "I013", "chance": 0.1, "quantity": [1, 1]} ] },
        "E004": { "name": "หัวหน้าโจรป่า", "max_hp": 90, "atk": 10, "def": 5, "spd": 6, "luck": 5, "card_pool_tag": "bandit_leader", "region_types": ["plains", "forest"],
                  "drop_table": [ {"item_id": "I003", "chance": 0.25, "quantity": [1, 1]}, {"item_id": "I004", "chance": 0.15, "quantity": [1, 1]} ] },
        "E005": { "name": "ซามูไรรับจ้าง", "max_hp": 75, "atk": 12, "def": 4, "spd": 7, "luck": 6, "card_pool_tag": "ronin_strong", "region_types": ["plains"],
                  "drop_table": [ {"item_id": "I033", "chance": 0.2, "quantity": [1, 1]}, {"item_id": "W010", "chance": 0.05, "quantity": [1, 1]} ] },
        "E006": { "name": "พลหอกอาชิการุ", "max_hp": 60, "atk": 8, "def": 4, "spd": 5, "luck": 4, "card_pool_tag": "ashigaru_spear", "region_types": ["plains"],
                  "drop_table": [ {"item_id": "I002", "chance": 0.4, "quantity": [1, 2]}, {"item_id": "I026", "chance": 0.2, "quantity": [1, 1]} ] },
        "E007": { "name": "นินจาลอบสังหาร", "max_hp": 65, "atk": 11, "def": 3, "spd": 12, "luck": 8, "card_pool_tag": "ninja", "region_types": ["forest", "mountain", "swamp"],
                  "drop_table": [ {"item_id": "I021", "chance": 0.3, "quantity": [1, 3]}, {"item_id": "I020", "chance": 0.15, "quantity": [1, 1]} ] },
        "E008": { "name": "องเมียวจิฝึกหัด", "max_hp": 55, "atk": 10, "def": 2, "spd": 6, "luck": 7, "card_pool_tag": "onmyoji", "region_types": ["plains"],
                  "drop_table": [ {"item_id": "I013", "chance": 0.25, "quantity": [1, 1]}, {"item_id": "I031", "chance": 0.4, "quantity": [1, 2]} ] },
        "E009": { "name": "นักบวชโซเฮย์", "max_hp": 85, "atk": 10, "def": 6, "spd": 6, "luck": 5, "card_pool_tag": "sohei_monk", "region_types": ["mountain"],
                  "drop_table": [ {"item_id": "I010", "chance": 0.3, "quantity": [1, 2]}, {"item_id": "I018", "chance": 0.15, "quantity": [1, 1]} ] },
        
        # --- สัตว์ ---
        "A001": { "name": "หมาป่า", "max_hp": 40, "atk": 8, "def": 1, "spd": 8, "luck": 5, "card_pool_tag": "animal_basic", "region_types": ["forest", "mountain"],
                  "drop_table": [ {"item_id": "I052", "chance": 0.6, "quantity": [1, 2]} ] },
        "A002": { "name": "หมูป่ายักษ์", "max_hp": 90, "atk": 12, "def": 5, "spd": 4, "luck": 2, "card_pool_tag": "animal_brute", "region_types": ["forest"],
                  "drop_table": [ {"item_id": "I052", "chance": 0.8, "quantity": [2, 4]} ] },
        "A003": { "name": "หมีป่า", "max_hp": 100, "atk": 13, "def": 6, "spd": 4, "luck": 3, "card_pool_tag": "bear", "region_types": ["forest", "mountain"],
                  "drop_table": [ {"item_id": "I052", "chance": 0.8, "quantity": [3, 5]} ] },
        "A004": { "name": "งูยักษ์", "max_hp": 70, "atk": 9, "def": 3, "spd": 7, "luck": 5, "card_pool_tag": "giant_snake", "region_types": ["swamp", "forest"],
                  "drop_table": [ {"item_id": "I052", "chance": 0.5, "quantity": [1, 3]}, {"item_id": "I022", "chance": 0.1, "quantity": [1, 1]} ] },
        "A005": { "name": "จิ้งจอกเจ้าเล่ห์ (Kitsune)", "max_hp": 60, "atk": 10, "def": 3, "spd": 9, "luck": 9, "card_pool_tag": "kitsune", "region_types": ["forest", "haunted_forest"],
                  "drop_table": [ {"item_id": "I016", "chance": 0.2, "quantity": [1, 1]}, {"item_id": "I028", "chance": 0.02, "quantity": [1, 1]} ] },
        "A006": { "name": "ตะขาบยักษ์ (Ōmukade)", "max_hp": 80, "atk": 11, "def": 7, "spd": 5, "luck": 4, "card_pool_tag": "giant_centipede", "region_types": ["mountain"],
                  "drop_table": [ {"item_id": "I051", "chance": 0.4, "quantity": [1, 2]}, {"item_id": "I022", "chance": 0.15, "quantity": [1, 1]} ] },
        "A007": { "name": "เหยี่ยวภูเขา", "max_hp": 45, "atk": 9, "def": 2, "spd": 11, "luck": 6, "card_pool_tag": "hawk", "region_types": ["mountain"],
                  "drop_table": [ {"item_id": "I054", "chance": 0.3, "quantity": [1, 3]} ] },
        "A008": { "name": "ลิงภูเขา", "max_hp": 40, "atk": 7, "def": 3, "spd": 8, "luck": 6, "card_pool_tag": "monkey", "region_types": ["mountain"],
                  "drop_table": [ {"item_id": "I008", "chance": 0.4, "quantity": [1, 1]} ] },

        # --- ปีศาจ (โยไค) ---
        "Y001": { "name": "กัปปะ (Kappa)", "max_hp": 70, "atk": 9, "def": 5, "spd": 8, "luck": 6, "card_pool_tag": "yokai_water", "region_types": ["swamp"],
                  "drop_table": [ {"item_id": "I009", "chance": 0.5, "quantity": [1, 1]}, {"item_id": "I035", "chance": 0.15, "quantity": [1, 1]} ] },
        "Y002": { "name": "โอนิ (Oni)", "max_hp": 120, "atk": 15, "def": 8, "spd": 3, "luck": 3, "card_pool_tag": "yokai_brute", "region_types": ["mountain", "haunted_forest"],
                  "drop_table": [ {"item_id": "I005", "chance": 0.4, "quantity": [1, 3]}, {"item_id": "I055", "chance": 0.1, "quantity": [1, 1]} ] },
        "Y003": { "name": "เท็งงุ (Tengu)", "max_hp": 85, "atk": 11, "def": 4, "spd": 10, "luck": 7, "card_pool_tag": "yokai_swift", "region_types": ["mountain", "forest"],
                  "drop_table": [ {"item_id": "I019", "chance": 0.2, "quantity": [1, 2]}, {"item_id": "I042", "chance": 0.1, "quantity": [1, 1]} ] },
        "Y004": { "name": "ยูเร (Yurei)", "max_hp": 50, "atk": 7, "def": 2, "spd": 7, "luck": 5, "card_pool_tag": "yokai_spirit", "region_types": ["haunted_forest"],
                  "drop_table": [ {"item_id": "I018", "chance": 0.2, "quantity": [1, 1]}, {"item_id": "I047", "chance": 0.05, "quantity": [1, 1]} ] },
        "Y005": { "name": "คาไมทาจิ (Kamaitachi)", "max_hp": 55, "atk": 9, "def": 2, "spd": 15, "luck": 8, "card_pool_tag": "kamaitachi", "region_types": ["plains"],
                  "drop_table": [ {"item_id": "I019", "chance": 0.3, "quantity": [1, 1]}, {"item_id": "I004", "chance": 0.15, "quantity": [1, 1]} ] },
        "Y006": { "name": "สึจิกุโมะ (Tsuchigumo)", "max_hp": 95, "atk": 11, "def": 7, "spd": 4, "luck": 5, "card_pool_tag": "tsuchigumo", "region_types": ["mountain", "forest"],
                  "drop_table": [ {"item_id": "I054", "chance": 0.6, "quantity": [2, 5]}, {"item_id": "I022", "chance": 0.2, "quantity": [1, 1]} ] },
        "Y007": { "name": "เนะโกะมาตะ (Nekomata)", "max_hp": 65, "atk": 9, "def": 4, "spd": 9, "luck": 8, "card_pool_tag": "nekomata", "region_types": ["plains", "haunted_forest"],
                  "drop_table": [ {"item_id": "I007", "chance": 0.4, "quantity": [1, 2]}, {"item_id": "I048", "chance": 0.05, "quantity": [1, 1]} ] },
        "Y008": { "name": "โรคุโรคุบิ (Rokurokubi)", "max_hp": 70, "atk": 8, "def": 5, "spd": 6, "luck": 6, "card_pool_tag": "rokurokubi", "region_types": ["plains"],
                  "drop_table": [ {"item_id": "I046", "chance": 0.03, "quantity": [1, 1]} ] },
        "Y009": { "name": "นูริคาเบะ (Nurikabe)", "max_hp": 110, "atk": 7, "def": 12, "spd": 2, "luck": 2, "card_pool_tag": "nurikabe", "region_types": ["haunted_forest"],
                  "drop_table": [ {"item_id": "I051", "chance": 0.7, "quantity": [1, 3]} ] },
        "Y010": { "name": "คาราคาซะ-โอบาเกะ (Karakasa-obake)", "max_hp": 50, "atk": 7, "def": 4, "spd": 7, "luck": 7, "card_pool_tag": "karakasa", "region_types": ["haunted_forest"],
                  "drop_table": [ {"item_id": "I053", "chance": 0.3, "quantity": [1, 2]} ] },
        "Y011": { "name": "โจโรกุโมะ (Jorōgumo)", "max_hp": 85, "atk": 10, "def": 6, "spd": 7, "luck": 7, "card_pool_tag": "jorogumo", "region_types": ["forest", "haunted_forest"],
                  "drop_table": [ {"item_id": "I022", "chance": 0.25, "quantity": [1, 1]}, {"item_id": "I048", "chance": 0.1, "quantity": [1, 1]} ] },
        "Y012": { "name": "ยูกิอนนะ (Yuki-onna)", "max_hp": 75, "atk": 11, "def": 3, "spd": 8, "luck": 6, "card_pool_tag": "yuki_onna", "region_types": ["mountain"],
                  "drop_table": [ {"item_id": "I027", "chance": 0.15, "quantity": [1, 1]} ] },
        "Y013": { "name": "โคดามะ (Kodama)", "max_hp": 40, "atk": 5, "def": 5, "spd": 6, "luck": 8, "card_pool_tag": "kodama", "region_types": ["forest"],
                  "drop_table": [ {"item_id": "I012", "chance": 0.5, "quantity": [1, 3]} ] },
        "Y014": { "name": "บาเกะ-โซริ (Bake-zōri)", "max_hp": 30, "atk": 6, "def": 2, "spd": 8, "luck": 5, "card_pool_tag": "bakezori", "region_types": ["plains"],
                  "drop_table": [ {"item_id": "I054", "chance": 0.2, "quantity": [1, 2]} ] },
        "Y015": { "name": "อิตตัน-โมเมน (Ittan-momen)", "max_hp": 60, "atk": 8, "def": 4, "spd": 9, "luck": 6, "card_pool_tag": "ittanmomen", "region_types": ["haunted_forest"],
                  "drop_table": [ {"item_id": "I054", "chance": 0.7, "quantity": [2, 4]} ] },
        "Y016": { "name": "โออิเตะเกโบริ (Oiteke-bori)", "max_hp": 65, "atk": 9, "def": 6, "spd": 4, "luck": 5, "card_pool_tag": "oitekebori", "region_types": ["swamp"],
                  "drop_table": [ {"item_id": "I007", "chance": 0.3, "quantity": [1, 3]} ] },
        "Y017": { "name": "อาคานาเมะ (Akaname)", "max_hp": 45, "atk": 5, "def": 3, "spd": 7, "luck": 4, "card_pool_tag": "akaname", "region_types": ["swamp", "haunted_forest"],
                  "drop_table": [ {"item_id": "I001", "chance": 0.1, "quantity": [1, 1]} ] },
        "Y018": { "name": "โอนิบิ (Onibi)", "max_hp": 50, "atk": 10, "def": 1, "spd": 9, "luck": 7, "card_pool_tag": "onibi", "region_types": ["haunted_forest", "swamp"],
                  "drop_table": [ {"item_id": "I056", "chance": 0.5, "quantity": [1, 3]}, {"item_id": "I024", "chance": 0.1, "quantity": [1, 1]} ] },
        "Y019": { "name": "โนปเประโบ (Noppera-bō)", "max_hp": 60, "atk": 7, "def": 4, "spd": 7, "luck": 8, "card_pool_tag": "nopperabo", "region_types": ["plains", "haunted_forest"],
                  "drop_table": [ {"item_id": "I020", "chance": 0.15, "quantity": [1, 1]} ] },
        "Y020": { "name": "กาชาโดคุโระ (Gashadokuro)", "max_hp": 200, "atk": 18, "def": 10, "spd": 3, "luck": 1, "card_pool_tag": "gashadokuro", "region_types": ["haunted_forest"],
                  "drop_table": [ {"item_id": "I050", "chance": 0.2, "quantity": [1, 1]}, {"item_id": "I011", "chance": 0.3, "quantity": [1, 1]} ] }
    }
    return enemies

def get_enemy_card_pools():
    """คืน Dictionary ของชุดการ์ดสำหรับศัตรู"""
    pools = {
        # --- ชุดการ์ดดั้งเดิม ---
        "human_basic": [Card("ฟัน", "ATTACK", 4, ""), Card("ปาหิน", "ATTACK", 2, ""), Card("ป้องกันตัว", "DEFEND", 3, "")],
        "ronin_basic": [Card("เพลงดาบสามัญ", "ATTACK", 6, ""), Card("ตั้งท่า", "DEFEND", 5, "")],
        "human_strong": [Card("ฟาดด้วยพลอง", "ATTACK", 8, ""), Card("สวดมนต์ป้องกัน", "DEFEND", 7, "")],
        "animal_basic": [Card("กัด", "ATTACK", 5, ""), Card("ข่วน", "ATTACK", 4, "")],
        "animal_brute": [Card("พุ่งชน", "ATTACK", 10, ""), Card("กระทืบ", "ATTACK", 8, "")],
        "yokai_water": [Card("ดึงลงน้ำ", "ATTACK", 7, ""), Card("กระดองแข็ง", "DEFEND", 6, "")],
        "yokai_brute": [Card("ทุบด้วยคานาโบ", "ATTACK", 12, ""), Card("คำรามข่มขวัญ", "SKILL", 0, "")],
        "yokai_swift": [Card("ดาบวายุ", "ATTACK", 9, ""), Card("หายตัวในสายลม", "DEFEND", 8, "")],
        "yokai_spirit": [Card("สัมผัสเยือกแข็ง", "ATTACK", 6, ""), Card("ร่างโปร่งแสง", "DEFEND", 10, "")],

        # --- ชุดการ์ดใหม่ ---
        "bandit_leader": [Card("บัญชาการ", "SKILL", 0, ""), Card("ฟันดาบใหญ่", "ATTACK", 8, ""), Card("เกราะหนัง", "DEFEND", 6, "")],
        "ronin_strong": [Card("เพลงดาบไร้สำนัก", "ATTACK", 9, ""), Card("ปัดป้อง", "DEFEND", 7, "")],
        "ashigaru_spear": [Card("แทงหอก", "ATTACK", 7, ""), Card("ตั้งแนวป้องกัน", "DEFEND", 5, "")],
        "ninja": [Card("มีดสั้นอาบยาพิษ", "ATTACK", 7, ""), Card("ระเบิดควัน", "DEFEND", 6, "")],
        "onmyoji": [Card("ยันต์เพลิง", "ATTACK", 9, ""), Card("ยันต์ป้องกัน", "DEFEND", 4, "")],
        "sohei_monk": [Card("ฟาดด้วยง้าว", "ATTACK", 9, ""), Card("สมาธิเหล็ก", "DEFEND", 8, "")],
        "bear": [Card("ตะปบ", "ATTACK", 11, ""), Card("หนังหนา", "DEFEND", 5, "")],
        "giant_snake": [Card("ฉก", "ATTACK", 8, ""), Card("รัด", "ATTACK", 6, "")],
        "kitsune": [Card("เปลวไฟจิ้งจอก", "ATTACK", 9, ""), Card("สร้างภาพลวงตา", "DEFEND", 7, "")],
        "giant_centipede": [Card("กัดกิน", "ATTACK", 9, ""), Card("เกราะไคติน", "DEFEND", 6, "")],
        "hawk": [Card("โฉบโจมตี", "ATTACK", 7, ""), Card("บินหลบ", "DEFEND", 4, "")],
        "monkey": [Card("ขว้างของ", "ATTACK", 5, ""), Card("กระโดดหลบ", "DEFEND", 5, "")],
        "kamaitachi": [Card("คมมีดสายลม", "ATTACK", 8, ""), Card("เร็วปานวายุ", "DEFEND", 5, "")],
        "tsuchigumo": [Card("พ่นใย", "SKILL", 0, ""), Card("ขาแมงมุม", "ATTACK", 9, "")],
        "nekomata": [Card("กรงเล็บวิญญาณ", "ATTACK", 8, ""), Card("คำสาปแมว", "SKILL", 0, "")],
        "rokurokubi": [Card("คอเหวี่ยงฟาด", "ATTACK", 7, ""), Card("ยืดคอหลบ", "DEFEND", 6, "")],
        "nurikabe": [Card("กระแทก", "ATTACK", 6, ""), Card("กำแพงศิลา", "DEFEND", 10, "")],
        "karakasa": [Card("กระโดดทับ", "ATTACK", 6, ""), Card("หมุนร่มป้องกัน", "DEFEND", 5, "")],
        "jorogumo": [Card("เขี้ยวพิษ", "ATTACK", 9, ""), Card("ใยแมงมุม", "DEFEND", 7, "")],
        "yuki_onna": [Card("ลมหายใจเยือกแข็ง", "ATTACK", 9, ""), Card("เกล็ดน้ำแข็ง", "DEFEND", 6, "")],
        "kodama": [Card("เสียงสะท้อนในป่า", "SKILL", 0, ""), Card("รากไม้ป้องกัน", "DEFEND", 8, "")],
        "bakezori": [Card("วิ่งชน", "ATTACK", 5, ""), Card("ส่งเสียงน่ารำคาญ", "SKILL", 0, "")],
        "ittanmomen": [Card("รัดคอ", "ATTACK", 8, ""), Card("ผืนผ้าป้องกัน", "DEFEND", 7, "")],
        "oitekebori": [Card("เสียงเรียกจากหนองน้ำ", "SKILL", 0, ""), Card("โคลนดูด", "ATTACK", 7, "")],
        "akaname": [Card("เลียลดพลัง", "SKILL", 0, ""), Card("โจมตีด้วยความสกปรก", "ATTACK", 4, "")],
        "onibi": [Card("ลูกไฟวิญญาณ", "ATTACK", 9, ""), Card("เปลวไฟลวงตา", "DEFEND", 4, "")],
        "nopperabo": [Card("ทำให้หวาดกลัว", "SKILL", 0, ""), Card("โจมตีไม่ให้ตั้งตัว", "ATTACK", 7, "")],
        "gashadokuro": [Card("บดขยี้", "ATTACK", 15, ""), Card("กระดูกเหล็ก", "DEFEND", 9, "")]
    }
    return pools

