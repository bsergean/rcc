'''Tools to help initialize a redis cluster on kubernete

Copyright (c) 2020 Machine Zone, Inc. All rights reserved.
'''

import asyncio
import logging
import os
import shutil
import tempfile
import traceback

import click

from rcc.cluster.init_cluster import runNewCluster


@click.command()
@click.option('--size', default=3, type=int)
@click.option('--replicas', default=1, type=int)
@click.option('--start_port', default=30001, type=int)
@click.option('--password', '-a')
@click.option('--user')
@click.option('--use_redis_cli', '-c', is_flag=True)
def make_cluster(size, start_port, password, user, replicas, use_redis_cli):
    '''Create, initialize and run a redis cluster
    and a redis cluster proxy'''
    root = tempfile.mkdtemp()
    clusterReadyFile = os.path.join(root, 'redis_cluster_ready.json')

    manual = not use_redis_cli

    try:
        asyncio.get_event_loop().run_until_complete(
            runNewCluster(
                root,
                clusterReadyFile,
                start_port,
                size,
                password,
                user,
                replicas,
                manual,
            )
        )
    except Exception as e:
        backtrace = traceback.format_exc()
        logging.debug(f'cluster_nodes traceback: {backtrace}')
        logging.error(f'cluster_nodes error: {e}')
    finally:
        shutil.rmtree(root)
