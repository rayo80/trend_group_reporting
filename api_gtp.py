from openai import OpenAI
import os
# Configura tu clave API
apikey = 'ESCRIBETUCLAVEAQUI'
os.environ['OPENAI_API_KEY'] = apikey

# for clave, valor in os.environ.items():
#     print(f'{clave}: {valor}')
client = OpenAI()

# Configura tu clave API
# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "user", "content": "Análisis de sentimiento para: "
#                                 "Por la pesima experiencia, en la creacion de el condominio, "
#                                 "minimo deberiamos tener estacionamiento de visitas"},
#     {"role": "user", "content": "Problemas principales y conclusión de lo anterior"}
#   ]
# )
#
# print(completion.choices[0].message)
# print(completion.choices[0].message)


def devolver_analisis(comentario):
    if comentario:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Análisa el sentimiento para el siguiente comentario y "
                                            "dime en general que refleja: "
                                            + comentario},
            ]
        )

        return completion.choices[0].message.content
    return None


def conclusion(comentarios: list):
    comentarios_filtrados = [c for c in comentarios if c is not None]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Problemas principales y conclusion de: -" + "-".join(comentarios_filtrados)},
        ]
    )
    print("conclusiones", completion.choices[0].message.content)
    return completion.choices[0].message.content
