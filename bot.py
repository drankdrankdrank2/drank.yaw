import discord
import json

# Bot settings
TOKEN = "MTMzOTM1MzQyNzUyODEyNjU3MA.GZaDht.CeMpnN_-s_NWvZ3BCMiaCtDpkfBYWVkGLEB698"
GUILD_ID = 1336513396119699466 # Replace with your server ID
DEBUG_ROLE_ID = 1339355313874145412  # Replace with the Debug role ID
TOKEN_FILE = "tokens.json"

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = discord.Client(intents=intents)

def load_tokens():
    """Load tokens from the JSON file."""
    try:
        with open(TOKEN_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_tokens(tokens):
    """Save tokens to the JSON file."""
    with open(TOKEN_FILE, "w") as file:
        json.dump(tokens, file, indent=4)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Check if message starts with "!"
    if message.content.startswith("!"):
        user_token = message.content[1:].strip()  # Remove "!" from the token
        tokens = load_tokens()
        
        if user_token in tokens and not tokens[user_token]["used"]:
            guild = bot.get_guild(GUILD_ID)
            role = guild.get_role(DEBUG_ROLE_ID)
            member = guild.get_member(message.author.id)
            
            if role and member:
                await member.add_roles(role)
                tokens[user_token]["used"] = True
                save_tokens(tokens)
                await message.channel.send(f"✅ **{message.author.mention}, you have been given the Debug role!**")
            else:
                await message.channel.send("⚠️ **Error: Could not assign the role.**")
        else:
            await message.channel.send("❌ **Invalid or already used token!**")

# Run the bot
bot.run(TOKEN)
