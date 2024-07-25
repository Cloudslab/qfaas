from qfaas.database.dbUser import retrieve_user

async def get_role(username: str):
    user = await retrieve_user(username)
    return user['role']
