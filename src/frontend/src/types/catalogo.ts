export interface Categoria {
  id: number
  nombre: string
}

export interface UnidadMedida {
  id: number
  nombre: string
}

export interface Producto {
  id: number
  codigo: string
  nombre: string
  categoria: Categoria
  unidad_medida: UnidadMedida
  precio_compra: number
  precio_venta: number
  umbral_stock_minimo: number
  activo: boolean
}

export interface CategoriaCreate {
  nombre: string
}

export interface UnidadMedidaCreate {
  nombre: string
}

export interface ProductoCreate {
  codigo: string
  nombre: string
  categoria_id: number
  unidad_medida_id: number
  precio_compra: number
  precio_venta: number
  umbral_stock_minimo: number
}

export type ProductoUpdate = Partial<ProductoCreate>
