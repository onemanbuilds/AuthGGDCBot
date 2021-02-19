import aiohttp
import discord
import json
from subprocess import check_output
from discord.ext import commands
from os import name,system
from base64 import b64decode,b64encode

#add salt to the encrypted data
#make genlicense work
#make code cleaner

colors = {}
colors['white'] = "\033[1;37m"
colors['green'] = "\033[0;32m"
colors['red'] = "\033[0;31m"
colors['yellow'] = "\033[1;33m"

general_commands = {
    f"⚙️ `prefix <newprefix>`":"Admins can change the bot's prefix.",
    f"⚙️ `setaid <newaid>`":"Owners can change the auth.gg aid.",
    f"⚙️ `setapikey <newapikey>`":"Owners can change the auth.gg apikey.",
    f"⚙️ `setsecret <newsecret>`":"Owners can change the auth.gg secret.",
    f"⚙️ `setauthkey <newauthkey>`":"Admins can change the authkey.",
    f"🕵️ `getuserinfo <username>`":"Admins can get the user's (email, rank, hwid, variable, lastlogin, lastip, expiry date).",
    f"🕵️ `usercount`":"Admins can check the user count.",
    f"🕵️ `licenseinfo <license>`":"Admins can get license infos by license (rank, used, used by, created at).",
    f"🕵️ `gethwid <username>`":"Admins can get the user's hwid.",
    f"🕵️ `expiry <username> <password>`":"Users can get their license expiration date. **be careful others can snipe it.**",
    f"❌ `deluser <username>`":"Admins can delete users from the database.",
    f"❌ `dellicense <license>`":"Admins can delete user's license.",
    f"✏️ `editvar <username> <value>`":"Admins can edit user variables.",
    f"✏️ `editrank <username> <rank>`":"Admins can edit the user's rank.",
    f"✏️ `changepw <username> <newpassword>`":"Admins can change the user's password if the user forgot it.",
    f"✏️ `sethwid <username>`":"Owners can set the user's hwid.",
    f"👍 `uselicense <license>`":"Admins can set the license state to used.",
    f"👎 `unuselicense <license>`":"Admins can set the license state to unused.",
    f"⏰ `resethwid <username>`":"Owners can reset the user's hwid.",
}

api_url = "https://api.auth.gg/v1/"


def ReadConfig():
    with open('[Data]/configs.json','r') as f:
        return json.load(f)

def ReplaceValueInJsonb64(filename,key,new_value):
    with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)

    data[key] = b64encode(new_value.encode()).decode()

    with open(filename, "w") as jsonFile:
        json.dump(data, jsonFile)

def ReplaceValueInJson(filename,key,new_value):
    with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)

    data[key] = new_value

    with open(filename, "w") as jsonFile:
        json.dump(data, jsonFile)

async def GetUserHWID(authkey,username):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'https://developers.auth.gg/HWID/?type=fetch&authorization={authkey}&user={username}') as response:
                response_json = await response.json(content_type=None)
                if response_json['status'] == 'success':
                    hwid = response_json['value']
                    if hwid == '':
                        return
                    else:
                        return hwid
                else:
                    print(colors['white']+'Failed to get hwid')
    except ValueError as v:
        print(colors['yellow']+'JSON Value error at GETUSERHWID {0}'.format(colors['red']+str(v)))

admin_role_id = ReadConfig()['admin_role_id']
owner_role_id = ReadConfig()['owner_role_id']

bot = commands.Bot(ReadConfig()['prefix'])
bot.remove_command('help')

@bot.event
async def on_ready():
    print(colors['white']+'[#] AUTH.GG READY!')

@bot.command(pass_context=True)
async def help(ctx):
    await ctx.message.delete()
    try:
        embed_message = discord.Embed(title='HELP',color=0x0070ff,timestamp=ctx.message.created_at)
        for key in general_commands:
            embed_message.add_field(name=key,value=general_commands[key],inline=False)
        await ctx.send(embed=embed_message)
    except Exception as e:
        print(colors['yellow']+'EXCEPTION at HELP {0}'.format(colors['red']+str(e)))
    

@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def prefix(ctx,newprefix):
    await ctx.message.delete()
    
    if newprefix is None:
        return

    try:
        ReplaceValueInJson('[Data]/configs.json','prefix',newprefix)
    except ValueError as v:
        print(colors['yellow']+'JSON Value error at PREFIX CHANGE {0}'.format(colors['red']+str(v)))
    else:
        bot.command_prefix = ReadConfig()['prefix']
        embed = discord.Embed(title='PREFIX',color=0x00ff00,description=f'PREFIX SET TO **{newprefix}**\n{ctx.author.mention}')
        await ctx.send(embed=embed)

#worked but admins could change it to the default role id so all of the users could use the admin commands
#@bot.command(pass_context=True)
#async def setadminroleid(ctx,role: discord.Role):
#    await ctx.message.delete()

#    if role is None:
#        return

#    try:
#        roleid = role.id
#        ReplaceValueInJson('[Data]/configs.json','admin_role_id',roleid)
#    except ValueError as v:
#        print(colors['yellow']+'JSON Value error at ADMIN ROLE ID CHANGE {0}'.format(colors['red']+str(v)))
#    else:
#        embed = discord.Embed(title='ADMINROLEID',color=0x00ff00,description=f'ADMINROLEID SET TO **{str(roleid)}**\n{ctx.author.mention}')
#        await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_role(owner_role_id)
async def setaid(ctx,newaid):
    await ctx.message.delete()

    if newaid is None:
        return

    try:
        ReplaceValueInJsonb64('[Data]/configs.json','aid',newaid)
    except ValueError as v:
        print(colors['yellow']+'JSON Value error at AID CHANGE {0}'.format(colors['red']+str(v)))
    else:
        embed = discord.Embed(title='AID',color=0x00ff00,description=f'AID SET TO **{newaid}**\n{ctx.author.mention}')
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_role(owner_role_id)
async def setapikey(ctx,newapikey):
    await ctx.message.delete()

    if newapikey is None:
        return

    try:
        ReplaceValueInJsonb64('[Data]/configs.json','apikey',newapikey)
    except ValueError as v:
        print(colors['yellow']+'JSON Value error at APIKEY CHANGE {0}'.format(colors['red']+str(v)))
    else:
        embed = discord.Embed(title='APIKEY',color=0x00ff00,description=f'APIKEY SET TO **{newapikey}**\n{ctx.author.mention}')
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_role(owner_role_id)
async def setsecret(ctx,newsecret):
    await ctx.message.delete()

    if newsecret is None:
        return

    try:
        ReplaceValueInJsonb64('[Data]/configs.json','secret',newsecret)
    except ValueError as v:
        print(colors['yellow']+'JSON Value error at SECRET CHANGE {0}'.format(colors['red']+str(v)))
    else:
        embed = discord.Embed(title='SECRET',color=0x00ff00,description=f'SECRET SET TO **{newsecret}**\n{ctx.author.mention}')
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def setauthkey(ctx,newauthkey):
    await ctx.message.delete()
    try:
        ReplaceValueInJsonb64('[Data]/configs.json','authkey',newauthkey)
    except ValueError as v:
        print(colors['yellow']+'JSON Value error at AUTHKEY CHANGE {0}'.format(colors['red']+str(v)))
    else:
        embed = discord.Embed(title='AUTHKEY',color=0x00ff00,description=f'AUTHKEY SET TO **{newauthkey}**\n{ctx.author.mention}')
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def expiry(ctx,username,password):
    await ctx.message.delete()

    if username is None:
        return
    
    if password is None:
        return

    aid = b64decode(ReadConfig()['aid']).decode()
    apikey = b64decode(ReadConfig()['apikey']).decode()
    secret = b64decode(ReadConfig()['secret']).decode()
    authkey = b64decode(ReadConfig()['authkey']).decode()
    hwid = await GetUserHWID(authkey,username)

    payload = {
        'type':'login',
        'aid':aid,
        'apikey':apikey,
        'secret':secret,
        'username':username,
        'password':password,
        'hwid':hwid
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url,data=payload) as response:
            try:
                response_json = await response.json(content_type=None)

                if response_json['result'] == 'success':
                    expiry = response_json['expiry']
                    if expiry == '': expiry = 'NOT FOUND'
    
                    embed = discord.Embed(title='EXPIRY',color=0x00ff00,description=f'USER: **{username}**\nYOUR LICENSE WILL EXPIRE AT: **{expiry}**\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['result'] == 'invalid_details':
                    embed = discord.Embed(title='EXPIRY',color=0xff0000,description=f'INVALID LOGIN DETAILS **{username}**\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['result'] == 'invalid_hwid':
                    embed = discord.Embed(title='EXPIRY',color=0xff0000,description=f'INVALID HWID **{username}**\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['result'] == 'hwid_updated':
                    embed = discord.Embed(title='EXPIRY',color=0xff0000,description=f'HWID UPDATED **{username}**\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['result'] == 'time_expired':
                    embed = discord.Embed(title='EXPIRY',color=0xff0000,description=f'YOUR LICENSE EXPIRED **{username}**\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['result'] == 'failed':
                    print(colors['yellow']+'EXPIRY'+colors['red']+' Invalid api key')
                else:
                    embed = discord.Embed(title='EXPIRY',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at EXPIRY {0}'.format(colors['red']+str(v)))
            
@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def getuserinfo(ctx,username):
    await ctx.message.delete()

    if username is None:
        return

    authkey = b64decode(ReadConfig()['authkey']).decode()
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/USERS/?type=fetch&authorization={authkey}&user={username}') as response:
            try:
                response_json = await response.json(content_type=None)
                
                if response_json['status'] == 'success':
                    email = response_json['email']
                    rank = response_json['rank']
                    hwid = response_json['hwid']
                    variable = response_json['variable']
                    lastlogin = response_json['lastlogin']
                    lastip = response_json['lastip']
                    expiry = response_json['expiry']

                    if email == '': email = 'NOT FOUND'
                    if rank == '': rank = 'NOT FOUND'
                    if hwid == '': hwid = 'NOT FOUND'
                    if variable == '': variable = 'NOT FOUND'
                    if lastlogin == '': lastlogin = 'NOT FOUND'
                    if lastip == '': lastip = 'NOT FOUND'
                    if expiry == '': expiry = 'NOT FOUND'

                    embed = discord.Embed(title='USERINFO',color=0x00ff00,description=f'USERNAME: **{username}**\nEMAIL: **{email}**\nRANK: **{rank}**\nHWID: ||**{hwid}**||\nVARIABLE: **{variable}**\nLASTLOGIN: **{lastlogin}**\nLASTIP: ||**{lastip}**||\n EXPIRY: **{expiry}**\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='USERINFO',color=0xff0000,description=f'FAILED TO GET USERINFO USER **{username}**\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='USERINFO',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at GETUSERINFO {0}'.format(colors['red']+str(v)))

@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def deluser(ctx,username):
    await ctx.message.delete()

    if username is None:
        return

    authkey = b64decode(ReadConfig()['authkey']).decode()
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/USERS/?type=delete&authorization={authkey}&user={username}') as response:
            try:
                response_json = await response.json(content_type=None)
                
                if response_json['status'] == 'success':
                    embed = discord.Embed(title='DELUSER',color=0x00ff00,description=f'USER: **{username}** DELETED!\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='DELUSER',color=0xff0000,description=f'FAILED TO DELETE USER **{username}**\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='DELUSER',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at DELUSER {0}'.format(colors['red']+str(v)))

@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def editvar(ctx,username,value):
    await ctx.message.delete()

    if username is None:
        return

    if value is None:
        return

    authkey = b64decode(ReadConfig()['authkey']).decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/USERS/?type=editvar&authorization={authkey}&user={username}&value={value}') as response:
            try:
                response_json = await response.json(content_type=None)
                
                if response_json['status'] == 'success':
                    embed = discord.Embed(title='EDITVAR',color=0x00ff00,description=f'USER: **{username}**\nVARIABLE **{value}** ADDED!\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='EDITVAR',color=0xff0000,description=f'FAILED TO ADD USER **{username}** VARIABLE\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='EDITVAR',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at EDITVAR {0}'.format(colors['red']+str(v)))

@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def editrank(ctx,username,rank):
    await ctx.message.delete()

    if username is None:
        return
    
    if rank is None:
        return

    authkey = b64decode(ReadConfig()['authkey']).decode()
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/USERS/?type=editrank&authorization={authkey}&user={username}&rank={rank}') as response:
            try:
                response_json = await response.json(content_type=None)
                
                if response_json['status'] == 'success':
                    embed = discord.Embed(title='EDITRANK',color=0x00ff00,description=f'USER: **{username}**\nRANK SET TO **{rank}**!\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='EDITRANK',color=0xff0000,description=f'FAILED TO EDIT **{username}** RANK\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='EDITRANK',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at EDITRANK {0}'.format(colors['red']+str(v)))

@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def changepw(ctx,username,newpassword):
    await ctx.message.delete()

    if username is None:
        return
    
    if newpassword is None:
        return

    authkey = b64decode(ReadConfig()['authkey']).decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/USERS/?type=changepw&authorization={authkey}&user={username}&password={newpassword}') as response:
            try:
                response_json = await response.json(content_type=None)
                
                if response_json['status'] == 'success':
                    embed = discord.Embed(title='CHANGEPW',color=0x00ff00,description=f'USER: **{username}** PASSWORD SET TO ||JUST KIDDING||!\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='CHANGEPW',color=0xff0000,description=f'FAILED TO CHANGE USER **{username}** PASSWORD\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='CHANGEPW',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at CHANGEPW {0}'.format(colors['red']+str(v)))


@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def usercount(ctx):
    await ctx.message.delete()

    authkey = b64decode(ReadConfig()['authkey']).decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/USERS/?type=count&authorization={authkey}') as response:
            try:
                response_json = await response.json(content_type=None)
                if response_json['status'] == 'success':
                    usernum = response_json['value']
                    embed = discord.Embed(title='USERCOUNT',color=0x00ff00,description=f'TOTAL USERS: **{usernum}**\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='USERCOUNT',color=0xff0000,description=f'FAILED TO GET USERS COUNT\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='USERCOUNT',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at USERCOUNT {0}'.format(colors['red']+str(v)))

@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def licenseinfo(ctx,license):
    await ctx.message.delete()

    if license is None:
        return

    authkey = b64decode(ReadConfig()['authkey']).decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/LICENSES/?type=fetch&authorization={authkey}&license={license}') as response:
            try:
                response_json = await response.json(content_type=None)
                if response_json['status'] == 'success':
                    #print(response_json)
                    rank = response_json['rank']
                    used = response_json['used']
                    used_by = response_json['used_by']
                    created = response_json['created']

                    if rank == '': rank = 'NOT FOUND'
                    if used == '': used = 'NOT FOUND'
                    if used_by == '': used_by = 'NOT FOUND'
                    if created == '': created = 'NOT FOUND'

                    embed = discord.Embed(title='LICENSEINFO',color=0x00ff00,description=f'LICENSE: ||**{license}**||\nRANK: **{rank}**\nUSED: **{used}**\nUSED BY: **{used_by}**\nCREATED: **{created}**\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='LICENSEINFO',color=0xff0000,description=f'FAILED TO GET LICENSE INFO ||**{license}**||\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='LICENSEINFO',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at LICENSEINFO {0}'.format(colors['red']+str(v)))

@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def dellicense(ctx,license):
    await ctx.message.delete()

    if license is None:
        return

    authkey = b64decode(ReadConfig()['authkey']).decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/LICENSES/?type=delete&license={license}&authorization={authkey}') as response:
            try:
                response_json = await response.json(content_type=None)
                if response_json['status'] == 'success':
                    embed = discord.Embed(title='DELLICENSE',color=0x00ff00,description=f'LICENSE DELETED: ||**{license}**||\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='DELLICENSE',color=0xff0000,description=f'FAILED TO DELETE LICENSE ||**{license}**||\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='DELLICENSE',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at DELLICENSE {0}'.format(colors['red']+str(v)))

@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def uselicense(ctx,license):
    await ctx.message.delete()

    if license is None:
        return

    authkey = b64decode(ReadConfig()['authkey']).decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/LICENSES/?type=use&license={license}&authorization={authkey}') as response:
            try:
                response_json = await response.json(content_type=None)
                if response_json['status'] == 'success':
                    embed = discord.Embed(title='USELICENSE',color=0x00ff00,description=f'LICENSE USED: ||**{license}**||\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='USELICENSE',color=0xff0000,description=f'FAILED TO USE LICENSE ||**{license}**||\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='USELICENSE',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at USELICENSE {0}'.format(colors['red']+str(v)))

@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def unuselicense(ctx,license):
    await ctx.message.delete()

    if license is None:
        return

    authkey = b64decode(ReadConfig()['authkey']).decode()
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/LICENSES/?type=unuse&license={license}&authorization={authkey}') as response:
            try:
                response_json = await response.json(content_type=None)
                if response_json['status'] == 'success':
                    embed = discord.Embed(title='UNUSELICENSE',color=0x00ff00,description=f'LICENSE UNUSED: ||**{license}**||\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='UNUSELICENSE',color=0xff0000,description=f'FAILED TO UNUSE LICENSE ||**{license}**||\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='UNUSELICENSE',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at UNUSELICENSE {0}'.format(colors['red']+str(v)))

#@bot.command(pass_context=True)
#@commands.has_role(owner_role_id)
#async def genlicense(ctx,days,amount,level,format,prefix,length):
#    await ctx.message.delete()

#    if days is None:
#        return
#    if amount is None:
#        return
#    if level is None:
#        return
#    if format is None or int(format) > 5:
#        return
#    if prefix is None:
#        return
#    if length is None:
#        return

#    authkey = b64decode(config['authkey']).decode()
    
#    payload = {
#        'format':int(format),
#        'prefix':prefix,
#        'length':int(length),
#        'days':int(days),
#        'amount':int(amount),
#        'level':int(level),
#    }

#    async with aiohttp.ClientSession() as session:
#        async with session.post(f'https://developers.auth.gg/LICENSES/?type=generate&authorization={authkey}',data=payload) as response:
#            try:
#                response_json = await response.json(content_type=None)
#                print(response_json)
#                if response_json['status'] == 'success':
#                    embed = discord.Embed(title='GENLICENSE',color=0x00ff00,description=f'LICENSE UNUSED: asd\n{ctx.author.mention}')
#                    await ctx.send(embed=embed)
#                elif response_json['status'] == 'failed':
#                    embed = discord.Embed(title='GENLICENSE',color=0xff0000,description=f'FAILED TO UNUSE LICENSE asd\n{ctx.author.mention}')
#                    await ctx.send(embed=embed)
#                else:
#                    embed = discord.Embed(title='GENLICENSE',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
#                    await ctx.send(embed=embed)
#            except ValueError as v:
#                print(colors['yellow']+'JSON Value error at GENLICENSE {0}'.format(colors['red']+str(v)))

@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def licensecount(ctx):
    await ctx.message.delete()

    authkey = b64decode(ReadConfig()['authkey']).decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/LICENSES/?type=count&authorization={authkey}') as response:
            try:
                response_json = await response.json(content_type=None)
                if response_json['status'] == 'success':
                    count = response_json['value']
                    embed = discord.Embed(title='LICENSECOUNT',color=0x00ff00,description=f'LICENSE COUNT: **{count}**\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='LICENSECOUNT',color=0xff0000,description=f'FAILED TO GET LICENSE COUNT\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='LICENSECOUNT',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at LICENSECOUNT {0}'.format(colors['red']+str(v)))

@bot.command(pass_context=True)
@commands.has_role(admin_role_id)
async def gethwid(ctx,username):
    await ctx.message.delete()

    if username is None:
        return

    authkey = b64decode(ReadConfig()['authkey']).decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/HWID/?type=fetch&authorization={authkey}&user={username}') as response:
            try:
                response_json = await response.json(content_type=None)
                if response_json['status'] == 'success':
                    hwid = response_json['value']
                    if hwid == '': hwid = 'NOT FOUND'
                    embed = discord.Embed(title='GETHWID',color=0x00ff00,description=f'USER: **{username}**\nHWID: ||**{hwid}**||\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='GETHWID',color=0xff0000,description=f'FAILED TO GET USER **{username}** HWID\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='GETHWID',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at GETHWID {0}'.format(colors['red']+str(v)))

@bot.command(pass_context=True)
@commands.has_role(owner_role_id)
async def resethwid(ctx,username):
    await ctx.message.delete()

    if username is None:
        return

    authkey = b64decode(ReadConfig()['authkey']).decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/HWID/?type=reset&authorization={authkey}&user={username}') as response:
            try:
                response_json = await response.json(content_type=None)
                if response_json['status'] == 'success':
                    embed = discord.Embed(title='RESETHWID',color=0x00ff00,description=f'USER: **{username}** HWID RESET DONE\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='RESETHWID',color=0xff0000,description=f'FAILED TO RESET USER **{username}** HWID\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='RESETHWID',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at RESETHWID {0}'.format(colors['red']+str(v)))

@bot.command(pass_context=True)
@commands.has_role(owner_role_id)
async def sethwid(ctx,username,newhwid):
    await ctx.message.delete()

    if username is None:
        return

    if newhwid is None:
        return

    authkey = b64decode(ReadConfig()['authkey']).decode()

    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://developers.auth.gg/HWID/?type=set&authorization={authkey}&user={username}&hwid={newhwid}') as response:
            try:
                response_json = await response.json(content_type=None)
                if response_json['status'] == 'success':
                    embed = discord.Embed(title='SETHWID',color=0x00ff00,description=f'USER: **{username}**\nHWID SET TO ||**{newhwid}**||\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                elif response_json['status'] == 'failed':
                    embed = discord.Embed(title='SETHWID',color=0xff0000,description=f'FAILED TO SET USER **{username}** HWID\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='SETHWID',color=0xff0000,description=f'SOMETHING WENT WRONG\n{ctx.author.mention}')
                    await ctx.send(embed=embed)
            except ValueError as v:
                print(colors['yellow']+'JSON Value error at SETHWID {0}'.format(colors['red']+str(v)))

bot.run(ReadConfig()['token'])