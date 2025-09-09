# -*- coding: utf-8 -*-

def get_armors():
    """
    คืน Dictionary ของชุดเกราะและเครื่องสวมใส่ทั้งหมด
    slot: ช่องที่สวมใส่ ('head', 'body', 'feet')
    sale_locations: ประเภทของร้านค้าที่วางขาย
    """
    armors = {
        # --- ศีรษะ (ดั้งเดิม) ---
        "AR001": { "name": "ผ้าคาดหัว", "slot": "head", "bonus_def": 1, "price": 40, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "AR002": { "name": "หมวกฟาง (ซัง笠)", "slot": "head", "bonus_def": 2, "price": 70, "sale_locations": ["ร้านค้าเล็กๆ", "ตลาด"] },
        "AR003": { "name": "หมวกเกราะอาชิการุ (จิน笠)", "slot": "head", "bonus_def": 4, "price": 150, "sale_locations": ["โรงตีดาบ"] },
        "AR004": { "name": "หน้ากากเมนโป", "slot": "head", "bonus_def": 3, "price": 200, "sale_locations": ["ตลาด", "โรงตีดาบ"] },
        "AR005": { "name": "หมวกเกราะซามูไร (คาบูโตะ)", "slot": "head", "bonus_def": 7, "price": 400, "sale_locations": ["โรงตีดาบ"] },

        # --- ลำตัว (ดั้งเดิม) ---
        "AR006": { "name": "เสื้อผ้าขาดๆ", "slot": "body", "bonus_def": 1, "price": 10, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "AR007": { "name": "ชุดยูกาตะ", "slot": "body", "bonus_def": 2, "price": 80, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "AR008": { "name": "เกราะหนัง", "slot": "body", "bonus_def": 5, "price": 250, "sale_locations": ["โรงตีดาบ", "ร้านค้าเล็กๆ"] },
        "AR009": { "name": "เกราะอก (โด)", "slot": "body", "bonus_def": 8, "price": 450, "sale_locations": ["โรงตีดาบ"] },
        "AR010": { "name": "ชุดเกราะซามูไร (โยโรย)", "slot": "body", "bonus_def": 12, "price": 800, "sale_locations": ["โรงตีดาบ"] },
        "AR011": { "name": "เสื้อคลุมนักเดินทาง", "slot": "body", "bonus_def": 3, "price": 120, "sale_locations": ["ตลาด", "ร้านค้าเล็กๆ"] },

        # --- เท้า (ดั้งเดิม) ---
        "AR012": { "name": "รองเท้าฟาง (วาราจิ)", "slot": "feet", "bonus_def": 1, "price": 30, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "AR013": { "name": "รองเท้าเกี๊ยะไม้ (เกตะ)", "slot": "feet", "bonus_def": 2, "price": 60, "sale_locations": ["ตลาด"] },
        "AR014": { "name": "รองเท้าทาบิ", "slot": "feet", "bonus_def": 1, "price": 45, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "AR015": { "name": "สนับแข้ง (ซึเนะอาเตะ)", "slot": "feet", "bonus_def": 4, "price": 180, "sale_locations": ["โรงตีดาบ"] },
        "AR016": { "name": "รองเท้าเกราะซามูไร", "slot": "feet", "bonus_def": 6, "price": 350, "sale_locations": ["โรงตีดาบ"] },
        
        # --- NEW ARMORS (20 เพิ่มเติม) ---
        
        # ศีรษะ (เพิ่มเติม)
        "AR017": { "name": "ผ้าคาดหัวนักสู้ (ฮะจิมาขิ)", "slot": "head", "bonus_def": 1, "price": 50, "sale_locations": ["ร้านค้าเล็กๆ", "โรงตีดาบ"] },
        "AR018": { "name": "หมวกสานของโรนิน (อามิกาสะ)", "slot": "head", "bonus_def": 2, "price": 80, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "AR019": { "name": "ผ้าคลุมศีรษะนักบวช", "slot": "head", "bonus_def": 3, "price": 120, "sale_locations": ["ตลาด"] },
        "AR020": { "name": "หน้ากากเท็งงุ", "slot": "head", "bonus_def": 4, "price": 300, "sale_locations": ["ตลาด"] },
        "AR021": { "name": "หน้ากากโอนิ", "slot": "head", "bonus_def": 5, "price": 350, "sale_locations": ["ตลาด"] },
        "AR022": { "name": "หมวกเกราะไดเมียว (คาบูโตะชั้นสูง)", "slot": "head", "bonus_def": 9, "price": 700, "sale_locations": [] }, # Rare drop/quest item

        # ลำตัว (เพิ่มเติม)
        "AR023": { "name": "เสื้อกิโมโนของพ่อค้า", "slot": "body", "bonus_def": 2, "price": 90, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "AR024": { "name": "เสื้อเกราะโซ่ (คุซาริคาตาบิระ)", "slot": "body", "bonus_def": 6, "price": 300, "sale_locations": ["โรงตีดาบ", "ตลาด"] },
        "AR025": { "name": "ชุดนักบวชโซเฮย์", "slot": "body", "bonus_def": 7, "price": 400, "sale_locations": ["ตลาด"] },
        "AR026": { "name": "ชุดนินจา (ชิโนบิ โชโซคุ)", "slot": "body", "bonus_def": 4, "price": 350, "sale_locations": ["ตลาด"] },
        "AR027": { "name": "เสื้อเกราะอกหนัก", "slot": "body", "bonus_def": 10, "price": 600, "sale_locations": ["โรงตีดาบ"] },
        "AR028": { "name": "เสื้อคลุมขนสัตว์", "slot": "body", "bonus_def": 4, "price": 200, "sale_locations": ["ร้านค้าเล็กๆ"] },
        "AR029": { "name": "เกราะอกที่ขึ้นสนิม", "slot": "body", "bonus_def": 3, "price": 100, "sale_locations": [] },
        "AR030": { "name": "เสื้อคลุมฮาโอริชั้นดี", "slot": "body", "bonus_def": 3, "price": 220, "sale_locations": ["ตลาด"] },

        # เท้า (เพิ่มเติม)
        "AR031": { "name": "รองเท้าทาบิของนินจา", "slot": "feet", "bonus_def": 2, "price": 100, "sale_locations": ["ตลาด"] },
        "AR032": { "name": "สนับแข้งเหล็ก", "slot": "feet", "bonus_def": 5, "price": 250, "sale_locations": ["โรงตีดาบ"] },
        "AR033": { "name": "รองเท้าฟางที่ใกล้ขาด", "slot": "feet", "bonus_def": 0, "price": 5, "sale_locations": [] },
        "AR034": { "name": "รองเท้าหนังสำหรับเดินทาง", "slot": "feet", "bonus_def": 3, "price": 120, "sale_locations": ["ร้านค้าเล็กๆ", "ตลาด"] },
        "AR035": { "name": "สนับแข้งของนักรบภูเขา", "slot": "feet", "bonus_def": 4, "price": 200, "sale_locations": ["โรงตีดาบ"] },
        "AR036": { "name": "รองเท้าเกราะเบา", "slot": "feet", "bonus_def": 3, "price": 150, "sale_locations": ["โรงตีดาบ", "ร้านค้าเล็กๆ"] },
    }
    return armors

