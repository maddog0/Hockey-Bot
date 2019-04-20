from discord.ext import commands
from teams import *

class PrefrencesCog(commands.Cog, name = 'Prefrence Settings'):

    """These commands will let you set your prefrences"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setAllGames(self,ctx, a: bool):
        key = "all_games"
        value = a
        update_server(ctx.guild.id, key, value)
        await ctx.send("all games set to " + str(a))

    @setAllGames.error
    async def setAllGames_error(self,ctx,error):
        await ctx.send(error)

    @commands.command()
    async def setChannel(self,ctx):
        key = "messages"
        value = ctx.channel.id
        update_server(ctx.guild.id, key, value)
        await ctx.send("all messages will now come to this channel")

    @setChannel.error
    async def setChannel_error(self,ctx,error):
        await ctx.send(error)

    @commands.command()
    async def setPlayoffs(self,ctx, a: bool):
        key = "playoffs"
        value = a
        update_server(ctx.guild.id, key, value)
        await ctx.send("playoffs set to " + str(a))

    @setPlayoffs.error
    async def setPlayoffs_error(self,ctx, error):
        await ctx.send(error)

    @commands.command()
    async def addLikedTeam(self,ctx, team):
        team = get_team(team)
        key = "liked_teams"
        if team != None:
            liked_teams = get_likedTeams(ctx.guild.id)
            if team["_id"] not in liked_teams[key]:
                liked_teams["liked_teams"].append(team["_id"])
                update_server(ctx.guild.id, key, liked_teams["liked_teams"])
                await ctx.send('Added '+team["name"]+' to liked teams')
            else:
                await ctx.send('you already liked the ' + team["name"])
        else:
            await ctx.send('''I couldn't find this team, please check your spelling''')
    
    @addLikedTeam.error
    async def addLikedTeam_error(self,ctx, error):
        await ctx.send(error)

    @commands.command()
    async def removeLikedTeam(self,ctx, team):
        team = get_team(team)
        key = "liked_teams"
        if team != None:
            liked_teams = get_likedTeams(ctx.guild.id)
            if team["_id"] in liked_teams[key]:
                liked_teams["liked_teams"].remove(team["_id"])
                update_server(ctx.guild.id, key,liked_teams["liked_teams"])
                await ctx.send('Removed ' +team["name"]+' from your list of liked teams')
            else:
                await ctx.send('the ' +team["name"]+' are not on your list of liked teams')
        else:
            await ctx.send('''I couldn't find this team, please check your spelling''')

    @removeLikedTeam.error
    async def removeLikedTeam_error(self,ctx, error):
        await ctx.send(error)

def setup(bot):
    bot.add_cog(PrefrencesCog(bot))
