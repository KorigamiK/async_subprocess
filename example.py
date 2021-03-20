from async_subprocess import async_subprocess, timer
import asyncio

loop = asyncio.get_event_loop()


@timer
async def main():
    # A bad and bodgy way to do this, I know. But it just works
    # the last element maybe description or input and  second last element maybe description
    cmds = [
        ("bash", "-c", "ls && cd ./xx", "hi"),
        ("bash", "-c", "sleep 2 && asdfa", "hello"),
        ("bash", "-c", "echo hehe && sleep 3", "bye"),
        ("bash", "-c", "python3 teset.py", "input", ["hi"]),
    ]
    tasks = []
    for i in cmds:
        # print(len(i))
        if len(i) <= 4:
            tasks.append(
                asyncio.create_task(async_subprocess(*i[:-1], description=i[-1]))
            )
        else:
            tasks.append(
                asyncio.create_task(
                    async_subprocess(*i[:-2], description=i[-2], std_inputs=i[-1])
                )
            )

    return await asyncio.gather(*tasks)


print(loop.run_until_complete(main()))