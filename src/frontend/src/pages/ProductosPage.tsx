import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { crearProducto, desactivarProducto, editarProducto, listarProductos } from '../api/catalogo'
import type { ApiError } from '../api/client'
import ConfirmDialog from '../components/ConfirmDialog'
import ProductoForm from '../components/ProductoForm'
import ProductoTable from '../components/ProductoTable'
import type { Producto, ProductoCreate } from '../types/catalogo'

export default function ProductosPage() {
  const navigate = useNavigate()
  const [productos, setProductos] = useState<Producto[]>([])
  const [soloActivos, setSoloActivos] = useState(true)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')
  const [formAbierto, setFormAbierto] = useState(false)
  const [productoEditando, setProductoEditando] = useState<Producto | undefined>(undefined)
  const [productoADesactivar, setProductoADesactivar] = useState<Producto | null>(null)

  async function cargar() {
    setCargando(true)
    setError('')
    try {
      setProductos(await listarProductos(soloActivos))
    } catch (e) {
      setError((e as ApiError).message)
    } finally {
      setCargando(false)
    }
  }

  useEffect(() => {
    void cargar()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [soloActivos])

  async function manejarSubmit(data: ProductoCreate) {
    if (productoEditando) {
      await editarProducto(productoEditando.id, data)
    } else {
      await crearProducto(data)
    }
    setFormAbierto(false)
    setProductoEditando(undefined)
    await cargar()
  }

  async function confirmarDesactivacion() {
    if (!productoADesactivar) return
    try {
      await desactivarProducto(productoADesactivar.id)
      setProductoADesactivar(null)
      await cargar()
    } catch (e) {
      setError((e as ApiError).message)
      setProductoADesactivar(null)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-serif text-3xl tracking-tightest">Productos</h1>
          <p className="mt-1 text-sm text-muted">
            Definición canónica del catálogo de la ferretería.
          </p>
        </div>
        <div className="flex items-center gap-4">
          <label className="flex items-center gap-2 text-sm text-muted">
            <input
              type="checkbox"
              checked={!soloActivos}
              onChange={(e) => setSoloActivos(!e.target.checked)}
            />
            Mostrar desactivados
          </label>
          <button
            type="button"
            className="btn-primary"
            onClick={() => {
              setProductoEditando(undefined)
              setFormAbierto(true)
            }}
          >
            Nuevo producto
          </button>
        </div>
      </div>

      {error && (
        <p className="rounded-md bg-[#FDEBEC] px-3 py-2 text-sm text-[#9F2F2D]">{error}</p>
      )}

      {formAbierto && (
        <ProductoForm
          valorInicial={productoEditando}
          onSubmit={manejarSubmit}
          onCancelar={() => {
            setFormAbierto(false)
            setProductoEditando(undefined)
          }}
        />
      )}

      {cargando ? (
        <p className="text-sm text-muted">Cargando productos…</p>
      ) : (
        <ProductoTable
          productos={productos}
          onVer={(id) => navigate(`/productos/${id}`)}
          onEditar={(producto) => {
            setProductoEditando(producto)
            setFormAbierto(true)
          }}
          onDesactivar={(producto) => setProductoADesactivar(producto)}
        />
      )}

      <ConfirmDialog
        abierto={productoADesactivar !== null}
        titulo="Desactivar producto"
        mensaje={
          productoADesactivar
            ? `¿Desea desactivar "${productoADesactivar.nombre}"? Su historial se conservará.`
            : ''
        }
        onConfirmar={confirmarDesactivacion}
        onCancelar={() => setProductoADesactivar(null)}
      />
    </div>
  )
}
