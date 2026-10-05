class ErrorDominio(Exception):
    def __init__(self, mensaje: str, campo: str | None = None) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.campo = campo


class RecursoNoEncontradoError(ErrorDominio):
    pass


class RecursoDuplicadoError(ErrorDominio):
    pass


class ValidacionNegocioError(ErrorDominio):
    pass
