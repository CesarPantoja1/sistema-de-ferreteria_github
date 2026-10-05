src/
├── backend/
│   ├── pyproject.toml [Nuevo]
│   └── backend/
│       ├── __init__.py [Nuevo]
│       ├── main.py [Nuevo]
│       ├── database.py [Nuevo]
│       ├── catalogo/
│       │   ├── __init__.py [Nuevo]
│       │   ├── models.py [Nuevo]
│       │   ├── schemas.py [Nuevo]
│       │   ├── repositories.py [Nuevo]
│       │   ├── services.py [Nuevo]
│       │   └── routes.py [Nuevo]
│       └── shared/
│           ├── __init__.py [Nuevo]
│           └── errors.py [Nuevo]
└── frontend/
    ├── index.html [Nuevo]
    ├── package.json [Nuevo]
    ├── vite.config.ts [Nuevo]
    ├── tsconfig.json [Nuevo]
    ├── tailwind.config.js [Nuevo]
    ├── postcss.config.js [Nuevo]
    └── src/
        ├── main.tsx [Nuevo]
        ├── App.tsx [Nuevo]
        ├── index.css [Nuevo]
        ├── api/
        │   ├── client.ts [Nuevo]
        │   └── catalogo.ts [Nuevo]
        ├── types/
        │   └── catalogo.ts [Nuevo]
        ├── components/
        │   ├── Layout.tsx [Nuevo]
        │   ├── ProductoForm.tsx [Nuevo]
        │   ├── ProductoTable.tsx [Nuevo]
        │   ├── CategoriaManager.tsx [Nuevo]
        │   ├── UnidadMedidaManager.tsx [Nuevo]
        │   └── ConfirmDialog.tsx [Nuevo]
        └── pages/
            ├── ProductosPage.tsx [Nuevo]
            ├── ProductoDetallePage.tsx [Nuevo]
            └── ConfiguracionPage.tsx [Nuevo]