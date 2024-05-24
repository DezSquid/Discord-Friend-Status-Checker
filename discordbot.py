import discord
from discord.ext import tasks
from plyer import notification

# Replace with your bot's token
TOKEN = 'HERE'
# Replace with the ID of the user you want to track
USER_ID = HERE

class MyClient(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_check = True

    async def on_ready(self):
        print(f'Logged on as {self.user}')
        if len(self.guilds) > 0:
            self.guild = self.guilds[0]
            print(f'Bot is in the guild: {self.guild.name}')
        else:
            print('Bot is not in any guilds')
        self.check_status.start()

    @tasks.loop(seconds=2)  # Check every minute
    async def check_status(self):
        member = self.guild.get_member(USER_ID)
        if member is not None:
            if self.first_check:
                print(f'Checking status for {member.name}: {member.status}')
                self.first_check = False
            if member.status == discord.Status.online:
                self.send_notification(f'{member.name} is now online!')
                print(f'{member.name} is now Online! Press Enter to exit')
                input()  # Wait for user to press Enter
                await self.close()  # Close the bot
        else:
            print(f'Member with ID {USER_ID} not found in the guild.')

    async def on_member_update(self, before, after):
        if before.id == USER_ID:
            if before.status != discord.Status.online and after.status == discord.Status.online:
                self.send_notification(f'{after.name} has come online!')
                print(f'{after.name} is now Online! Press Enter to exit')
                input()  # Wait for user to press Enter
                await self.close()  # Close the bot

    def send_notification(self, message):
        notification.notify(
            title="Discord Notification",
            message=message,
            app_name="Discord Bot",
            timeout=10  # Duration in seconds
        )
        print(f'Notification sent: {message}')

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.guilds = True  # Ensuring guilds intent is enabled
client = MyClient(intents=intents)

client.run(TOKEN)
