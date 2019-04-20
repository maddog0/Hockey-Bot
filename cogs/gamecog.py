from discord.ext import commands
from games import *

class gamesCog(commands.Cog, name = 'game details'):

    """these commands will get game info"""
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def getGameScore (self,ctx, team):
        game = find_game_involving_team(team)
        if game != None:
            home = game['homeTriCode']
            homescore = game['homeScore']
            away = game['awayTriCode']
            awayscore = game['awayScore']
            if awayscore > homescore:
                message='{0}-{1} {2}-{3}'.format(away,awayscore,home,homescore)
                await ctx.send(message)
            else:
                message='{0}-{1} {2}-{3}'.format(home,homescore,away,awayscore)
                await ctx.send(message)                
                
        else:
            await ctx.send('could not find a game involving the requested team')

def setup(bot):
    bot.add_cog(gamesCog(bot))
