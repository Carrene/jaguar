import asyncio
import asyncpg

from nanohttp import settings


_connection = None


async def get_connection():
    global _connection
    if _connection is None:
        _connection = await asyncpg.connect(settings.db.url)

    return _connection


async def close_connection():
    global _connection
    if _connection is None:
        return

    await _connection.close()
    _connection = None



async def get_members_by_target(target_id):
    query = '''
    SELECT m.id, m.reference_id
    FROM member m
    LEFT OUTER JOIN target_member tm ON m.id = tm.member_id
    WHERE tm.target_id = $1
    '''
    members = await (await get_connection()).fetch(query, target_id)
    return members

