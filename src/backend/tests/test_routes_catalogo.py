def _crear_categoria(client, nombre="Plomería"):
    return client.post("/api/catalogo/categorias", json={"nombre": nombre})


def _crear_unidad(client, nombre="Pieza"):
    return client.post("/api/catalogo/unidades-medida", json={"nombre": nombre})


def _crear_producto(client, categoria_id, unidad_id, **overrides):
    payload = {
        "codigo": "P-001",
        "nombre": "Tubo PVC 1/2",
        "categoria_id": categoria_id,
        "unidad_medida_id": unidad_id,
        "precio_compra": 1.5,
        "precio_venta": 2.5,
        "umbral_stock_minimo": 5,
    }
    payload.update(overrides)
    return client.post("/api/catalogo/productos", json=payload)


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_listar_categorias_vacio(client):
    resp = client.get("/api/catalogo/categorias")
    assert resp.status_code == 200
    assert resp.json() == []


def test_crear_categoria_201(client):
    resp = _crear_categoria(client)
    assert resp.status_code == 201
    assert resp.json()["nombre"] == "Plomería"


def test_crear_categoria_duplicada_409(client):
    _crear_categoria(client)
    resp = _crear_categoria(client)
    assert resp.status_code == 409
    assert resp.json()["detail"]


def test_crear_categoria_nombre_vacio_422(client):
    resp = client.post("/api/catalogo/categorias", json={"nombre": ""})
    assert resp.status_code == 422


def test_editar_categoria(client):
    cat_id = _crear_categoria(client).json()["id"]
    resp = client.put(f"/api/catalogo/categorias/{cat_id}", json={"nombre": "Electricidad"})
    assert resp.status_code == 200
    assert resp.json()["nombre"] == "Electricidad"


def test_editar_categoria_inexistente_404(client):
    resp = client.put("/api/catalogo/categorias/999", json={"nombre": "X"})
    assert resp.status_code == 404


def test_flujo_completo_producto(client):
    cat = _crear_categoria(client).json()
    uni = _crear_unidad(client).json()

    creado = _crear_producto(client, cat["id"], uni["id"])
    assert creado.status_code == 201
    body = creado.json()
    assert body["activo"] is True
    assert body["categoria"]["nombre"] == "Plomería"
    assert body["unidad_medida"]["nombre"] == "Pieza"
    producto_id = body["id"]

    listado = client.get("/api/catalogo/productos?solo_activos=true")
    assert listado.status_code == 200
    assert len(listado.json()) == 1

    detalle = client.get(f"/api/catalogo/productos/{producto_id}")
    assert detalle.status_code == 200
    assert detalle.json()["codigo"] == "P-001"

    editado = client.put(f"/api/catalogo/productos/{producto_id}", json={"precio_venta": 9.99})
    assert editado.status_code == 200
    assert editado.json()["precio_venta"] == 9.99

    desactivado = client.patch(f"/api/catalogo/productos/{producto_id}/desactivar")
    assert desactivado.status_code == 200
    assert desactivado.json()["activo"] is False

    activos = client.get("/api/catalogo/productos?solo_activos=true").json()
    assert activos == []
    todos = client.get("/api/catalogo/productos?solo_activos=false").json()
    assert len(todos) == 1

    detalle_inactivo = client.get(f"/api/catalogo/productos/{producto_id}")
    assert detalle_inactivo.status_code == 200
    assert detalle_inactivo.json()["activo"] is False


def test_crear_producto_codigo_duplicado_409(client):
    cat = _crear_categoria(client).json()
    uni = _crear_unidad(client).json()
    _crear_producto(client, cat["id"], uni["id"])
    resp = _crear_producto(client, cat["id"], uni["id"], nombre="Otro")
    assert resp.status_code == 409


def test_crear_producto_datos_invalidos_422(client):
    cat = _crear_categoria(client).json()
    uni = _crear_unidad(client).json()
    resp = _crear_producto(client, cat["id"], uni["id"], precio_venta=-1)
    assert resp.status_code == 422


def test_crear_producto_categoria_inexistente_404(client):
    uni = _crear_unidad(client).json()
    resp = _crear_producto(client, 999, uni["id"])
    assert resp.status_code == 404


def test_obtener_producto_inexistente_404(client):
    assert client.get("/api/catalogo/productos/999").status_code == 404
