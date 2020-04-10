'''Tools to help initialize a redis cluster on kubernete

Copyright (c) 2020 Machine Zone, Inc. All rights reserved.
'''

import asyncio
import logging
import tempfile

import click

from rcc.cluster.init_cluster import runNewCluster


@click.command()
@click.option('--size', default=3, type=int)
@click.option('--start_port', default=11000, type=int)
@click.option('--password', '-a')
def make_cluster(size, start_port, password):
    '''Create, configure, initialize and run a redis cluster
    and a redis cluster proxy'''
    root = tempfile.mkdtemp()

    try:
        asyncio.run(runNewCluster(root, start_port, size, password))
    except Exception as e:
        logging.error(f'cluster_nodes error: {e}')
