import { useEffect, useState } from 'react'

import { crearCategoria, editarCategoria, listarCategorias } from '../api/catalogo'
import type { ApiError } from '../api/client'
import type { Categoria } from '../types/catalogo'

export default function CategoriaManager() {
  const [categorias, setCategorias] = useState<Categoria[]>([])
  const [nuevo, setNuevo] = useState('')
  const [editandoId, setEditandoId] = useState<number | null>(null)
  const [nombreEdicion, setNombreEdicion] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    listarCategorias()
      .then(setCategorias)
      .catch((e: ApiError) => setError(e.message))
  }, [])

  async function manejarCreacion(evento: React.FormEvent) {
    evento.preventDefault()
    setError('')
    if (!nuevo.trim()) {
      setError('El nombre de la categoría es obligatorio')
      return
    }
    try {
      const creada = await crearCategoria({ nombre: nuevo.trim() })
      setCategorias((actual) => [...actual, creada])
      setNuevo('')
    } catch (e) {
      setError((e as ApiError).message)
    }
  }

  async function guardarEdicion(id: number) {
    setError('')
    if (!nombreEdicion.trim()) {
      setError('El nombre de la categoría es obligatorio')
      return
    }
    try {
      const actualizada = await editarCategoria(id, { nombre: nombreEdicion.trim() })
      setCategorias((actual) =>
        actual.map((categoria) => (categoria.id === id ? actualizada : categoria)),
      )
      setEditandoId(null)
      setNombreEdicion('')
    } catch (e) {
      setError((e as ApiError).message)
    }
  }

  return (
    <section className="card p-6">
      <h2 className="font-serif text-lg tracking-tightest">Categorías</h2>
      <p className="mt-1 text-sm text-muted">Clasificaciones propias del rubro.</p>

      {error && (
        <p className="mt-4 rounded-md bg-[#FDEBEC] px-3 py-2 text-sm text-[#9F2F2D]">{error}</p>
      )}

      <form onSubmit={manejarCreacion} className="mt-5 flex gap-2">
        <input
          className="input"
          placeholder="Nueva categoría"
          aria-label="Nueva categoría"
          value={nuevo}
          onChange={(e) => setNuevo(e.target.value)}
        />
        <button type="submit" className="btn-primary shrink-0">
          Añadir
        </button>
      </form>

      <ul className="mt-5 divide-y divide-line border-t border-line">
        {categorias.map((categoria) => (
          <li key={categoria.id} className="flex items-center justify-between gap-3 py-3">
            {editandoId === categoria.id ? (
              <>
                <input
                  className="input"
                  aria-label="Editar categoría"
                  value={nombreEdicion}
                  onChange={(e) => setNombreEdicion(e.target.value)}
                />
                <div className="flex shrink-0 gap-1">
                  <button
                    type="button"
                    className="btn-primary px-3 py-1 text-xs"
                    onClick={() => guardarEdicion(categoria.id)}
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
                <span className="text-sm">{categoria.nombre}</span>
                <button
                  type="button"
                  className="btn-ghost px-3 py-1 text-xs"
                  onClick={() => {
                    setEditandoId(categoria.id)
                    setNombreEdicion(categoria.nombre)
                  }}
                >
                  Editar
                </button>
              </>
            )}
          </li>
        ))}
        {categorias.length === 0 && (
          <li className="py-3 text-sm text-muted">Aún no hay categorías configuradas.</li>
        )}
      </ul>
    </section>
  )
}
