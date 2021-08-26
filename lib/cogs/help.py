from discord.ext.commands import *
from discord.ext.menus import MenuPages, ListPageSource
from discord.utils import *
from discord import *
from typing import Optional
import time

def syntax(command):
    cmd_and_aliases="|".join([str(command), *command.aliases])
    params=[]
    for key,value in command.params.items():
        if key not in ("self","ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")
    params=" ".join(params)
    return f"```;{cmd_and_aliases} {params}```"

class HelpMenu(ListPageSource):
    def __init__(self,ctx,data):
        self.ctx=ctx
        
        super().__init__(data,per_page=2)

    async def write_page(self,menu,fields=[]):
        offset=(menu.current_page*self.per_page)+1
        len_data=len(self.entries)
        embed = Embed(title="도움말",description="도움말 목록",colour=self.ctx.author.colour)
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(text=f"전체 {len_data:,}개 중 {offset:,} - {min(len_data,offset+self.per_page-1):,}번째 명령어")

        for name,value in fields:
            embed.add_field(name=name,value=value,inline=False)
        return embed


    async def format_page(self,menu,entries):
        fields = []
        for entry in entries:
            fields.append((entry.brief or "설명 없음",syntax(entry)))
        return await self.write_page(menu, fields)

class Help(Cog):
    def __init__(self,bot):
        self.bot=bot
        self.bot.remove_command("help")
    
    async def cmd_help(self,ctx,command):
        embed=Embed(title=f"`{command}` 명령어 사용법",description=f"사용법{syntax(command)}",color=ctx.author.color)
        embed.add_field(name="설명",value=command.help)

        message=await ctx.send(embed=embed)

    @command(name="help",help="이걸 왜",brief="도움말")
    async def show_help(self,ctx,cmd:Optional[str]):
        if cmd is None:
            menu=MenuPages(source=HelpMenu(ctx,list(self.bot.commands)),clear_reactions_after=False,delete_message_after=False,timeout=100.0)
            menupage=await menu.start(ctx)
        else:
            if command:=get(self.bot.commands,name=cmd):
                await self.cmd_help(ctx,command)
            else:
                await ctx.send("존재하지 않는 명령어입니다.")
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")
    
def setup(bot):
    bot.add_cog(Help(bot))