from aiocache import cached

from app.db import GetDB
from app.db.crud.admin_host_override import get_overrides


@cached(ttl=30)
async def get_admin_host_overrides(admin_id: int) -> dict[int, dict]:
    """Cached {host_id: {display_name, sort_order, is_disabled}} for an admin."""
    if not admin_id:
        return {}
    async with GetDB() as db:
        rows = await get_overrides(db, admin_id)
    return {
        row.host_id: {
            "display_name": row.display_name,
            "sort_order": row.sort_order,
            "is_disabled": row.is_disabled,
        }
        for row in rows
    }


async def invalidate_admin_host_overrides() -> None:
    try:
        await get_admin_host_overrides.cache.clear()
    except Exception:
        pass
