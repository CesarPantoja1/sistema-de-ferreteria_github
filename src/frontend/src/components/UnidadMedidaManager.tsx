import { useEffect, useState } from 'react'

import { crearUnidadMedida, editarUnidadMedida, listarUnidadesMedida } from '../api/catalogo'
import type { ApiError } from '../api/client'
import type { UnidadMedida } from '../types/catalogo'

export default function UnidadMedidaManager() {
  const [unidades, setUnidades] = useState<UnidadMedida[]>([])
  const [nuevo, setNuevo] = useState('')
  const [editandoId, setEditandoId] = useState<number | null>(null)
  const [nombreEdicion, setNombreEdicion] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    listarUnidadesMedida()
      .then(setUnidades)
      .catch((e: ApiError) => setError(e.message))
  }, [])

  async function manejarCreacion(evento: React.FormEvent) {
    evento.preventDefault()
    setError('')
    if (!nuevo.trim()) {
      setError('El nombre de la unidad de medida es obligatorio')
      return
    }
    try {
      const creada = await crearUnidadMedida({ nombre: nuevo.trim() })
      setUnidades((actual) => [...actual, creada])
      setNuevo('')
    } catch (e) {
      setError((e as ApiError).message)
    }
  }

  async function guardarEdicion(id: number) {
    setError('')
    if (!nombreEdicion.trim()) {
      setError('El nombre de la unidad de medida es obligatorio')
      return
    }
    try {
      const actualizada = await editarUnidadMedida(id, { nombre: nombreEdicion.trim() })
      setUnidades((actual) => actual.map((unidad) => (unidad.id === id ? actualizada : unidad)))
      setEditandoId(null)
      setNombreEdicion('')
    } catch (e) {
      setError((e as ApiError).message)
    }
  }

  return (
    <section className="card p-6">
      <h2 className="font-serif text-lg tracking-tightest">Unidades de medida</h2>
      <p className="mt-1 text-sm text-muted">Pieza, metro, kilo, caja y otras.</p>

      {error && (
        <p className="mt-4 rounded-md bg-[#FDEBEC] px-3 py-2 text-sm text-[#9F2F2D]">{error}</p>
      )}

      <form onSubmit={manejarCreacion} className="mt-5 flex gap-2">
        <input
          className="input"
          placeholder="Nueva unidad de medida"
          aria-label="Nueva unidad de medida"
          value={nuevo}
          onChange={(e) => setNuevo(e.target.value)}
        />
        <button type="submit" className="btn-primary shrink-0">
          Añadir
        </button>
      </form>

      <ul className="mt-5 divide-y divide-line border-t border-line">
        {unidades.map((unidad) => (
          <li key={unidad.id} className="flex items-center justify-between gap-3 py-3">
            {editandoId === unidad.id ? (
              <>
                <input
                  className="input"
                  aria-label="Editar unidad de medida"
                  value={nombreEdicion}
                  onChange={(e) => setNombreEdicion(e.target.value)}
                />
                <div className="flex shrink-0 gap-1">
                  <button
                    type="button"
                    className="btn-primary px-3 py-1 text-xs"
                    onClick={() => guardarEdicion(unidad.id)}
                  >
                    Guardar
                  </button>
                  <button
                    type="button"
                    className="btn-ghost px-3 py-1 text-xs"
                    onClick={() => setEditandoId(null)}
                  >
                    Cancelar
                  </button>
                </div>
              </>
            ) : (
              <>
                <span className="text-sm">{unidad.nombre}</span>
                <button
                  type="button"
                  className="btn-ghost px-3 py-1 text-xs"
                  onClick={() => {
                    setEditandoId(unidad.id)
                    setNombreEdicion(unidad.nombre)
                  }}
                >
                  Editar
                </button>
              </>
            )}
          </li>
        ))}
        {unidades.length === 0 && (
          <li className="py-3 text-sm text-muted">Aún no hay unidades configuradas.</li>
        )}
      </ul>
    </section>
  )
}
