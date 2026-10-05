import { NavLink, Outlet } from 'react-router-dom'

const navItems = [
  { to: '/productos', label: 'Productos' },
  { to: '/configuracion', label: 'Configuración' },
]

export default function Layout() {
  return (
    <div className="min-h-screen bg-canvas">
      <header className="border-b border-line bg-canvas/80 backdrop-blur-sm">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-5">
          <NavLink to="/productos" className="flex items-baseline gap-3">
            <span className="font-serif text-xl italic tracking-tightest">Sistema de ferretería</span>
            <span className="hidden font-mono text-[11px] uppercase tracking-[0.14em] text-muted sm:inline">
              inventario
            </span>
          </NavLink>
          <nav className="flex items-center gap-1">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  [
                    'rounded-md px-3 py-1.5 text-sm transition-colors',
                    isActive ? 'bg-ink text-white' : 'text-muted hover:bg-bone hover:text-ink',
                  ].join(' ')
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-6 py-12">
        <Outlet />
      </main>
    </div>
  )
}
