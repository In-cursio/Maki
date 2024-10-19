import motor.motor_asyncio
from info import DATABASE_URI, DATABASE_NAME


class FSub:
    def __init__(self):
        if DATABASE_URI:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
            self.db = self.client[DATABASE_NAME]
            self.col_req = self.db["Join_Reqs"]
            self.col_fsub = self.db["FSub"]
        else:
            self.client = None
            self.db = None
            self.col_req = None
            self.col_fsub = None

    def isActive(self):
        if self.client is not None:
            return True
        else:
            return False

    async def add_user(self, req_channel, user_id, first_name, username, date):
        try:
            await self.col_req.insert_one(
                {
                    "_id": int(user_id),
                    "req_channel": int(req_channel),
                    "user_id": int(user_id),
                    "first_name": first_name,
                    "username": username,
                    "date": date,
                }
            )
        except Exception:
            pass

    async def get_user(self, req_channel, user_id):
        return await self.col_req.find_one(
            {"req_channel": int(req_channel), "user_id": int(user_id)}
        )

    async def get_all_users(self, req_channel):
        return await self.col_req.find({"req_channel": int(req_channel)}).to_list(None)

    async def delete_user(self, req_channel, user_id):
        await self.col_req.delete_one(
            {"req_channel": int(req_channel), "user_id": int(user_id)}
        )

    async def delete_all_users(self, req_channel):
        await self.col_req.delete_many({"req_channel": int(req_channel)})

    async def get_all_users_count(self, req_channel):
        return await self.col_req.count_documents({"req_channel": int(req_channel)})

    async def add_auth_channel(self, auth_channel):
        try:
            await self.col_fsub.delete_one({"req_channel": {"$exists": True}})
            await self.col_fsub.update_one(
                {"auth_channel": {"$exists": True}},
                {"$set": {"auth_channel": int(auth_channel)}},
                upsert=True,
            )
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    async def add_req_channel(self, req_channel):
        try:
            await self.col_fsub.delete_one({"auth_channel": {"$exists": True}})
            await self.col_fsub.update_one(
                {"req_channel": {"$exists": True}},
                {"$set": {"req_channel": int(req_channel)}},
                upsert=True,
            )
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    async def get_auth_channel(self):
        document = await self.col_fsub.find_one(
            {"auth_channel": {"$exists": True}}
        )  # Adjust the query as needed
        if document:
            return document.get("auth_channel")
        return None

    async def get_req_channel(self):
        document = await self.col_fsub.find_one(
            {"req_channel": {"$exists": True}}
        )
        if document:
            return document.get("req_channel")
        return None

    async def delete_auth_channel(self, auth_channel):
        try:
            result = await self.col_fsub.delete_one({"auth_channel": auth_channel if isinstance(auth_channel, int) else str(auth_channel)})            
            if result.deleted_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f"An error occurred during deletion: {e}")
            return False

    async def delete_req_channel(self, req_channel):
        try:
            result = await self.col_fsub.delete_one({"req_channel": req_channel if isinstance(req_channel, int) else str(req_channel)})
            if result.deleted_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f"An error occurred during deletion: {e}")
            return False

