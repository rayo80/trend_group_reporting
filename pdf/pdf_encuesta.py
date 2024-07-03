from io import BytesIO

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, TableStyle, Image, Spacer, Paragraph
from reportlab.platypus.tables import Table

import matplotlib.pyplot as plt
from io import BytesIO

from pdf.pdf_common import PDFBase, CompStyles, ShowElement


def colr(x, y, z):
    return x/255, y/255, z/255


LIGHT_GRAY = colors.HexColor(0xadc8f9)
TRANSPARENT = colors.HexColor('#00FFFFFF')


class EncuestaPDF(PDFBase):
    def __init__(self, df, resumen, conclusiones="conclusion"):
        super().__init__()
        # sobrescribo la hoja de estilos para letra por defecto
        self.stysheet = CompStyles.customs_sheet()
        self.stytable = CompStyles.customs_table()
        self.df = df
        self.resumen = resumen
        self.conclusiones = conclusiones

    def get_header_title(self):
        return "ENCUESTA ANALIZADA CON CHAT-GTP"

    def get_title(self):
        return "ENCUESTA"

    @ShowElement(space_after=0, space_before=0)
    def indicadores(self):
        data = [
            ['INDICADORES', 'VALORES'],
            ['SNG SATISFACCION', self.resumen['sng_satisfaccion']],
            ['TOTAL_CONOCIAN', self.resumen['total_conocian']],
            ['SNG RECOMENDACION', self.resumen['sng_recomendacion']],
            ['PROMEDIO RECOMENDACION', self.resumen['promedio_recomendacion']],
            ['COMENTARIOS', self.resumen['comentarios']],
            ['DURACION ', self.resumen['duracion']],
        ]
        t = Table(data, colWidths=(8 * cm, 5 * cm))
        t.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), LIGHT_GRAY),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        self.elements.append(t)
        self.elements.append(Spacer(1, 0.5 * cm))

    @ShowElement(space_after=0.5, space_before=1)
    def grafico(self):
        buffer = BytesIO()
        frequencias = self.df['satisfaccion_general'].value_counts().sort_index()

        # Crear un gráfico de pastel
        labels = frequencias.index.tolist()
        sizes = frequencias.values.tolist()
        plt.figure(figsize=(6, 4))
        plt.pie(sizes, labels=labels)
        plt.axis("equal")
        plt.title("SATISFACCION")
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        imagen = Image(buffer, width=360, height=240)
        return imagen

    @ShowElement(space_after=1, space_before=1)
    def grafico2(self):
        buffer = BytesIO()
        frequencias = self.df['recomendacion'].value_counts().sort_index()

        plt.figure(figsize=(6, 4))
        plt.bar(frequencias.index, frequencias.values, color='skyblue')
        plt.xlabel('Puntajes')
        plt.ylabel('Frecuencia')
        plt.title("RECOMENDACION")
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.tight_layout()
        imagen = Image(buffer, width=360, height=240)
        return imagen

    @ShowElement(space_after=2.5, space_before=0)
    def items_table(self, df):
        """este podria ser un pdf item base que píntaria segun el query y el seriaslizer"""
        df = df.drop(columns=['fecha'])
        df = df.fillna('')
        df['recomendacion_abierta'] = df['recomendacion_abierta'].map(lambda x: Paragraph(str(x),
                                                                                          style=self.stysheet['Card']))
        df['sentimientos'] = df['sentimientos'].map(lambda x: Paragraph(str(x), style=self.stysheet['Card']))
        header = df.columns.values.tolist()
        header = [x.upper() for x in header]
        header[1] = header[1][:3]
        header[2] = header[2][:3]
        header[3] = header[3][:3]

        data = [header, *df.values.tolist()]

        itemstable = Table(data, repeatRows=1,
                           colWidths=(2.5 * cm, 0.7 * cm, 0.7 * cm, 0.7 * cm, '*', '*'))

        itemstable.setStyle(self.stytable['item_table_curve'])
        return itemstable

    @ShowElement(space_after=0, space_before=0)
    def add_conclusiones(self):
        self.conclusiones = (self.conclusiones.replace(":", ":<br/>").
                             replace("Conclusión:", "<br/>Conclusión:"))
        data = [
            ['CONCLUSIONES', ],
            [Paragraph(self.conclusiones, style=self.stysheet['Card'])],
        ]

        t = Table(data, colWidths=(15 * cm,))
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), LIGHT_GRAY),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        self.elements.append(t)

    def generate(self):
        self.indicadores()
        self.grafico()
        self.grafico2()
        self.items_table(self.df)
        self.add_conclusiones()

    def footer(self, canvas, doc):
        canvas.saveState()
        self.draw_logo(canvas, doc)
        self.draw_title(canvas, doc)
        canvas.restoreState()
