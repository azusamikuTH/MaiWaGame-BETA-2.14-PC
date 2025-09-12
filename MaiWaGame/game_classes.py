# -*- coding: utf-8 -*-
import random

class Card:
    def __init__(self, name, card_type, value, desc):
        self.name = name; self.type = card_type; self.value = value; self.desc = desc
    def to_dict(self): return self.__dict__
    @classmethod
    def from_dict(cls, data): return cls(data['name'], data['type'], data['value'], data['desc'])

class Weapon:
    def __init__(self, weapon_id, name, bonus_atk, price):
        self.id = weapon_id; self.name = name; self.bonus_atk = bonus_atk; self.price = price
    def to_dict(self): return self.__dict__
    @classmethod
    def from_dict(cls, data): return cls(data['id'], data['name'], data['bonus_atk'], data['price'])

class Armor:
    def __init__(self, armor_id, name, slot, bonus_def, price):
        self.id = armor_id; self.name = name; self.slot = slot; self.bonus_def = bonus_def; self.price = price
    def to_dict(self): return self.__dict__
    @classmethod
    def from_dict(cls, data): return cls(data['id'], data['name'], data['slot'], data['bonus_def'], data['price'])

class Character:
    # --- EDIT: เปลี่ยนชื่อ 'defense' เป็น 'defense_stat' ---
    def __init__(self, name, max_hp, atk, defense_stat, spd, luck):
        self.name = name; self.max_hp = max_hp; self.hp = max_hp; self.atk = atk; self.defense_stat = defense_stat; self.spd = spd; self.luck = luck
        self.deck = []; self.hand = []; self.discard = []; self.defense_bonus = 0

    def is_alive(self): return self.hp > 0
    def draw_hand(self, num_cards=4):
        self.discard.extend(self.hand); self.hand = []
        for _ in range(num_cards):
            if not self.deck:
                if not self.discard: break
                self.deck = self.discard; self.discard = []; random.shuffle(self.deck)
            if self.deck: self.hand.append(self.deck.pop())
    
    def take_damage(self, damage):
        # --- EDIT: เปลี่ยนไปใช้ get_total_def ---
        total_defense = getattr(self, 'get_total_def', lambda: self.defense_stat)() + self.defense_bonus
        actual_damage = max(0, damage - total_defense)
        self.hp = max(0, self.hp - actual_damage)
        self.defense_bonus = 0
        return actual_damage

class Player(Character):
    def __init__(self, name):
        # --- EDIT: เปลี่ยนชื่อ 'defense' เป็น 'defense_stat' ---
        super().__init__(name, 100, 10, 5, 7, 5) # 5 คือ defense_stat พื้นฐาน
        self.money = 50; self.current_location_id = ""; self.current_region_id = ""; self.reputation = {}; self.active_quests = {}; self.completed_quests = []
        self.original_deck = []; self.weapon_inventory = []; self.armor_inventory = []; self.item_inventory = {}
        self.equipped_weapon = None; self.equipped_head = None; self.equipped_body = None; self.equipped_feet = None

    def get_total_atk(self):
        bonus = self.equipped_weapon.bonus_atk if self.equipped_weapon else 0
        return self.atk + bonus
    
    def get_total_def(self):
        head = self.equipped_head.bonus_def if self.equipped_head else 0
        body = self.equipped_body.bonus_def if self.equipped_body else 0
        feet = self.equipped_feet.bonus_def if self.equipped_feet else 0
        # --- EDIT: เปลี่ยนไปใช้ defense_stat ---
        return self.defense_stat + head + body + feet

    def build_deck(self, card_pool, size=10):
        safe_size = min(len(card_pool), size); self.original_deck = random.sample(card_pool, safe_size); self.deck = list(self.original_deck); random.shuffle(self.deck)

    def to_dict(self):
        return {
            'name': self.name, 'max_hp': self.max_hp, 'hp': self.hp, 'atk': self.atk, 
            'defense_stat': self.defense_stat, # <-- EDIT
            'spd': self.spd, 'luck': self.luck, 'money': self.money,
            'current_location_id': self.current_location_id, 'current_region_id': self.current_region_id,
            'reputation': self.reputation, 'active_quests': self.active_quests, 'completed_quests': self.completed_quests,
            'original_deck': [c.to_dict() for c in self.original_deck], 'weapon_inventory': [w.to_dict() for w in self.weapon_inventory],
            'armor_inventory': [a.to_dict() for a in self.armor_inventory], 'item_inventory': self.item_inventory,
            'equipped_weapon': self.equipped_weapon.to_dict() if self.equipped_weapon else None,
            'equipped_head': self.equipped_head.to_dict() if self.equipped_head else None,
            'equipped_body': self.equipped_body.to_dict() if self.equipped_body else None,
            'equipped_feet': self.equipped_feet.to_dict() if self.equipped_feet else None,
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(data['name'])
        player.max_hp = data.get('max_hp', 100); player.hp = data.get('hp', 100); player.atk = data.get('atk', 10); 
        player.defense_stat = data.get('defense_stat', 5); # <-- EDIT
        player.spd = data.get('spd', 7); player.luck = data.get('luck', 5); player.money = data.get('money', 50); player.current_location_id = data.get('current_location_id', "L002"); player.current_region_id = data.get('current_region_id', "R001");
        player.reputation = data.get('reputation', {}); player.active_quests = data.get('active_quests', {}); player.completed_quests = data.get('completed_quests', [])
        player.original_deck = [Card.from_dict(c) for c in data.get('original_deck', [])]; player.deck = list(player.original_deck); random.shuffle(player.deck)
        player.weapon_inventory = [Weapon.from_dict(w) for w in data.get('weapon_inventory', [])]; player.armor_inventory = [Armor.from_dict(a) for a in data.get('armor_inventory', [])]; player.item_inventory = data.get('item_inventory', {})
        if data.get('equipped_weapon'): player.equipped_weapon = Weapon.from_dict(data['equipped_weapon'])
        if data.get('equipped_head'): player.equipped_head = Armor.from_dict(data['equipped_head'])
        if data.get('equipped_body'): player.equipped_body = Armor.from_dict(data['equipped_body'])
        if data.get('equipped_feet'): player.equipped_feet = Armor.from_dict(data['equipped_feet'])
        return player

class Enemy(Character):
    # --- EDIT: เปลี่ยนชื่อ 'defense' เป็น 'defense_stat' ---
    def __init__(self, enemy_id, name, max_hp, atk, defense_stat, spd, luck, card_pool):
        super().__init__(name, max_hp, atk, defense_stat, spd, luck); self.enemy_id = enemy_id; self.deck = random.sample(card_pool, min(len(card_pool), 10))

