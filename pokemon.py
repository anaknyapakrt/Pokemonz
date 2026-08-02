import discord
from discord.ext import commands
from logic import Fighter, Pokemon, Wizard
import random

# Setting up intents for the bot
intents = discord.Intents.default()  # Getting the default settings
intents.messages = True              # Allowing the bot to process messages
intents.message_content = True       # Allowing the bot to read message content
intents.guilds = True                # Allowing the bot to work with servers (guilds)

# Creating a bot with a defined command prefix and activated intents
bot = commands.Bot(command_prefix='!', intents=intents)

# An event that is triggered when the bot is ready to run
@bot.event
async def on_ready():
    # bot.user may be None in some type-checking contexts; use its string representation
    print(f'Logged in as {bot.user}')  # Outputs the bot's user to the console

# The '!go' command
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Getting the name of the message's author
    # Check whether the user already has a Pokémon. If not, then...
    if author not in Pokemon.pokemons.keys():
        change = random.randint(1, 3)
        if change == 1:
            pokemon = Pokemon(author)
        elif change == 2:
            pokemon = Wizard(author)
        else:
            pokemon = Fighter(author)

        await ctx.send(await pokemon.info())  # Sending information about the Pokémon
        image_url = await pokemon.show_img()  # Getting the URL of the Pokémon image
        if image_url:
            embed = discord.Embed()  # Creating an embed message
            embed.set_image(url=image_url)  # Setting up the Pokémon's image
            await ctx.send(embed=embed)  # Sending an embedded message with an image
        else:
            await ctx.send("Failed to upload an image of the pokémon.")
    else:
        await ctx.send("You've already created your own Pokémon.")  # A message that is printed whether a Pokémon has already been created
# Running the bot

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Kedua peserta harus memiliki Pokemon untuk bertarung!")
    else:
        await ctx.send("Tetapkan pengguna yang ingin Anda serang dengan menyebut mereka.")

@bot.command()
async def feed(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        result = await pokemon.feed()
        await ctx.send(result)
    else:
        await ctx.send("Kamu belum punya Pokémon! Ketik !go terlebih dahulu.")

bot.run("PUT YOUR TOKEN HERE")  # Running the bot with the token that is provided by Discord for your bot
