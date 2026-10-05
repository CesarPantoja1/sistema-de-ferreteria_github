import { fireEvent, render, screen } from '@testing-library/react'

import ConfirmDialog from './ConfirmDialog'

describe('ConfirmDialog', () => {
  it('no renderiza nada cuando está cerrado', () => {
    render(
      <ConfirmDialog
        abierto={false}
        titulo="Desactivar producto"
        mensaje="¿Seguro?"
        onConfirmar={() => undefined}
        onCancelar={() => undefined}
      />,
    )
    expect(screen.queryByText('Desactivar producto')).toBeNull()
  })

  it('muestra título y mensaje cuando está abierto', () => {
    render(
      <ConfirmDialog
        abierto
        titulo="Desactivar producto"
        mensaje="Se conservará el historial"
        onConfirmar={() => undefined}
        onCancelar={() => undefined}
      />,
    )
    expect(screen.getByText('Desactivar producto')).toBeTruthy()
    expect(screen.getByText('Se conservará el historial')).toBeTruthy()
  })

  it('invoca onConfirmar y onCancelar desde los botones', () => {
    let confirmaciones = 0
    let cancelaciones = 0
    render(
      <ConfirmDialog
        abierto
        titulo="Desactivar"
        mensaje="¿Seguro?"
        onConfirmar={() => {
          confirmaciones += 1
        }}
        onCancelar={() => {
          cancelaciones += 1
        }}
      />,
    )

    fireEvent.click(screen.getByText('Confirmar'))
    expect(confirmaciones).toBe(1)

    fireEvent.click(screen.getByText('Cancelar'))
    expect(cancelaciones).toBe(1)
  })
})
