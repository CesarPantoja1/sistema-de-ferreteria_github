import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL ?? '/api'

export interface ApiError extends Error {
  campo?: string | null
}

export const client = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const data = error?.response?.data
    const apiError: ApiError = new Error(
      data?.detail ?? 'Ocurrió un error inesperado al comunicarse con el servidor',
    )
    apiError.campo = data?.campo ?? null
    return Promise.reject(apiError)
  },
)
