import asyncio
import numpy as np
from helpers.screengrab_perm import get_screencast_node_id
from helpers.screengrab_pipeline import build_pipeline, get_screengrab
from helpers.colors import rgb_to_linear, linear_to_rgb, get_brightness
from pywizlight import discovery, wizlight, PilotBuilder
from time import sleep
import sys

async def main():
    fd, node_id = get_screencast_node_id()
    _, appsink = build_pipeline(fd, node_id)
    bulbs = await discovery.discover_lights(broadcast_space='192.168.0.255')

    if not bulbs:
        print('No bulbs found')
        sys.exit(0)

    bulb = bulbs[0]
    light = wizlight(bulb.ip)

    while True:
        screen_data = get_screengrab(appsink)
        linear_data = rgb_to_linear(screen_data)
        
        mean = linear_data.mean(axis=(1, 0))
        bulb_color = linear_to_rgb(mean)
        bulb_color = (int(bulb_color[0]), int(bulb_color[1]), int(bulb_color[2]))

        new_brightness = get_brightness(bulb_color)
        await light.turn_on(
            PilotBuilder(rgb=bulb_color,
            brightness=new_brightness)
        )
        sleep(0.1)

if __name__ == '__main__':
    asyncio.run(main())