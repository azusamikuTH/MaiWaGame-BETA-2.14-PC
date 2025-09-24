# -*- coding: utf-8 -*-
import random
import time

class Card:
    def __init__(self, name, card_type, value, desc, temporary=False, uses=0):
        self.name = name
        self.type = card_type
        self.value = value
        self.desc = desc
        self.temporary = temporary
        self.uses = uses

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('name'),
            data.get('type'),
            data.get('value'),
            data.get('desc'),
            data.get('temporary', False),
            data.get('uses', 0)
        )

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
    def __init__(self, name, max_hp, atk, defense_stat, spd, luck):
        self.name = name
        self.base_max_hp = max_hp # Store original value for scaling
        self.max_hp = max_hp
        self.hp = max_hp
        self.base_atk = atk
        self.atk = atk
        self.base_def = defense_stat
        self.defense_stat = defense_stat
        self.base_spd = spd
        self.spd = spd
        self.luck = luck
        self.deck = []; self.hand = []; self.discard = []
        self.defense_bonus = 0
        self.status_effects = {} # e.g., {'poison': 3} for 3 turns
        self.combat_buffs = {'atk': 0, 'def': 0, 'luck': 0, 'spd': 0}
        self.god_mode = False

    def is_alive(self): return self.hp > 0
    
    def get_total_atk(self):
        final_atk = self.atk + self.combat_buffs['atk']
        if 'fear' in self.status_effects: final_atk = max(1, final_atk - self.status_effects['fear'])
        if 'charm' in self.status_effects: final_atk *= 0.5
        return int(max(1, final_atk))

    def get_total_def(self):
        final_def = self.defense_stat + self.combat_buffs['def']
        if 'vulnerable' in self.status_effects: final_def = max(0, final_def - self.status_effects['vulnerable'])
        if 'charm' in self.status_effects: final_def *= 0.5
        return int(max(0, final_def))
    
    def get_total_spd(self):
        final_spd = self.spd + self.combat_buffs['spd']
        if 'slow' in self.status_effects: final_spd = max(1, final_spd - self.status_effects['slow'])
        return int(max(1, final_spd))

    def take_damage(self, damage):
        if self.god_mode: return 0
        total_defense = self.get_total_def() + self.defense_bonus
        actual_damage = max(1, damage - total_defense) # Always take at least 1 damage
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
        
    def apply_status_effect(self, effect, duration):
        # Effects can stack in duration or power
        if effect in ['poison', 'bleed', 'fear', 'slow', 'vulnerable', 'stun', 'charm']:
            self.status_effects[effect] = self.status_effects.get(effect, 0) + duration
            print(f"{self.name} ติดสถานะ {effect.capitalize()}!")
        
    def tick_status_effects(self, game_instance=None):
        if not self.is_alive(): return
        
        effects_to_remove = []
        for effect, duration in list(self.status_effects.items()):
            if effect == 'poison':
                damage = 5
                self.hp = max(0, self.hp - damage)
                print(f"{self.name} ได้รับความเสียหายจากพิษ {damage} หน่วย!")
            elif effect == 'bleed':
                damage = 3
                self.hp = max(0, self.hp - damage)
                print(f"{self.name} เสียเลือด {damage} หน่วย!")
            
            self.status_effects[effect] -= 1
            if self.status_effects[effect] <= 0:
                effects_to_remove.append(effect)

        for effect in effects_to_remove:
            if effect in self.status_effects:
                del self.status_effects[effect]
                print(f"{self.name} หายจากอาการ {effect.capitalize()} แล้ว")

        if not self.is_alive() and isinstance(self, Enemy):
             self.trigger_passive('on_death', game_instance)


class Player(Character):
    def __init__(self, name):
        super().__init__(name, 100, 10, 5, 7, 5) 
        self.money = 50; self.current_location_id = ""; self.current_region_id = ""
        self.reputation = {}; self.active_quests = {}; self.completed_quests = []
        self.original_deck = []; self.weapon_inventory = []; self.armor_inventory = []
        self.item_inventory = {} # name: {'quantity': X, 'id': Y}
        self.equipped_weapon = None; self.equipped_head = None; self.equipped_body = None; self.equipped_feet = None
        self.level = 1; self.xp = 0; self.xp_to_next_level = 100; self.stat_points = 0
        self.next_fight_buffs = {'atk': 0, 'def': 0, 'luck': 0}
        self.known_recipes = []
        self.temp_skill_cards = []

    def get_total_atk(self):
        bonus = self.equipped_weapon.bonus_atk if self.equipped_weapon else 0
        base_total = self.atk + bonus
        # Player's total ATK is calculated differently from the Character base
        final_atk = base_total + self.combat_buffs['atk']
        if 'fear' in self.status_effects: final_atk = max(1, final_atk - self.status_effects['fear'])
        if 'charm' in self.status_effects: final_atk *= 0.5
        return int(max(1, final_atk))
    
    def get_total_def(self):
        head = self.equipped_head.bonus_def if self.equipped_head else 0
        body = self.equipped_body.bonus_def if self.equipped_body else 0
        feet = self.equipped_feet.bonus_def if self.equipped_feet else 0
        base_total = self.defense_stat + head + body + feet
        # Player's total DEF is calculated differently from the Character base
        final_def = base_total + self.combat_buffs['def']
        if 'vulnerable' in self.status_effects: final_def = max(0, final_def - self.status_effects['vulnerable'])
        if 'charm' in self.status_effects: final_def *= 0.5
        return int(max(0, final_def))

    def add_item(self, item_name, quantity, item_id):
        if item_name in self.item_inventory:
            self.item_inventory[item_name]['quantity'] += quantity
        else:
            self.item_inventory[item_name] = {'quantity': quantity, 'id': item_id}
            
    def remove_item(self, item_name, quantity=1):
        if item_name in self.item_inventory:
            self.item_inventory[item_name]['quantity'] -= quantity
            if self.item_inventory[item_name]['quantity'] <= 0:
                del self.item_inventory[item_name]
    
    def add_temp_card(self, card):
        # Prevents duplicate temporary cards
        for existing_card in self.temp_skill_cards:
            if existing_card.name == card.name:
                existing_card.uses += card.uses
                return
        self.temp_skill_cards.append(card)

    def remove_temp_card(self, card_name):
        self.temp_skill_cards = [c for c in self.temp_skill_cards if c.name != card_name]

    def draw_hand(self, num_cards=4):
        self.discard.extend(self.hand); self.hand = []
        # Combine permanent and temporary deck for drawing
        current_deck = self.deck + self.temp_skill_cards
        
        for _ in range(num_cards):
            if not self.deck: # Only reshuffle the main deck
                if not self.discard: break
                self.deck.extend(self.discard)
                self.discard = []
                random.shuffle(self.deck)

            # Recalculate current_deck after potential reshuffle
            current_deck = self.deck + self.temp_skill_cards
            
            if current_deck:
                card_to_draw_index = random.randrange(len(current_deck))
                card_to_draw = current_deck.pop(card_to_draw_index)
                
                self.hand.append(card_to_draw)
                
                # If a non-temp card was drawn, remove it from its source deck
                if not card_to_draw.temporary and card_to_draw in self.deck:
                    self.deck.remove(card_to_draw)
                elif card_to_draw.temporary and card_to_draw in self.temp_skill_cards:
                    # Temp cards are conceptually "drawn" but not removed from the source list until used up
                    pass


    def build_deck(self, card_pool, size=10):
        safe_size = min(len(card_pool), size); self.original_deck = random.sample(card_pool, safe_size); self.deck = list(self.original_deck); random.shuffle(self.deck)

    def add_xp(self, amount):
        if amount <= 0: return
        print(f"ได้รับค่าประสบการณ์ {amount} แต้ม!"); time.sleep(1); self.xp += amount
        leveled_up = False
        while self.xp >= self.xp_to_next_level:
            excess_xp = self.xp - self.xp_to_next_level; self.level += 1; self.xp = excess_xp; self.xp_to_next_level = int(self.xp_to_next_level * 1.5); self.stat_points += 5; leveled_up = True
        if leveled_up:
            self.max_hp += 10; self.hp = self.max_hp
            print("\n" + "*"*20); print(f"!!! เลื่อนระดับเป็นเลเวล {self.level} !!!"); print("พลังชีวิตสูงสุดเพิ่มขึ้น 10 หน่วยและฟื้นฟูจนเต็ม!"); print(f"คุณได้รับ 5 แต้มสถานะ"); print("*"*20); time.sleep(3)

    def to_dict(self):
        return {
            'name': self.name, 'max_hp': self.max_hp, 'hp': self.hp, 'atk': self.atk, 'defense_stat': self.defense_stat, 'spd': self.spd, 'luck': self.luck, 'money': self.money,
            'current_location_id': self.current_location_id, 'current_region_id': self.current_region_id,
            'reputation': self.reputation, 'active_quests': self.active_quests, 'completed_quests': self.completed_quests,
            'original_deck': [c.to_dict() for c in self.original_deck], 'weapon_inventory': [w.to_dict() for w in self.weapon_inventory],
            'armor_inventory': [a.to_dict() for a in self.armor_inventory], 'item_inventory': self.item_inventory,
            'equipped_weapon': self.equipped_weapon.to_dict() if self.equipped_weapon else None,
            'equipped_head': self.equipped_head.to_dict() if self.equipped_head else None,
            'equipped_body': self.equipped_body.to_dict() if self.equipped_body else None,
            'equipped_feet': self.equipped_feet.to_dict() if self.equipped_feet else None,
            'level': self.level, 'xp': self.xp, 'xp_to_next_level': self.xp_to_next_level, 'stat_points': self.stat_points,
            'next_fight_buffs': self.next_fight_buffs, 'known_recipes': self.known_recipes,
            'temp_skill_cards': [c.to_dict() for c in self.temp_skill_cards]
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(data['name'])
        player.max_hp = data.get('max_hp', 100); player.hp = data.get('hp', 100); player.atk = data.get('atk', 10); player.defense_stat = data.get('defense_stat', 5); player.spd = data.get('spd', 7); player.luck = data.get('luck', 5); player.money = data.get('money', 50); player.current_location_id = data.get('current_location_id', "L002"); player.current_region_id = data.get('current_region_id', "R001");
        player.reputation = data.get('reputation', {}); player.active_quests = data.get('active_quests', {}); player.completed_quests = data.get('completed_quests', [])
        player.original_deck = [Card.from_dict(c) for c in data.get('original_deck', [])]; player.deck = list(player.original_deck); random.shuffle(player.deck)
        player.weapon_inventory = [Weapon.from_dict(w) for w in data.get('weapon_inventory', [])]; player.armor_inventory = [Armor.from_dict(a) for a in data.get('armor_inventory', [])]; player.item_inventory = data.get('item_inventory', {})
        if data.get('equipped_weapon'): player.equipped_weapon = Weapon.from_dict(data['equipped_weapon'])
        if data.get('equipped_head'): player.equipped_head = Armor.from_dict(data['equipped_head'])
        if data.get('equipped_body'): player.equipped_body = Armor.from_dict(data['equipped_body'])
        if data.get('equipped_feet'): player.equipped_feet = Armor.from_dict(data['equipped_feet'])
        player.level = data.get('level', 1); player.xp = data.get('xp', 0); player.xp_to_next_level = data.get('xp_to_next_level', 100); player.stat_points = data.get('stat_points', 0)
        player.next_fight_buffs = data.get('next_fight_buffs', {'atk': 0, 'def': 0, 'luck': 0})
        player.known_recipes = data.get('known_recipes', [])
        player.temp_skill_cards = [Card.from_dict(c) for c in data.get('temp_skill_cards', [])]
        return player

class Enemy(Character):
    def __init__(self, enemy_id, name, max_hp, atk, defense_stat, spd, luck, moveset, is_boss=False, passives=None):
        super().__init__(name, max_hp, atk, defense_stat, spd, luck)
        self.enemy_id = enemy_id
        self.moveset = moveset
        self.is_boss = is_boss
        self.passives = passives if passives else []
        self.move_cooldowns = {move['name']: 0 for move in moveset if 'cooldown' in move}
        self.is_charging = False
        self.charge_info = None

    @classmethod
    def from_dict(cls, enemy_id, data, is_boss=False):
        return cls(
            enemy_id,
            data['name'],
            data['max_hp'],
            data['atk'],
            data['defense_stat'],
            data['spd'],
            data['luck'],
            data['moveset'],
            is_boss,
            data.get('passives')
        )

    def tick_cooldowns(self):
        for move_name in self.move_cooldowns:
            if self.move_cooldowns[move_name] > 0:
                self.move_cooldowns[move_name] -= 1

    def choose_move(self, player_hp_percent):
        self.tick_cooldowns()

        if self.is_charging:
            self.charge_info['turns_left'] -= 1
            if self.charge_info['turns_left'] <= 0:
                self.is_charging = False
                # Make the charge attack type 'attack' so it executes
                charged_move = self.charge_info['move'].copy()
                charged_move['type'] = 'attack' 
                return charged_move
            else:
                print(f"{self.name} is still charging...")
                return None

        # Filter out moves on cooldown or passive moves
        available_moves = [m for m in self.moveset if self.move_cooldowns.get(m['name'], 0) == 0 and m.get('type') != 'passive']
        if not available_moves:
             # Default attack if no moves are available
             return {"name": "Struggle", "type": "attack", "power": 0.8, "desc": "It flails wildly!"}

        # Simple AI logic
        heal_moves = [m for m in available_moves if m.get('effect') == 'heal' and self.hp < self.max_hp * 0.4]
        buff_moves = [m for m in available_moves if 'buff' in m.get('effect', '')]
        
        if heal_moves and random.random() < 0.7: # High chance to heal when low
            chosen_move = random.choice(heal_moves)
        elif buff_moves and random.random() < 0.3: # Lower chance to buff
             chosen_move = random.choice(buff_moves)
        else: # Attack
            attack_options = [m for m in available_moves if m['type'] in ['attack', 'charge', 'skill'] and 'debuff' in m.get('effect', '')]
            if not attack_options: # Fallback to any available move
                attack_options = available_moves
            chosen_move = random.choice(attack_options)
        
        if 'cooldown' in chosen_move:
            self.move_cooldowns[chosen_move['name']] = chosen_move['cooldown']
        
        if chosen_move.get('type') == 'charge':
            self.is_charging = True
            self.charge_info = {
                'move': chosen_move,
                'turns_left': chosen_move.get('charge_turns', 1)
            }
            print(f"{self.name} is charging up a powerful attack!")
            return None # Don't attack this turn

        return chosen_move

    def trigger_passive(self, trigger, game_instance, source=None):
        if not self.is_alive(): return # Don't trigger passives if dead, except on_death
        if trigger != 'on_death' and not self.is_alive(): return
        
        player = game_instance.player
        for passive in self.passives:
            if passive['trigger'] == trigger:
                print(f"** {self.name}'s Passive '{passive['name']}' activates! **")
                effect = passive['effect']
                if effect == 'counter_attack':
                    if source == player: # Make sure player is the source
                        damage = int(self.get_total_atk() * passive.get('power', 0.5))
                        print(f"{self.name} counter-attacks!")
                        actual_damage = player.take_damage(damage)
                        print(f"You take {actual_damage} damage from the counter!")
                elif effect == 'thorns':
                     if source == player:
                        damage = passive.get('power', 5)
                        print(f"{self.name}'s thorny exterior hurts you!")
                        actual_damage = player.take_damage(damage)
                        print(f"You take {actual_damage} damage from thorns!")
                elif effect == 'last_stand':
                    self.combat_buffs['atk'] += passive.get('power', 10)
                    print(f"{self.name} is enraged! Its attack greatly increases!")
                elif effect == 'hp_regen':
                    heal_amount = int(self.max_hp * passive.get('power', 0.05)) # power is % of max HP
                    self.hp = min(self.max_hp, self.hp + heal_amount)
                    print(f"{self.name} regenerates {heal_amount} HP!")

