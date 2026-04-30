import aiohttp

class Joke:
    def __init__(self, id, contents):
        self.id = id
        self.contents = contents

async def get_quote():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://icanhazdadjoke.com', headers={"Accept": "application/json"}) as response:
            words = await response.json()
            print(words)
            return words['joke']
