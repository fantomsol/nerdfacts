class Pokemon:
    def __init__(self, pb_pokemon):
        self.name = pb_pokemon.name
        self.base_experience = pb_pokemon.base_experience
        self.types = [t.type.name for t in pb_pokemon.types]
        self.height = pb_pokemon.height[0]
        self.weight = pb_pokemon.weight
