from discord.ext.commands import Cog


class testcog(Cog):
    def __init__(self,bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("testcog")
        await self.bot.testchannel.send("testing. attention please")
        print("cog ready")
def setup(bot):
    bot.add_cog(testcog(bot))