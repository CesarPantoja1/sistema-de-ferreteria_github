import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { obtenerProducto } from '../api/catalogo'
import type { ApiError } from '../api/client'
import type { Producto } from '../types/catalogo'

function formatearPrecio(valor: number): string {
  return valor.toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function Atributo({ etiqueta, valor }: { etiqueta: string; valor: string }) {
  return (
    <div className="border-b border-line py-4 last:border-b-0">
      <dt className="text-xs font-medium uppercase tracking-[0.08em] text-muted">{etiqueta}</dt>
      <dd className="mt-1 text-sm">{valor}</dd>
    </div>
  )
}

export default function ProductoDetallePage() {
  const { id } = useParams<{ id: string }>()
  const [producto, setProducto] = useState<Producto | null>(null)
  const [error, setError] = useState('')
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    setCargando(true)
    setError('')
    obtenerProducto(Number(id))
      .then(setProducto)
      .catch((e: ApiError) => setError(e.message))
      .finally(() => setCargando(false))
  }, [id])

  if (cargando) {
    return <p className="text-sm text-muted">Cargando producto…</p>
  }

  if (error || !producto) {
    return (
      <div className="card p-10 text-center">
        <h1 className="font-serif text-2xl tracking-tightest">Producto no encontrado</h1>
        <p className="mt-2 text-sm text-muted">
          {error || 'El producto solicitado no existe en el catálogo.'}
        </p>
        <Link to="/productos" className="btn-ghost mt-6 inline-flex">
          Volver a productos
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.14em] text-muted">
            {producto.codigo}
          </p>
          <h1 className="mt-1 font-serif text-3xl tracking-tightest">{producto.nombre}</h1>
        </div>
        <div className="flex items-center gap-3">
          {producto.activo ? (
            <span className="badge bg-[#EDF3EC] text-[#346538]">Activo</span>
          ) : (
            <span className="badge bg-[#FDEBEC] text-[#9F2F2D]">Desactivado</span>
          )}
          <Link to="/productos" className="btn-ghost">
            Volver
          </Link>
        </div>
      </div>

      <div className="card px-6 py-2">
        <dl>
          <Atributo etiqueta="Categoría" valor={producto.categoria.nombre} />
          <Atributo etiqueta="Unidad de medida" valor={producto.unidad_medida.nombre} />
          <Atributo
            etiqueta="Precio de compra"
            valor={formatearPrecio(producto.precio_compra)}
          />
          <Atributo etiqueta="Precio de venta" valor={formatearPrecio(producto.precio_venta)} />
          <Atributo
            etiqueta="Umbral de stock mínimo"
            valor={formatearPrecio(producto.umbral_stock_minimo)}
          />
        </dl>
      </div>
    </div>
  )
}
