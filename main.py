import asyncio
from asyncio.subprocess import PIPE
from time import time

def timer(function):
    async def wrapped_func(*args, **kwargs):
        s = time()
        res = await function(*args, **kwargs)
        print(f'{function.__name__} took {time()-s} seconds')
        return res
    return wrapped_func

async def async_subprocess(*cmd_args, std_inputs: list=[], loop:asyncio.AbstractEventLoop=None, description='Process'):
    process = await asyncio.create_subprocess_exec(*cmd_args, stderr=PIPE, stdin=PIPE, loop=loop, stdout=PIPE)

    async def _read_stream(stream: asyncio.StreamReader, stream_type: str):
        ''' Breaks if an empty line is the output of error '''
        while True:
            line = await stream.readline()
            # await asyncio.sleep(.1)
            if line:
                print(f"[{description}] {stream_type}: {line.decode('utf-8').strip()}")
            else:
                break

    async def _write_stream(stream: asyncio.StreamWriter, inputs: list):
        '''waits 1 sec for each input'''
        for input in inputs:
            await asyncio.sleep(1)
            buf = f'{input}\n'.encode()
            print(f'[{description}] stdin: {input}')

            stream.write(buf)
            await stream.drain()

    stderr_stream = process.stderr
    stdout_stream = process.stdout
    stdin_stream = process.stdin
    await asyncio.gather(_read_stream(stdout_stream, 'stdout'), _read_stream(stderr_stream, 'stderr'), _write_stream(stdin_stream, std_inputs))
    return await process.wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop = None
    @timer
    async def main():
        # A bad and bodgy way to do this, I know. But it just works 
        cmds = [('bash', '-c', 'ls && cd ./xx', 'hi'),
            ('bash', '-c', 'sleep 2 && asdfa', 'hello'),
            ('bash', '-c', 'echo hehe && sleep 3', 'bye'),
            ('bash', '-c', 'python3 tempCodeRunnerFile.py', 'input', ['hi'])
        ]
        tasks = []
        for i in cmds:
            # print(len(i))
            if len(i) <= 4:
                tasks.append(asyncio.create_task(async_subprocess(*i[:-1], description=i[-1])))
            else:
                tasks.append(asyncio.create_task(async_subprocess(*i[:-2], description=i[-2], std_inputs=i[-1])))
        await asyncio.wait(tasks)

    print(loop.run_until_complete(main()))