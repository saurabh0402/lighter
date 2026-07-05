import asyncio
from helpers.screengrab_perm import get_screencast_node_id
from helpers.screengrab_pipeline import build_pipeline, get_screengrab

async def main():
    fd, node_id = get_screencast_node_id()
    _, appsink = build_pipeline(fd, node_id)
    screen_data = get_screengrab(appsink)
    print(screen_data)

    # bulbs = await discovery.discover_lights(broadcast_space='192.168.0.255')
    # bulb = bulbs[0]

    # light = wizlight(bulb.ip)
    # await light.turn_on(PilotBuilder(warm_white=255))

    # for i in range(255, 10, -1):
    #     await light.turn_on(PilotBuilder(rgb=(255,0,0), brightness=i))
    #     print(i)
    #     sleep(0.1)

if __name__ == '__main__':
    asyncio.run(main())