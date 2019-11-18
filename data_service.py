import motor.motor_asyncio
import logging


DATABASE_LOGGER = logging.getLogger('DATABASE')
MAX_PER_PAGE = 100


class DataService:
    def __init__(self, connection_url, db_name):
        client = motor.motor_asyncio.AsyncIOMotorClient(connection_url)
        self.collection = client[db_name].packages

    async def upsert(self, data):
        result = await self.collection.find_one_and_replace(
            {
                'package': data['package']
            },
            data,
            upsert=True,
            return_document=True,
        )
        DATABASE_LOGGER.info('Upsert info for package %s', result['package'])

    async def find(self, page=0, on_page=20, order_field='_id'):
        cursor = self.collection.find().sort(order_field, -1).skip(page * on_page).limit(on_page)
        result = await cursor.to_list(length=MAX_PER_PAGE)
        return result

    async def count(self):
        return await self.collection.count_documents({})
