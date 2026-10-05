import CategoriaManager from '../components/CategoriaManager'
import UnidadMedidaManager from '../components/UnidadMedidaManager'

export default function ConfiguracionPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-serif text-3xl tracking-tightest">Configuración del rubro</h1>
        <p className="mt-1 text-sm text-muted">
          Categorías y unidades de medida disponibles al registrar o editar productos.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <CategoriaManager />
        <UnidadMedidaManager />
      </div>
    </div>
  )
}
