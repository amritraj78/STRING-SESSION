from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
import config

if config.MONGO_DB_URI:
    mongo = MongoCli(config.MONGO_DB_URI)
    db = mongo.StringGen
else:
    mongo = None

    class DummyCollection:
        async def find_one(self, *args, **kwargs):
            return None

        async def insert_one(self, *args, **kwargs):
            return None

        def find(self, *args, **kwargs):
            class AsyncIterator:
                def __aiter__(self):
                    return self

                async def __anext__(self):
                    raise StopAsyncIteration

            return AsyncIterator()

    class DummyDB:
        def __getattr__(self, name):
            return DummyCollection()

    db = DummyDB()
