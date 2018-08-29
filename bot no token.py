# UserOfTheWeekBot by Kemtalis

import sys
import discord
from discord.ext import commands
import random
from discord.ext.commands import Bot
import asyncio

nominations = {}
ranks = {0: 0}
voted = {}
roleforedit = "Elder"
botchannel = 'skald-of-the-week'
channels = []
topnames = []
channum = 0
lastauthor = ""
commandsymbol = '!'

bot = commands.Bot(command_prefix=commandsymbol)


@bot.event
async def on_ready():
    count = 0
    global channum

    for each in bot.get_all_channels():
        channels.append(each)
        if str(each) == botchannel:
            break
        count += 1

    channum = count
    print(bot.user.name + " is ready to go!")


@bot.event
async def on_message(message):
    global lastauthor
    if str(message.channel) == botchannel.lower():
        lastauthor = message.author
        await bot.process_commands(message)


@bot.event
async def on_command_error(event, *args, **kwargs):
    if type(event) == discord.ext.commands.BadArgument:
        print(channum)
        await bot.send_message(channels[channum], "Sorry {}, but that is not a valid user. "
                                                  "If you didn't please use the @ symbol\n"
                                                  "Your message should say ![command] @[user]"
                               .format(lastauthor.mention))


@bot.command(pass_context=True)
async def vote(ctx, user: discord.Member):
    if voted.get(ctx.message.author.mention, 'null') == 'null':
        if nominations.get(user.mention, 'null') != 'null':
            await bot.say("Your vote has been added for {}. Thank you!".format(user.name))
            voted[ctx.message.author.mention] = user.name
            nominations[user.mention] += 1
        else:
            await bot.say("Thank you for nominating {}! Congrats on being nominated {}!".format(user.name, user.mention))
            voted[ctx.message.author.mention] = user.name
            nominations[user.mention] = 1
        print(nominations)
    else:
        await bot.say("Sorry {} but you have already voted once. Please wait to vote again until next week.".format(
            ctx.message.author.mention))


@bot.command(pass_context=True)
async def top3(ctx):
    global topnames
    if len(nominations) > 0:
        topnames = sorted(nominations, key=nominations.get)
        topnames.reverse()
    else:
        topnames = {}

    # If people have been nominated.
    if len(topnames) >= 1:
        leaderboard = discord.Embed(title="Skald of the Week Leaderboard", color=0x00ff00)

        # If more than 3 people have been nominated
        if len(topnames) > 3:

            # If there is a 4 or more way tie
            if nominations[topnames[0]] == nominations[topnames[3]]:
                leaderboard.add_field(name="Its a tie", value="Uh. Oh there is a huge tie for first. "
                                                              "A mod will have to use !randsotw"
                                                              " or !listtie (NOT RECOMENDED)")

            # 3 Way Tie for second
            elif nominations[topnames[1]] == nominations[topnames[3]]:
                leaderboard.add_field(name="1st Place:", value="{} with {} vote(s)"
                                      .format(topnames[0], nominations[topnames[0]]))
                leaderboard.add_field(name="Tied for 2nd!", value="Tied. You can check your place with !sotwrank")

            # Tie for 3rd
            elif nominations[topnames[2]] == nominations[topnames[3]]:
                leaderboard.add_field(name="1st Place:", value="{} with {} vote(s)"
                                      .format(topnames[0], nominations[topnames[0]]))
                leaderboard.add_field(name="2nd Place:", value="{} with {} vote(s)"
                                      .format(topnames[1], nominations[topnames[1]]))
                leaderboard.add_field(name="3rd Place:", value="Tied. You can check your place with !sotwrank")

            # If there is a 3 way tie
            elif nominations[topnames[0]] == nominations[topnames[2]]:
                leaderboard.add_field(name="3 Way Tie!",
                                      value="{}, {}, and {} with {} vote(s)"
                                      .format(topnames[0], topnames[1], topnames[2], nominations[topnames[1]]))
            # If there is a 2 way tie
            elif nominations[topnames[0]] == nominations[topnames[1]]:
                leaderboard.add_field(name="Tied for 1st!", value="{} and {} with {} vote(s)"
                                      .format(topnames[0], topnames[1], nominations[topnames[1]]))
                leaderboard.add_field(name="3rd Place:", value="{} with {} vote(s)"
                                      .format(topnames[2], nominations[topnames[2]]))
            # Tie for second
            elif nominations[topnames[0]] == nominations[topnames[1]]:
                leaderboard.add_field(name="1st Place:", value="{} with {} vote(s)"
                                      .format(topnames[0], nominations[topnames[0]]))
                leaderboard.add_field(name="Tied for 2nd!", value="{} and {} with {} vote(s)"
                                      .format(topnames[1], topnames[2], nominations[topnames[1]]))

            # No Tie
            else:
                leaderboard.add_field(name="1st Place:", value="{} with {} vote(s)"
                                      .format(topnames[0], nominations[topnames[0]]))
                leaderboard.add_field(name="2nd Place:", value="{} with {} vote(s)"
                                      .format(topnames[1], nominations[topnames[1]]))
                leaderboard.add_field(name="3rd Place:", value="{} with {} vote(s)"
                                      .format(topnames[2], nominations[topnames[2]]))

        # If 3 people have been nominated
        elif len(topnames) == 3:

            # If there is a 3 way tie
            if nominations[topnames[0]] == nominations[topnames[2]]:
                leaderboard.add_field(name="3 Way Tie!",
                                      value="{}, {}, and {} with {} vote(s)"
                                      .format(topnames[0], topnames[1], topnames[2], nominations[topnames[1]]))

            # If there is a 2 way tie
            elif nominations[topnames[0]] == nominations[topnames[1]]:
                leaderboard.add_field(name="Tied for 1st!", value="{} and {} with {} vote(s)"
                                      .format(topnames[0], topnames[1], nominations[topnames[1]]))
                leaderboard.add_field(name="3rd Place:", value="{} with {} vote(s)"
                                      .format(topnames[2], nominations[topnames[2]]))

            # Tie for second
            elif nominations[topnames[1]] == nominations[topnames[2]]:
                leaderboard.add_field(name="1st Place:", value="{} with {} vote(s)"
                                      .format(topnames[0], nominations[topnames[0]]))
                leaderboard.add_field(name="Tied for 2nd!", value="{} and {} with {} vote(s)"
                                      .format(topnames[1], topnames[2], nominations[topnames[1]]))

                # Tie for 3rd
            elif nominations[topnames[2]] == nominations[topnames[3]]:
                leaderboard.add_field(name="1st Place:", value="{} with {} vote(s)"
                                      .format(topnames[0], nominations[topnames[0]]))
                leaderboard.add_field(name="2nd Place:", value="{} with {} vote(s)"
                                      .format(topnames[1], nominations[topnames[1]]))
                leaderboard.add_field(name="3rd Place:", value="Tied. You can check your place with !sotwrank")

            # No tie
            else:
                leaderboard.add_field(name="1st Place:", value="{} with {} vote(s)"
                                      .format(topnames[0], nominations[topnames[0]]))
                leaderboard.add_field(name="2nd Place:", value="{} with {} vote(s)"
                                      .format(topnames[1], nominations[topnames[1]]))
                leaderboard.add_field(name="3rd Place:", value="{} with {} vote(s)"
                                      .format(topnames[2], nominations[topnames[2]]))

        # If 2 people have been nominated
        elif len(topnames) == 2:
            # If there is a 2 way tie
            if nominations[topnames[0]] == nominations[topnames[1]]:
                leaderboard.add_field(name="Tied for 1st!", value="{} and {} with {} vote(s)"
                                      .format(topnames[0], topnames[1], nominations[topnames[1]]))

            # No Tie
            else:
                leaderboard.add_field(name="1st Place:", value="{} with {} vote(s)"
                                      .format(topnames[0], nominations[topnames[0]]))
                leaderboard.add_field(name="2nd Place:", value="{} with {} vote(s)"
                                      .format(topnames[1], nominations[topnames[1]]))

        # If 1 person has been nominated
        elif len(topnames) == 1:
            leaderboard.add_field(name="1st Place:", value="{} with {} vote(s)"
                                  .format(topnames[0], nominations[topnames[0]]))
        await bot.say(embed=leaderboard)
    else:
        await bot.say("No one has been nominated yet.  Use !vote to nominate someone!")


@bot.command(pass_context=True)
async def delv(ctx, user: discord.Member):
    haspermission = False
    for x in ctx.message.author.roles:
        if str(x) == roleforedit:
            haspermission = True

    if haspermission:
        print("Made it")
        if user.mention in voted:
            print("a")
            nominations[user.mention] -= 1
            voted.pop(user.mention)
            await bot.say("{}'s vote has been deleted".format(user.mention))
            print(nominations)


@bot.command(pass_context=True)
async def sotwrank(ctx, user: discord.Member= 'null'):
        if user == 'null':
            user = ctx.message.author
        if len(nominations) > 0:
            ranks = {}
            for person in nominations:
                if ranks.get(nominations[person], 'null') == 'null':
                    ranks[nominations[person]] = 1
                else:
                    ranks[nominations[person]] += 1
            print(ranks)
            sortedranks = list(ranks.keys())
            sortedranks.sort()
            print(sortedranks.index(nominations[user.mention]))
            rankembed = discord.Embed(title="", color=0x00ff00)
            rankembed.set_thumbnail(url=user.avatar_url)
            rankembed.add_field(name="{}'s rank".format(user.name), value='You are rank {} out of {} nomination(s)'
                                .format(sortedranks.index(nominations[user.mention]) + 1, len(nominations)))
            await bot.say(embed=rankembed)
        else:
            await bot.say("No one has been nominated yet.  Use !vote to nominate someone!")



@bot.command(pass_context=True)
async def erole(ctx, str):
    global roleforedit
    haspermission = False
    for x in ctx.message.author.roles:
        if str(x) == roleforedit:
            haspermission = True
    if haspermission:
        roleforedit = str;


@bot.command(pass_context=True)
async def listtie(ctx):
    haspermission = False
    tiedusers = []
    for x in ctx.message.author.roles:
        if str(x) == roleforedit:
            haspermission = True
    if haspermission:
        if len(nominations) > 0:
            ranks = {}
            for person in nominations:
                if ranks.get(nominations[person], 'null') == 'null':
                    ranks[nominations[person]] = 1
                else:
                    ranks[nominations[person]] += 1
            rs = list(ranks.keys())
            rs.sort()
        else:
            await bot.say("Sorry, {}, but no one has been nominated yet.".format(ctx.message.author.mention))
        if len(rs) > 0:
            for x in nominations:
                if nominations[x] == rs[0]:
                    tiedusers.append(x)
            await bot.say(', '.join(tiedusers))

@bot.command(pass_context=True)
async def randsotw(ctx):
    print("a")
    haspermission = False
    tiedusers = []
    for x in ctx.message.author.roles:
        if str(x) == roleforedit:
            haspermission = True
    if haspermission:
        if len(nominations) > 0:
            print('x')
            ranks = {}
            for person in nominations:
                if ranks.get(nominations[person], 'null') == 'null':
                    ranks[nominations[person]] = 1
                else:
                    ranks[nominations[person]] += 1
            rs = list(ranks.keys())
            rs.sort()
        else:
            await bot.say("Sorry, {}, but no one has been nominated yet.".format(ctx.message.author.mention))
        if len(rs) > 0:
            print("q")
            for x in nominations:
                if nominations[x] == rs[0]:
                    tiedusers.append(x)
            print('y')
            winner = random.randint(0, len(tiedusers)-1)
            winnername = tiedusers[winner]
            print(winnername)
            await bot.say("Congrats {}! You are the user of the week!".format(winnername))


@bot.command(pass_context=True)
async def sotw(ctx):
    haspermission = False
    for x in ctx.message.author.roles:
        if str(x) == roleforedit:
            haspermission = True
    if haspermission:
        await bot.say('Thank you for choosing the User of the Week bot by Kemtalis!\n'
                      'Below are some commands that might be useful.\n'
                      'Commands with a -- before them require the editor role (default="Elder")\n\n'
                      '!vote @[user]:     Allows you to nominate and vote for people with in your chat\n'
                      '!top3:     Shows the 3 users with the most votes for User of the Week\n'
                      '!sotwrank:     Shows your rank vs. the rest of the nominations\n'
                      '!sotw:      Shows these commands for the User of the week bot.\n'
                      '--delv @[user]:     Deletes the users vote so that they can vote for someone else\n'
                      '--!erole [newrole]:     Changes the role required for deleting a persons vote (ex. Moderator) '
                      'and for changing this setting.)\n'
                      '--!randsotw:        Choses a random winner from the people with the higest ammount of votes\n'
                      '--!tie:     Lists users that are tied for first place. This could potentially list everyone in '
                      'your server so be careful!\n'
                      '--!resetsotw:     resets the bot so users can begin voting the next week.'
                      )
    else:
        await bot.say('Thank you for choosing the User of the Week bot by Kemtalis!\n'
        'Below are some commands that might be useful.\n'
        '!vote @[user]:     Allows you to nominate and vote for people with in your chat\n'
        '!top3:     Shows the 3 users with the most votes for User of the Week\n'
        '!sotwrank:     Shows your rank vs. the rest of the nominations\n'
        '!sotw:      Shows these commands for the User of the week bot.\n'
          )


@bot.command(pass_context=True)
async def resetsotw(ctx):
    haspermission = False
    for x in ctx.message.author.roles:
        if str(x) == roleforedit:
            haspermission = True
    if haspermission:
        global nominations
        global ranks
        global voted
        global channels
        global topnames
        global channum
        nominations = {}
        ranks = {0: 0}
        voted = {}
        channels = []
        topnames = []
        channum = 0

bot.remove_command('help')

bot.run("BOT TOKEN GOES HERE")
