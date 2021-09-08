from asyncio import sleep
from discord import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import *
from glob import glob
import sys
sys.path.append("C:/pythonfile/discordbot/data/db")
import db
PREFIX = ";"
OWNER_IDS=[528074180814438434]
COGS=[path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS=(CommandNotFound,BadArgument)
def cooldowntype(type):
    if type=="user":
        return "유저"
    elif type=="guild":
        return "서버"
    else:
        return "Unknown"
class Ready():
    def __init__(self):
        for cog in COGS:
            setattr(self,cog,False)
    def ready_up(self,cog):
        setattr(self,cog,True)
        print(f"{cog} cog ready")
    def all_ready(self):
        return all([getattr(self,cog) for cog in COGS])
class Bot(Bot):
    def __init__(self):
        self.PREFIX=PREFIX
        self.ready=False
        self.cogs_ready=Ready()
        self.guild=None
        self.scheduler=AsyncIOScheduler()
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

    async def on_connect(self):
        print("bot connected!")
    
    async def on_disconnect(self):
        print("bot disconnected!")
    
    async def on_member_join(self,member):
        db.newuser(member.id)

    async def on_error(self,err,*args,**kwargs):
        if err == "on_command_error":
            await args[0].send("뭔가 잘못됨")

        raise


    async def on_command_error(self,ctx,exc):
        if any([isinstance(exc,error) for error in IGNORE_EXCEPTIONS]):
            pass
        elif isinstance(exc,MissingRequiredArgument):
            await ctx.send("뭔가 빼먹으신듯?")
        elif isinstance(exc,CommandOnCooldown):
            await ctx.send(f"{cooldowntype(str(exc.cooldown.type).split('.')[-1])} 쿨다운에 걸려있는 명령어입니다. {exc.retry_after:,.2f}초만 기다려주세요.")
        elif hasattr(exc,"original"):
            if isinstance(exc.original,Forbidden):
                await ctx.send("권한이 없습니다.")
            else:
                raise(exc.original)
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.testbot=self.get_user(751008755185090570)
            self.guild=self.get_guild(742916227986620573)
            self.testchannel=self.get_channel(777004746799054899)
            self.warnchannel=self.get_channel(742920350735794316)
            await self.change_presence(status=Status.online, activity=Game("채팅 지켜보기"))
            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            self.ready=True
            print("bot ready")

        else:
            print("bot reconnected")
        
    async def on_message(self,message):
        emojilist=self.emojis
        await self.process_commands(message)
        if message.author == self.testbot:
            return
        if message.content == 'hello there':
            await message.channel.send('general kenobi')
        if message.content == 'test_make_database':
            db.makedb()
            await message.channel.send('database is built')
        if message.guild == self.guild:    
            if message.author != self.testbot:
                if str(message.author) != '코로나19 알림봇#4394' and str(message.author) != 'Space Launch Bot#3646':
                    userid = int(message.author.id)
                    message=message.content.encode("UTF-8")
                    decodedmessage=message.decode("UTF-8")
                    db.logging(userid, decodedmessage)
bot=Bot()