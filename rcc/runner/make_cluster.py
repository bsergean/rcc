'''Tools to help initialize a redis cluster on kubernete

Copyright (c) 2020 Machine Zone, Inc. All rights reserved.
'''

import asyncio
import tempfile

import click

from rcc.cluster.init_cluster import runNewCluster


@click.command()
@click.option('--size', default=3, type=int)
@click.option('--start_port', default=11000, type=int)
def make_cluster(size, start_port):
    root = tempfile.mkdtemp()

    asyncio.run(runNewCluster(root, start_port, size))
