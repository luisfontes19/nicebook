import os

from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import TableStyle

from nicebook.configs import Configs, Heading


class Styler:
    configs: Configs
    stylesheet: StyleSheet1
    table_style: TableStyle

    def __init__(self, configs: Configs):
        self.configs = configs
        self.stylesheet = StyleSheet1()
        self.generate_styles()

    def generate_styles(self):
        self.__body_styles()
        self.__title_page_styles()
        self.__headings_styles()
        self.__toc_styles()
        self.__code_styles()
        self.__link_styles()
        self.__blockquote_styles()
        self.__image_styles()
        self.__table_style()
        self.__load_fonts()

    @staticmethod
    def __convert_alignment(alignment: str) -> int:
        if alignment == "left":
            return 0
        elif alignment == "center":
            return 1
        elif alignment == "right":
            return 2
        elif alignment == "justify":
            return 4
        else:
            return 0

    def register_font(self, font_path: str):
        name = os.path.basename(font_path).replace(".ttf", "")
        pdfmetrics.registerFont(TTFont(name, font_path))
        pdfmetrics.registerFontFamily(name, normal=name, bold=name, italic=name, boldItalic=name)

    def __load_fonts(self):
        # # We keep and inject roboto so we can use unicode chars like checkboxes
        # p = os.path.join(os.path.dirname(__file__), "bin",  "Roboto-Regular.ttf")
        # self.register_font(p)

        for f in self.configs.document.fonts:
           self.register_font(f)



    def __image_styles(self):
        image = self.configs.document.images
        default_font_size = self.configs.document.body.font_size

        self.stylesheet.add(ParagraphStyle(name='ImageLegend',
            parent=self.stylesheet['BodyText'],
            fontSize=default_font_size - 4,
            alignment=Styler.__convert_alignment("center"),

        ))

    def __body_styles(self,):
        body = self.configs.document.body

        self.stylesheet.add(ParagraphStyle(name='Normal',
            fontName=body.font,
            fontSize=body.font_size,
            leading=body.leading,
            alignment=Styler.__convert_alignment(body.alignment),
            spaceBefore=body.space_before * inch,
            spaceAfter=body.space_after * inch,
            textColor=HexColor(body.color)
            )
        )

        self.stylesheet.add(ParagraphStyle(name='BodyText',
            parent=self.stylesheet['Normal'])
        )

    def __title_page_styles(self):
        title = self.configs.document.title_page.title
        self.stylesheet.add(ParagraphStyle(name='TitlePageTitle',
            parent=self.stylesheet['Normal'],
            fontName=title.font,
            fontSize=title.font_size,
            leading=title.leading,
            alignment=Styler.__convert_alignment(title.alignment),
            spaceBefore=title.space_before * inch,
            spaceAfter=title.space_after * inch,
            textColor=HexColor(title.color))
        )

        subject = self.configs.document.title_page.subject
        self.stylesheet.add(ParagraphStyle(name='TitlePageSubject',
            parent=self.stylesheet['Normal'],
            fontName=subject.font,
            fontSize=subject.font_size,
            leading=subject.leading,
            alignment=Styler.__convert_alignment(subject.alignment),
            spaceBefore=subject.space_before * inch,
            spaceAfter=subject.space_after * inch,
            textColor=HexColor(subject.color))
        )


        author = self.configs.document.title_page.author
        self.stylesheet.add(ParagraphStyle(name='TitlePageAuthor',
            parent=self.stylesheet['Normal'],
            fontName=author.font,
            fontSize=author.font_size,
            leading=author.leading,
            alignment=Styler.__convert_alignment(author.alignment),
            spaceBefore=author.space_before * inch,
            spaceAfter=author.space_after * inch,
            textColor=HexColor(author.color))
        )

    def __headings_styles(self):
        for i in range(1,7):
            heading:Heading = getattr(self.configs.document, f"heading{i}")

            self.stylesheet.add(ParagraphStyle(name=f'heading{i}',
                parent=self.stylesheet['Normal'],
                fontName = heading.font,
                fontSize=heading.font_size,
                leading=heading.leading,
                spaceAfter=heading.space_after * inch,
                spaceBefore=heading.space_before * inch,
                alignment=Styler.__convert_alignment(heading.alignment),
                textColor=HexColor(heading.color))

            )


    def __toc_styles(self):

        # These are used for the identation
        # TODO: allow customization of this style
        for i in range(1,7):
            self.stylesheet.add(ParagraphStyle(name=f'TOCLevel{i}',
                parent=self.stylesheet['BodyText'],
                leftIndent=self.configs.document.toc.indentation * inch * (i-1),)
            )

        toc = self.configs.document.toc
        self.stylesheet.add(ParagraphStyle(name=f'TOCHeading',
            parent=self.stylesheet['Normal'],
            fontName = toc.heading_font + '-Bold',
            fontSize=toc.heading_font_size,
            leading=toc.leading,
            textColor=HexColor(toc.heading_color))
        )


        # IMAGE TOC
        # These are used for the identation
        # TODO: allow customization of this style
        for i in range(1,7):
            self.stylesheet.add(ParagraphStyle(name=f'ImageTOCLevel{i}',
                parent=self.stylesheet['BodyText'],
                leftIndent=self.configs.document.images.list_of_figures.indentation * inch * (i-1),)
            )

        lof = self.configs.document.images.list_of_figures
        self.stylesheet.add(ParagraphStyle(name=f'ImageTOCHeading',
            parent=self.stylesheet['Normal'],
            fontName = lof.heading_font + '-Bold',
            fontSize=lof.heading_font_size,
            leading=lof.leading,
            textColor=HexColor(lof.heading_color))
        )

    def __code_styles(self):
        code = self.configs.document.code
        self.stylesheet.add(ParagraphStyle(name='Code',
            parent=self.stylesheet['Normal'],
            fontName=code.font,
            fontSize=code.font_size,
            textColor=HexColor(code.color))

        )

    def __link_styles(self):
        links = self.configs.document.links
        self.stylesheet.add(ParagraphStyle(name='link',
            textColor=HexColor(links.color),
            underline=links.underline, # TODO: check why this is not working
            underlineColor=HexColor(links.color))

        )

    def __blockquote_styles(self):
        self.stylesheet.add(ParagraphStyle(name='Blockquote',
            parent=self.stylesheet['Normal'],
            leftIndent=20,
            rightIndent=20,
            textColor="gray",
            spaceAfter=0.2 * inch,
        ))


    def __table_style(self):
        table_configs = self.configs.document.tables
        header_configs = table_configs.header

        style = [
            # header
            ('ALIGN', (0, 0), (-1, 0), table_configs.text_alignment.upper()),
            ('FONTNAME', (0, 0), (-1, 0), header_configs.font),
            ('BACKGROUND', (0, 0), (-1, 0),header_configs.background_color ),

            # Rest
            ('ALIGN', (1, 0), (-1, 0), header_configs.text_alignment.upper()),

        ]

        if table_configs.style == "grid":
            style.append(('GRID', (0, 0), (-1, -1), 1, table_configs.grid_color))
        elif table_configs.style == "grid_inner":
            style.append(('INNERGRID', (0,0), (-1,-1), 1, table_configs.inner_grid_color),)
        else:
            style.append(('LINEABOVE', (0,0), (-1,0), 2, table_configs.border_color))
            style.append(('LINEABOVE', (0,1), (-1,-1), 0.25, table_configs.border_color))
            style.append(('LINEBELOW', (0,-1), (-1,-1), 2, table_configs.border_color))

        self.table_style = TableStyle(style)
        return self.table_style
