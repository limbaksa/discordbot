from discord.ext.commands import *
from asyncio import sleep
from discord import *
from discord.utils import get
from typing import Optional
import sys
sys.path.append("C:/Users/andyp/OneDrive/바탕 화면/discordbot/discordbot/data/db")
import db
mutetime={1:3600,2:18000,3:999999999999999999999999999999999999999999999999999999}
class admin(Cog):
    def __init__(self,bot):
        self.bot = bot

    
    @command(name="mute",help="나쁜 사람을 위한 뮤트. 박사만 사용가능.",brief="뮤트")
    async def mute(self, ctx, member: Member, *, reason: Optional[str]):
        roleidlist=[i.id for i in ctx.author.roles]
        if 875218121219268660 in roleidlist:
            muterole = get(ctx.guild.roles, name="mute")
            memrolenamelist=[i.name for i in member.roles]
            delrolelist=[get(ctx.guild.roles, name=i) for i in memrolenamelist]
            for i in range(1,len(delrolelist)):
                await member.remove_roles(delrolelist[i])
            await member.add_roles(muterole)
            await self.bot.warnchannel.send(f"{member.display_name}님이 {reason}으로 뮤트를 받으셨습니다.")
            warn=db.addwarn(int(member.id))
            length=mutetime[warn]
            await sleep(length)
            await member.remove_roles(muterole)
            for i in range(1,len(delrolelist)):
                await member.add_roles(delrolelist[i])
        else:
            await ctx.send("권한이 부족하시군요")
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("admin")

def setup(bot):
    bot.add_cog(admin(bot))