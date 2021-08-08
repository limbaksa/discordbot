from discord import Intents
from discord import Embed
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

from ..db import db
PREFIX = "+"
OWNER_IDS=[528074180814438434]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX=PREFIX
        self.ready=False
        self.guild=None
        self.scheduler=AsyncIOScheduler()
        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX,owner_ids=OWNER_IDS,intents=Intents.all())
        
    def run(self,version):
        self.VERSION=version

        with open("./lib/bot/token.0","r",encoding="utf-8") as tf:
            self.TOKEN=tf.read()
        
        print("running bot...")
        super().run(self.TOKEN,reconnect=True)

    async def print_message(self):
        await testchannel.send("오늘은 밤새 가동되려나보네요")
    async def on_connect(self):
        print("bot connected!")
    
    async def on_disconnect(self):
        print("bot disconnected!")

    async def on_error(self,err,*args,**kwargs):
        if err == "on_command_error":
            await args[0].send("something went wrong.")

        raise


    async def on_command_error(self,ctx,exc):
        if isinstance(exc, CommandsNotFound):
            pass
        elif hasattr(exec,"original"):
            raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.ready=True
            self.guild=self.get_guild(742916227986620573)
            self.testchannel=self.get_channel(777004746799054899)
            self.scheduler.add_job(self.print_message,CronTrigger(hour=4,minute=0,second=0)) #KST (GMT+9)
            self.scheduler.start()
            print("bot ready")

        else:
            print("bot reconnected")
        
    async def on_message(self,message):
        
        if message.author == 751008755185090570:
            return
        if message.content == 'hello there':
            await message.channel.send('general kenobi')
        if message.guild == self.guild:    
            if message.author != 751008755185090570:
                if message.author != 679973416216035368 and message.author != 485112161367097367:
                    name = str(message.author)
                    logfile = open( 'C:/Users/andyp/OneDrive/바탕 화면/discordbot/discordbot/lib/db/discordlog.txt' , 'a' )
                    logfile.write('\n'+ message.content + "-" + name )
                    logfile.close()
        else:
            pass



bot=Bot()