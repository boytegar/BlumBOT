import subprocess
import asyncio
import json

async def get_payload(gameId, points):
    process = await asyncio.create_subprocess_exec('node', 'payload/blum.mjs', gameId, str(points), stdout=asyncio.subprocess.PIPE)
    output, _ = await process.communicate()
    payload = output.decode('utf-8').strip()
    return json.dumps({'payload': payload})

import subprocess

def get_payloads(gameid, points, freeze):
    points_str = str(points)
    freeze_str = str(freeze)
    
    process = subprocess.run(
        ['node', 'payload/blum.mjs', gameid, points_str, freeze_str],
        stdout=subprocess.PIPE,
        text=True)

    if process.returncode != 0:
        print(f"Error: {process.stderr.strip()}")
        return None

    payload = process.stdout.strip()
    return payload

