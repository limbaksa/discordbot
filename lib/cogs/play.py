from discord.ext.commands import *
from random import choice
from discord import *
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
class play(Cog):
    def __init__(self,bot):
        self.bot = bot
    @command(name="hello",aliases=["hi"],help="인사를 해줍니다",brief="인사")
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

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("play")
def setup(bot):
    bot.add_cog(play(bot))