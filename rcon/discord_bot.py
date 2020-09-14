import os
import logging
import asyncio

import discord
from discord.ext import commands, tasks

from rcon.extended_commands import Rcon

DISCORD_BOT_PREFIX = "#"
DISCORD_BOT_TOKEN = ""


class DiscordBot:
    bot = commands.Bot(command_prefix=DISCORD_BOT_PREFIX)


    def _get_servers(self):
        # I needed to get the address, port and password for all
        # servers, if there's a better way please let me know
        env_vars = {}
        with open(".env", "r") as f:
            for line in f.readlines():
                if not "=" in line:
                    continue
                line = line.strip().split("=", 1)
                key = line[0]
                value = line[1]
                if any([key.startswith("HLL_HOST"), key.startswith("HLL_PORT"), key.startswith("HLL_PASSWORD")]):
                    env_vars[key] = value
        
        servers = []
        server_info = {}
        env_vals = [value for key, value in env_vars.items()]
        while len(env_vals) >= 3:

            server_info['host'] = env_vals[0]
            try: server_info['port'] = int(env_vals[1])
            except ValueError: server_info['port'] = ''
            server_info['password'] = env_vals[2]
            
            if all([len(val) for val in env_vals[:3]]):
                servers.append(server_info)
            del env_vals[:3]

        print(servers)
        return servers
    
    def __init__(self):
        self.servers = self._get_servers()
        self.rcon = [Rcon(server) for server in self.servers]

        



    

    @bot.event
    async def on_ready(self):
        pass

    
    def get_server_data(self, server_index):
        pass






discordbot = DiscordBot()
#bot.run(DISCORD_BOT_TOKEN)