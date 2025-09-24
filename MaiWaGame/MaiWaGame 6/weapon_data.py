# -*- coding: utf-8 -*-

def get_weapons():
    """
    คืน Dictionary ของอาวุธทั้งหมดในเกม
    sale_locations: ประเภทของร้านค้าที่วางขายอาวุธชิ้นนี้
    - ร้านค้าเล็กๆ: ร้านค้าทั่วไปในเมืองบ้านนอก
    - โรงตีดาบ: ร้านอาวุธหลัก
    - ตลาด: แหล่งรวมของแปลกในเมืองหลวง
    """
    weapons = {
        # --- อาวุธพื้นฐาน ---
        "W001": { "name": "มีดสั้นทันโตะ", "bonus_atk": 2, "price": 50, "sale_locations": ["ร้านค้าเล็กๆ", "โรงตีดาบ"] },
        "W002": { "name": "ดาบสั้นวากิซาชิ", "bonus_atk": 4, "price": 120, "sale_locations": ["โรงตีดาบ"] },
        "W003": { "name": "ดาบคาตานะ", "bonus_atk": 7, "price": 250, "sale_locations": ["โรงตีดาบ"] },
        "W004": { "name": "หอกยาริ", "bonus_atk": 6, "price": 220, "sale_locations": ["โรงตีดาบ"] },
        "W005": { "name": "ดาบยาวโนดาจิ", "bonus_atk": 10, "price": 400, "sale_locations": ["โรงตีดาบ"] },
        "W006": { "name": "โบคุเคน (ดาบไม้)", "bonus_atk": 1, "price": 20, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "W007": { "name": "เคียวเกี่ยวข้าวคามะ", "bonus_atk": 2, "price": 40, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "W008": { "name": "มีดคุไน", "bonus_atk": 3, "price": 60, "sale_locations": ["ร้านค้าเล็กๆ", "ตลาด"] },
        "W009": { "name": "พลองไม้โบ", "bonus_atk": 3, "price": 70, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "W010": { "name": "ดาบคาตานะเก่า", "bonus_atk": 5, "price": 150, "sale_locations": ["ร้านค้าเล็กๆ", "โรงตีดาบ"] },

        # --- อาวุธระดับกลาง ---
        "W011": { "name": "ตะบองเหล็กคานาโบ", "bonus_atk": 5, "price": 150, "sale_locations": ["โรงตีดาบ"] },
        "W012": { "name": "ขวานรบมาซาคาริ", "bonus_atk": 7, "price": 240, "sale_locations": ["โรงตีดาบ"] },
        "W013": { "name": "ดาบเหล็กกล้าทาชิ", "bonus_atk": 8, "price": 300, "sale_locations": ["โรงตีดาบ"] },
        "W014": { "name": "ง้าวนากินาตะ", "bonus_atk": 8, "price": 280, "sale_locations": ["โรงตีดาบ"] },
        "W015": { "name": "ดาบสั้นโยโรยโดชิ", "bonus_atk": 4, "price": 140, "sale_locations": ["โรงตีดาบ"] },

        # --- อาวุธพิเศษ (หาได้จากตลาดในเมืองหลวง) ---
        "W016": { "name": "เคียวติดโซ่คุซาริกามะ", "bonus_atk": 5, "price": 200, "sale_locations": ["ตลาด"] },
        "W017": { "name": "ดาบนินจา", "bonus_atk": 6, "price": 260, "sale_locations": ["ตลาด"] },
        "W018": { "name": "ทอนฟา", "bonus_atk": 4, "price": 110, "sale_locations": ["ตลาด"] },
        "W019": { "name": "ไซ", "bonus_atk": 4, "price": 130, "sale_locations": ["ตลาด"] },
        "W020": { "name": "พัดเหล็กเท็ตสึเซ็น", "bonus_atk": 2, "price": 80, "sale_locations": ["ตลาด"] },
        "W021": { "name": "ดาบชิราซายะ", "bonus_atk": 6, "price": 200, "sale_locations": ["ตลาด"] },
        "W022": { "name": "กระบองสองท่อนนุนชะกุ", "bonus_atk": 5, "price": 160, "sale_locations": ["ตลาด"] },

        # --- อาวุธระดับสูง (หาได้จากโรงตีดาบในเมืองหลวง) ---
        "W023": { "name": "หอกสามง่ามจูมอนจิยาริ", "bonus_atk": 9, "price": 350, "sale_locations": ["โรงตีดาบ"] },
        "W024": { "name": "ดาบคาตานะชั้นดี", "bonus_atk": 9, "price": 380, "sale_locations": ["โรงตีดาบ"] },
        "W025": { "name": "ดาบยักษ์ซันบาโต", "bonus_atk": 12, "price": 550, "sale_locations": ["โรงตีดาบ"] },
        
        # --- NEW WEAPONS (10 เพิ่มเติม) ---
        "W026": { "name": "ดาบโค้งอุจิกาตานะ", "bonus_atk": 8, "price": 320, "sale_locations": ["โรงตีดาบ"] },
        "W027": { "name": "พลองเหล็กเท็ตสึโบ", "bonus_atk": 9, "price": 330, "sale_locations": ["โรงตีดาบ"] },
        "W028": { "name": "เคียวโซ่คู่ (นิโชกามะ)", "bonus_atk": 6, "price": 240, "sale_locations": ["ตลาด"] },
        "W029": { "name": "สนับมือเท็คโค", "bonus_atk": 3, "price": 90, "sale_locations": ["ตลาด"] },
        "W030": { "name": "ดาบไม้ไผ่ชิไน", "bonus_atk": 1, "price": 30, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "W031": { "name": "ลูกตุ้มโซ่ฟุนโด", "bonus_atk": 4, "price": 150, "sale_locations": ["ตลาด"] },
        "W032": { "name": "หอกยาวโออุมิยาริ", "bonus_atk": 11, "price": 450, "sale_locations": ["โรงตีดาบ"] },
        "W033": { "name": "ดาบโคดาจิ", "bonus_atk": 6, "price": 230, "sale_locations": ["โรงตีดาบ"] },
        "W034": { "name": "ดาบในไม้เท้า (ชิโคมิซึเอะ)", "bonus_atk": 7, "price": 380, "sale_locations": ["ตลาด"] },
        "W035": { "name": "ดาบในตำนานมาซามุเนะ", "bonus_atk": 15, "price": 9999, "sale_locations": [] }, # Rare/Quest Item
    }
    return weapons
