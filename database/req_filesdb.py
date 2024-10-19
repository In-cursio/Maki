import motor.motor_asyncio
from info import DATABASE_URI, DATABASE_NAME


class ReqFiles:
    def __init__(self):
        if DATABASE_URI:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
            self.db = self.client[DATABASE_NAME]
            self.col = self.db["Req_Files"]

        else:
            self.client = None
            self.db = None
            self.col = None

    def isActive(self):
        if self.client is not None:
            return True
        else:
            return False


    async def add_file(self, user_id, group_id, file_mode, file_id):
        if self.isActive():
            await self.col.delete_one(
                {"user_id": user_id, "group_id": group_id}
            )
            doc = {
                "user_id": user_id,
                "group_id": group_id,
                "file_mode": file_mode,
                "file_id": file_id,
            }
            await self.col.insert_one(doc)
            return True

    async def delete_file(self, user_id, group_id):
        if self.isActive():
            await self.col.delete_one(
                {"user_id": user_id, "group_id": group_id}
            )
            return True

    async def get_file(self, user_id, group_id):
        if self.isActive():
            doc = await self.col.find_one({"user_id": user_id, "group_id": group_id})
            return doc

    async def delete_all_files(self):
        if self.isActive():
            result = await self.col.delete_many({})
            return result.deleted_count
        return False
