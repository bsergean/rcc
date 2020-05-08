'''Test utilities

Copyright (c) 2020 Machine Zone, Inc. All rights reserved.
'''

import asyncio
import os

from rcc.client import RedisClient


def makeClient(port=None, redisPassword='', redisUser=''):
    # redis_url = 'redis://localhost:10000'  # for cluster
    redisUrl = 'redis://localhost'

    if port is not None:
        redisUrl += f':{port}'

    client = RedisClient(redisUrl, redisPassword, redisUser)
    return client


# Start redis server at a given port
async def runRedisServer(port):
    cmd = f'redis-server --port {port}'

    try:
        proc = await asyncio.create_subprocess_shell(cmd)
        stdout, stderr = await proc.communicate()
    finally:
        proc.terminate()


async def getSupportedCommands(client):
    command = await client.send('COMMAND')
    commands = set()
    for item in command:
        commands.add(item[0].decode())

    return commands


async def isCommandSupported(client, cmd):
    commands = await getSupportedCommands(client)
    return cmd in commands


def getRedisServerMajorVersion():
    cmd = f'redis-server --version'
    output = os.popen(cmd).read()
    for token in output.split():
        if token.startswith('v='):
            version = token.split('=')[1]
            major, _, _ = version.partition('.')
            return int(major)

    raise ValueError('Cannot compute redis-server version')
