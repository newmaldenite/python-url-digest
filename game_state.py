class GameState:
    def __init__(self):
        self.location = "dungeon_entrance"
        self.inventory = []
        self.monsters = {
            "dungeon_entrance": ["Thunderbeak Wyvern"]
        }

    def move_to(self, location):
        self.location = location
        return f"You moved to {location}."

    def get_monsters_in_current_location(self):
        return self.monsters.get(self.location, [])

game_state = GameState()