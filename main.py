import discord
from sys import argv
# from asyncio import sleep
from aioconsole import ainput
from os import system,getenv
from dotenv import load_dotenv


load_dotenv()

class base(discord.Client):
  def __init__(self,*,loop=None,**options):
    super().__init__(loop=loop,**options)
    self.current_guild = 0
    self.current_channel = 0


  async def on_ready(self):
    print(f'{self.user.name} connected to discord!')
    await base.cli_input(self)

  async def on_message(self,message):
     if message.channel.id != self.current_channel or message.author == self.user: return
     print(f'[{message.author.name}] {message.content}')

  async def cli_input(self):
    while True:
      inp = (await ainput('')).split(' ')
      match inp[0].lower():
        case 'send': await self.get_channel(self.current_channel).send(' '.join(inp[1:]))
        case 'set':
          match inp[1].lower():
            case 'guild': self.current_guild = int(inp[2]) if len(inp[2]) == 18 else self.guilds[int(inp[2])].id
            case 'channel': self.current_channel = int(inp[2]) if len(inp[2]) == 18 else self.get_guild(self.current_guild).text_channels[int(inp[2])].id
        case 'list':
          match inp[1].lower():
            case 'guilds':
              index,res = 0,[]
              for guild in self.guilds:
                res.append(f'[{index}] [{guild.id}] {guild.name}')
                index += 1
              print('\n'.join(res))
            case 'channels':
              index,res = 0,[]
              if self.current_guild not in [guild.id for guild in self.guilds]: print('you must be in a guild to list channels!'); continue
              for channel in self.get_guild(self.current_guild).text_channels:
                res.append(f'[{index}] [{channel.id}] {channel.name}')
                index += 1
              print('\n'.join(res))
        case 'clear': system('clear'); print('console cleared.')
        # case 'relog': self.logout(); await sleep(5); self.start()
        case 'exit': print('exiting...'); exit()
        case '': pass
        case _: print('unknown command')

client = base()

try: client.run(argv[1] if len(argv) > 1 else getenv('token'))
except SystemExit: pass