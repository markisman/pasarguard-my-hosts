import PageHeader from '@/components/layout/page-header'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Switch } from '@/components/ui/switch'
import { Separator } from '@/components/ui/separator'
import { useQuery } from '@tanstack/react-query'
import { ArrowDown, ArrowUp, GripVertical, RotateCcw, Search } from 'lucide-react'
import { useMemo, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { toast } from 'sonner'

type MyHost = {
  host_id: number
  remark: string
  display_name: string | null
  sort_order: number | null
  override_disabled: boolean
  priority: number
}

async function fetchMyHosts(): Promise<MyHost[]> {
  const res = await fetch('/api/my_hosts', { credentials: 'include' })
  if (!res.ok) throw new Error('failed to load hosts')
  const data = await res.json()
  return data.hosts as MyHost[]
}

async function saveMyHosts(items: MyHost[]): Promise<void> {
  const res = await fetch('/api/my_hosts', {
    method: 'PUT',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      items: items.map(h => ({
        host_id: h.host_id,
        display_name: h.display_name || null,
        sort_order: h.sort_order,
        is_disabled: h.override_disabled,
      })),
    }),
  })
  if (!res.ok) throw new Error('failed to save hosts')
}

export default function MyHostsPage() {
  const { t } = useTranslation()
  const { data } = useQuery({ queryKey: ['my-hosts'], queryFn: fetchMyHosts })
  const [draft, setDraft] = useState<MyHost[] | null>(null)
  const [search, setSearch] = useState('')

  const hosts = useMemo(() => {
    const list = draft ?? data ?? []
    const q = search.trim().toLowerCase()
    const filtered = q ? list.filter(h => (h.display_name || h.remark).toLowerCase().includes(q)) : list
    return [...filtered].sort((a, b) => (a.sort_order ?? a.priority) - (b.sort_order ?? b.priority))
  }, [draft, data, search])

  const update = (items: MyHost[]) => setDraft(items)

  const move = (index: number, dir: -1 | 1) => {
    const list = [...hosts]
    const j = index + dir
    if (j < 0 || j >= list.length) return
    ;[list[index], list[j]] = [list[j], list[index]]
    list.forEach((h, i) => (h.sort_order = i))
    update(list)
  }

  const resetOrder = () => update(hosts.map(h => ({ ...h, sort_order: null })))
  const resetAll = () => update(hosts.map(h => ({ ...h, sort_order: null, display_name: null, override_disabled: false })))

  const save = async () => {
    try {
      await saveMyHosts(hosts)
      toast.success(t('myHosts.saved', { defaultValue: 'Saved' }))
      setDraft(null)
    } catch {
      toast.error('Save failed')
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title={t('myHosts.title', { defaultValue: 'My Hosts' })}
        description={t('myHosts.subtitle', { defaultValue: 'Change the server names and order shown to you. These changes only affect your account.' })}
      />
      <Separator />

      <div className="flex items-center gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-2 top-2.5 h-4 w-4 opacity-50" />
          <Input
            className="pl-8"
            placeholder={t('myHosts.search', { defaultValue: 'Search hosts' })}
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
        <Button variant="outline" onClick={resetOrder}>
          <ArrowUp className="mr-2 h-4 w-4" />
          {t('myHosts.resetOrder', { defaultValue: 'Reset order' })}
        </Button>
        <Button variant="outline" onClick={resetAll}>
          <RotateCcw className="mr-2 h-4 w-4" />
          {t('myHosts.resetAll', { defaultValue: 'Reset all' })}
        </Button>
        <Button onClick={save} disabled={!draft}>
          {t('myHosts.save', { defaultValue: 'Save' })}
        </Button>
      </div>

      <div className="flex flex-col gap-2">
        {hosts.map((h, i) => (
          <div key={h.host_id} className="flex items-center gap-2 rounded-lg border p-2">
            <GripVertical className="h-4 w-4 opacity-40" />
            <Input
              className="flex-1"
              value={h.display_name ?? ''}
              placeholder={h.remark}
              onChange={e => {
                const list = [...hosts]
                list[i] = { ...h, display_name: e.target.value }
                update(list)
              }}
            />
            <Button variant="outline" size="icon" onClick={() => move(i, -1)}>
              <ArrowUp className="h-4 w-4" />
            </Button>
            <Button variant="outline" size="icon" onClick={() => move(i, 1)}>
              <ArrowDown className="h-4 w-4" />
            </Button>
            <Switch
              checked={!h.override_disabled}
              onCheckedChange={v => {
                const list = [...hosts]
                list[i] = { ...h, override_disabled: !v }
                update(list)
              }}
            />
          </div>
        ))}
      </div>
    </div>
  )
}
