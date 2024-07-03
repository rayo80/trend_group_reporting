import prueba as pb
import api_gtp as gtp
import pandas as pd
from pdf.pdf_encuesta import EncuestaPDF

objetos = pb.consultar()
resumen = pb.get_values(objetos)
dic = [{'email': ob.email,
        'fecha': ob.fecha,
        'satisfaccion_general': ob.satisfaccion_general,
        'conocia_empresa': ob.conocia_empresa,
        'recomendacion': ob.recomendacion,
        'recomendacion_abierta': ob.recomendacion_abierta
        } for ob in objetos]

df = pd.DataFrame(dic,
                  columns=['email',
                           'fecha',
                           'satisfaccion_general',
                           'conocia_empresa',
                           'recomendacion',
                           'recomendacion_abierta']
                  )

"""esto solo ejecutable una vez...consume credito"""
df["sentimientos"] = None
df['sentimientos'] = df['recomendacion_abierta'].apply(gtp.devolver_analisis)
conclusiones = gtp.conclusion(df["recomendacion_abierta"].tolist())
df.to_csv('output.csv', index=False)
"""Si ya se almaceno en el csv usar esto"""
# df = pd.read_csv('output.csv')
pdf = EncuestaPDF(df, resumen, conclusiones)
output_filename = 'encuesta.pdf'

# Escribir los bytes en un archivo PDF
with open(output_filename, 'wb') as pdf_file:
    pdf_file.write(pdf.build())

