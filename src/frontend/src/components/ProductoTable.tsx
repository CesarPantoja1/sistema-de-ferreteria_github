import type { Producto } from '../types/catalogo'

interface ProductoTableProps {
  productos: Producto[]
  onVer: (id: number) => void
  onEditar: (producto: Producto) => void
  onDesactivar: (producto: Producto) => void
}

function formatearPrecio(valor: number): string {
  return valor.toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

export default function ProductoTable({
  productos,
  onVer,
  onEditar,
  onDesactivar,
}: ProductoTableProps) {
  if (productos.length === 0) {
    return (
      <div className="card p-10 text-center text-sm text-muted">
        No hay productos para mostrar.
      </div>
    )
  }

  return (
    <div className="card overflow-hidden">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b border-line text-muted">
            <th className="px-4 py-3 font-medium">Código</th>
            <th className="px-4 py-3 font-medium">Nombre</th>
            <th className="px-4 py-3 font-medium">Categoría</th>
            <th className="px-4 py-3 font-medium">Unidad</th>
            <th className="px-4 py-3 text-right font-medium">Precio venta</th>
            <th className="px-4 py-3 text-right font-medium">Umbral mín.</th>
            <th className="px-4 py-3 font-medium">Estado</th>
            <th className="px-4 py-3 text-right font-medium">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {productos.map((producto) => (
            <tr key={producto.id} className="border-b border-line last:border-b-0">
              <td className="px-4 py-3 font-mono text-xs">{producto.codigo}</td>
              <td className="px-4 py-3">{producto.nombre}</td>
              <td className="px-4 py-3 text-muted">{producto.categoria.nombre}</td>
              <td className="px-4 py-3 text-muted">{producto.unidad_medida.nombre}</td>
              <td className="px-4 py-3 text-right font-mono text-xs">
                {formatearPrecio(producto.precio_venta)}
              </td>
              <td className="px-4 py-3 text-right font-mono text-xs">
                {formatearPrecio(producto.umbral_stock_minimo)}
              </td>
              <td className="px-4 py-3">
                {producto.activo ? (
                  <span className="badge bg-[#EDF3EC] text-[#346538]">Activo</span>
                ) : (
                  <span className="badge bg-[#FDEBEC] text-[#9F2F2D]">Desactivado</span>
                )}
              </td>
              <td className="px-4 py-3">
                <div className="flex justify-end gap-1">
                  <button
                    type="button"
                    className="btn-ghost px-2 py-1 text-xs"
                    onClick={() => onVer(producto.id)}
                  >
                    Ver
                  </button>
                  <button
                    type="button"
                    className="btn-ghost px-2 py-1 text-xs"
                    onClick={() => onEditar(producto)}
                  >
                    Editar
                  </button>
                  <button
                    type="button"
                    className="btn-ghost px-2 py-1 text-xs"
                    disabled={!producto.activo}
                    onClick={() => onDesactivar(producto)}
                  >
                    Desactivar
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
