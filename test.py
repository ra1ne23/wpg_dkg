import discord
from discord.ext import commands
from discord.utils import get
import requests
from PIL import Image, ImageFont, ImageDraw
import io

client=commands.Bot(command_prefix=".")
client.remove_command("help")

#Join
@client.command()
async def join(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		await ctx.send(f'Бот присоединился к каналу: {channel}')

#Leave
@client.command()
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)

	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await connect.channel()
		await ctx.send(f'Бот отключился от канала: {channel}')

#Status
@client.event

async def on_ready():
	print('Bot присоединился')

	await client.change_presence( status = discord.Status.online, activity = discord.Game('Programming Server'))

#Clear
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)

async def clear(ctx,amount=100): #Очистка чата
	await ctx.channel.purge(limit=amount) 

#Kick
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)

async def kick(ctx, member: discord.Member, *, reason = None):
	await ctx.channel.purge(limit=1)

	await member.kick( reason = reason ) 
	await ctx.send (f'kick user {member.mention}') #Ban

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)

async def ban( ctx, member: discord.Member , *,  reason = None ):
	await ctx.channel.purge( limit = 1 )

	await member.ban(reason=reason)
	await ctx.send (f'ban user {member.mention}') 

#Mute
@client.command()
@commands.has_permissions(administrator = True)

async def user_mute( ctx, member: discord.Member ):
	await ctx.channel.purge( limit = 1 )

	mute_role = discord.utils.get( ctx.message.guild.roles, name ='MUTE' )

	await member.add_roles(mute_role)
	await ctx.send(f'У { member.mention }, ограничение чата, за нарушение правил!')

#Выдача роли Member
@client.event

async def on_member_join( member ):
	channel=client.get_channel( 823930964844478471 )

	role = discord.utils.get( member.guild.roles, id = 823932478355275826 )

	await member.add_roles( role )
	await channel.send( emb = discord.Embed( description =f'Пользователь {member.name}, присоединился к нам!',color = 0x0c0c0c))

#help
@client.command( pass_context = True )
@commands.has_permissions(administrator = True)

async def help(ctx):
	emb = discord.Embed( title = 'Cписок команд')

	emb.add_field( name = 'clear'.format(client), value = "Очистка чата")
	emb.add_field( name = 'kick'.format(client), value = "Выгонять участников")
	emb.add_field( name = 'ban'.format(client), value = "Ограничить доступ к серверу")
	emb.add_field( name = 'user_mute'.format(client), value = "Блокировать сообщения")
	emb.add_field( name = 'help'.format(client), value = "Открывает список команд")
	emb.add_field( name = 'join'.format(client), value = "Бот присоединится к голосовому каналу")
	emb.add_field( name = 'leave'.format(client), value = "Бот отключается от голосового канала")

	await ctx.send(embed=emb)

client.run('ODI1MjgyMDAxOTE3NTc1MjA4.YF7pwg.rlQHrx23-hfaiOi-inJGCtxrHVA') 
