# General

[![PyPI version](https://badge.fury.io/py/rcc.svg)](https://badge.fury.io/py/rcc)
![Build status](https://github.com/machinezone/rcc/workflows/unittest/badge.svg)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/rcc.svg)](https://img.shields.io/pypi/pyversions/rcc)
[![License](https://img.shields.io/pypi/l/rcc.svg)](https://img.shields.io/pypi/l/rcc)
[![Wheel](https://img.shields.io/pypi/wheel/rcc.svg)](https://img.shields.io/pypi/wheel/rcc)

A Redis Cluster Client

## Rationale

The main asyncio redis library does not support redis cluster at this point. There is another library named aredis which has cluster support, but which has some small bugs for which pull requests existed, that were not merged until recently. Getting a redis client to work is not terribly hard, thanks to the design of redis, so I started this project and got it to work in a limited amount of time.

## Tools

Several tools come with this package, as subcommands of rcc.

* keyspace / will turn on redis keyspace notifications and tell you what your _hot_ keys are.
* binpacking / will help reshard your cluster in an optimal way based on your usage. This will consume the output of the analyze-keyspace command
* make-cluster / will create configuration files for running a redis cluster, start redis servers and initialize the cluster (using redis-cli commands)

Interested? Go read the [docs](https://machinezone.github.io/rcc/)
