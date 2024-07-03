from io import BytesIO
import datetime
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

#  from reportes import pdf_serializers as rps
from reportlab.pdfgen import canvas
import pandas as pd


def colr(x, y, z):
    return x/255, y/255, z/255


LIGHT_GRAY = colors.HexColor(0xadc8f9)
TRANSPARENT = colors.HexColor('#00FFFFFF')


class ShowElement:
    """Decorator class."""

    def __init__(self, space_after=1.0, space_before=0.0):
        """Instantiate the class."""
        self.spc_aft = space_after
        self.spc_bfr = space_before

    def __call__(self, func):
        """Calling the class."""
        def wrapper(cls, *args):
            """Wrapper function that decorates the function."""
            if self.spc_bfr > 0:
                cls.elements.append(Spacer(1, self.spc_bfr * cm))
            table = func(cls, *args)
            cls.elements.append(table)
            if self.spc_aft > 0:
                cls.elements.append(Spacer(1, self.spc_aft * cm))
        return wrapper


def custom_stylesheet():
    stylesheet = getSampleStyleSheet()
    stylesheet.add(
        ParagraphStyle(
            name='MyHeader',
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=10
        )
    )
    stylesheet.add(
        ParagraphStyle(
            name='DocumentFont',
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=10
        )
    )
    stylesheet.add(
        ParagraphStyle(
            name='Card',
            parent=stylesheet['Normal'],
            spaceBefore=10,
            fontSize=8,
        )
    )
    return stylesheet


class CompStyles:

    @classmethod
    def customs_sheet(cls):
        stylesheet = getSampleStyleSheet()
        stylesheet.add(
            ParagraphStyle(
                name='MyHeader',
                fontName='Helvetica-Bold',
                fontSize=16,
                leading=10
                )
            )

        stylesheet.add(
            ParagraphStyle(
                name='DocumentFont',
                fontName='Helvetica-Bold',
                fontSize=12,
                leading=10
                )
            )

        stylesheet.add(
            ParagraphStyle(
                name='Card',
                parent=stylesheet['Normal'],
                spaceBefore=10,
                fontSize=8,
                )
            )

        return stylesheet

    @classmethod
    def customs_table(cls):

        tb_style = dict()

        tb_style['basic_table'] = TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ])

        tb_style['middle_table'] = TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ])

        tb_style['bottom_table'] = TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ])

        tb_style['line_table'] = TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 0.7, colors.black),  # Add lines before each cell
            # ('LINEBELOW', (0, -1), (-1, -1), 0.7, colors.black)
            ],
            parent=tb_style['basic_table'])

        tb_style['asist_table'] = TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 0.7, colors.black),  # Add lines before each cell
            # ('LINEBELOW', (0, -1), (-1, -1), 0.7, colors.black)

            ],
            parent=tb_style['basic_table'])

        tb_style['mov_table'] = TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 0.7, colors.black),  # Add lines before each cell
            ('LINEABOVE', (0, 1), (-1, 1), 0.7, colors.black),
            # ('LINEBELOW', (0, -2), (-1, -1), 0.7, colors.black),  # Add lines before each cell
            ('LINEAFTER', (1, 1), (1, -1), 0.7, colors.black),
            ('LINEAFTER', (3, 1), (3, -1), 0.7, colors.black),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
            ],
            parent=tb_style['basic_table'])

        tb_style['finish_table'] = TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 0.7, colors.black),  # Add lines before each cell
            ('LINEAFTER', (1, 0), (1, 0), 0.7, colors.black),
            ('LINEAFTER', (3, 0), (3, 0), 0.7, colors.black),
            ('LINEBELOW', (0, -2), (-1, -1), 0.7, colors.black),  # Add lines before each cell
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('ALIGN', (5, 0), (5, -1), 'RIGHT'),
            ('SPAM', (0, 1), (-1, -1)),
            ],
            parent=tb_style['basic_table'])

        tb_style['background'] = TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BACKGROUND', (0, 0), (-1, -1), LIGHT_GRAY),
        ])

        tb_style['header_box'] = TableStyle([
                ('FONT', (0, 0), (-1, 1), 'Helvetica-Bold', 12),
                ('FONT', (0, 1), (-1, 1), 'Helvetica-Bold', 12),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#00FFFFFF')),
                ('BOX', (0, 0), (-1, -1), 1.2, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ],
            hAlign='RIGHT')

        tb_style['item_table'] = TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 0), (-1, 0), LIGHT_GRAY),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ])

        tb_style['item_table_curve'] = TableStyle(
                [('ROUNDEDCORNERS', (2, 2, 2, 2))],
                parent=tb_style['item_table'])

        tb_style['grid_table'] = [
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('FONTNAME', (0, 0), (-2, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, '#CFEAD4'),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ]

        tb_style['container'] = TableStyle([
                 ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                 ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),

        ])

        tb_style['company_logo'] = TableStyle([
                 ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                 ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                 ('BOX', (0, 0), (-2, 1), 0.5, colors.black),
                 ('LEFTPADDING', (1, 0), (-1, -1), 15),
        ])

        return tb_style


class PDFBase:

    def __init__(self):
        self.buffer = BytesIO()
        self.styles = CompStyles.customs_sheet()
        self.elements = []
        self.doc = None

    def draw_logo(self, lienzo, doc):
        lienzo.drawImage('pdf/logo.png',
                         doc.leftMargin,
                         doc.height + doc.bottomMargin + doc.topMargin - 40 - 0.5 * cm,
                         height=40, anchor='sw', preserveAspectRatio=True, mask=(0, 0, 0, 0))

    def draw_title(self, lienzo, doc):
        p = Paragraph(self.get_header_title(), self.styles['Title'])
        w, h = p.wrap(doc.width, doc.topMargin)
        p.drawOn(lienzo, doc.leftMargin, doc.height + doc.bottomMargin + doc.topMargin - h - 0.6 * cm)

    def get_margins(self):
        return {
            'left': 1 * cm,
            'right': 1 * cm,
            'top': 2 * cm,
            'bottom': 1 * cm,
        }

    def get_title(self):
        raise NotImplemented('Falta implementar get_title')

    def get_header_title(self):
        raise NotImplemented('Falta implementar get_header_title')

    def header(self):
        return 'HEADER'

    def generate(self):
        raise NotImplemented('Falta implementar generate')

    def build(self):
        margins = self.get_margins()
        self.doc = SimpleDocTemplate(self.buffer,
                                     pageSize=A4,
                                     leftMargin=margins['left'],
                                     rightMargin=margins['right'],
                                     topMargin=margins['top'],
                                     bottomMargin=margins['bottom'],
                                     title=self.get_title(),
                                     author='TGA')
        self.header()
        self.generate()
        self.doc.build(self.elements, onFirstPage=self.footer, onLaterPages=self.footer)
        self.buffer.seek(0)
        return self.buffer.read()

    def set_space_and_draw(self, tb, space):
        self.elements.append(tb)
        self.elements.append(Spacer(1, space * cm))

    def footer(self, lienzo, doc):
        return
