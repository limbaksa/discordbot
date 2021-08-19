from discord.ext.commands import *
from random import choice
from asyncio import sleep
from discord import *
from discord.utils import get
from typing import Optional
import time
def mornin():
    ctime=time.localtime()
    if ctime.tm_hour<=6 and 2<=ctime.tm_hour:
        return 0
    elif ctime.tm_hour<=11 and 6<=ctime.tm_hour:
        return 1
    elif ctime.tm_hour<=16 and 11<=ctime.tm_hour:
        return 2
    elif ctime.tm_hour<=21 and 16<=ctime.tm_hour:
        return 3
    else:
        return 4
class testcog(Cog):
    def __init__(self,bot):
        self.bot = bot
    @command(name="hello",aliases=["hi"],help="인사를 해줍니다")
    @cooldown(1,10,BucketType.user)
    async def hello(self,ctx):
        cur=mornin()
        if cur==0:
            asdf="안 자고 뭘 하시는 건가요?"
        elif cur==1:
            asdf="좋은 아침이에요!"
        elif cur==2:
            asdf="점심은 드셨나요?"
        elif cur==3:
            asdf="안녕하세요"
        elif cur==4:
            asdf="좋은 하루 보내셨나요?"
        await ctx.send(f"{ctx.author.mention}님 {choice(('안녕하세요!',asdf))}")

    @command(name="mute",help="나쁜 사람을 위한 뮤트. 박사만 사용가능.")
    async def mute(self, ctx, member: Member, length:int, *, reason: Optional[str]):
        roleidlist=[i.id for i in ctx.author.roles]
        if 875218121219268660 in roleidlist:
            muterole = get(ctx.guild.roles, name="mute")
            memrolenamelist=[i.name for i in member.roles]
            delrolelist=[get(ctx.guild.roles, name=i) for i in memrolenamelist]
            for i in range(1,len(delrolelist)):
                await member.remove_roles(delrolelist[i])
            await member.add_roles(muterole)
            await self.bot.warnchannel.send(f"{member.display_name}님이 {reason}으로 뮤트를 받으셨습니다.")
            await sleep(length)
            await member.remove_roles(muterole)
            for i in range(1,len(delrolelist)):
                await member.add_roles(delrolelist[i])

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("testcog")
        print("cog ready")
def setup(bot):
    bot.add_cog(testcog(bot))