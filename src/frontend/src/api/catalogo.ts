import { client } from './client'
import type {
  Categoria,
  CategoriaCreate,
  Producto,
  ProductoCreate,
  ProductoUpdate,
  UnidadMedida,
  UnidadMedidaCreate,
} from '../types/catalogo'

export async function listarProductos(soloActivos = true): Promise<Producto[]> {
  const { data } = await client.get<Producto[]>('/catalogo/productos', {
    params: { solo_activos: soloActivos },
  })
  return data
}

export async function obtenerProducto(id: number): Promise<Producto> {
  const { data } = await client.get<Producto>(`/catalogo/productos/${id}`)
  return data
}

export async function crearProducto(data: ProductoCreate): Promise<Producto> {
  const { data: creado } = await client.post<Producto>('/catalogo/productos', data)
  return creado
}

export async function editarProducto(id: number, data: ProductoUpdate): Promise<Producto> {
  const { data: actualizado } = await client.put<Producto>(`/catalogo/productos/${id}`, data)
  return actualizado
}

export async function desactivarProducto(id: number): Promise<Producto> {
  const { data: desactivado } = await client.patch<Producto>(
    `/catalogo/productos/${id}/desactivar`,
  )
  return desactivado
}

export async function listarCategorias(): Promise<Categoria[]> {
  const { data } = await client.get<Categoria[]>('/catalogo/categorias')
  return data
}

export async function crearCategoria(data: CategoriaCreate): Promise<Categoria> {
  const { data: creada } = await client.post<Categoria>('/catalogo/categorias', data)
  return creada
}

export async function editarCategoria(id: number, data: CategoriaCreate): Promise<Categoria> {
  const { data: actualizada } = await client.put<Categoria>(`/catalogo/categorias/${id}`, data)
  return actualizada
}

export async function listarUnidadesMedida(): Promise<UnidadMedida[]> {
  const { data } = await client.get<UnidadMedida[]>('/catalogo/unidades-medida')
  return data
}

export async function crearUnidadMedida(data: UnidadMedidaCreate): Promise<UnidadMedida> {
  const { data: creada } = await client.post<UnidadMedida>('/catalogo/unidades-medida', data)
  return creada
}

export async function editarUnidadMedida(
  id: number,
  data: UnidadMedidaCreate,
): Promise<UnidadMedida> {
  const { data: actualizada } = await client.put<UnidadMedida>(
    `/catalogo/unidades-medida/${id}`,
    data,
  )
  return actualizada
}
