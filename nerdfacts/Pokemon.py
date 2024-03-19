class Pokemon:
    def __init__(self, pb_pokemon):
        self.name = pb_pokemon.name
        self.base_experience = pb_pokemon.base_experience
        self.types = [t.type.name for t in pb_pokemon.types]
        self.height = float(pb_pokemon.height) / 10.0  # dm to m
        self.weight = pb_pokemon.weight / 10.0  # hg to kg
