import os

import discord
import json
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')


intents = discord.Intents.default()
intents.voice_states = True  # Permite detectar canais de voz

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # Árvore de comandos para slash commands


# Plataformas disponíveis e suas mensagens
PLATAFORMAS_DISPONIVEIS = {
    "netflix.com": {
        "nome": "Netflix",
        "mensagem": "🎬 A Netflix está disponível! Preparando para reproduzir..."
    },
    "youtube.com": {
        "nome": "YouTube",
        "mensagem": "📺 O YouTube está pronto! Enviando para reprodução..."
    }
}

# Plataformas que ainda não estão prontas
PLATAFORMAS_NAO_DISPONIVEIS = {
    "primevideo.com": "Prime Video",
    "disneyplus.com": "Disney+"
}

@tree.command(name="reproduzir", description="Seu link foi recebido com sucesso.")
async def reproduzir(interaction: discord.Interaction, link: str):
    """Salva o link, o usuário e o canal de voz para outro bot usar."""

    user = interaction.user.name
    voice_channel = interaction.user.voice.channel if interaction.user.voice else None

    if not voice_channel:
        await interaction.response.send_message(
            f"{user}, você precisa estar em um canal de voz para usar este comando.",
            ephemeral=True
        )
        return

    plataforma = None
    mensagem = None

    # Verificar se a plataforma está disponível
    for dominio, dados in PLATAFORMAS_DISPONIVEIS.items():
        if dominio in link:
            plataforma = dados["nome"]
            mensagem = dados["mensagem"]
            break

    # Se a plataforma ainda não está disponível
    if not plataforma:
        for dominio, nome in PLATAFORMAS_NAO_DISPONIVEIS.items():
            if dominio in link:
                await interaction.response.send_message(
                    f"⚠️ **{nome} ainda não está disponível para reprodução.**",
                    ephemeral=True
                )
                return

    # Se não for uma plataforma reconhecida
    if not plataforma:
        await interaction.response.send_message(
            "❌ Essa plataforma não tem compatibilidade.",
            ephemeral=True
        )
        return

    # Adicionar horário atual
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guild_name = interaction.guild.name

    # Criar dicionário com os dados
    data = {
        "Usuário": user,
        "Servidor": guild_name,
        "Canal de Voz": voice_channel.name,
        "Plataforma": plataforma,
        "Link": link,
        "Horário": horario
    }

    # Salvar em JSON
    with open("bot_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    # Exibir no terminal
    print("\n=== Requisition ===")
    print(json.dumps(data, indent=4, ensure_ascii=False))

    # Enviar mensagem personalizada para a plataforma
    await interaction.response.send_message(f"✅ {mensagem}", ephemeral=True)

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