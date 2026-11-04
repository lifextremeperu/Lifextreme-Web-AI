"""
Cog del Asistente Comunitario RAG para Discord.
Escucha menciones y mensajes directos, procesando respuestas con Groq LPU de forma no bloqueante.
"""
import discord
from discord.ext import commands
from .rag_service import query_discord_rag

class AssistantCog(commands.Cog, name="Asistente"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignorar mensajes del propio bot
        if message.author.bot:
            return

        # Responder si mencionan al bot o si es un mensaje directo
        is_mentioned = self.bot.user in message.mentions
        is_dm = isinstance(message.channel, discord.DMChannel)

        if is_mentioned or is_dm:
            # Limpiar la mención del texto
            clean_content = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            
            if not clean_content:
                await message.reply(
                    f"🏔️ ¡Hola {message.author.mention}! Soy **MAX**, tu asistente de expediciones de Lifextreme. "
                    "Pregúntame sobre rutas técnicas en Perú (Ausangate, Salkantay, Huayhuash), aclimatación o equipo de montaña. 🧗⚡"
                )
                return

            # Indicador visual de que el bot está escribiendo
            async with message.channel.typing():
                response = await query_discord_rag(clean_content, author_name=message.author.display_name)
                # Discord limita los mensajes a 2000 caracteres
                if len(response) > 1950:
                    response = response[:1950] + "..."
                await message.reply(response)

async def setup(bot: commands.Bot):
    await bot.add_cog(AssistantCog(bot))
