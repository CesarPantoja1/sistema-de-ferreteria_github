import { fireEvent, render, screen } from '@testing-library/react'

import type { Producto } from '../types/catalogo'
import ProductoTable from './ProductoTable'

const productoActivo: Producto = {
  id: 1,
  codigo: 'P-001',
  nombre: 'Tubo PVC 1/2',
  categoria: { id: 10, nombre: 'Plomería' },
  unidad_medida: { id: 20, nombre: 'Pieza' },
  precio_compra: 1.5,
  precio_venta: 2.5,
  umbral_stock_minimo: 5,
  activo: true,
}

const productoInactivo: Producto = {
  ...productoActivo,
  id: 2,
  codigo: 'P-002',
  nombre: 'Llave inglesa',
  activo: false,
}

describe('ProductoTable', () => {
  it('renderiza los datos anidados de categoría y unidad', () => {
    render(
      <ProductoTable
        productos={[productoActivo]}
        onVer={() => undefined}
        onEditar={() => undefined}
        onDesactivar={() => undefined}
      />,
    )
    expect(screen.getByText('Tubo PVC 1/2')).toBeTruthy()
    expect(screen.getByText('Plomería')).toBeTruthy()
    expect(screen.getByText('Pieza')).toBeTruthy()
    expect(screen.getByText('Activo')).toBeTruthy()
  })

  it('dispara los callbacks con el id y producto correctos', () => {
    const vistos: number[] = []
    const editados: Producto[] = []
    const desactivados: Producto[] = []
    render(
      <ProductoTable
        productos={[productoActivo]}
        onVer={(id) => vistos.push(id)}
        onEditar={(producto) => editados.push(producto)}
        onDesactivar={(producto) => desactivados.push(producto)}
      />,
    )

    fireEvent.click(screen.getByText('Ver'))
    expect(vistos).toEqual([1])

    fireEvent.click(screen.getByText('Editar'))
    expect(editados).toEqual([productoActivo])

    fireEvent.click(screen.getByText('Desactivar'))
    expect(desactivados).toEqual([productoActivo])
  })

  it('deshabilita desactivar para productos inactivos y muestra el badge', () => {
    render(
      <ProductoTable
        productos={[productoInactivo]}
        onVer={() => undefined}
        onEditar={() => undefined}
        onDesactivar={() => undefined}
      />,
    )
    const boton = screen.getByText('Desactivar') as HTMLButtonElement
    expect(boton.disabled).toBe(true)
    expect(screen.getByText('Desactivado')).toBeTruthy()
  })

  it('muestra estado vacío cuando no hay productos', () => {
    render(
      <ProductoTable
        productos={[]}
        onVer={() => undefined}
        onEditar={() => undefined}
        onDesactivar={() => undefined}
      />,
    )
    expect(screen.getByText('No hay productos para mostrar.')).toBeTruthy()
  })
})
