from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AdminHostOverride


async def get_overrides(db: AsyncSession, admin_id: int) -> list[AdminHostOverride]:
    result = await db.execute(
        select(AdminHostOverride).where(AdminHostOverride.admin_id == admin_id)
    )
    return list(result.scalars().all())


async def replace_overrides(
    db: AsyncSession,
    admin_id: int,
    items: list[dict],
) -> list[AdminHostOverride]:
    """Bulk upsert for one admin. Items not present are removed.

    Each item: {"host_id": int, "display_name": str|None, "sort_order": int|None, "is_disabled": bool}
    """
    existing_rows = await get_overrides(db, admin_id)
    existing = {row.host_id: row for row in existing_rows}

    seen: set[int] = set()
    for item in items:
        host_id = int(item["host_id"])
        seen.add(host_id)
        row = existing.get(host_id)
        if row is None:
            row = AdminHostOverride(admin_id=admin_id, host_id=host_id)
            db.add(row)
        row.display_name = item.get("display_name") or None
        row.sort_order = item.get("sort_order")
        row.is_disabled = bool(item.get("is_disabled", False))

    # Remove overrides for hosts the admin no longer customizes
    for host_id, row in existing.items():
        if host_id not in seen:
            await db.delete(row)

    await db.commit()

    # Return the current set
    return await get_overrides(db, admin_id)


async def delete_overrides_for_host(db: AsyncSession, host_id: int) -> None:
    rows = (await db.execute(select(AdminHostOverride).where(AdminHostOverride.host_id == host_id))).scalars().all()
    for row in rows:
        await db.delete(row)
    await db.commit()


async def delete_overrides_for_admin(db: AsyncSession, admin_id: int) -> None:
    rows = (await db.execute(select(AdminHostOverride).where(AdminHostOverride.admin_id == admin_id))).scalars().all()
    for row in rows:
        await db.delete(row)
    await db.commit()
