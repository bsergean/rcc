'''Migrate slots from one node to another

Copyright (c) 2020 Machine Zone, Inc. All rights reserved.
'''

import asyncio

import click

from rcc.client import RedisClient
from rcc.cluster.reshard import migrateSlot, makeClientfromNode


async def runMigration(src_addr, dst_addr, redisPassword, redisUser, slot, dry):
    redisClient = RedisClient(src_addr, redisPassword, redisUser)
    nodes = await redisClient.cluster_nodes()

    masterNodes = [node for node in nodes if node.role == 'master']
    masterClients = [
        makeClientfromNode(node, redisPassword, redisUser) for node in masterNodes
    ]

    # find source and destination nodes by ip:port
    for node in masterNodes:
        nodeUrl = f'redis://{node.ip}:{node.port}'

        if nodeUrl == src_addr:
            sourceNode = node

        if nodeUrl == dst_addr:
            destinationNode = node

    return await migrateSlot(
        masterClients, redisPassword, redisUser, slot, sourceNode, destinationNode, dry
    )


@click.command()
@click.option('--src-addr')
@click.option('--dst-addr')
@click.option('--password', '-a')
@click.option('--user')
@click.option('--dry', is_flag=True)
@click.argument('slot')
def migrate(src_addr, dst_addr, password, user, slot, dry):
    '''Migrate one slot from a node to another one'''

    asyncio.run(runMigration(src_addr, dst_addr, password, user, slot, dry))
