from asyncio import sleep
from discord import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from glob import glob

from ..db import db
PREFIX = "!"
OWNER_IDS=[528074180814438434]
COGS=[path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

class Ready():
    def __init__(self):
        for cog in COGS:
            setattr(self,cog,False)
    def ready_up(self,cog):
        setattr(self,cog,True)
        print(f"{cog} cog ready")
    def all_ready(self):
        return all([getattr(self,cog) for cog in COGS])
class Bot(BotBase):
    def __init__(self):
        self.PREFIX=PREFIX
        self.ready=False
        self.cogs_ready=Ready()
        self.guild=None
        self.scheduler=AsyncIOScheduler()
        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX,owner_ids=OWNER_IDS,intents=Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")
        print("setup complete")

    def run(self,version):
        self.VERSION=version
        print("running setup")
        self.setup()
        with open("./lib/bot/token.0","r",encoding="utf-8") as tf:
            self.TOKEN=tf.read()
        
        print("running bot...")
        super().run(self.TOKEN,reconnect=True)

    async def print_message(self):
        await self.testchannel.send("오늘은 밤새 가동되려나보네요")
    async def on_connect(self):
        print("bot connected!")
    
    async def on_disconnect(self):
        print("bot disconnected!")

    async def on_error(self,err,*args,**kwargs):
        if err == "on_command_error":
            await args[0].send("뭔가 잘못됨")

        raise


    async def on_command_error(self,ctx,exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exec,"original"):
            raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild=self.get_guild(742916227986620573)
            self.testchannel=self.get_channel(777004746799054899)
            self.warnchannel=self.get_channel(742920350735794316)
            self.scheduler.add_job(self.print_message,CronTrigger(hour=4,minute=0,second=0)) #KST (GMT+9)
            self.scheduler.start()
            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            self.ready=True
            print("bot ready")

        else:
            print("bot reconnected")
        
    async def on_message(self,message):
        emojilist=self.emojis
        await self.process_commands(message)
        if message.author == 751008755185090570:
            return
        if message.content == 'hello there':
            await message.channel.send('general kenobi')
        if message.guild == self.guild:    
            if message.author != 751008755185090570:
                if message.author != 679973416216035368 and message.author != 485112161367097367:
                    name = str(message.author)
                    logfile = open( 'C:/Users/andyp/OneDrive/바탕 화면/discordbot/discordbot/lib/db/discordlog.txt' , 'a' ,encoding="UTF-8" )
                    logfile.write('\n'+ message.content + "-" + name )
                    logfile.close()




bot=Bot()