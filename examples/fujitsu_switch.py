import asyncio
import logging

import yaml

import netdev

config_path = 'config.yaml'

logging.basicConfig(level=logging.INFO)
netdev.logger.setLevel(logging.DEBUG)

async def task(param):
    async with netdev.create(**param) as fuj:
        # Testing sending configuration set
        out = await fuj.send_config_set(['vlan database', 'exit'])
        print(out)
        # Testing sending simple command
        out = await fuj.send_command('show ver')
        print(out)


async def run():
    config = yaml.safe_load(open(config_path, 'r'))
    devices = yaml.safe_load(open(config['device_list'], 'r'))
    tasks = [task(dev) for dev in devices if dev['device_type'] == 'fujitsu_switch']
    await asyncio.wait(tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
