"""
Feature: My Hosts (per-admin host customization)
================================================

What it does
------------
Allows every admin (and sub-admin / reseller) to, ONLY FOR THEIR OWN ACCOUNT:
  * rename hosts (custom display name shown in subscription links & configs)
  * reorder hosts (custom sort order)
  * enable/disable hosts (hide a host from their own subscription output)

It never touches the global host config, and other admins are unaffected.

How it plugs in
---------------
1. New table `admin_host_overrides` (admin_id, host_id, display_name, sort_order, is_disabled)
2. CRUD + a small cached accessor in app/core/admin_host_overrides.py
3. Router `/api/my_hosts` (GET list for current admin, PUT to save)
4. One integration point in app/subscription/share.py -> process_inbounds_and_tags()
   (right after hosts are loaded, before randomize/process)
5. Dashboard page "My Hosts" + sidebar entry + i18n

Files
-----
app/db/models.append.py            -> append to app/db/models.py
app/db/crud/admin_host_override.py -> new file
app/core/admin_host_overrides.py   -> new file
app/models/admin_host_override.py  -> new file
app/operation/my_hosts.py          -> new file
app/routers/my_hosts.py            -> new file
migrations/alembic_...             -> new alembic revision
patches/share.py.patch             -> unified diff for app/subscription/share.py
patches/routers_init.patch         -> register router in app/routers/__init__.py (if needed)
frontend/README.md                 -> dashboard (React) integration notes + component
INSTALL.md                         -> how to apply

STATUS: code prepared, NOT built/tested. Needs `bun run build` for dashboard and
a container rebuild before deploy. See INSTALL.md.
"""
