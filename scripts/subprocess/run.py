import sys
import asyncio
import subprocess

# #https://github.com/intel/dffml/tree/master/feature/git/dffml_feature_git/util/proc.py
# async def _create(*args, **kwargs):
#     """
#     Runs a subprocess using asyncio.create_subprocess_exec and returns the
#     process.
#     """
#     #LOGGER.debug("proc.create: %r", args)
#     proc = await asyncio.create_subprocess_exec(
#         *args,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE,
#         start_new_session=True,
#         **kwargs,
#     )
#     proc.name = args[0]
#     proc.args = args[1:]
#     return proc
#
# #https://github.com/intel/dffml/tree/master/feature/git/dffml_feature_git/util/proc.py
# async def _check_output(*args, **kwargs):
#     """
#     Runs a subprocess using asyncio.create_subprocess_exec and returns either
#     its standard error or output.
#     """
#     proc = await _create(*args, **kwargs)
#     stdout, stderr = await get_output(proc)
#     await stop(proc)
#     return stdout or stderr

async def run_process():
    try:
        output = subprocess.check_output(['python', '../brawlstats-counter/count-participants.py'])
        return output
    except subprocess.CalledProcessError as e:
        return e.output

async def main_program(args):
    print(args)
    output = await run_process()
    output_lines = output.decode('utf-8')
    print(output_lines)

asyncio.run(main_program(sys.argv))
