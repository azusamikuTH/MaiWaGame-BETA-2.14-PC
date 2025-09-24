# -*- coding: utf-8 -*-

def get_recipes():
    """
    คืน Dictionary ของสูตรสร้างของ (พิมพ์เขียว) ทั้งหมด
    - result: ID ของไอเทมที่จะได้
    - type: 'weapon', 'armor', 'item'
    - materials: Dictionary ของ {item_id: quantity}
    """
    recipes = {
        # --- WEAPON RECIPES ---
        "C001": { "name": "ดาบคาตานะ", "result": "W003", "type": "weapon", "materials": {"I051": 5, "I052": 2, "I056": 3} },
        "C002": { "name": "ดาบคาตานะชั้นดี", "result": "W024", "type": "weapon", "materials": {"I055": 2, "I051": 5, "I103": 1} },
        "C003": { "name": "ดาบยักษ์ซันบาโต", "result": "W025", "type": "weapon", "materials": {"I055": 5, "I051": 10, "I108": 1} },
        "C004": { "name": "หอกยาริ", "result": "W004", "type": "weapon", "materials": {"I051": 3, "I053": 5} },
        "C005": { "name": "ง้าวนากินาตะ", "result": "W014", "type": "weapon", "materials": {"I051": 4, "I053": 6, "I105": 1} },
        "C006": { "name": "ดาบนินจาอาบยาพิษ", "result": "W017", "type": "weapon", "materials": {"W017": 1, "I022": 3, "I111": 1} },
        "C007": { "name": "พลองเหล็กเท็ตสึโบ", "result": "W027", "type": "weapon", "materials": {"I051": 15, "I055": 1, "I108": 2} },
        "C008": { "name": "ดาบในไม้เท้า", "result": "W034", "type": "weapon", "materials": {"W001": 1, "I053": 5, "I110": 1} },
        "C009": { "name": "หอกวายุ", "result": "W023", "type": "weapon", "materials": {"W004": 1, "I102": 3, "I107": 1} },
        "C010": { "name": "ดาบในตำนานมาซามุเนะ", "result": "W035", "type": "weapon", "materials": {"W024": 1, "I050": 3, "I112": 1, "I101": 5} },
        
        # --- ARMOR RECIPES ---
        "C011": { "name": "เกราะหนัง", "result": "AR008", "type": "armor", "materials": {"I052": 8, "I054": 4} },
        "C012": { "name": "เกราะอก (โด)", "result": "AR009", "type": "armor", "materials": {"I051": 10, "I052": 5, "I054": 5} },
        "C013": { "name": "ชุดเกราะซามูไร (โยโรย)", "result": "AR010", "type": "armor", "materials": {"AR009": 1, "I055": 2, "I048": 1} },
        "C014": { "name": "หมวกเกราะซามูไร (คาบูโตะ)", "result": "AR005", "type": "armor", "materials": {"I051": 7, "I052": 3, "I108": 1} },
        "C015": { "name": "สนับแข้ง (ซึเนะอาเตะ)", "result": "AR015", "type": "armor", "materials": {"I051": 5, "I052": 2} },
        "C016": { "name": "ชุดนินจา (ชิโนบิ โชโซคุ)", "result": "AR026", "type": "armor", "materials": {"I054": 10, "I048": 2, "I111": 2} },
        "C017": { "name": "หน้ากากโอนิ", "result": "AR021", "type": "armor", "materials": {"I053": 5, "I108": 3, "I104": 1} },
        "C018": { "name": "เสื้อคลุมขนสัตว์", "result": "AR028", "type": "armor", "materials": {"I052": 12, "I054": 6, "I106": 1} },
        "C019": { "name": "เกราะวิญญาณ", "result": "AR009", "type": "armor", "materials": {"AR009": 1, "I101": 3, "I109": 1} }, # Example of re-crafting an item
        "C020": { "name": "หมวกเกราะไดเมียว", "result": "AR022", "type": "armor", "materials": {"AR005": 1, "I050": 1, "I048": 3, "I112": 1} },

        # --- ITEM RECIPES ---
        "C021": { "name": "ยาฟื้นฟูชั้นดี (ขวด)", "result": "I003", "type": "item", "materials": {"I001": 2, "I012": 1} },
        "C022": { "name": "ยาฟื้นฟูชั้นเลิศ (ขวด)", "result": "I011", "type": "item", "materials": {"I003": 3, "I006": 1, "I109": 1} },
        "C023": { "name": "หินลับมีดอย่างดี", "result": "I033", "type": "item", "materials": {"I004": 2, "I051": 3} },
        "C024": { "name": "ยันต์ชำระล้าง", "result": "I027", "type": "item", "materials": {"I031": 1, "I032": 1, "I109": 1} },
        "C025": { "name": "ระเบิดควัน", "result": "I020", "type": "item", "materials": {"I024": 1, "I054": 1} },
        "C026": { "name": "ดินประสิว", "result": "I024", "type": "item", "materials": {"I056": 5, "I104": 1} },
        "C027": { "name": "ยาพิษอย่างแรง", "result": "I022", "type": "item", "materials": {"I022": 1, "I111": 3} },
        "C028": { "name": "ยันต์วายุ", "result": "I042", "type": "item", "materials": {"I031": 1, "I102": 1, "I107": 1} },
        "C029": { "name": "น้ำมนต์ศักดิ์สิทธิ์", "result": "I035", "type": "item", "materials": {"I039": 1, "I006": 1} },
        "C030": { "name": "เครื่องรางนำโชคสูงสุด", "result": "I016", "type": "item", "materials": {"I016": 1, "I050": 1, "I110": 1} },
    }
    return recipes
