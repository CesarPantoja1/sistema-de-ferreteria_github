import { useEffect, useState } from 'react'

import { listarCategorias, listarUnidadesMedida } from '../api/catalogo'
import type { ApiError } from '../api/client'
import type { Categoria, Producto, ProductoCreate, UnidadMedida } from '../types/catalogo'

interface ProductoFormProps {
  valorInicial?: Producto
  onSubmit: (data: ProductoCreate) => Promise<void>
  onCancelar: () => void
}

interface FormState {
  codigo: string
  nombre: string
  categoria_id: string
  unidad_medida_id: string
  precio_compra: string
  precio_venta: string
  umbral_stock_minimo: string
}

function estadoInicial(valorInicial?: Producto): FormState {
  return {
    codigo: valorInicial?.codigo ?? '',
    nombre: valorInicial?.nombre ?? '',
    categoria_id: valorInicial ? String(valorInicial.categoria.id) : '',
    unidad_medida_id: valorInicial ? String(valorInicial.unidad_medida.id) : '',
    precio_compra: valorInicial ? String(valorInicial.precio_compra) : '',
    precio_venta: valorInicial ? String(valorInicial.precio_venta) : '',
    umbral_stock_minimo: valorInicial ? String(valorInicial.umbral_stock_minimo) : '',
  }
}

export default function ProductoForm({ valorInicial, onSubmit, onCancelar }: ProductoFormProps) {
  const [form, setForm] = useState<FormState>(estadoInicial(valorInicial))
  const [categorias, setCategorias] = useState<Categoria[]>([])
  const [unidades, setUnidades] = useState<UnidadMedida[]>([])
  const [errores, setErrores] = useState<Record<string, string>>({})
  const [errorGeneral, setErrorGeneral] = useState('')
  const [enviando, setEnviando] = useState(false)

  useEffect(() => {
    Promise.all([listarCategorias(), listarUnidadesMedida()])
      .then(([cats, unis]) => {
        setCategorias(cats)
        setUnidades(unis)
      })
      .catch((error: ApiError) => setErrorGeneral(error.message))
  }, [])

  function actualizar(campo: keyof FormState, valor: string) {
    setForm((actual) => ({ ...actual, [campo]: valor }))
  }

  function validar(): Record<string, string> {
    const nuevos: Record<string, string> = {}
    if (!form.codigo.trim()) nuevos.codigo = 'El código es obligatorio'
    if (!form.nombre.trim()) nuevos.nombre = 'El nombre es obligatorio'
    if (!form.categoria_id) nuevos.categoria_id = 'Seleccione una categoría'
    if (!form.unidad_medida_id) nuevos.unidad_medida_id = 'Seleccione una unidad de medida'
    for (const campo of ['precio_compra', 'precio_venta', 'umbral_stock_minimo'] as const) {
      const valor = Number(form[campo])
      if (form[campo] === '' || Number.isNaN(valor) || valor < 0) {
        nuevos[campo] = 'Debe ser un valor numérico mayor o igual a cero'
      }
    }
    return nuevos
  }

  async function manejarEnvio(evento: React.FormEvent) {
    evento.preventDefault()
    const validaciones = validar()
    setErrores(validaciones)
    setErrorGeneral('')
    if (Object.keys(validaciones).length > 0) return

    const payload: ProductoCreate = {
      codigo: form.codigo.trim(),
      nombre: form.nombre.trim(),
      categoria_id: Number(form.categoria_id),
      unidad_medida_id: Number(form.unidad_medida_id),
      precio_compra: Number(form.precio_compra),
      precio_venta: Number(form.precio_venta),
      umbral_stock_minimo: Number(form.umbral_stock_minimo),
    }

    setEnviando(true)
    try {
      await onSubmit(payload)
    } catch (error) {
      const apiError = error as ApiError
      if (apiError.campo) {
        setErrores({ [apiError.campo]: apiError.message })
      } else {
        setErrorGeneral(apiError.message)
      }
    } finally {
      setEnviando(false)
    }
  }

  const titulo = valorInicial ? 'Editar producto' : 'Nuevo producto'

  return (
    <form onSubmit={manejarEnvio} className="card space-y-5 p-6" noValidate>
      <h2 className="font-serif text-lg tracking-tightest">{titulo}</h2>

      {errorGeneral && (
        <p className="rounded-md bg-[#FDEBEC] px-3 py-2 text-sm text-[#9F2F2D]">{errorGeneral}</p>
      )}

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label className="label" htmlFor="codigo">
            Código
          </label>
          <input
            id="codigo"
            className="input"
            value={form.codigo}
            onChange={(e) => actualizar('codigo', e.target.value)}
          />
          {errores.codigo && <p className="mt-1 text-xs text-[#9F2F2D]">{errores.codigo}</p>}
        </div>
        <div>
          <label className="label" htmlFor="nombre">
            Nombre
          </label>
          <input
            id="nombre"
            className="input"
            value={form.nombre}
            onChange={(e) => actualizar('nombre', e.target.value)}
          />
          {errores.nombre && <p className="mt-1 text-xs text-[#9F2F2D]">{errores.nombre}</p>}
        </div>
        <div>
          <label className="label" htmlFor="categoria_id">
            Categoría
          </label>
          <select
            id="categoria_id"
            className="input"
            value={form.categoria_id}
            onChange={(e) => actualizar('categoria_id', e.target.value)}
          >
            <option value="">Seleccione…</option>
            {categorias.map((categoria) => (
              <option key={categoria.id} value={categoria.id}>
                {categoria.nombre}
              </option>
            ))}
          </select>
          {errores.categoria_id && (
            <p className="mt-1 text-xs text-[#9F2F2D]">{errores.categoria_id}</p>
          )}
        </div>
        <div>
          <label className="label" htmlFor="unidad_medida_id">
            Unidad de medida
          </label>
          <select
            id="unidad_medida_id"
            className="input"
            value={form.unidad_medida_id}
            onChange={(e) => actualizar('unidad_medida_id', e.target.value)}
          >
            <option value="">Seleccione…</option>
            {unidades.map((unidad) => (
              <option key={unidad.id} value={unidad.id}>
                {unidad.nombre}
              </option>
            ))}
          </select>
          {errores.unidad_medida_id && (
            <p className="mt-1 text-xs text-[#9F2F2D]">{errores.unidad_medida_id}</p>
          )}
        </div>
        <div>
          <label className="label" htmlFor="precio_compra">
            Precio de compra
          </label>
          <input
            id="precio_compra"
            type="number"
            min="0"
            step="0.01"
            className="input font-mono"
            value={form.precio_compra}
            onChange={(e) => actualizar('precio_compra', e.target.value)}
          />
          {errores.precio_compra && (
            <p className="mt-1 text-xs text-[#9F2F2D]">{errores.precio_compra}</p>
          )}
        </div>
        <div>
          <label className="label" htmlFor="precio_venta">
            Precio de venta
          </label>
          <input
            id="precio_venta"
            type="number"
            min="0"
            step="0.01"
            className="input font-mono"
            value={form.precio_venta}
            onChange={(e) => actualizar('precio_venta', e.target.value)}
          />
          {errores.precio_venta && (
            <p className="mt-1 text-xs text-[#9F2F2D]">{errores.precio_venta}</p>
          )}
        </div>
        <div>
          <label className="label" htmlFor="umbral_stock_minimo">
            Umbral de stock mínimo
          </label>
          <input
            id="umbral_stock_minimo"
            type="number"
            min="0"
            step="0.01"
            className="input font-mono"
            value={form.umbral_stock_minimo}
            onChange={(e) => actualizar('umbral_stock_minimo', e.target.value)}
          />
          {errores.umbral_stock_minimo && (
            <p className="mt-1 text-xs text-[#9F2F2D]">{errores.umbral_stock_minimo}</p>
          )}
        </div>
      </div>

      <div className="flex justify-end gap-2">
        <button type="button" className="btn-ghost" onClick={onCancelar} disabled={enviando}>
          Cancelar
        </button>
        <button type="submit" className="btn-primary" disabled={enviando}>
          {enviando ? 'Guardando…' : 'Guardar'}
        </button>
      </div>
    </form>
  )
}
