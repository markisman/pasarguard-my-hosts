# Feature: My Hosts — installation guide

> Status: **code prepared, NOT built/tested.** Apply, build the dashboard, rebuild
> the image, back up the DB, then run the migration.

## 1. Files to copy into a clone of PasarGuard/panel (v5.4.1)

| from (this package) | to (repo) |
|---|---|
| `backend/app/db/models.append.py` (content) | **append** to `app/db/models.py` |
| `backend/app/models/admin_host_override.py` | `app/models/admin_host_override.py` |
| `backend/app/db/crud/admin_host_override.py` | `app/db/crud/admin_host_override.py` |
| `backend/app/core/admin_host_overrides.py` | `app/core/admin_host_overrides.py` |
| `backend/app/operation/my_hosts.py` | `app/operation/my_hosts.py` |
| `backend/app/routers/my_hosts.py` | `app/routers/my_hosts.py` |
| `backend/migrations/alembic_add_admin_host_overrides.py` | `app/db/migrations/versions/<rev>_add_admin_host_overrides.py` |
| `frontend/MyHosts.tsx` + `frontend/README.md` | dashboard page (see frontend/README) |

## 2. Apply the two small patches
```
cd <repo>
git apply backend/patches/share.py.diff
git apply backend/patches/routers__init__.py.diff
```
(If they fail because of version drift, edit by hand — the changes are tiny and
described inside each diff.)

## 3. Fix the migration head
In `.../add_admin_host_overrides.py` set `down_revision` to the current head:
```
docker exec pasarguard-pasarguard-1 alembic heads
```

## 4. Build the dashboard
```
cd dashboard && bun install && VITE_BASE_API=/ bun run build
cp build/index.html build/404.html
```

## 5. Build & deploy a CUSTOM image (so upstream updates don't wipe it)
```
docker build -t pasarguard/panel:custom .
# then in /opt/pasarguard/docker-compose.yml set image: pasarguard/panel:custom
docker compose up -d
```

## 6. Apply DB migration
```
docker exec pasarguard-pasarguard-1 alembic upgrade head
```

## Rollback
- set the old image back, or:
```
docker exec pasarguard-pasarguard-1 alembic downgrade -1
```
- the new table is additive; dropping it restores the original behaviour.

## API added
- `GET  /api/my_hosts`  → list of hosts with the caller's override applied
- `PUT  /api/my_hosts`  → `{"items":[{"host_id":1,"display_name":"UK","sort_order":2,"is_disabled":false}, ...]}`
- Affects ONLY the calling admin's own subscription output. Global host config untouched.
