interface ConfirmDialogProps {
  abierto: boolean
  titulo: string
  mensaje: string
  onConfirmar: () => void
  onCancelar: () => void
}

export default function ConfirmDialog({
  abierto,
  titulo,
  mensaje,
  onConfirmar,
  onCancelar,
}: ConfirmDialogProps) {
  if (!abierto) return null

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-ink/20 px-4"
      role="dialog"
      aria-modal="true"
      aria-label={titulo}
    >
      <div className="w-full max-w-sm rounded-lg border border-line bg-surface p-6">
        <h2 className="font-serif text-lg tracking-tightest">{titulo}</h2>
        <p className="mt-3 text-sm text-muted">{mensaje}</p>
        <div className="mt-6 flex justify-end gap-2">
          <button type="button" className="btn-ghost" onClick={onCancelar}>
            Cancelar
          </button>
          <button type="button" className="btn-primary" onClick={onConfirmar}>
            Confirmar
          </button>
        </div>
      </div>
    </div>
  )
}
