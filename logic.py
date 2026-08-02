import aiohttp  # A library for asynchronous HTTP requests
import random


class Pokemon:

    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

        
        self.power = random.randint(30,60)
        self.hp = random.randint(200,400)
        self.height = 0
        self.weight = 0

    def update_stats(self, new_power, new_hp):
        self.power = new_power
        self.hp = new_hp 

    async def feed(self):
        # Fetching from a different API endpoint (Berry API)
        url = f'https://pokeapi.co{random.randint(1, 64)}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                berry_name = "Berry"
                if response.status == 200:
                    data = await response.json()
                    berry_name = data['name'].title()

                # Rare drop chance (1 out of 5)
                if random.randint(1, 5) == 1:
                    self.power += 20
                    self.hp += 50
                    return f"drop langka! memakan {berry_name} emas! power +20, HP +50! "
                else:
                    self.power += 5
                    self.hp += 10
                    return f"yummy! pokemon memakan {berry_name}. power +5, HP +10."

        
    async def get_name(self):
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response

                    self.height = data['height']  # Storing the height of the Pokémon
                    self.weight = data['weight']  # Storing the weight of the Pokémon

                    return data['forms'][0]['name']  # Returning a Pokémon's name
                else:
                    return "Pikachu"  # Return the default name if the request fails

    async def info(self):
        # A method that returns information about the pokémon
        if not self.name:
            self.name = await self.get_name()  # Retrieving a name if it has not yet been uploaded
        return f"""Nama Pokemon: {self.name}
                Tinggi pokemon: {self.height}
                Berat pokemon: {self.weight}
                Kekuatan pokemon: {self.power}
                Kesehatan pokemon: {self.hp}"""

    async def show_img(self):
        # An asynchronous method to retrieve the URL of a pokémon image via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API untuk permintaan
        async with aiohttp.ClientSession() as session:  # Membuka HTTP session
            async with session.get(url) as response:  # Mengirim permintaan GET
                if response.status == 200:
                    data = await response.json()  # Menerima dan mendekode respons JSON
                    return data['sprites']['front_default']  # Mengembalikan URL gambar Pokémon
                else:
                    return None

    async def attack(self, enemy):

        if isinstance(enemy, Wizard):
            change = random.randint(1, 5)
            if change==1:
                return "pokemon penyihir menggunakan perisai selama pertarungan"


        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pertarungan @{self.pokemon_trainer} dengan @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"@{self.pokemon_trainer} menang melawan @{enemy.pokemon_trainer}!"
        
class Wizard(Pokemon):
    pass

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(1, 10 )
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nPokemon petarung menggunakan serangan super. Kekuatan di tambahkan adalah {super_power}!"
