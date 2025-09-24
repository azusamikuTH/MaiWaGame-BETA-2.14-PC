# -*- coding: utf-8 -*-

def get_bosses():
    """
    คืน Dictionary ของบอสทั้งหมดในเกม (v5.7 Update)
    - เพิ่ม passive_skills
    - ปรับปรุงบอสลับ
    """
    bosses = {
        # --- Tier 1 (Easy) ---
        "B001": { 
            "name": "หัวหน้ากองโจร 'กระทิงดำ'", "tier": 1, "max_hp": 150, "atk": 12, "defense_stat": 8, "spd": 6, "luck": 5, "xp_reward": 100, "region_types": ["plains", "forest"],
            "moveset": [
                {"name": "ฟันดาบใหญ่", "type": "attack", "power": 1.2, "desc": "มันเหวี่ยงดาบใหญ่เข้าใส่อย่างแรง!"},
                {"name": "บัญชาการ", "type": "skill", "effect": "buff_atk", "power": 3, "cooldown": 3, "desc": "มันตะโกนสั่งการ เพิ่มพลังโจมตีให้ตัวเอง!"}
            ],
            "passive_skills": [
                {"name": "ลูกพี่ใหญ่", "trigger": "start_of_combat", "effect": "buff_def", "power": 5, "desc": "เพิ่มพลังป้องกันเมื่อเริ่มการต่อสู้"},
                {"name": "กัดไม่ปล่อย", "trigger": "on_hit", "effect": "stat_buff_on_hit", "stat": "atk", "power": 1, "desc": "เมื่อถูกโจมตี จะเพิ่มพลังโจมตีของตัวเอง"},
                {"name": "ฮึดสู้", "trigger": "low_health", "effect": "buff_atk", "power": 5, "desc": "เมื่อ HP ต่ำ จะเพิ่มพลังโจมตี"}
            ],
            "drop_table": [{"item_id": "I003", "chance": 1.0, "quantity": [1, 2]}, {"item_id": "W003", "chance": 0.1, "quantity": [1, 1]}] 
        },
        "B002": { 
            "name": "หมีป่ายักษ์ 'โอนิคุมะ'", "tier": 1, "max_hp": 200, "atk": 15, "defense_stat": 10, "spd": 4, "luck": 3, "xp_reward": 120, "region_types": ["forest", "mountain"],
            "moveset": [
                {"name": "ตะปบคลั่ง", "type": "attack", "power": 1.5, "cooldown": 2, "desc": "มันตะปบอย่างบ้าคลั่ง!"},
                {"name": "คำรามก้อง", "type": "skill", "effect": "debuff_atk", "power": 4, "cooldown": 3, "desc": "มันคำรามก้องป่า ลดพลังโจมตีของคุณ!"}
            ],
            "passive_skills": [
                {"name": "หนังหนา", "trigger": "permanent", "effect": "damage_reduction", "power": 2, "desc": "ลดความเสียหายที่ได้รับทั้งหมดลง 2 หน่วย"},
                {"name": "สัญชาตญาณสัตว์ป่า", "trigger": "on_hit", "effect": "counter_attack", "power": 0.3, "chance": 0.25, "desc": "มีโอกาสสวนกลับเมื่อถูกโจมตี"},
                {"name": "บาดเจ็บและเกรี้ยวกราด", "trigger": "low_health", "effect": "buff_atk", "power": 8, "desc": "เมื่อ HP ต่ำ จะเพิ่มพลังโจมตีอย่างมหาศาล"}
            ],
            "drop_table": [{"item_id": "I106", "chance": 1.0, "quantity": [1, 2]}, {"item_id": "I011", "chance": 0.1, "quantity": [1, 1]}] 
        },
        # --- Tier 2 (Medium) ---
        "B007": { 
            "name": "จอมทัพอาชิการุ 'ทาดาโอกิ'", "tier": 2, "max_hp": 250, "atk": 18, "defense_stat": 12, "spd": 8, "luck": 6, "xp_reward": 300, "region_types": ["plains"],
            "moveset": [
                {"name": "เพลงหอกวายุ", "type": "attack", "power": 1.2, "desc": "ปลายหอกของเขารวดเร็วจนมองไม่ทัน!"},
                {"name": "ตั้งค่ายกล", "type": "skill", "effect": "buff_def", "power": 10, "cooldown": 3, "desc": "เขาสั่งให้ทหารตั้งค่ายกล เพิ่มพลังป้องกันอย่างมหาศาล!"}
            ],
             "passive_skills": [
                {"name": "ระเบียบวินัย", "trigger": "permanent", "effect": "status_resist", "resist": ["fear", "charm"], "desc": "มีภูมิต้านทานต่อความกลัวและเสน่ห์"},
                {"name": "แม่ทัพ", "trigger": "start_of_combat", "effect": "buff_atk", "power": 5, "desc": "เพิ่มพลังโจมตีเมื่อเริ่มการต่อสู้"},
                {"name": "กลยุทธ์", "trigger": "every_3_turns", "effect": "buff_def", "power": 5, "desc": "ทุกๆ 3 เทิร์น จะเพิ่มพลังป้องกัน"}
            ],
            "drop_table": [{"item_id": "W014", "chance": 0.2, "quantity": [1, 1]}, {"item_id": "AR010", "chance": 0.1, "quantity": [1, 1]}] 
        },
        # --- Tier 3 (Main Boss) ---
        "B009": { 
            "name": "จอมทัพปีศาจ 'ชูเท็นโดจิ'", "tier": 3, "max_hp": 500, "atk": 25, "defense_stat": 15, "spd": 10, "luck": 8, "xp_reward": 1000, "region_types": ["haunted_forest"],
            "moveset": [
                {"name": "ดาบโลหิตอสูร", "type": "attack", "power": 1.5, "effect": "bleed", "duration": 3, "chance": 0.5, "desc": "ดาบของมันอาบไปด้วยเลือดและเสียงกรีดร้อง!"},
                {"name": "คลื่นพลังปีศาจ", "type": "charge", "power": 3.0, "cooldown": 4, "desc": "มันรวบรวมพลังปีศาจมหาศาลไว้ที่ดาบ!"}
            ],
            "passive_skills": [
                {"name": "เกราะปีศาจ", "trigger": "permanent", "effect": "thorns", "power": 5, "desc": "สะท้อนความเสียหายกลับไปเมื่อถูกโจมตีระยะใกล้"},
                {"name": "ราชันย์แห่งโอนิ", "trigger": "start_of_combat", "effect": "apply_status_to_player", "status": "fear", "duration": 2, "desc": "ทำให้ผู้เล่นติดสถานะหวาดกลัวเมื่อเริ่มการต่อสู้"},
                {"name": "ฟื้นฟูพลังอสูร", "trigger": "low_health", "effect": "heal", "power": 100, "desc": "เมื่อ HP ต่ำ จะฟื้นฟูพลังชีวิตตัวเอง 1 ครั้ง"}
            ],
            "drop_table": [{"item_id": "W025", "chance": 0.5, "quantity": [1, 1]}, {"item_id": "I108", "chance": 1.0, "quantity": [1, 2]}] 
        },
        # --- Tier 4 (Secret Super Boss) - Reworked ---
        "B010": { 
            "name": "จิ้งจอกเก้าหาง 'ทามาโมะ'", "tier": 4, "max_hp": 500, "atk": 20, "defense_stat": 12, "spd": 15, "luck": 10, "xp_reward": 1500, "region_types": ["haunted_forest"],
            "moveset": [
                {"name": "กรงเล็บจิ้งจอก", "type": "attack", "power": 1.0, "desc": "นางข่วนด้วยกรงเล็บที่คมกริบและว่องไว"},
                {"name": "มนต์มายาเสน่หา", "type": "attack", "power": 0.8, "effect": "charm", "duration": 2, "chance": 0.6, "cooldown": 3, "desc": "นางส่งยิ้มหวาน... จิตใจของคุณพลันว่างเปล่า!"},
                {"name": "วิญญาณคำสาป", "type": "skill", "effect": "apply_status_to_player", "status": "fear", "duration": 2, "cooldown": 4, "desc": "นางร่ายมนต์ดำ ทำให้คุณหวาดกลัวจนขยับไม่ได้"},
                {"name": "เปลวไฟจิ้งจอกสีคราม", "type": "charge", "power": 2.5, "cooldown": 4, "desc": "ลูกไฟสีครามขนาดใหญ่ปรากฏขึ้นรอบตัวนาง!"}
            ],
            "passive_skills": [
                {"name": "ดวงใจจิ้งจอก", "trigger": "on_player_level", "effect": "increase_crit_chance", "desc": "โอกาสติดคริติคอลเพิ่มขึ้น 1% ทุกๆ 1 เลเวลของผู้เล่น"},
                {"name": "ร่างมายา", "trigger": "permanent", "effect": "evade_chance", "power": 0.20, "desc": "มีโอกาส 20% ที่จะหลบการโจมตีได้"},
                {"name": "หนึ่งหาง หนึ่งชีวิต", "trigger": "on_death", "effect": "revive", "revive_count": 1, "revive_hp_percent": 0.3, "desc": "เมื่อพ่ายแพ้ จะสละ 1 หางเพื่อฟื้นคืนชีพ 1 ครั้ง"}
            ],
            "drop_table": [{"item_id": "I110", "chance": 1.0, "quantity": [1, 1]}, {"item_id": "S025", "chance": 0.2, "quantity": [1, 1]}] 
        }
    }
    return bosses

