import discord
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# load environment variables of .env file
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# configure the Google Generative AI API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# function to upload a text file
def upload_text_file(file_path):
    try:
        text_file = genai.upload_file(file_path)  # Upload the text file
        return text_file
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

# function to generate an answer using the text file content
async def generate_answer(text_file, question):
    try:
        prompt = f"{question} ({text_file.name})"  # use the file name as context
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content([prompt, text_file])
        
        print(f"API Response: {response.text}")  # debugging: Print the entire API response
        return response.text.strip()  # return the response text
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "I'm sorry, I couldn't generate an answer."

# function to log the query, response, and time taken
def log_query(user_question, answer, response_time):
    with open("chat_log.txt", "a") as log_file:
        log_file.write(f"Question: {user_question}\n")
        log_file.write(f"Answer: {answer}\n")
        log_file.write(f"Response Time: {response_time} seconds\n")
        log_file.write("-" * 40 + "\n")  # Separator between logs

# function to check if a user is an admin
def is_admin(message):
    return message.author.guild_permissions.administrator

# set up your Discord bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ask'):
        user_question = message.content[5:].strip()  # Get the question after !ask
        print(f"User Question: '{user_question}'")

        # upload the text file (update the file path as necessary)
        text_file = upload_text_file('faq_data.txt')  # replace with your text file path

        if text_file:
            start_time = time.time()  # start tracking time
            
            # generate an answer using the uploaded text file
            answer = await generate_answer(text_file, user_question)

            end_time = time.time()  # end tracking time
            response_time = round(end_time - start_time, 2)  # calculate response time

            print(f"Answer: '{answer}'")
            await message.channel.send(answer)

            # log the user question, bot answer, and response time
            log_query(user_question, answer, response_time)
        else:
            await message.channel.send("Error: Could not upload text file.")

    elif message.content.startswith('!hello'):
        await message.channel.send('Hi there! How can I assist you today?')

    elif message.content.startswith('!kick'):
        if is_admin(message):
            member = message.mentions[0] if message.mentions else None
            if member:
                await member.kick(reason="Kicked by admin command.")
                await message.channel.send(f"{member.display_name} has been kicked.")
            else:
                await message.channel.send("Please mention a user to kick.")

    elif message.content.startswith('!mute'):
        if is_admin(message):
            parts = message.content.split()
            if len(parts) < 3:
                await message.channel.send("Please mention a user and specify the duration in hours.")
                return

            member = message.mentions[0] if message.mentions else None
            try:
                hours = float(parts[2])  # Get the duration in hours
                duration = int(hours * 3600)  # Convert hours to seconds
            except ValueError:
                await message.channel.send("Please specify a valid number for the duration in hours.")
                return

            if member:
                # Get the "Muted" role
                muted_role = discord.utils.get(message.guild.roles, name="Muted")
                if muted_role:
                    await member.add_roles(muted_role)
                    await message.channel.send(f"{member.display_name} has been muted for {hours} hours.")
                    
                    # Wait for the specified duration
                    await asyncio.sleep(duration)
                    
                    # Remove the "Muted" role after the duration
                    await member.remove_roles(muted_role)
                    await message.channel.send(f"{member.display_name} has been unmuted after {hours} hours.")
                else:
                    await message.channel.send("Muted role not found. Please create a 'Muted' role.")
            else:
                await message.channel.send("Please mention a user to mute.")
    
    elif message.content.startswith('!deletechatlog'):
        # Check if the author has admin permissions
        if message.author.guild_permissions.administrator:
            try:
                os.remove("chat_log.txt")  # Remove the chat log file
                await message.channel.send("Chat log has been deleted successfully.")
            except Exception as e:
                await message.channel.send(f"Error deleting chat log: {e}")
        else:
            await message.channel.send("You do not have permission to delete the chat log.")

    elif message.content.startswith('!help'):
        help_message = (
            "**Stackup Helper Bot**\n"
            "I'm here to help you with general questions and some admin functionalities!\n\n"
            "**General Commands:**\n"
            "- `!ask <question>`: Ask me a general question about stackup and I'll do my best to provide an answer.\n\n"
            "**Admin Commands:**\n"
            "- `!kick @user`: Kick a user from the server.\n"
            "- `!mute @user <duration>`: Mute a user for a specified duration (e.g., 2 for 2hours).\n"
            "- `!deletechatlog`: Delete the entire chat log history.\n\n"
            "If you have any questions or need assistance, feel free to ask!"
        )
        await message.channel.send(help_message)


    elif message.content.startswith('!commands'):
        commands_list = """
        **Available Commands:**
        - `!help`: For bot information and commands.
        - `!ask [question]`: Ask a question.
        - `!kick @user`: Kick a user from the server by admin.
        - `!mute @user duration in hours`: Mute a user by admin.
        - `!deletechatlog`:Delete the chat log history by admin. 
        """
        await message.channel.send(commands_list)

if __name__ == '__main__':
    client.run(DISCORD_TOKEN)
