from sqlalchemy.ext.asyncio import AsyncSession

from app.core.admin_host_overrides import invalidate_admin_host_overrides
from app.core.hosts import host_manager
from app.db.crud.admin_host_override import get_overrides, replace_overrides


class MyHostsOperation:
    async def list_hosts(self, db: AsyncSession, admin_id: int) -> list[dict]:
        hosts = await host_manager.get_hosts()  # dict[int, SubscriptionInboundData]
        overrides = {row.host_id: row for row in await get_overrides(db, admin_id)}

        result: list[dict] = []
        for host_id, host_data in hosts.items():
            ov = overrides.get(host_id)
            port = None
            if host_data.port:
                port = host_data.port[0] if isinstance(host_data.port, list) else host_data.port
            result.append(
                {
                    "host_id": host_id,
                    "inbound_tag": host_data.inbound_tag,
                    "address": list(host_data.address) if host_data.address else [],
                    "port": port,
                    "remark": host_data.remark,
                    "priority": host_data.priority,
                    "is_disabled": False,
                    "display_name": ov.display_name if ov else None,
                    "sort_order": ov.sort_order if ov else None,
                    "override_disabled": bool(ov.is_disabled) if ov else False,
                }
            )

        result.sort(key=lambda h: h["sort_order"] if h["sort_order"] is not None else h["priority"])
        return result

    async def save_hosts(self, db: AsyncSession, admin_id: int, items: list) -> None:
        data = [it.model_dump() if hasattr(it, "model_dump") else dict(it) for it in items]
        await replace_overrides(db, admin_id, data)
        await invalidate_admin_host_overrides()


my_hosts_operation = MyHostsOperation()
