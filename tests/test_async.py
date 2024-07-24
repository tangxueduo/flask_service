import pytest
import asyncio
import time

async def buy_potatos():
    print('buy potatos')

async def get_money():
    asyncio.sleep(10)
    time.sleep(10) # 真正的延迟
    return 11

async def buy_tomatos():
    # 这里等待get_money返回，
    res = await get_money()
    print(res)
    print('buy tomatos')

def test_async():
    loop = asyncio.get_event_loop()
    # 加入队列中的任务是异步完成的，由于tomatos 睡了10s。所以延迟完成，potatos 先完成
    res = loop.run_until_complete(asyncio.wait([buy_tomatos(),buy_potatos()]))
    print(f'loop res: {res}')
    loop.close()
