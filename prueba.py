import mysql.connector
import datetime as dt

config = {
    'user': 'postulante',
    'password': 'HB<tba!Sp6U2j5CN',
    'host': '54.219.2.160',
    'database': 'prueba_postulantes'
}


class Encuesta:
    def __init__(self, email, fecha, satisfeccion_general, conocia_empresa, recomendacion, recomendacion_abierta):
        self.email = email
        self.fecha = fecha
        self.satisfaccion_general = satisfeccion_general
        self.conocia_empresa = conocia_empresa
        self.recomendacion = recomendacion
        self.recomendacion_abierta = recomendacion_abierta

    def __repr__(self):
        return f"Encuesta(id={self.email}, satisfaccion='{self.satisfaccion_general}', fecha={self.fecha})"

    @property
    def fecha_date(self):
        return dt.datetime.strptime(self.fecha, '%Y-%m-%d %H:%M:%S')

    @property
    def conoce(self):
        if self.conocia_empresa == "Sí":
            return True
        elif self.conocia_empresa == "No":
            return False

    @property
    def satisfecho(self):
        if self.satisfaccion_general in (6, 7):
            return True
        return False

    @property
    def neutro(self):
        if self.satisfaccion_general == 5:
            return True
        return False

    @property
    def insatisfecho(self):
        if self.satisfaccion_general in (1, 2, 3, 4):
            return True
        return False


def sng_satisfaccion(encuestas: list[Encuesta]) -> float:
    satisfaccion = 0
    neutros = 0
    insatisfaccion = 0
    total = 0

    for enc in encuestas:
        total += 1
        if enc.satisfecho:
            satisfaccion += 1
        elif enc.neutro:
            neutros += 1
        elif enc.insatisfecho:
            insatisfaccion += 1

    sng = round((satisfaccion * 100)/total) - round((insatisfaccion * 100)/total)
    return sng


def sng_recomendacion(encuestas: list, atributo: str) -> float:
    """ Podria usar esta función para lograr lo mismo que arriba
    pero dejare el de properties porque puedes devolver una lista rapidamente"""
    satisfaccion = 0
    neutros = 0
    insatisfaccion = 0
    total = 0
    for enc in encuestas:
        val = getattr(enc, str(atributo))
        total += 1
        if val in (6, 7):
            satisfaccion += 1
        elif val == 5:
            neutros += 1
        elif val in (1, 2, 3, 4):
            insatisfaccion += 1

    sng = round((satisfaccion * 100) / total) - round((insatisfaccion * 100) / total)

    return sng


def total_conocia(encuestas: list[Encuesta]) -> int:
    total = 0
    for enc in encuestas:
        if enc.conoce:
            total += 1
    return total


def promedio_recomendacion(encuestas: list[Encuesta]) -> float:
    recomendaciones = [e.recomendacion for e in encuestas]
    if not recomendaciones:
        return 0
    return sum(recomendaciones) / len(recomendaciones)


def total_comentaron(encuestas: list[Encuesta]) -> int:
    """Se que repito el for y que cada metodo podria hacer con un solo for
    pero me gusta ver asi cada problema"""
    total = 0
    for enc in encuestas:
        if enc.recomendacion_abierta:
            total += 1
    return total


def duracion(encuestas: list[Encuesta]) -> dt.timedelta:
    fechas = [e.fecha_date for e in encuestas]
    minimo = min(fechas)
    maximo = max(fechas)
    dif = maximo - minimo
    # para ser mas exactos podria usar dateutils
    return dif


def consultar():
    # Conectar a la base de datos
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    # esta mal escrito ahi
    query = "SELECT email, fecha, satisfeccion_general, conocia_empresa, recomendacion, recomendacion_abierta FROM encuesta"

    cursor.execute(query)
    resultados = cursor.fetchall()
    objetos = [Encuesta(row['email'],
                        row['fecha'],
                        row['satisfeccion_general'],
                        row['conocia_empresa'],
                        row['recomendacion'],
                        row['recomendacion_abierta']
                        ) for row in resultados]

    cursor.close()
    connection.close()
    return objetos


def get_values(encuestas: list[Encuesta]):
    a = sng_satisfaccion(encuestas)
    b = total_conocia(encuestas)
    c = sng_recomendacion(encuestas, 'recomendacion')
    d = promedio_recomendacion(encuestas)
    e = total_comentaron(encuestas)
    f = duracion(encuestas)

    print(f"El SNG de satisfacción es {a} \n"
          f"Personas que conocian la empresa {b} \n"
          f"EL SNG de recomendacion es {c} \n"
          f"Nota Promedio de recomendaciones {d} \n"
          f"Comentarios {e} \n"
          f"la duracion ess de {f.days} dias, {round(f.seconds / 3600, 2)} horas \n")
    return {
        "sng_satisfaccion": a,
        "total_conocian": b,
        "sng_recomendacion": c,
        "promedio_recomendacion": d,
        "comentarios": e,
        "duracion": f
    }


if __name__ == "__main__":
    objetos = consultar()
    get_values(objetos)


