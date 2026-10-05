import { Navigate, Route, Routes } from 'react-router-dom'

import Layout from './components/Layout'
import ConfiguracionPage from './pages/ConfiguracionPage'
import ProductoDetallePage from './pages/ProductoDetallePage'
import ProductosPage from './pages/ProductosPage'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Navigate to="/productos" replace />} />
        <Route path="/productos" element={<ProductosPage />} />
        <Route path="/productos/:id" element={<ProductoDetallePage />} />
        <Route path="/configuracion" element={<ConfiguracionPage />} />
        <Route path="*" element={<Navigate to="/productos" replace />} />
      </Route>
    </Routes>
  )
}
