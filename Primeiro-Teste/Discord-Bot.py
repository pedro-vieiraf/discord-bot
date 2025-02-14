import os

import discord
import json
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.voice_states = True  # Permite detectar canais de voz

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # Árvore de comandos para slash commands


@tree.command(name="reproduzir", description="Seu link foi recebido com sucesso.")
async def reproduzir(interaction: discord.Interaction, link: str):
    """Salva o link, o usuário e o canal de voz para outro bot usar."""

    user = interaction.user.name  # Pega o nome do usuário que enviou o comando
    voice_channel = interaction.user.voice.channel if interaction.user.voice else None

    if not voice_channel:
        await interaction.response.send_message(
            f"{user}, você precisa estar em um canal de voz para usar este comando.",
            ephemeral=True
        )
        return

    guild_name = interaction.guild.name  # Nome do servidor

    # Criar dicionário com os dados
    data = {
        "Usuário": user,
        "Servidor": guild_name,
        "Canal de Voz": voice_channel.name,
        "Link": link
    }

    # Salvar em JSON
    with open("bot_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    # Exibir no terminal
    print("\n=== Requisition ===")
    print(json.dumps(data, indent=4, ensure_ascii=False))

    await interaction.response.send_message(
        "Informações salvas! O bot do Selenium pode usá-las agora.",
        ephemeral=True
    )


@tree.command(name="hello", description="Diz Hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Olá {interaction.user.mention}!")


@tree.command(name="soma", description="Some dois números")
async def Soma(interaction: discord.Interaction, numero1: int, numero2: int):
    numero_somado = numero1 + numero2
    await interaction.response.send_message(f"A soma de {numero1} + {numero2} = {numero_somado}")


@bot.event
async def on_ready():
    """Registra os comandos de Slash quando o bot estiver pronto."""
    try:
        await tree.sync()  # Sincroniza os comandos de Slash
        print(f"Bot conectado como {bot.user}")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")


bot.run(TOKEN)