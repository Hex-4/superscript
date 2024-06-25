import sys
import asyncio
async def read_file(location):
    try:
        with open(location, "r") as f:
            return f.read()
    except FileNotFoundError:
        print("File not found.")
        return ""

async def main():
    args = sys.argv
    args.pop(0)
    if "--debug" in args:
        debug = True
        print("Debug mode on. GLHF!")
    location = args[0]
    if location:
        program = await read_file(location)
        print(program)
    else:
        # Response mode
        pass

asyncio.run(main())