import requests
import yt_dlp as ytdl
import random
from discord.ext import commands
import time
import requests
import psutil
import platform
import os
import yt_dlp
import shutil
import asyncio
import json
import subprocess
import discord
import git
from discord import File
import datetime
import random
import string
import threading

# Configuración
BOT_TOKEN = 'MTI0NTU0NzcwOTg3NjkyODU0Mw.GliFcU.uK7Mt1qo8SPpGK1WQFCkD8J9lnj8OarnAx7O2M'  # Reemplaza con tu token
PREFIX = '#'  # Prefijo de comandos

# Inicializar el cliente de Discord
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=PREFIX, intents=intents)

# Función para verificar progreso de descarga
def check_progress(id):
    while True:
        response = requests.get(f'https://p.oceansaver.in/ajax/progress.php?id={id}')
        data = response.json()
        if data['success'] and data['progress'] == 1000:
            return data['download_url']
        time.sleep(5)

# Evento cuando el bot está listo
@client.event
async def on_ready():
    print(f'Bot conectado como🌹{client.user}')

# Configuración de opciones de yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'downloads/%(title)s.%(ext)s',  # Carpeta donde se guardará el archivo
    'ffmpeg_location': '/usr/bin/ffmpeg'  # Ruta de ffmpeg en Replit
}

def descargar_audio(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        

# Comando para descargar música
@client.command()
async def play(ctx, *, query: str):
    if not query:
        await ctx.send("🎵 Escribe el nombre o link del video.")
        return

    # Usar yt-dlp para obtener los resultados de búsqueda
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with ytdl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if not info.get('entries'):
            await ctx.send("⚠️ No se encontraron resultados.")
            return

        video = info['entries'][0]
        video_url = video['url']

    try:
        # Obtener enlace de descarga de audio en MP3
        response = requests.get(f'https://p.oceansaver.in/ajax/download.php?format=mp3&url={video_url}&api=dfcb6d76f2f6a9894gjkege8a4ab232222')
        data = response.json()

        if not data['success']:
            raise Exception('No se pudo descargar.')

        download_url = check_progress(data['id'])
        await ctx.send(f"🎵 *{video['title']}*\n🔗 [Descargar Audio]({download_url})")
    except Exception as e:
        await ctx.send(f"❌ Error al descargar: {str(e)}")

# Comando para descargar video
@client.command()
async def video(ctx, *, query: str):
    if not query:
        await ctx.send("🎬 Escribe el nombre o link del video.")
        return

    # Usar yt-dlp para obtener los resultados de búsqueda
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with ytdl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if not info.get('entries'):
            await ctx.send("⚠️ No se encontraron resultados.")
            return

        video = info['entries'][0]
        video_url = video['url']

    try:
        # Obtener enlace de descarga de video en 720p
        response = requests.get(f'https://p.oceansaver.in/ajax/download.php?format=720&url={video_url}&api=dfcb6d76f2f6a9894gjkege8a4ab232222')
        data = response.json()

        if not data['success']:
            raise Exception('No se pudo descargar.')

        download_url = check_progress(data['id'])
        await ctx.send(f"🎬 *{video['title']}*\n🔗 [Descargar Video]({download_url})")
    except Exception as e:
        await ctx.send(f"❌ Error al descargar: {str(e)}")

# Comandos de moderación
@client.command()
async def ban(ctx, user: discord.User):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ No tienes permisos.")
        return
    await ctx.guild.ban(user)
    await ctx.send(f"🔨 Usuario baneado: {user}")

@client.command()
async def kick(ctx, user: discord.User):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ No tienes permisos.")
        return
    await ctx.guild.kick(user)
    await ctx.send(f"👢 Usuario expulsado: {user}")

# Comando de juegos
@client.command()
async def dado(ctx):
    resultado = random.randint(1, 6)
    await ctx.send(f"🎲 Has sacado un **{resultado}**")

@client.command()
async def ball(ctx):
    respuestas = ["Sí", "No", "Tal vez", "Pregunta otra vez", "No lo sé"]
    respuesta = random.choice(respuestas)
    await ctx.send(f"🎱 Respuesta: {respuesta}")

# Comando de memes
@client.command()
async def meme(ctx):
    response = requests.get('https://meme-api.com/gimme')
    if response.status_code == 200:
        meme_url = response.json()['url']
        await ctx.send(meme_url)
    else:
        await ctx.send('❌ Error al obtener un meme.')

# Comando de información
@client.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! Latencia: {client.latency * 1000:.2f}ms')

# Comando para obtener el avatar de un usuario
@client.command()
async def avatar(ctx, user: discord.User = None):
    user = user or ctx.author
    await ctx.send(user.avatar_url)

# Comando para cambiar prefijo (opcional)
@client.command()
async def setprefix(ctx, new_prefix: str):
    global PREFIX
    PREFIX = new_prefix
    await ctx.send(f"✅ Prefijo cambiado a: {new_prefix}")

# comando para generar waifus
@client.command()
async def waifu(ctx):
    """Comando para generar una waifu aleatoria"""
    try:
        # Hacer la solicitud a la API de waifu.pics para obtener una waifu
        response = requests.get('https://api.waifu.pics/sfw/waifu')

        if response.status_code == 200:
            data = response.json()
            waifu_image_url = data['url']  # Obtén la URL de la imagen

            # Enviar la imagen de la waifu al canal
            await ctx.send(waifu_image_url)
        else:
            await ctx.send("❌ No se pudo obtener la imagen de waifu.")
    except Exception as e:
        await ctx.send(f"❌ Error al generar la waifu: {str(e)}")

#comando de descargar música 
@client.command()
async def download(ctx, url: str, media_type: str = 'audio'):
    """Comando para descargar audio o video de YouTube.
    
    Argumentos:
    url -- Enlace de YouTube.
    media_type -- 'audio' para descargar solo el audio, 'video' para descargar el video.
    """
    await ctx.send(f"🔽 Iniciando descarga de {media_type}...")

    # Definir opciones de yt-dlp dependiendo del tipo de medio
    if media_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif media_type == 'video':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'quiet': True,
        }
    else:
        await ctx.send("❌ Tipo de medio no válido. Usa 'audio' o 'video'.")
        return

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Descargar el archivo de YouTube
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)

            # Enviar el archivo descargado
            if media_type == 'audio':
                await ctx.send(f"🎵 Aquí tienes el audio de *{info_dict['title']}*:", file=discord.File(filename))
            elif media_type == 'video':
                await ctx.send(f"🎬 Aquí tienes el video de *{info_dict['title']}*:", file=discord.File(filename))
            
            # Borrar el archivo después de enviarlo
            os.remove(filename)

    except Exception as e:
        await ctx.send(f"❌ Error al descargar el archivo: {str(e)}")

#comando de info del bot
@client.command()
async def info(ctx):
    """Comando para obtener información del bot, como el uso de RAM, servidores y más."""
    
    # Obtener uso de RAM (memoria en MB)
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # En MB

    # Obtener información sobre el sistema
    system_info = platform.uname()

    # Obtener el número de servidores y canales
    guild_count = len(client.guilds)
    channel_count = sum(len(guild.text_channels) + len(guild.voice_channels) for guild in client.guilds)

    embed = discord.Embed(
        title="Información del Bot",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="Sistema", value=f"{system_info.system} {system_info.release} ({system_info.machine})", inline=False)
    embed.add_field(name="Versión de Python", value=f"{platform.python_version()}", inline=False)
    embed.add_field(name="Uso de RAM", value=f"{memory_usage:.2f} MB", inline=False)
    embed.add_field(name="Servidores", value=f"{guild_count} servidores", inline=False)
    embed.add_field(name="Canales", value=f"{channel_count} canales", inline=False)
    embed.add_field(name="Hosting", value="SKAHOSTING", inline=False)  # O el nombre del hosting si es otro

    await ctx.send(embed=embed)

# Configuración del bot
OWNER_ID = 1252023555487567932  # Reemplaza con tu ID de Discord

# Función para verificar si el usuario es el dueño
def is_owner(ctx):
    return ctx.author.id == OWNER_ID

# Comando para reiniciar el bot
@client.command()
async def restart(ctx):
    """Reinicia el bot (Solo el owner)."""
    if not is_owner(ctx):
        await ctx.send("❌ No tienes permisos para ejecutar este comando.")
        return
    
    await ctx.send("🔄 Reiniciando el bot...")
    await client.close()  # Cierra el bot para que se reinicie en Replit automáticamente

# Comando para eliminar archivos innecesarios y mostrar cuántos eliminó
@client.command()
async def delai(ctx):
    """Elimina archivos almacenados que no sirven (Solo el owner)."""
    if not is_owner(ctx):
        await ctx.send("❌ No tienes permisos para ejecutar este comando.")
        return
    
    try:
        dirs_to_clean = ["temp", "logs", "cache"]  # Carpetas a limpiar
        total_deleted_files = 0
        total_deleted_folders = 0

        for directory in dirs_to_clean:
            if os.path.exists(directory):
                file_count = sum([len(files) for _, _, files in os.walk(directory)])  # Cuenta archivos en la carpeta
                shutil.rmtree(directory)
                total_deleted_files += file_count
                total_deleted_folders += 1
        
        await ctx.send(f"✅ Se eliminaron {total_deleted_folders} carpetas y {total_deleted_files} archivos innecesarios.")
    
    except Exception as e:
        await ctx.send(f"❌ Error al eliminar archivos: {str(e)}")

# Comando para eliminar sesiones activas innecesarias y mostrar cuántas eliminó
@client.command()
async def ds(ctx):
    """Elimina sesiones que no sirven (Solo el owner)."""
    if not is_owner(ctx):
        await ctx.send("❌ No tienes permisos para ejecutar este comando.")
        return
    
    try:
        session_files = ["session.data", "session.lock", "session.json"]
        deleted_files = []
        
        for file in session_files:
            if os.path.exists(file):
                os.remove(file)
                deleted_files.append(file)
        
        if deleted_files:
            await ctx.send(f"✅ Se eliminaron {len(deleted_files)} sesiones: {', '.join(deleted_files)}")
        else:
            await ctx.send("⚠️ No había sesiones activas para eliminar.")
    
    except Exception as e:
        await ctx.send(f"❌ Error al eliminar sesiones: {str(e)}")

# Diccionario de imágenes para los comandos
imagenes_comandos = {
    "info": "https://ibb.co/RTzbyCN2",
    "ping": "https://ibb.co/7tkRQdHQ",
    "ban": "https://ibb.co/sd9DFgrh",
    "kick": "https://ibb.co/LhC3xWx1",
    "mute": "https://ibb.co/nqYts6D5",
}

#informacion del owner
@client.command()
async def owner(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Solo el creador del bot puede usar este comando.")
        return

    embed = discord.Embed(
        title="👑 Creadora del Bot",
        description="Información de la persona que hizo posible este bot.",
        color=discord.Color.gold()
    )
    embed.set_thumbnail(url="https://ibb.co/RTzbyCN2")  # Cambia la imagen si quieres
    embed.add_field(name="👩‍💻 Nombre", value="Natalia Zuleta", inline=False)
    embed.add_field(name="📞 Contacto", value="+5592996077349", inline=False)
    embed.add_field(name="📌 Descripción", value="Soy la creadora de este bot y diseñadora quien edito el bot 💋❤️.", inline=False)
    
    await ctx.send(embed=embed)

# Lista de templates de memes disponibles
templates = [
    "drake/not_this/YES.png",
    "expanding_brain/Expandiendo/el/cerebro.png",
    "one_does_not/simply/NO.png",
    "why_though/por_que/NO.png",
    "condescending_wonka/Este/es/el/mejor/YES.png",
    "success_kid/Exito/YES.png"
]

# Función para generar meme aleatorio sin repetirse
used_templates = set()  # Guarda los templates ya usados

def generar_meme(texto_arriba, texto_abajo):
    # Asegurarse de que no se repita el mismo template
    available_templates = [t for t in templates if t not in used_templates]
    
    if not available_templates:
        used_templates.clear()  # Reinicia la lista si todos los templates han sido usados
    
    meme_template = random.choice(available_templates)
    meme_url = f"https://api.memegen.link/images/{meme_template.replace('YES', texto_arriba).replace('NO', texto_abajo)}"
    
    # Marcar este template como usado
    used_templates.add(meme_template)
    
    return meme_url

@client.command()
async def mme(ctx, *, texto: str):
    """
    Genera un meme aleatorio con un texto proporcionado.
    El comando debe ser usado como #mme texto_arriba|texto_abajo
    """
    # Verificar si el texto tiene dos partes separadas por "|"
    if "|" not in texto:
        await ctx.send("Por favor, usa el formato correcto: #mme texto_arriba|texto_abajo")
        return

    texto_arriba, texto_abajo = texto.split("|", 1)

    # Generar meme con los textos proporcionados
    meme_url = generar_meme(texto_arriba, texto_abajo)

    # Enviar el meme generado
    await ctx.send(meme_url)
    
# ✅ Activar todos los permisos necesarios
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# 📂 Archivo donde se guardarán los usuarios
USERS_FILE = "users.json"

# 📌 Imágenes para los embeds
IMAGEN_REGISTRO = "https://i.ibb.co/rtXByCN/registro.jpg"
IMAGEN_PERFIL = "https://i.ibb.co/7tkRQdHQ/perfil.jpg"
IMAGEN_NIVEL_UP = "https://i.ibb.co/sd9DFgr/nivel-up.jpg"
IMAGEN_ADVERTENCIA = "https://i.ibb.co/LhC3xWx/advertencia.jpg"

# 📜 Cargar o crear el archivo de usuarios
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

def cargar_usuarios():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def guardar_usuarios(usuarios):
    with open(USERS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)

# 🔹 Comando de REGISTRO
@client.command()
async def reg(ctx, *, info):
    usuarios = cargar_usuarios()
    user_id = str(ctx.author.id)

    if user_id in usuarios:
        await ctx.send("⚠️ Ya estás registrado en el sistema.")
        return

    try:
        nombre, edad = info.split(".")
        usuarios[user_id] = {
            "nombre": nombre,
            "edad": edad,
            "nivel": 1,
            "xp": 0,
            "advertencias": 0
        }
        guardar_usuarios(usuarios)

        embed = discord.Embed(title="✅ Registro Completado", color=discord.Color.green())
        embed.set_thumbnail(url=IMAGEN_REGISTRO)
        embed.add_field(name="📛 Nombre", value=nombre, inline=True)
        embed.add_field(name="🎂 Edad", value=edad, inline=True)
        embed.set_footer(text="Bienvenido al sistema")
        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Formato incorrecto. Usa el comando así: `#reg nombre.edad`\nEjemplo: `#reg NATI.16`")

# 🔹 Comando para VER PERFIL
@client.command()
async def profile(ctx):
    usuarios = cargar_usuarios()
    user_id = str(ctx.author.id)

    if user_id not in usuarios:
        await ctx.send("⚠️ No estás registrado. Usa `#reg nombre.edad` para registrarte.")
        return

    datos = usuarios[user_id]
    embed = discord.Embed(title=f"Perfil de {ctx.author.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=IMAGEN_PERFIL)
    embed.add_field(name="📛 Nombre", value=datos["nombre"], inline=True)
    embed.add_field(name="🎂 Edad", value=datos["edad"], inline=True)
    embed.add_field(name="⭐ Nivel", value=datos["nivel"], inline=True)
    embed.add_field(name="🎮 Experiencia", value=datos["xp"], inline=True)
    embed.add_field(name="🚨 Advertencias", value=datos["advertencias"], inline=True)
    embed.set_footer(text="Tu información en el sistema")
    await ctx.send(embed=embed)

# 🔹 Comando para ADVERTIR USUARIOS
@client.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member, *, reason="No especificado"):
    usuarios = cargar_usuarios()
    user_id = str(member.id)

    if user_id not in usuarios:
        await ctx.send("⚠️ El usuario no está registrado en el sistema.")
        return

    usuarios[user_id]["advertencias"] += 1
    guardar_usuarios(usuarios)

    embed = discord.Embed(title="⚠️ Advertencia", color=discord.Color.red())
    embed.set_thumbnail(url=IMAGEN_ADVERTENCIA)
    embed.add_field(name="👤 Usuario", value=member.mention, inline=True)
    embed.add_field(name="📜 Razón", value=reason, inline=True)
    embed.add_field(name="🚨 Total Advertencias", value=usuarios[user_id]["advertencias"], inline=True)
    embed.set_footer(text="Sistema de advertencias")
    await ctx.send(embed=embed)

    if usuarios[user_id]["advertencias"] >= 3:
        await ctx.guild.ban(member, reason="Acumuló 3 advertencias")
        await ctx.send(f"🚨 {member.mention} ha sido **baneado** por acumular 3 advertencias.")

# 🔹 Comando de SUBIR DE NIVEL
@client.command()
async def adventure(ctx):
    usuarios = cargar_usuarios()
    user_id = str(ctx.author.id)

    if user_id not in usuarios:
        await ctx.send("⚠️ No estás registrado. Usa `#reg nombre.edad` para registrarte.")
        return

    xp_ganado = random.randint(5, 15)
    usuarios[user_id]["xp"] += xp_ganado

    # Si el XP es mayor a 50, sube de nivel
    if usuarios[user_id]["xp"] >= 50:
        usuarios[user_id]["xp"] = 0
        usuarios[user_id]["nivel"] += 1
        nivel_up = True
    else:
        nivel_up = False

    guardar_usuarios(usuarios)

    embed = discord.Embed(title="🎮 Aventura", color=discord.Color.purple())
    embed.set_thumbnail(url=IMAGEN_NIVEL_UP if nivel_up else IMAGEN_PERFIL)
    embed.add_field(name="👤 Usuario", value=ctx.author.mention, inline=True)
    embed.add_field(name="🆙 XP Ganado", value=xp_ganado, inline=True)
    embed.add_field(name="⭐ Nivel", value=usuarios[user_id]["nivel"], inline=True)
    embed.set_footer(text="Sigue jugando para subir de nivel")
    await ctx.send(embed=embed)

    if nivel_up:
        await ctx.send(f"🎉 ¡Felicidades {ctx.author.mention}! **Has subido al nivel {usuarios[user_id]['nivel']}** 🎉")

# 📂 Archivo donde están los subbots
SUBBOTS_FILE = "subbots.json"

# 📌 Función para cargar subbots
def cargar_subbots():
    with open(SUBBOTS_FILE, "r") as f:
        return json.load(f)

# 📌 Lista de subbots en ejecución
subbots_activos = []

async def iniciar_subbot(token, nombre):

    @client.event
    async def on_ready():
        print(f"✅ Subbot {nombre} conectado como {client.user}")

    @client.command()
    async def hola(ctx):
        await ctx.send(f"👋 ¡Hola! Soy un subbot de {nombre}")

    # Puedes agregar más comandos aquí...

    await client.start(token)

async def iniciar_todos_subbots():
    subbots = cargar_subbots()
    tareas = []

    for user_id, data in subbots.items():
        token = data["token"]
        nombre = data["nombre"]
        tarea = asyncio.create_task(iniciar_subbot(token, nombre))
        subbots_activos.append(tarea)

    await asyncio.gather(*subbots_activos)

# Cambia esto con tu token del bot
OWNER_ID = 1252023555487567932  # Reemplázalo con tu ID de Discord
GITHUB_REPO = "https://github.com/nati-1616/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"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="#", intents=intents)

# Comando para subir los cambios a GitHub
@client.command()
async def subirgit(ctx):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ No tienes permisos para usar este comando.")

    try:
        repo = git.Repo(os.getcwd())  # Obtiene el repositorio
        repo.git.add(".")  # Agrega todos los cambios
        repo.index.commit("Actualización desde Replit")  # Confirma los cambios
        repo.remote().push()  # Sube los cambios
        await ctx.send("✅ Bot actualizado en GitHub.")
    except Exception as e:
        await ctx.send(f"❌ Error al subir: `{e}`")

# Comando para actualizar el bot desde GitHub
@client.command()
async def actualizar(ctx):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ No tienes permisos para usar este comando.")

    try:
        repo = git.Repo(os.getcwd())
        origin = repo.remote()
        origin.pull()  # Descarga la última versión del repositorio
        await ctx.send("✅ Bot actualizado. Reiniciando...")
        os.system("kill 1")  # Reinicia el bot en Replit
    except Exception as e:
        await ctx.send(f"❌ Error al actualizar: `{e}`")

# Variables globales
PALABRAS_PROHIBIDAS = [
    "puta", "porno", "nsfw", "joder", "mierda", "idiota", "nopor", "pornografía", "hentai", 
    "sexo", "fuck", "bitch", "masturbación", "dildo", "pornhub", "redtube", "xvideos", "hentaitube",
    "porno explícito", "violación", "pedofilia", "abuso", "abusivo", "racismo", "nazismo", "discriminación",
    "terrorismo", "asesinato", "suicidio", "feminista", "racista", "odio", "violento", "drogas", "crack",
    "cocaína", "heroína", "crack", "mdma", "metanfetamina", "marihuana", "weed", "bitchass", "slut",
    "fuck you", "asshole", "cunt", "motherfucker", "douchebag", "bastard", "cock", "pussy", "tits", "penis",
    "sex", "pornografía infantil", "pervertido", "zoofilia", "sado", "macho", "drogadicto", "loco", "imbécil",
    "idiota", "maricón", "tranny", "gordo", "freak", "zorra", "bitch", "stupid", "dumbass", "prick", "cabrón",
    "basura", "mierdero", "escoria", "tóxico", "puta madre", "maldito", "bestia", "ganso", "pendejo", "cerdo",
    "tarado", "mongólico", "cabronazo", "slutty", "fuckface", "ugly", "bitching", "racista",    ]

EXTENSIONES_NSFW = [
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".mp4", ".avi", ".mov", ".wmv", ".mkv", ".flv", ".svg", ".bmp", ".tiff"
]

# Comando #kiss
@client.command()
async def kiss(ctx, member: discord.Member):
    """Comando para enviar un gif de un anime dándole un beso al etiquetado"""
    
    # URL para obtener el gif de Tenor
    url = 'https://api.tenor.com/v1/search'
    params = {
        'q': 'anime kiss',
        'key': 'LIVDSRZULELA',  # Esta es la clave de API pública de Tenor
        'limit': 1  # Puede enviar más GIFs si quieres ajustar el número
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['results']:
        gif_url = data['results'][0]['media'][0]['gif']['url']
        await ctx.send(f'{ctx.author.mention} le da un beso a {member.mention} 😘', embed=discord.Embed().set_image(url=gif_url))
    else:
        await ctx.send("Lo siento, no pude encontrar un GIF para eso 😞")

# Comando #slap (Cachetada)
@client.command()
async def slap(ctx, member: discord.Member):
    """Comando para enviar un gif de una anime dándole una cachetada al etiquetado"""
    
    # URL para obtener el gif de Tenor
    url = 'https://api.tenor.com/v1/search'
    params = {
        'q': 'anime slap',
        'key': 'LIVDSRZULELA',  # Esta es la clave de API pública de Tenor
        'limit': 50  # Límite de resultados
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['results']:
        # Obtener el URL del GIF
        gif_url = data['results'][0]['media'][0]['gif']['url']
        
        # Crear el embed con más detalles para que se vea más profesional
        embed = discord.Embed(
            title="¡Cachetada!", 
            description=f"{ctx.author.mention} acaba de darle una cachetada a {member.mention}! 😳",
            color=discord.Color.red()
        )
        
        embed.set_image(url=gif_url)  # Agregar la imagen del GIF
        embed.set_footer(text="¡Ouch! Eso debe haber dolido...")  # Mensaje en el pie del embed
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("Lo siento, no pude encontrar un GIF para eso 😞")

# Comando #hug (abrazo)
@client.command()
async def hug(ctx, member: discord.Member):
    """Comando para enviar un gif de un anime dando un abrazo al etiquetado"""
    
    # URL para obtener el gif de Tenor
    url = 'https://api.tenor.com/v1/search'
    params = {
        'q': 'anime hug',
        'key': 'LIVDSRZULELA',  # Esta es la clave de API pública de Tenor
        'limit': 50  # Límite de resultados
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['results']:
        gif_url = data['results'][0]['media'][0]['gif']['url']
        await ctx.send(f'{ctx.author.mention} le da un abrazo a {member.mention} 🤗', embed=discord.Embed().set_image(url=gif_url))
    else:
        await ctx.send("Lo siento, no pude encontrar un GIF para eso 😞")

# Comando #embarazar
@client.command()
async def embarazar(ctx, member: discord.Member):
    """Comando para enviar un gif humorístico de un anime embarazando al etiquetado"""
    
    # URL para obtener el gif de Tenor
    url = 'https://api.tenor.com/v1/search'
    params = {
        'q': 'anime pregnancy',
        'key': 'LIVDSRZULELA',  # Esta es la clave de API pública de Tenor
        'limit': 50  # Limite de resultados (hasta 50 diferentes GIFs)
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['results']:
        # Elegir un GIF aleatorio de los resultados
        gif_url = random.choice(data['results'])['media'][0]['gif']['url']
        
        # Crear el embed con más detalles para hacerlo divertido
        embed = discord.Embed(
            title="¡Sorpresa! Embarazo en el aire",
            description=f"{ctx.author.mention} acaba de embarazar a {member.mention}... 😳",
            color=discord.Color.purple()
        )
        
        embed.set_image(url=gif_url)  # Agregar la imagen del GIF
        embed.set_footer(text="¿Qué estará pasando ahora? 🤔")  # Mensaje en el pie del embed
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("Lo siento, no pude encontrar un GIF para eso 😞")
        

# Base de datos en un archivo JSON
def abrir_datos():
    try:
        with open("economia.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_datos(data):
    with open("economia.json", "w") as f:
        json.dump(data, f, indent=4)

# **Comando para ver el balance**
@client.command()
async def balance(ctx):
    user = str(ctx.author.id)
    data = abrir_datos()
    
    if user not in data:
        data[user] = {"dinero": 500, "banco": 0}
    
    dinero = data[user]["dinero"]
    banco = data[user]["banco"]
    
    embed = discord.Embed(title=f"💰 Balance de {ctx.author.name}", color=discord.Color.green())
    embed.add_field(name="Cartera", value=f"💵 {dinero}", inline=True)
    embed.add_field(name="Banco", value=f"🏦 {banco}", inline=True)
    
    await ctx.send(embed=embed)
    guardar_datos(data)

# **Comando para trabajar**
@client.command()
async def trabajar(ctx):
    user = str(ctx.author.id)
    data = abrir_datos()
    
    if user not in data:
        data[user] = {"dinero": 500, "banco": 0}
    
    salario = random.randint(100, 500)
    data[user]["dinero"] += salario

    embed = discord.Embed(
        title="💼 Trabajaste y ganaste dinero!",
        description=f"{ctx.author.mention} ha trabajado y ganó 💵 {salario}",
        color=discord.Color.blue()
    )
    
    await ctx.send(embed=embed)
    guardar_datos(data)

# **Comando para depositar en el banco**
@client.command()
async def depositar(ctx, cantidad: int):
    user = str(ctx.author.id)
    data = abrir_datos()
    
    if user not in data or data[user]["dinero"] < cantidad:
        await ctx.send("❌ No tienes suficiente dinero para depositar.")
        return

    data[user]["dinero"] -= cantidad
    data[user]["banco"] += cantidad

    await ctx.send(f"✅ {ctx.author.mention} ha depositado 💵 {cantidad} en el banco.")
    guardar_datos(data)

# **Comando para retirar del banco**
@client.command()
async def retirar(ctx, cantidad: int):
    user = str(ctx.author.id)
    data = abrir_datos()
    
    if user not in data or data[user]["banco"] < cantidad:
        await ctx.send("❌ No tienes suficiente dinero en el banco para retirar.")
        return

    data[user]["banco"] -= cantidad
    data[user]["dinero"] += cantidad

    await ctx.send(f"✅ {ctx.author.mention} ha retirado 💵 {cantidad} del banco.")
    guardar_datos(data)

# **Comando para robar dinero**
@client.command()
async def robar(ctx, miembro: discord.Member):
    user = str(ctx.author.id)
    victima = str(miembro.id)
    data = abrir_datos()

    if user not in data:
        data[user] = {"dinero": 500, "banco": 0}
    if victima not in data:
        data[victima] = {"dinero": 500, "banco": 0}

    if data[victima]["dinero"] < 100:
        await ctx.send("❌ No puedes robar a alguien que tiene menos de 100 en la cartera.")
        return

    probabilidad = random.randint(1, 100)
    if probabilidad <= 50:
        monto = random.randint(50, 200)
        data[user]["dinero"] += monto
        data[victima]["dinero"] -= monto
        await ctx.send(f"💰 {ctx.author.mention} robó exitosamente 💵 {monto} a {miembro.mention}.")
    else:
        multa = random.randint(50, 200)
        data[user]["dinero"] -= multa
        await ctx.send(f"🚔 {ctx.author.mention} intentó robar a {miembro.mention} y fue atrapado. Pagó una multa de 💵 {multa}.")

    guardar_datos(data)

# 📌 Productos de la tienda (ahora llamado `productos_tienda` para evitar errores)
productos_tienda = {
    "VIP": 1000,
    "Premium": 2000,
    "Role Legendario": 5000
}

@client.command()
async def tienda(ctx):
    embed = discord.Embed(title="🛒 Tienda del Servidor", color=discord.Color.gold())
    
    for item, precio in productos_tienda.items():  # ✅ Ahora funciona sin errores
        embed.add_field(name=item, value=f"💵 {precio}", inline=False)
    
    await ctx.send(embed=embed)

@client.command()
async def comprar(ctx, item: str):
    user = str(ctx.author.id)
    data = abrir_datos()  # Asegurar que se carga el dinero del usuario

    if item not in productos_tienda:
        await ctx.send("❌ Ese objeto no está en la tienda.")
        return

    if user not in data or data[user]["dinero"] < productos_tienda[item]:
        await ctx.send("❌ No tienes suficiente dinero para comprar eso.")
        return

    data[user]["dinero"] -= productos_tienda[item]
    
    guardar_datos(data)  # ✅ Ahora guarda los cambios correctamente

    await ctx.send(f"✅ {ctx.author.mention} ha comprado **{item}** por 💵 {productos_tienda[item]}.")

# Genera un token aleatorio
def generar_token():
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return token

# Función para verificar si el token es válido
def validar_token(token):
    try:
        with open("tokens.json", "r") as file:
            tokens = json.load(file)
    except FileNotFoundError:
        return False

    return token in tokens and not tokens[token]["activo"]

# Función para activar el token en el archivo
def activar_token(token, user_id):
    try:
        with open("tokens.json", "r") as file:
            tokens = json.load(file)
    except FileNotFoundError:
        tokens = {}

    if token in tokens and not tokens[token]["activo"]:
        tokens[token]["activo"] = True
        tokens[token]["user_id"] = user_id

        with open("tokens.json", "w") as file:
            json.dump(tokens, file)

# Comando para generar un token (solo para el propietario)
@client.command(name="token")
async def generar_token_cmd(ctx):
    if ctx.author.id == 1252023555487567932:  # Reemplaza con tu ID de Discord
        token = generar_token()
        # Guarda el token en el archivo JSON como inactivo
        try:
            with open("tokens.json", "r") as file:
                tokens = json.load(file)
        except FileNotFoundError:
            tokens = {}

        tokens[token] = {"activo": False, "user_id": None}
        with open("tokens.json", "w") as file:
            json.dump(tokens, file)

        await ctx.send(f"Tu token Premium generado es: **{token}**")
    else:
        await ctx.send("❌ No tienes permisos para usar este comando.")

# Comando para activar Premium con un token
@client.command(name="premium")
async def activar_premium(ctx, token: str):
    if validar_token(token):
        activar_token(token, ctx.author.id)
        await ctx.send(f"🎉 {ctx.author.mention}, ¡has activado tu cuenta Premium con el token! 🎉")
    else:
        await ctx.send(f"❌ {ctx.author.mention}, el token es inválido o ya fue usado.")

    # Verifica si el token existe y no ha sido usado
    if token in tokens and not tokens[token]["activo"]:
        tokens[token]["activo"] = True  # Marca el token como usado
        tokens[token]["user_id"] = ctx.author.id  # Asigna el usuario

        with open("tokens.json", "w") as file:
            json.dump(tokens, file, indent=4)

        await ctx.send(f"✅ {ctx.author.mention}, tu cuenta ahora es **Premium**. ¡Disfruta de los beneficios! 🎉")
    else:
        await ctx.send("❌ Token inválido o ya ha sido usado.")
        
# Verifica si el usuario tiene premium
def es_premium(user_id):
    try:
        with open("tokens.json", "r") as file:
            tokens = json.load(file)
    except FileNotFoundError:
        return False

    for token, datos in tokens.items():
        if datos.get("user_id") == user_id and datos.get("activo"):
            return True
    return False

# Comando de ruleta de la suerte para usuarios premium
@client.command(name="ruleta")
async def ruleta_premium(ctx):
    if es_premium(ctx.author.id):  # Verifica si el usuario tiene premium
        premios = ["500 monedas", "nada 😢", "un cofre sorpresa", "un ítem raro", "1000 monedas"]
        premio = random.choice(premios)
        imagen = "ruleta_imagen.jpg"  # Ruta de la imagen de la ruleta (asegúrate de tener esta imagen en tu directorio)

        # Enviar mensaje con imagen
        await ctx.send(f"🎰 {ctx.author.mention} giró la ruleta y ganó: **{premio}**! 🎉", file=File(imagen))
    else:
        await ctx.send("❌ No tienes acceso a este comando. Activa Premium con `#premium <token>`.")

#buscador de play2
def generar_nombre():
    """Genera un nombre aleatorio para el archivo de audio."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".mp3"

def buscar_video(query):
    """Busca un video en YouTube y devuelve su información."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(query, download=False)
            if 'entries' in result:
                video = result['entries'][0]
            else:
                video = result
            return {
                'title': video.get('title'),
                'channel': video.get('uploader'),
                'duration': video.get('duration'),
                'views': video.get('view_count'),
                'url': video.get('webpage_url'),
                'thumbnail': video.get('thumbnail')  # Miniatura del video
            }
        except Exception as e:
            print(f"Error al buscar el video: {e}")
            return None

def descargar_audio(url):
    """Descarga el audio de un video de YouTube."""
    nombre_archivo = generar_nombre()
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': nombre_archivo,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return nombre_archivo

@client.command(name="play2")
async def play2(ctx, *, query: str):
    """Busca un video en YouTube, muestra su info y envía el audio."""
    info = buscar_video(query)
    if not info:
        await ctx.send("❌ No se encontró el video.")
        return

    embed = discord.Embed(title=info["title"], url=info["url"], color=discord.Color.blue())
    embed.set_author(name=info["channel"])
    embed.set_thumbnail(url=info["thumbnail"])
    embed.add_field(name="⏳ Duración", value=f"{info['duration'] // 60}:{info['duration'] % 60:02d} minutos", inline=True)
    embed.add_field(name="👀 Vistas", value=f"{info['views']:,}", inline=True)
    
    await ctx.send(embed=embed)
    
    await ctx.send("🎶 Descargando el audio, espera un momento...")
    archivo_audio = descargar_audio(info["url"])

    await ctx.send("✅ Audio descargado, enviando...")

    with open(archivo_audio, "rb") as f:
        await ctx.send(file=discord.File(f, filename="audio.mp3"))

    os.remove(archivo_audio)

# Función para obtener una imagen waifu NSFW de waifu.pics
def get_waifu_image():
    url = "https://api.waifu.pics/nsfw/waifu"
    response = requests.get(url)
    data = response.json()
    return data['url']

# Función para obtener una imagen waifu NSFW más realista (puedes usar otra API aquí si la tienes)
def get_realistic_waifu():
    url = "https://api.waifu.pics/nsfw/realistic"  # Suponiendo que tienes una API similar
    response = requests.get(url)
    data = response.json()
    return data['url']

# Comando #wfu para imagen NSFW waifu
@client.command()
async def wfu(ctx):
    # Obtener imagen NSFW de waifu
    image_url = get_waifu_image()
    
    # Crear un embed para mostrar la imagen
    embed = discord.Embed(title="Waifu NSFW", description="Aquí tienes una waifu NSFW", color=0xFF00FF)
    embed.set_image(url=image_url)
    
    # Enviar el embed en el canal de Discord
    await ctx.send(embed=embed)

# Comando #ft para imagen NSFW waifu más realista
@client.command()
async def ft(ctx):
    # Obtener imagen NSFW waifu más realista
    image_url = get_realistic_waifu()
    
    # Crear un embed para mostrar la imagen
    embed = discord.Embed(title="Waifu NSFW Realista", description="Aquí tienes una waifu más realista NSFW", color=0xFF00FF)
    embed.set_image(url=image_url)
    
    # Enviar el embed en el canal de Discord
    await ctx.send(embed=embed)

#comando para saber el clima
@client.command(name="clima")
async def clima(ctx, *, ciudad: str):
    try:
        # API Pública sin registro
        url = f"https://wttr.in/{ciudad}?format=%C+%t+%w+%m+%p+%h"
        datos = requests.get(url).text.split()

        estado = datos[0]  # Soleado, Lluvia, Nublado
        temperatura = datos[1]  # Temperatura actual
        viento = datos[2]  # Velocidad del viento
        humedad = datos[3]  # Humedad
        presion = datos[4]  # Presión atmosférica
        lluvia = datos[5]  # Probabilidad de lluvia

        imagen_url = f"https://wttr.in/{ciudad}_0tqp.png"

        # Pronóstico de 3 días
        forecast_url = f"https://wttr.in/{ciudad}?m&format=3"

        # Embed profesional
        embed = discord.Embed(
            title=f"🌤 Clima en {ciudad.capitalize()}",
            description=f"**Estado:** {estado}\n🌡 **Temperatura:** {temperatura}\n💨 **Viento:** {viento}\n💧 **Humedad:** {humedad}\n🌧 **Lluvia:** {lluvia}\n⚖ **Presión:** {presion}",
            color=discord.Color.blue()
        )
        embed.set_image(url=imagen_url)
        embed.add_field(name="🔮 Pronóstico 3 días", value=f"```{requests.get(forecast_url).text}```", inline=False)
        embed.set_footer(text="Fuente: wttr.in")

        await ctx.send(embed=embed)

    except Exception:
        await ctx.send("❌ No se pudo obtener el clima. Verifica el nombre de la ciudad.")

#estado del bot a tiempo real
comandos_usados = {}

@client.event
async def on_command(ctx):
    comando = ctx.command.name
    usuario = ctx.author.name
    if comando not in comandos_usados:
        comandos_usados[comando] = {"usos": 0, "fallos": 0, "tiempo": 0}
    comandos_usados[comando]["usos"] += 1
    ctx.start_time = time.time()  # Iniciar contador de tiempo

@client.event
async def on_command_completion(ctx):
    comando = ctx.command.name
    tiempo = round(time.time() - ctx.start_time, 3)  # Calcular tiempo
    comandos_usados[comando]["tiempo"] = tiempo

@client.event
async def on_command_error(ctx, error):
    comando = ctx.command.name if ctx.command else "Desconocido"
    usuario = ctx.author.name
    if comando not in comandos_usados:
        comandos_usados[comando] = {"usos": 0, "fallos": 0, "tiempo": 0}
    comandos_usados[comando]["fallos"] += 1

@client.command(name="statusbot")
async def statusbot(ctx):
    owner_id = 1252023555487567932  # Reemplaza con tu ID de Discord
    if ctx.author.id != owner_id:
        await ctx.send("❌ No tienes permisos para ver el estado del bot.")
        return
    
    embed = discord.Embed(
        title="📊 Estado del Bot",
        description="Verificación de comandos en tiempo real.",
        color=discord.Color.green()
    )

    for command in bot.commands:
        nombre = command.name
        usos = comandos_usados.get(nombre, {}).get("usos", 0)
        fallos = comandos_usados.get(nombre, {}).get("fallos", 0)
        tiempo = comandos_usados.get(nombre, {}).get("tiempo", 0)

        if fallos > 0:
            estado = "❌ **No Funciona**"
        elif usos > 0:
            estado = "✅ **Funciona Bien**"
        else:
            estado = "⚠ **Nunca usado**"

        embed.add_field(
            name=f"⚙ {nombre}",
            value=f"📌 Estado: {estado}\n▶ Usos: {usos} | ❌ Fallos: {fallos}\n⏱ **Tiempo de ejecución:** {tiempo}s",
            inline=False
        )

    await ctx.send(embed=embed)

#descargas de audio

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Busca el archivo descargado (en formato mp3)
    for file in os.listdir():
        if file.startswith("audio") and file.endswith(".mp3"):
            return file
    return None

@bot.command()
async def play2(ctx, url: str):
    await ctx.send("Descargando audio...")
    audio_file = download_audio(url)
    
    if audio_file:
        await ctx.send(file=discord.File(audio_file))
        os.remove(audio_file)  # Elimina el archivo después de enviarlo
    else:
        await ctx.send("Hubo un error al descargar el audio.")

#comando para descarga vídeo 2.0
@client.command(name="video2")
async def video2(ctx, *, query: str):
    if not query:
        await ctx.send("🎬 Escribe el nombre o el enlace del video.")
        return

    # Configuración de yt-dlp para búsqueda
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with ytdl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if not info.get('entries'):
            await ctx.send("⚠️ No se encontraron resultados.")
            return

        video = info['entries'][0]
        video_url = video['url']
        title = video.get('title', 'Título desconocido')
        uploader = video.get('uploader', 'Desconocido')
        duration = video.get('duration', 0)  # Duración en segundos
        thumbnail = video.get('thumbnail', '')

    # Convertir duración a formato hh:mm:ss
    duration_str = f"{duration // 3600}:{(duration % 3600) // 60}:{duration % 60}" if duration >= 3600 else f"{(duration % 3600) // 60}:{duration % 60}"

    try:
        # Obtener enlace de descarga en 720p
        response = requests.get(f'https://p.oceansaver.in/ajax/download.php?format=720&url={video_url}&api=dfcb6d76f2f6a9894gjkege8a4ab232222')
        data = response.json()

        if not data['success']:
            raise Exception("No se pudo obtener el enlace de descarga.")

        download_url = check_progress(data['id'])

        # Crear embed con color rosado
        embed = discord.Embed(
            title=f"🌸 🎬 {title}",
            description=f"📺 **Canal:** `{uploader}`\n⏳ **Duración:** `{duration_str}`\n🔗 [Ver en YouTube]({video_url})",
            color=discord.Color.magenta()  # Color rosado
        )
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name="⬇️ **Descargar**", value=f"[Haz clic aquí]({download_url})", inline=False)
        
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ **Error al descargar:** {str(e)}")

# comando de despedida
OWNER_ID = 1252023555487567932  # Reemplaza con tu ID de Discord

@client.command()
async def despedir(ctx):
    # Verifica si el usuario que ejecuta el comando es el owner
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ No tienes permiso para ejecutar este comando.")
        return
    
    mensaje_despedida = (
        "🌸 ¡Gracias por permitirme ser parte de este servidor! 🌸\n\n"
        "Fue un placer estar aquí, pero es momento de decir adiós.\n"
        "**Si necesitan algo, pueden contactar a mi dueña:**\n"
        "👑 NATI Zuleta\n"
        "📩 Contacto: [+5592996077349]\n\n"
        "¡Les deseo lo mejor! 💖"
    )

    await ctx.send(mensaje_despedida)  # Envía el mensaje de despedida
    await ctx.guild.leave()  # El bot se sale del servidor realmente

# Ejecutar el bot
client.run(BOT_TOKEN)
