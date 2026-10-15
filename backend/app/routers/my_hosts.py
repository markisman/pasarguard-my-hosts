from fastapi import APIRouter, Depends

from app.db import AsyncSession, get_db
from app.models.admin import AdminDetails
from app.models.admin_host_override import AdminHostOverrideBulk, MyHostsResponse
from app.operation.my_hosts import my_hosts_operation
from app.routers.authentication import require_permission

router = APIRouter(tags=["My Hosts"], prefix="/api/my_hosts")


@router.get("", response_model=MyHostsResponse)
async def list_my_hosts(
    db: AsyncSession = Depends(get_db),
    admin: AdminDetails = Depends(require_permission("hosts", "read")),
):
    """List hosts with THIS admin's customizations applied (name/order/visibility)."""
    hosts = await my_hosts_operation.list_hosts(db, admin.id)
    return {"hosts": hosts}


@router.put("", response_model=MyHostsResponse)
async def save_my_hosts(
    model: AdminHostOverrideBulk,
    db: AsyncSession = Depends(get_db),
    admin: AdminDetails = Depends(require_permission("hosts", "read")),
):
    """Save THIS admin's host customizations. Only affects the caller's account."""
    await my_hosts_operation.save_hosts(db, admin.id, model.items)
    hosts = await my_hosts_operation.list_hosts(db, admin.id)
    return {"hosts": hosts}
