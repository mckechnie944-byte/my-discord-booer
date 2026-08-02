import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. WEB SERVER ENGINE TO PASS RENDER'S HOSTING CHECK
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is awake!")

def run_web_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), MyServer)
    print(f"Web engine listening on port {port}")
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

# 2. DISCORD BOT APPLICATION ENGINE
intents = discord.Intents.default()
intents.voice_states = True 

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.tree.command(name="boo", description="Boo a user off the stage!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def boo(interaction: discord.Interaction, member: discord.User = None):
    await interaction.response.defer()
    target = member if member else interaction.user
    
    if target == interaction.user and member is None:
        await interaction.followup.send(f"👎 BOOOOOO! {interaction.user.mention} tried to boo nobody and booed themselves! 👎")
    else:
        await interaction.followup.send(f"🍅 BOOOOOO! {target.mention} is getting booed off the stage! 🍅")

    if interaction.guild is not None:
        if interaction.user.voice and interaction.user.voice.channel:
            voice_channel = interaction.user.voice.channel
            vc = discord.utils.get(bot.voice_clients, guild=interaction.guild)
            
            if not vc:
                vc = await voice_channel.connect()
                await asyncio.sleep(1) 
            elif vc.channel != voice_channel:
                await vc.move_to(voice_channel)
                await asyncio.sleep(1)
            
            if vc.is_playing():
                vc.stop()
                
            vc.play(discord.FFmpegPCMAudio('boo.mp3'))

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Success! {bot.user.name} is fully online and synchronized globally.")

# Put your secret token back inside the quotes below
bot.run('MTUzMzI2MTU5Mzk4MTM1NDAwNQ.GxmcGb.7QJrB97bGvbuOA4FU6kcmJsr6PcTOnqD24rnfc')