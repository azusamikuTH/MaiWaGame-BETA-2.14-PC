# -*- coding: utf-8 -*-

def get_items():
    """
    คืน Dictionary ของไอเทมสิ้นเปลืองทั้งหมดในเกม
    type: 
    - HEAL: ฟื้นฟูพลังชีวิต
    - BUFF_ATK: เพิ่มพลังโจมตีชั่วคราว
    - BUFF_DEF: เพิ่มพลังป้องกันชั่วคราว
    - CURE: รักษาอาการผิดปกติ
    - UTILITY: ไอเทมใช้งานพิเศษ
    - ATTACK: ไอเทมสำหรับโจมตี
    - VALUABLE: ของมีค่าสำหรับขาย
    - CRAFT: วัตถุดิบสำหรับสร้างของ
    """
    items = {
        # --- ไอเทมพื้นฐาน (I001 - I056) ---
        "I001": { "name": "ยาฟื้นฟูชั้นเลว (ขวด)", "type": "HEAL", "value": 20, "desc": "ฟื้นฟู HP 20 หน่วย", "price": 25, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I002": { "name": "ข้าวปั้น", "type": "HEAL", "value": 10, "desc": "ฟื้นฟู HP 10 หน่วย ช่วยประทังความหิว", "price": 10, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I003": { "name": "ยาฟื้นฟูชั้นดี (ขวด)", "type": "HEAL", "value": 50, "desc": "ฟื้นฟู HP 50 หน่วย", "price": 60, "sale_locations": ["ตลาด", "ร้านค้าเล็กๆ"] },
        "I004": { "name": "หินลับมีด", "type": "BUFF_ATK", "value": 5, "desc": "เพิ่มพลังโจมตี +5 ในการต่อสู้ครั้งต่อไป", "price": 40, "sale_locations": ["ร้านค้าเล็กๆ", "โรงตีดาบ"] },
        "I005": { "name": "เหล้าสาเก (จอก)", "type": "BUFF_ATK", "value": 8, "desc": "เพิ่ม ATK +8 แต่ลด DEF -3 ในการต่อสู้ครั้งต่อไป", "price": 30, "sale_locations": ["ร้านค้าเล็กๆ", "ตลาด"] },
        "I006": { "name": "สมุนไพรหายาก", "type": "HEAL", "value": 100, "desc": "ฟื้นฟู HP 100 หน่วย", "price": 150, "sale_locations": ["ตลาด"] },
        "I007": { "name": "ปลาแห้ง", "type": "HEAL", "value": 15, "desc": "ฟื้นฟู HP 15 หน่วย", "price": 12, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I008": { "name": "ดังโงะ", "type": "HEAL", "value": 8, "desc": "ฟื้นฟู HP 8 หน่วย ของว่างยามเดินทาง", "price": 7, "sale_locations": ["ร้านค้าเล็กๆ", "ตลาด"] },
        "I009": { "name": "น้ำเต้าบรรจุน้ำ", "type": "HEAL", "value": 5, "desc": "ฟื้นฟู HP 5 หน่วย ดับกระหาย", "price": 5, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I010": { "name": "ชุดสมุนไพร", "type": "HEAL", "value": 35, "desc": "ฟื้นฟู HP 35 หน่วย", "price": 40, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I011": { "name": "ยาฟื้นฟูชั้นเลิศ (ขวด)", "type": "HEAL", "value": 200, "desc": "ฟื้นฟู HP 200 หน่วย หรือชุบชีวิตเมื่อตาย (ใช้โดยอัตโนมัติ)", "price": 500, "sale_locations": [] },
        "I012": { "name": "รากไม้ทนทายาด", "type": "HEAL", "value": 25, "desc": "ฟื้นฟู HP 25 หน่วย มีรสขม", "price": 30, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I013": { "name": "ยันต์พิทักษ์", "type": "BUFF_DEF", "value": 5, "desc": "เพิ่มพลังป้องกัน +5 ในการต่อสู้ครั้งต่อไป", "price": 40, "sale_locations": ["ตลาด"] },
        "I014": { "name": "น้ำมันสน", "type": "BUFF_ATK", "value": 3, "desc": "เพิ่มพลังโจมตี +3 เป็นเวลา 3 เทิร์นในการต่อสู้ครั้งต่อไป", "price": 50, "sale_locations": ["ตลาด", "โรงตีดาบ"] },
        "I015": { "name": "เกราะหนังชุบแข็ง", "type": "BUFF_DEF", "value": 10, "desc": "เพิ่มพลังป้องกัน +10 แต่ลดความเร็ว -2 ในการต่อสู้ครั้งต่อไป", "price": 70, "sale_locations": ["โรงตีดาบ"] },
        "I016": { "name": "เครื่องรางนำโชค", "type": "UTILITY", "value": 5, "desc": "เพิ่มค่า Luck +5 ในการต่อสู้ครั้งต่อไป", "price": 100, "sale_locations": ["ตลาด"] },
        "I017": { "name": "ยาดุดัน", "type": "BUFF_ATK", "value": 12, "desc": "เพิ่มพลังโจมตี +12 ในเทิร์นแรกของการต่อสู้", "price": 60, "sale_locations": ["ตลาด"] },
        "I018": { "name": "ยาทนทรหด", "type": "BUFF_DEF", "value": 8, "desc": "เพิ่มพลังป้องกัน +8 ในการต่อสู้ครั้งต่อไป", "price": 60, "sale_locations": ["โรงตีดาบ"] },
        "I019": { "name": "เมล็ดพืชว่องไว", "type": "UTILITY", "value": 5, "desc": "เพิ่มค่า Speed +5 ในการต่อสู้ครั้งต่อไป", "price": 50, "sale_locations": ["ตลาด"] },
        "I020": { "name": "ระเบิดควัน", "type": "UTILITY", "value": 0, "desc": "ใช้เพื่อหลบหนีออกจากการต่อสู้", "price": 80, "sale_locations": ["ตลาด"] },
        "I021": { "name": "ดาวกระจาย (ชูริเคน)", "type": "ATTACK", "value": 10, "desc": "สร้างความเสียหาย 10 หน่วยแก่ศัตรู 1 ตัว", "price": 30, "sale_locations": ["ตลาด"] },
        "I022": { "name": "ยาพิษ (ขวด)", "type": "UTILITY", "value": 3, "desc": "เคลือบอาวุธ ทำให้การโจมตีครั้งต่อไปติดสถานะพิษ", "price": 120, "sale_locations": ["ตลาด"] },
        "I023": { "name": "ตะปูเรือใบ (มาคิบิชิ)", "type": "UTILITY", "value": 5, "desc": "สร้างความเสียหาย 5 หน่วยแก่ศัตรูที่โจมตีเข้ามา", "price": 40, "sale_locations": ["ตลาด"] },
        "I024": { "name": "ดินประสิว", "type": "ATTACK", "value": 15, "desc": "สร้างความเสียหาย 15 หน่วยแก่ศัตรูทั้งหมด", "price": 100, "sale_locations": ["ตลาด"] },
        "I025": { "name": "ยาถอนพิษ", "type": "CURE", "value": 0, "desc": "รักษาอาการพิษ", "price": 30, "sale_locations": ["ร้านค้าเล็กๆ", "ตลาด"] },
        "I026": { "name": "ผ้าพันแผลสะอาด", "type": "CURE", "value": 0, "desc": "รักษาอาการเลือดไหล", "price": 20, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I027": { "name": "ยันต์ชำระล้าง", "type": "CURE", "value": 0, "desc": "รักษาทุกอาการผิดปกติ", "price": 150, "sale_locations": ["ตลาด"] },
        "I028": { "name": "แผนที่สมบัติ (เศษเสี้ยว)", "type": "UTILITY", "value": 0, "desc": "ชิ้นส่วนของแผนที่ลึกลับ...?", "price": 200, "sale_locations": [] },
        "I029": { "name": "ตราตระกูลที่มัวหมอง", "type": "UTILITY", "value": 0, "desc": "ของดูต่างหน้าชิ้นสุดท้ายที่เหลืออยู่", "price": 0, "sale_locations": [] },
        "I030": { "name": "ลูกเต๋าโกง", "type": "UTILITY", "value": 0, "desc": "ดูเหมือนจะทำให้โชคดีขึ้นเล็กน้อย", "price": 300, "sale_locations": ["ตลาด"] },
        "I031": { "name": "คัมภีร์เปล่า", "type": "UTILITY", "value": 0, "desc": "กระดาษคุณภาพดีสำหรับจดบันทึก", "price": 15, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I032": { "name": "ถ่านหิน", "type": "UTILITY", "value": 0, "desc": "สำหรับเขียนหรือวาดภาพ", "price": 5, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I033": { "name": "หินลับมีดอย่างดี", "type": "BUFF_ATK", "value": 10, "desc": "เพิ่มพลังโจมตี +10 ในการต่อสู้ครั้งต่อไป", "price": 90, "sale_locations": ["โรงตีดาบ"] },
        "I034": { "name": "ชุดเครื่องมือซ่อมแซม", "type": "UTILITY", "value": 0, "desc": "สำหรับซ่อมแซมอาวุธ (ยังใช้งานไม่ได้)", "price": 120, "sale_locations": ["โรงตีดาบ"] },
        "I035": { "name": "น้ำมนต์ศักดิ์สิทธิ์", "type": "HEAL", "value": 30, "desc": "ฟื้นฟู HP 30 หน่วย และรักษาอาการผิดปกติ", "price": 100, "sale_locations": ["ตลาด"] },
        "I036": { "name": "ยาอายุวัฒนะ (ปลอม)", "type": "UTILITY", "value": 0, "desc": "พ่อค้าบอกว่าทำให้เป็นอมตะ... แต่ดูไม่น่าเชื่อถือ", "price": 1000, "sale_locations": ["ตลาด"] },
        "I037": { "name": "สมุนไพรบด", "type": "HEAL", "value": 30, "desc": "ฟื้นฟู HP 30 หน่วย", "price": 35, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I038": { "name": "ซุปมิโสะร้อน", "type": "HEAL", "value": 20, "desc": "ฟื้นฟู HP 20 หน่วย", "price": 20, "sale_locations": ["ร้านค้าเล็กๆ", "ตลาด"] },
        "I039": { "name": "น้ำจากบ่อน้ำพุร้อน", "type": "HEAL", "value": 40, "desc": "ฟื้นฟู HP 40 หน่วย มีสรรพคุณทางยา", "price": 50, "sale_locations": ["ตลาด"] },
        "I040": { "name": "เครื่องรางหิน不動", "type": "BUFF_DEF", "value": 7, "desc": "เพิ่มพลังป้องกัน +7 ในการต่อสู้ครั้งต่อไป", "price": 55, "sale_locations": ["ตลาด"] },
        "I041": { "name": "ผ้าคาดหัวฮะชิมาขิ", "type": "BUFF_ATK", "value": 4, "desc": "เพิ่มพลังโจมตี +4 ด้วยจิตวิญญาณนักสู้", "price": 45, "sale_locations": ["ร้านค้าเล็กๆ", "โรงตีดาบ"] },
        "I042": { "name": "ยันต์วายุ", "type": "UTILITY", "value": 8, "desc": "เพิ่มค่า Speed +8 ในการต่อสู้ครั้งต่อไป", "price": 60, "sale_locations": ["ตลาด"] },
        "I043": { "name": "ผงพริกไทย", "type": "UTILITY", "value": 0, "desc": "ขว้างใส่ศัตรูเพื่อลดความแม่นยำ (ยังใช้งานไม่ได้)", "price": 35, "sale_locations": ["ตลาด"] },
        "I044": { "name": "น้ำมันตะเกียง", "type": "UTILITY", "value": 0, "desc": "เชื้อเพลิง สามารถใช้ร่วมกับไฟได้ (ยังใช้งานไม่ได้)", "price": 20, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I045": { "name": "ลูกข่างเหล็ก", "type": "ATTACK", "value": 12, "desc": "ขว้างโจมตีศัตรู สร้างความเสียหาย 12 หน่วย", "price": 40, "sale_locations": ["ตลาด"] },
        "I046": { "name": "กิ๊บติดผมทำจากหยก", "type": "VALUABLE", "value": 250, "desc": "ของมีค่า ขายได้ราคาสูง", "price": 0, "sale_locations": [] },
        "I047": { "name": "ม้วนสารปิดผนึก", "type": "UTILITY", "value": 0, "desc": "จดหมายสำคัญที่ยังไม่ได้เปิดอ่าน", "price": 0, "sale_locations": [] },
        "I048": { "name": "ผ้าไหมชั้นดี", "type": "VALUABLE", "value": 150, "desc": "ผ้าไหมเนื้อดีจากต่างแดน", "price": 0, "sale_locations": [] },
        "I049": { "name": "ขลุ่ยไม้ไผ่", "type": "UTILITY", "value": 0, "desc": "เสียงของมันช่วยให้จิตใจสงบ", "price": 50, "sale_locations": ["ตลาด"] },
        "I050": { "name": "ก้อนทองคำเล็กๆ", "type": "VALUABLE", "value": 500, "desc": "ทองคำบริสุทธิ์ ขายได้ราคาสูงมาก", "price": 0, "sale_locations": [] },
        "I051": { "name": "เศษเหล็ก", "type": "CRAFT", "value": 0, "desc": "วัตถุดิบสำหรับตีเหล็ก", "price": 15, "sale_locations": ["โรงตีดาบ"] },
        "I052": { "name": "หนังสัตว์", "type": "CRAFT", "value": 0, "desc": "วัตถุดิบสำหรับทำเครื่องหนัง", "price": 20, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I053": { "name": "ไม้เนื้อแข็ง", "type": "CRAFT", "value": 0, "desc": "วัตถุดิบสำหรับงานไม้", "price": 10, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I054": { "name": "เส้นด้าย", "type": "CRAFT", "value": 0, "desc": "วัตถุดิบสำหรับเย็บผ้า", "price": 5, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "I055": { "name": "เหล็กทามะฮางาเนะ", "type": "CRAFT", "value": 0, "desc": "เหล็กชั้นดีสำหรับตีดาบคาตานะ", "price": 200, "sale_locations": ["โรงตีดาบ"] },
        "I056": { "name": "ถ่านไม้", "type": "CRAFT", "value": 0, "desc": "เชื้อเพลิงสำคัญสำหรับช่างตีดาบ", "price": 8, "sale_locations": ["โรงตีดาบ", "ร้านค้าเล็กๆ"] },

        # --- วัตถุดิบสร้างของใหม่ (I101+) ---
        "I101": { "name": "แก่นวิญญาณโยไค", "type": "CRAFT", "desc": "พลังงานที่ตกค้างจากโยไคที่ถูกกำจัด", "price": 0, "sale_locations": [] },
        "I102": { "name": "ผลึกวายุ", "type": "CRAFT", "desc": "ผลึกที่กักเก็บพลังแห่งสายลม (จากเท็งงุ, คาไมทาจิ)", "price": 0, "sale_locations": [] },
        "I103": { "name": "เหล็กกล้าไร้สนิม", "type": "CRAFT", "desc": "เหล็กพิเศษที่ทนทานและคมเป็นพิเศษ", "price": 0, "sale_locations": [] },
        "I104": { "name": "กำมะถันปีศาจ", "type": "CRAFT", "desc": "ผงกำมะถันจากบริเวณที่โอนิอาศัยอยู่", "price": 0, "sale_locations": [] },
        "I105": { "name": "ขนนกเท็งงุ", "type": "CRAFT", "desc": "ขนนกสีดำขลับที่สามารถสร้างลมได้", "price": 0, "sale_locations": [] },
        "I106": { "name": "ขนหมีโอนิคุมะ", "type": "CRAFT", "desc": "ขนของหมีป่ายักษ์ ทนทานและให้ความอบอุ่น", "price": 0, "sale_locations": [] },
        "I107": { "name": "ใบพัดสายลม", "type": "CRAFT", "desc": "วัตถุดิบสำหรับสร้างของเกี่ยวกับความเร็ว", "price": 0, "sale_locations": [] },
        "I108": { "name": "เขาโอนิ", "type": "CRAFT", "desc": "เขาที่หักของยักษ์โอนิ แข็งแกร่งดุจหินผา", "price": 0, "sale_locations": [] },
        "I109": { "name": "หยาดน้ำค้างศักดิ์สิทธิ์", "type": "CRAFT", "desc": "น้ำค้างจากยอดสมุนไพรบนภูเขาสูง", "price": 0, "sale_locations": [] },
        "I110": { "name": "ลูกแก้วจิ้งจอก", "type": "CRAFT", "desc": "ลูกแก้วที่คิซึเนะทิ้งไว้ มีพลังลึกลับสถิตอยู่", "price": 0, "sale_locations": [] },
        "I111": { "name": "พิษแมงมุมโจโรกุโมะ", "type": "CRAFT", "desc": "พิษร้ายแรงที่สกัดจากปีศาจแมงมุม", "price": 0, "sale_locations": [] },
        "I112": { "name": "เกล็ดมังกรวารี", "type": "CRAFT", "desc": "เกล็ดสีครามจากสิ่งมีชีวิตในตำนาน (สมมติ)", "price": 0, "sale_locations": [] },
    }
    return items

