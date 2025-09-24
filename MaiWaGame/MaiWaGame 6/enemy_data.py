# -*- coding: utf-8 -*-

def get_enemies():
    """
    คืน Dictionary ของศัตรูและปีศาจทั้งหมด
    moveset: รายการท่าโจมตีและความสามารถพิเศษของศัตรู
      - name: ชื่อท่า
      - type: 'attack' (โจมตีทันที), 'charge' (ชาร์จก่อนโจมตี), 'skill' (ใช้ความสามารถพิเศษ)
      - power: ตัวคูณความแรง หรือ ค่าพลังของสกิล
      - cooldown: จำนวนเทิร์นที่ต้องรอก่อนใช้ครั้งต่อไป
      - charge_turns: จำนวนเทิร์นที่ต้องชาร์จ
      - desc: คำอธิบายท่า
    """
    enemies = {
        # --- มนุษย์ ---
        "E001": { "name": "โจรป่า", "max_hp": 50, "atk": 6, "defense_stat": 3, "spd": 5, "luck": 3, "xp_reward": 15, "region_types": ["plains", "forest"],
                  "moveset": [
                      {"name": "ฟัน", "type": "attack", "power": 1.0, "desc": "มันเหวี่ยงดาบเข้าใส่!"},
                      {"name": "ปาหิน", "type": "attack", "power": 0.5, "desc": "มันขว้างหินใส่เพื่อก่อกวน!"}
                  ],
                  "drop_table": [ {"item_id": "I002", "chance": 0.5, "quantity": [1, 1]}, {"item_id": "I001", "chance": 0.2, "quantity": [1, 1]} ] },
        "E002": { "name": "โรนินตกอับ", "max_hp": 65, "atk": 10, "defense_stat": 4, "spd": 6, "luck": 4, "xp_reward": 25, "region_types": ["plains"],
                  "moveset": [
                      {"name": "เพลงดาบสามัญ", "type": "attack", "power": 1.0, "desc": "มันโจมตีด้วยเพลงดาบพื้นฐาน"},
                      {"name": "แทงสวน", "type": "attack", "power": 1.2, "cooldown": 2, "desc": "มันหาจังหวะแทงสวนอย่างรวดเร็ว!"}
                  ],
                  "drop_table": [ {"item_id": "I005", "chance": 0.3, "quantity": [1, 1]}, {"item_id": "W006", "chance": 0.05, "quantity": [1, 1]} ] },
        "E003": { "name": "นักรบภูเขา (ยามะบูชิ)", "max_hp": 80, "atk": 9, "defense_stat": 6, "spd": 5, "luck": 5, "xp_reward": 40, "region_types": ["mountain"],
                  "moveset": [
                      {"name": "ฟาดด้วยพลอง", "type": "attack", "power": 1.0, "desc": "มันใช้พลองฟาดเข้าใส่อย่างแรง!"},
                      {"name": "โจมตีต่อเนื่อง", "type": "attack", "power": 1.3, "cooldown": 3, "desc": "มันโจมตีต่อเนื่องอย่างดุดัน!"}
                  ],
                  "drop_table": [ {"item_id": "I010", "chance": 0.4, "quantity": [1, 2]}, {"item_id": "I013", "chance": 0.1, "quantity": [1, 1]} ] },
        "E004": { "name": "หัวหน้าโจรป่า", "max_hp": 90, "atk": 10, "defense_stat": 5, "spd": 6, "luck": 5, "xp_reward": 50, "region_types": ["plains", "forest"],
                   "moveset": [
                      {"name": "ฟันดาบ", "type": "attack", "power": 1.0, "desc": "มันฟันดาบอย่างชำนาญ"},
                      {"name": "ฟันดาบใหญ่", "type": "attack", "power": 1.5, "cooldown": 3, "desc": "มันรวบรวมพลังและฟันอย่างรุนแรง!"}
                  ],
                  "drop_table": [ {"item_id": "I003", "chance": 0.25, "quantity": [1, 1]}, {"item_id": "I004", "chance": 0.15, "quantity": [1, 1]} ] },
        "E005": { "name": "ซามูไรรับจ้าง", "max_hp": 75, "atk": 12, "defense_stat": 4, "spd": 7, "luck": 6, "xp_reward": 45, "region_types": ["plains"],
                   "moveset": [
                      {"name": "เพลงดาบไร้สำนัก", "type": "attack", "power": 1.1, "desc": "เพลงดาบของมันคาดเดาได้ยาก"},
                      {"name": "ปัดป้องโต้กลับ", "type": "attack", "power": 1.4, "cooldown": 3, "desc": "มันรอจังหวะและโต้กลับอย่างรุนแรง!"}
                  ],
                  "drop_table": [ {"item_id": "I033", "chance": 0.2, "quantity": [1, 1]}, {"item_id": "W010", "chance": 0.05, "quantity": [1, 1]} ] },
        "E006": { "name": "พลหอกอาชิการุ", "max_hp": 60, "atk": 8, "defense_stat": 4, "spd": 5, "luck": 4, "xp_reward": 20, "region_types": ["plains"],
                   "moveset": [
                      {"name": "แทงหอก", "type": "attack", "power": 1.0, "desc": "มันแทงหอกเข้ามาตรงๆ"},
                      {"name": "ตั้งแนวป้องกัน", "type": "skill", "effect": "buff_def", "power": 5, "cooldown": 2, "desc": "มันตั้งท่าป้องกัน เพิ่มพลังป้องกันชั่วคราว!"}
                  ],
                  "drop_table": [ {"item_id": "I002", "chance": 0.4, "quantity": [1, 2]}, {"item_id": "I026", "chance": 0.2, "quantity": [1, 1]} ] },
        "E007": { "name": "นินจาลอบสังหาร", "max_hp": 65, "atk": 11, "defense_stat": 3, "spd": 12, "luck": 8, "xp_reward": 60, "region_types": ["forest", "mountain", "swamp"],
                   "moveset": [
                      {"name": "มีดสั้นอาบยาพิษ", "type": "attack", "power": 0.8, "desc": "มีดของมันเคลื่อนไหวรวดเร็วจนมองไม่ทัน!"},
                      {"name": "ระเบิดควัน", "type": "skill", "effect": "debuff_acc", "power": 0, "cooldown": 3, "desc": "มันขว้างระเบิดควัน ทำให้การโจมตีครั้งต่อไปของคุณพลาดเป้า!"}
                  ],
                  "drop_table": [ {"item_id": "I021", "chance": 0.3, "quantity": [1, 3]}, {"item_id": "I020", "chance": 0.15, "quantity": [1, 1]} ] },
        "E008": { "name": "องเมียวจิฝึกหัด", "max_hp": 55, "atk": 10, "defense_stat": 2, "spd": 6, "luck": 7, "xp_reward": 35, "region_types": ["plains"],
                   "moveset": [
                      {"name": "ยันต์เพลิง", "type": "attack", "power": 1.2, "desc": "มันร่ายยันต์เรียกเปลวไฟโจมตี!"},
                      {"name": "ยันต์ป้องกัน", "type": "skill", "effect": "buff_def", "power": 4, "cooldown": 2, "desc": "มันร่ายยันต์ป้องกันตัวเอง!"}
                  ],
                  "drop_table": [ {"item_id": "I013", "chance": 0.25, "quantity": [1, 1]}, {"item_id": "I031", "chance": 0.4, "quantity": [1, 2]} ] },
        "E009": { "name": "นักบวชโซเฮย์", "max_hp": 85, "atk": 10, "defense_stat": 6, "spd": 6, "luck": 5, "xp_reward": 55, "region_types": ["mountain"],
                   "moveset": [
                      {"name": "ฟาดด้วยง้าว", "type": "attack", "power": 1.0, "desc": "มันใช้ง้าวนากินาตะโจมตีเป็นวงกว้าง"},
                      {"name": "สมาธิเหล็ก", "type": "skill", "effect": "buff_def", "power": 8, "cooldown": 3, "desc": "มันทำสมาธิ เพิ่มพลังป้องกันอย่างมหาศาล!"}
                  ],
                  "drop_table": [ {"item_id": "I010", "chance": 0.3, "quantity": [1, 2]}, {"item_id": "I018", "chance": 0.15, "quantity": [1, 1]} ] },
        
        # --- สัตว์ ---
        "A001": { "name": "หมาป่า", "max_hp": 40, "atk": 8, "defense_stat": 1, "spd": 8, "luck": 5, "xp_reward": 10, "region_types": ["forest", "mountain"],
                  "moveset": [
                      {"name": "กัด", "type": "attack", "power": 1.0, "desc": "มันกระโจนเข้ากัด!"},
                      {"name": "ข่วน", "type": "attack", "power": 0.8, "desc": "มันใช้กรงเล็บข่วนอย่างรวดเร็ว"}
                  ],
                  "drop_table": [ {"item_id": "I052", "chance": 0.6, "quantity": [1, 2]} ] },
        "A002": { "name": "หมูป่ายักษ์", "max_hp": 90, "atk": 12, "defense_stat": 5, "spd": 4, "luck": 2, "xp_reward": 30, "region_types": ["forest"],
                  "moveset": [
                      {"name": "พุ่งชน", "type": "charge", "power": 2.0, "cooldown": 3, "charge_turns": 1, "desc": "มันกระทืบเท้า เตรียมพุ่งเข้าชน!"}
                  ],
                  "drop_table": [ {"item_id": "I052", "chance": 0.8, "quantity": [2, 4]} ] },
        "A003": { "name": "หมีป่า", "max_hp": 100, "atk": 13, "defense_stat": 6, "spd": 4, "luck": 3, "xp_reward": 40, "region_types": ["forest", "mountain"],
                   "moveset": [
                      {"name": "ตะปบ", "type": "attack", "power": 1.2, "desc": "อุ้งเท้าอันทรงพลังของมันตะปบเข้าใส่!"},
                      {"name": "คำรามขู่", "type": "skill", "effect": "debuff_atk", "power": 2, "cooldown": 2, "desc": "มันคำรามเสียงดัง ลดพลังโจมตีของคุณชั่วคราว!"}
                  ],
                  "drop_table": [ {"item_id": "I052", "chance": 0.8, "quantity": [3, 5]} ] },
        "A004": { "name": "งูยักษ์", "max_hp": 70, "atk": 9, "defense_stat": 3, "spd": 7, "luck": 5, "xp_reward": 28, "region_types": ["swamp", "forest"],
                  "moveset": [
                      {"name": "ฉก", "type": "attack", "power": 1.0, "desc": "มันฉกอย่างรวดเร็ว!"},
                      {"name": "รัด", "type": "attack", "power": 0.8, "cooldown": 2, "desc": "มันพยายามจะรัดคุณ!"}
                  ],
                  "drop_table": [ {"item_id": "I052", "chance": 0.5, "quantity": [1, 3]}, {"item_id": "I022", "chance": 0.1, "quantity": [1, 1]} ] },
        "A005": { "name": "จิ้งจอกเจ้าเล่ห์ (Kitsune)", "max_hp": 60, "atk": 10, "defense_stat": 3, "spd": 9, "luck": 9, "xp_reward": 50, "region_types": ["forest", "haunted_forest"],
                   "moveset": [
                      {"name": "เปลวไฟจิ้งจอก", "type": "attack", "power": 1.2, "desc": "เปลวไฟสีฟ้าพุ่งเข้าใส่คุณ!"},
                      {"name": "สร้างภาพลวงตา", "type": "skill", "effect": "debuff_acc", "power": 0, "cooldown": 2, "desc": "มันสร้างภาพลวงตา ทำให้การโจมตีครั้งต่อไปของคุณพลาดเป้า!"}
                  ],
                  "drop_table": [ {"item_id": "I016", "chance": 0.2, "quantity": [1, 1]}, {"item_id": "I028", "chance": 0.02, "quantity": [1, 1]} ] },
        "A006": { "name": "ตะขาบยักษ์ (Ōmukade)", "max_hp": 80, "atk": 11, "defense_stat": 7, "spd": 5, "luck": 4, "xp_reward": 60, "region_types": ["mountain"],
                   "moveset": [
                      {"name": "กัดกิน", "type": "attack", "power": 1.1, "desc": "เขี้ยวอันน่าสยดสยองของมันพุ่งเข้าใส่!"},
                      {"name": "เกราะไคติน", "type": "skill", "effect": "buff_def", "power": 6, "cooldown": 3, "desc": "มันขดตัว เพิ่มพลังป้องกัน!"}
                  ],
                  "drop_table": [ {"item_id": "I051", "chance": 0.4, "quantity": [1, 2]}, {"item_id": "I022", "chance": 0.15, "quantity": [1, 1]} ] },
        "A007": { "name": "เหยี่ยวภูเขา", "max_hp": 45, "atk": 9, "defense_stat": 2, "spd": 11, "luck": 6, "xp_reward": 18, "region_types": ["mountain"],
                  "moveset": [{"name": "โฉบโจมตี", "type": "attack", "power": 1.0, "desc": "มันโฉบลงมาจากท้องฟ้าอย่างรวดเร็ว!"}],
                  "drop_table": [ {"item_id": "I054", "chance": 0.3, "quantity": [1, 3]} ] },
        "A008": { "name": "ลิงภูเขา", "max_hp": 40, "atk": 7, "defense_stat": 3, "spd": 8, "luck": 6, "xp_reward": 12, "region_types": ["mountain"],
                   "moveset": [
                      {"name": "ขว้างของ", "type": "attack", "power": 0.7, "desc": "มันขว้างก้อนหินและผลไม้ใส่!"},
                      {"name": "ข่วนหน้า", "type": "attack", "power": 1.0, "desc": "มันกระโดดเข้าข่วน!"}
                  ],
                  "drop_table": [ {"item_id": "I008", "chance": 0.4, "quantity": [1, 1]} ] },

        # --- ปีศาจ (โยไค) ---
        "Y001": { "name": "กัปปะ (Kappa)", "max_hp": 70, "atk": 9, "defense_stat": 5, "spd": 8, "luck": 6, "xp_reward": 70, "region_types": ["swamp"],
                   "moveset": [
                      {"name": "ดึงลงน้ำ", "type": "attack", "power": 1.0, "desc": "มันพยายามจะดึงขาคุณ!"},
                      {"name": "ขว้างแตงกวา", "type": "attack", "power": 0.6, "desc": "มันขว้างแตงกวาเน่าๆ ใส่!"}
                  ],
                  "drop_table": [ {"item_id": "I009", "chance": 0.5, "quantity": [1, 1]}, {"item_id": "I035", "chance": 0.15, "quantity": [1, 1]} ] },
        "Y002": { "name": "โอนิ (Oni)", "max_hp": 120, "atk": 15, "defense_stat": 8, "spd": 3, "luck": 3, "xp_reward": 150, "region_types": ["mountain", "haunted_forest"],
                  "moveset": [
                      {"name": "ทุบด้วยคานาโบ", "type": "attack", "power": 1.0, "desc": "มันเหวี่ยงกระบองเหล็กเข้าใส่อย่างบ้าคลั่ง!"},
                      {"name": "กระทืบปฐพี", "type": "charge", "power": 2.5, "cooldown": 4, "charge_turns": 1, "desc": "มันยกเท้าขึ้นสูง เตรียมกระทืบพื้นดินอย่างรุนแรง!"}
                  ],
                  "drop_table": [ {"item_id": "I005", "chance": 0.4, "quantity": [1, 3]}, {"item_id": "I055", "chance": 0.1, "quantity": [1, 1]} ] },
        "Y003": { "name": "เท็งงุ (Tengu)", "max_hp": 85, "atk": 11, "defense_stat": 4, "spd": 10, "luck": 7, "xp_reward": 120, "region_types": ["mountain", "forest"],
                  "moveset": [
                      {"name": "ดาบวายุ", "type": "attack", "power": 1.1, "desc": "เพลงดาบของมันรวดเร็วดั่งสายลม!"},
                      {"name": "พัดวายุ", "type": "attack", "power": 1.3, "cooldown": 3, "desc": "มันใช้พัดสร้างลมพายุพัดเข้าใส่!"}
                  ],
                  "drop_table": [ {"item_id": "I019", "chance": 0.2, "quantity": [1, 2]}, {"item_id": "I042", "chance": 0.1, "quantity": [1, 1]} ] },
        "Y004": { "name": "ยูเร (Yurei)", "max_hp": 50, "atk": 7, "defense_stat": 2, "spd": 7, "luck": 5, "xp_reward": 40, "region_types": ["haunted_forest"],
                  "moveset": [
                      {"name": "สัมผัสเยือกแข็ง", "type": "attack", "power": 1.0, "desc": "สัมผัสของมันทำให้รู้สึกหนาวเหน็บไปถึงกระดูก"},
                      {"name": "เสียงกรีดร้อง", "type": "skill", "effect": "debuff_atk", "power": 3, "cooldown": 2, "desc": "เสียงกรีดร้องของมันทำให้คุณเสียขวัญ ลดพลังโจมตีชั่วคราว!"}
                  ],
                  "drop_table": [ {"item_id": "I018", "chance": 0.2, "quantity": [1, 1]}, {"item_id": "I047", "chance": 0.05, "quantity": [1, 1]} ] },
        "Y005": { "name": "คาไมทาจิ (Kamaitachi)", "max_hp": 55, "atk": 9, "defense_stat": 2, "spd": 15, "luck": 8, "xp_reward": 65, "region_types": ["plains"],
                  "moveset": [{"name": "คมมีดสายลม", "type": "attack", "power": 1.0, "desc": "มันเคลื่อนไหวเร็วมากจนเห็นเป็นเพียงสายลมที่กรีดผ่าน!"}],
                  "drop_table": [ {"item_id": "I019", "chance": 0.3, "quantity": [1, 1]}, {"item_id": "I004", "chance": 0.15, "quantity": [1, 1]} ] },
        "Y006": { "name": "สึจิกุโมะ (Tsuchigumo)", "max_hp": 95, "atk": 11, "defense_stat": 7, "spd": 4, "luck": 5, "xp_reward": 90, "region_types": ["mountain", "forest"],
                   "moveset": [
                      {"name": "ขาแมงมุม", "type": "attack", "power": 1.0, "desc": "ขาอันแหลมคมของมันแทงเข้าใส่!"},
                      {"name": "พ่นใย", "type": "skill", "effect": "debuff_spd", "power": 3, "cooldown": 2, "desc": "มันพ่นใยเหนียวหนืด ลดความเร็วของคุณ!"}
                  ],
                  "drop_table": [ {"item_id": "I054", "chance": 0.6, "quantity": [2, 5]}, {"item_id": "I022", "chance": 0.2, "quantity": [1, 1]} ] },
        "Y007": { "name": "เนะโกะมาตะ (Nekomata)", "max_hp": 65, "atk": 9, "defense_stat": 4, "spd": 9, "luck": 8, "xp_reward": 75, "region_types": ["plains", "haunted_forest"],
                   "moveset": [
                      {"name": "กรงเล็บวิญญาณ", "type": "attack", "power": 1.0, "desc": "มันข่วนด้วยกรงเล็บที่ลุกเป็นไฟสีฟ้า!"},
                      {"name": "คำสาปแมว", "type": "skill", "effect": "debuff_luck", "power": 3, "cooldown": 3, "desc": "มันจ้องเขม็งมาที่คุณ ทำให้คุณรู้สึกโชคร้าย!"}
                  ],
                  "drop_table": [ {"item_id": "I007", "chance": 0.4, "quantity": [1, 2]}, {"item_id": "I048", "chance": 0.05, "quantity": [1, 1]} ] },
        "Y008": { "name": "โรคุโรคุบิ (Rokurokubi)", "max_hp": 70, "atk": 8, "defense_stat": 5, "spd": 6, "luck": 6, "xp_reward": 60, "region_types": ["plains"],
                  "moveset": [{"name": "คอเหวี่ยงฟาด", "type": "attack", "power": 1.2, "cooldown": 1, "desc": "คอมันยืดยาวออกมาแล้วเหวี่ยงฟาด!"}],
                  "drop_table": [ {"item_id": "I046", "chance": 0.03, "quantity": [1, 1]} ] },
        "Y009": { "name": "นูริคาเบะ (Nurikabe)", "max_hp": 110, "atk": 7, "defense_stat": 12, "spd": 2, "luck": 2, "xp_reward": 80, "region_types": ["haunted_forest"],
                   "moveset": [
                      {"name": "กระแทก", "type": "attack", "power": 1.0, "desc": "มันกระแทกด้วยร่างกายที่เป็นหิน!"},
                      {"name": "กำแพงศิลา", "type": "skill", "effect": "buff_def", "power": 10, "cooldown": 2, "desc": "มันเปลี่ยนร่างเป็นกำแพงหินที่แข็งแกร่ง!"}
                  ],
                  "drop_table": [ {"item_id": "I051", "chance": 0.7, "quantity": [1, 3]} ] },
        "Y010": { "name": "คาราคาซะ-โอบาเกะ (Karakasa-obake)", "max_hp": 50, "atk": 7, "defense_stat": 4, "spd": 7, "luck": 7, "xp_reward": 30, "region_types": ["haunted_forest"],
                  "moveset": [{"name": "กระโดดทับ", "type": "attack", "power": 1.0, "desc": "มันกระโดดทับด้วยขาเดียว!"}],
                  "drop_table": [ {"item_id": "I053", "chance": 0.3, "quantity": [1, 2]} ] },
        "Y011": { "name": "โจโรกุโมะ (Jorōgumo)", "max_hp": 85, "atk": 10, "defense_stat": 6, "spd": 7, "luck": 7, "xp_reward": 110, "region_types": ["forest", "haunted_forest"],
                   "moveset": [
                      {"name": "เขี้ยวพิษ", "type": "attack", "power": 1.0, "desc": "มันกัดด้วยเขี้ยวอาบยาพิษ!"},
                      {"name": "ล่อลวง", "type": "skill", "effect": "debuff_def", "power": 4, "cooldown": 3, "desc": "มันแปลงร่างเป็นหญิงงาม ทำให้คุณใจอ่อน!"}
                  ],
                  "drop_table": [ {"item_id": "I022", "chance": 0.25, "quantity": [1, 1]}, {"item_id": "I048", "chance": 0.1, "quantity": [1, 1]} ] },
        "Y012": { "name": "ยูกิอนนะ (Yuki-onna)", "max_hp": 75, "atk": 11, "defense_stat": 3, "spd": 8, "luck": 6, "xp_reward": 100, "region_types": ["mountain"],
                  "moveset": [{"name": "ลมหายใจเยือกแข็ง", "type": "attack", "power": 1.3, "cooldown": 2, "desc": "ลมหายใจของนางทำให้ทุกอย่างกลายเป็นน้ำแข็ง!"}],
                  "drop_table": [ {"item_id": "I027", "chance": 0.15, "quantity": [1, 1]} ] },
        "Y013": { "name": "โคดามะ (Kodama)", "max_hp": 40, "atk": 5, "defense_stat": 5, "spd": 6, "luck": 8, "xp_reward": 20, "region_types": ["forest"],
                  "moveset": [{"name": "เสียงสะท้อนในป่า", "type": "skill", "effect": "heal", "power": 10, "cooldown": 3, "desc": "มันส่งเสียงแปลกๆ ฟื้นฟูพลังให้ตัวเอง!"}],
                  "drop_table": [ {"item_id": "I012", "chance": 0.5, "quantity": [1, 3]} ] },
        "Y014": { "name": "บาเกะ-โซริ (Bake-zōri)", "max_hp": 30, "atk": 6, "defense_stat": 2, "spd": 8, "luck": 5, "xp_reward": 10, "region_types": ["plains"],
                  "moveset": [{"name": "วิ่งชน", "type": "attack", "power": 1.0, "desc": "รองเท้าฟางเก่าๆ วิ่งเข้าชนคุณ!"}],
                  "drop_table": [ {"item_id": "I054", "chance": 0.2, "quantity": [1, 2]} ] },
        "Y015": { "name": "อิตตัน-โมเมน (Ittan-momen)", "max_hp": 60, "atk": 8, "defense_stat": 4, "spd": 9, "luck": 6, "xp_reward": 50, "region_types": ["haunted_forest"],
                   "moveset": [{"name": "รัดคอ", "type": "attack", "power": 1.2, "cooldown": 1, "desc": "ผืนผ้าพุ่งเข้ามาพัวพันรอบตัวคุณ!"}],
                  "drop_table": [ {"item_id": "I054", "chance": 0.7, "quantity": [2, 4]} ] },
        "Y016": { "name": "โออิเตะเกโบริ (Oiteke-bori)", "max_hp": 65, "atk": 9, "defense_stat": 6, "spd": 4, "luck": 5, "xp_reward": 55, "region_types": ["swamp"],
                   "moveset": [
                      {"name": "โคลนดูด", "type": "attack", "power": 1.0, "desc": "มันสาดโคลนใส่คุณ!"},
                      {"name": "เสียงเรียกจากหนองน้ำ", "type": "skill", "effect": "debuff_spd", "power": 4, "cooldown": 3, "desc": "เสียงของมันทำให้คุณเคลื่อนไหวช้าลง!"}
                  ],
                  "drop_table": [ {"item_id": "I007", "chance": 0.3, "quantity": [1, 3]} ] },
        "Y017": { "name": "อาคานาเมะ (Akaname)", "max_hp": 45, "atk": 5, "defense_stat": 3, "spd": 7, "luck": 4, "xp_reward": 25, "region_types": ["swamp", "haunted_forest"],
                  "moveset": [{"name": "เลียลดพลัง", "type": "skill", "effect": "debuff_def", "power": 3, "cooldown": 1, "desc": "ลิ้นที่ยาวของมันเลียคุณ ทำให้เกราะอ่อนแอลง!"}],
                  "drop_table": [ {"item_id": "I001", "chance": 0.1, "quantity": [1, 1]} ] },
        "Y018": { "name": "โอนิบิ (Onibi)", "max_hp": 50, "atk": 10, "defense_stat": 1, "spd": 9, "luck": 7, "xp_reward": 45, "region_types": ["haunted_forest", "swamp"],
                  "moveset": [{"name": "ลูกไฟวิญญาณ", "type": "attack", "power": 1.1, "desc": "ลูกไฟวิญญาณพุ่งเข้าใส่!"}],
                  "drop_table": [ {"item_id": "I056", "chance": 0.5, "quantity": [1, 3]}, {"item_id": "I024", "chance": 0.1, "quantity": [1, 1]} ] },
        "Y019": { "name": "โนปเประโบ (Noppera-bō)", "max_hp": 60, "atk": 7, "defense_stat": 4, "spd": 7, "luck": 8, "xp_reward": 50, "region_types": ["plains", "haunted_forest"],
                   "moveset": [{"name": "ทำให้หวาดกลัว", "type": "skill", "effect": "debuff_atk", "power": 4, "cooldown": 2, "desc": "ใบหน้าที่ว่างเปล่าของมันทำให้คุณหวาดกลัว!"}],
                  "drop_table": [ {"item_id": "I020", "chance": 0.15, "quantity": [1, 1]} ] },
        "Y020": { "name": "กาชาโดคุโระ (Gashadokuro)", "max_hp": 200, "atk": 18, "defense_stat": 10, "spd": 3, "luck": 1, "xp_reward": 300, "region_types": ["haunted_forest"],
                   "moveset": [
                      {"name": "บดขยี้", "type": "attack", "power": 1.2, "desc": "โครงกระดูกมหึมาพยายามจะบดขยี้คุณ!"},
                      {"name": "คำรามก้อง", "type": "charge", "power": 2.0, "cooldown": 4, "charge_turns": 1, "desc": "มันอ้าปากกว้าง เตรียมคำรามก้อง!"}
                  ],
                  "drop_table": [ {"item_id": "I050", "chance": 0.2, "quantity": [1, 1]}, {"item_id": "I011", "chance": 0.3, "quantity": [1, 1]} ] }
    }
    return enemies
