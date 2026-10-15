# Dashboard integration — My Hosts page

Stack: React + React Router (file-based `src/pages/_dashboard.<route>.tsx`) +
TanStack Query + Radix/Tailwind. API client is orval-generated in `src/service/api`.

## Steps

1. **Regenerate the API client** so typed `getMyHosts` / `saveMyHosts` exist:
   - the backend already exposes `GET/PUT /api/my_hosts`, so after running the
     panel, run orval against the panel OpenAPI (`/openapi.json`) per `orval.config.ts`.
   - OR just use the plain `fetch` version in `MyHosts.tsx` below (no codegen needed).

2. **Copy** `MyHosts.tsx` → `dashboard/src/pages/_dashboard.my-hosts.tsx`.
   The filename gives the route `/my-hosts`.

3. **Sidebar**: add an entry next to "Hosts" in the dashboard nav
   (`src/app/*` / layout component). Use icon `Server` from `lucide-react` and
   `t('myHosts.title', { defaultValue: 'My Hosts' })`.

4. **i18n**: add keys to `src/locales/*`:
   ```
   myHosts: {
     title: "My Hosts",
     subtitle: "Change the server names and order shown to you. These changes only affect your account.",
     search: "Search hosts",
     resetOrder: "Reset order",
     resetAll: "Reset all",
     save: "Save",
     saved: "Saved",
     enabled: "Enabled"
   }
   ```

5. `cd dashboard && bun install && VITE_BASE_API=/ bun run build`

Notes
-----
- The page only needs the caller's own data (`/api/my_hosts`), so no extra
  permission is required beyond `hosts.read` on the backend.
- Names/order/visibility apply to the admin's own subscription links and copied
  configurations only.
