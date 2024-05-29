import re
from typing import Callable

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.tableofcontents import TableOfContents

from nicebook.components.better_image import BetterImage
from nicebook.configs import Configs


class NiceBookTemplate(SimpleDocTemplate):

    calculate_page: Callable
    current_file:str
    configs: Configs

    toc: TableOfContents
    image_toc: TableOfContents

    img_index:int

    start_page_count_at_page:int

    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self.configs = kwargs.get("configs")
        self.start_page_count_at_page = None
        NiceBookTemplate.img_index = 0


    def register_toc(self, toc: TableOfContents):
        self.toc = toc

    def register_image_toc(self, toc: TableOfContents):
        self.image_toc = toc

    def afterFlowable(self, flowable: Flowable):
        self.check_flowable_for_toc(flowable)


    def add_paragraph_to_toc(self, p: Paragraph):
        text = p.getPlainText()
        style:str = p.style.name

        if not style.startswith("heading"):
            return

        if self.start_page_count_at_page == None:
            # if we want to start pagination on first header
            # we just found it
            # other use use de defined page number
            if self.configs.document.start_page_count_on_first_header:
                self.start_page_count_at_page = self.page
            else:
                self.start_page_count_at_page = self.configs.document.start_page_count_at_page

        level = int(style[-1])

        toc_configs = self.configs.document.toc
        if not toc_configs or toc_configs.depth < level:
            return

        # Add indentation
        text = " " * (level - 1) * 2 + text

        page = self.calculate_page_number(self.page)
        self.toc.notify('TOCEntry', (level - 1, text, page))

    def add_image_to_toc(self, img: BetterImage):
        page = self.calculate_page_number(self.page)

        # Code snippet images do not have legend
        if img.code_snippet:
            return

        self.image_toc.notify('TOCEntry', (2, img.process_legend(), page))


    def check_flowable_for_toc(self, flowable: Flowable):
        # This is used to process the ToCs
        # If the current flowable has a heading style or is an image we add it to the respective ToC
        #   If its in the allowed depth
        k = flowable.__class__.__name__

        if k == 'Paragraph':
            self.add_paragraph_to_toc(flowable)

        if k == 'BetterImage':
            self.add_image_to_toc(flowable)



    def on_first_page(self, canvas: canvas.Canvas, doc: "NiceBookTemplate"):
        # This is used only to process the background image
        # Everything else happens in process_title_page so we can use regular components instead of needing to draw on the canvas

        conf = self.configs.document.title_page

        if conf.cover_image:
            page_size = self.configs.document.get_page_size()
            canvas.drawImage(conf.cover_image, 0, 0, width=page_size[0], height=page_size[1])
        else:
            self.__process_background_image(canvas, doc)

        self.__process_header_and_footer(canvas, doc)

    def on_later_pages(self, canvas: canvas.Canvas, doc: "NiceBookTemplate"):
        self.__process_header_and_footer(canvas, doc)
        self.__process_background_image(canvas, doc)

    def __process_header_and_footer(self, canvas: canvas.Canvas, doc: "NiceBookTemplate"):

        def process(header: bool):
            page_number = doc.page
            even = page_number % 2 == 0
            page_number_var_regex = re.compile(r"\$\{\{page_number\}\}")

            header_or_footer = self.configs.document.header if header else self.configs.document.footer
            conf = header_or_footer.even if even else header_or_footer.odd

            if not conf.enabled:
                return

            if page_number < header_or_footer.start_at_page:
                return

            text = conf.text
            if page_number_var_regex.search(text):
                calculated_page_number = self.calculate_page_number(doc.page)

                # If -1 means that start_page_count_on_first_header is true
                # and we dind't get any title yet to start numbering
                # So we just leave it empty
                if calculated_page_number ==-1 or doc.page < self.start_page_count_at_page:
                    calculated_page_number=""

                text = page_number_var_regex.sub(str(calculated_page_number), text)

            canvas.saveState()
            canvas.setFont(conf.font,conf.font_size)
            canvas.setFillColor(conf.color)

            page_size = self.configs.document.get_page_size()

            y = (page_size[1] - conf.space_before * inch - conf.font_size) if header else  conf.space_after * inch

            if conf.alignment == "right":
                canvas.drawRightString(
                    x=(page_size[0] - (self.configs.document.margin.right * inch)),
                    y = y,
                    text = text
                )
            elif conf.alignment == "center":
                canvas.drawCentredString(
                    x = page_size[0] / 2,
                    y = y,
                    text = text
                )
            else:
                canvas.drawString(
                    x = self.configs.document.margin.left * inch,
                    y = y,
                    text = text
                )

            canvas.restoreState()

        process(True) # header
        process(False) # footer

    def __process_background_image(self, canvas: canvas.Canvas, doc: "NiceBookTemplate"):
        img = self.configs.document.background_image

        if img:
            page_size = self.configs.document.get_page_size()
            canvas.drawImage(img, 0, 0, width=page_size[0], height=page_size[1])


    def calculate_page_number(self, page: int):
        if self.start_page_count_at_page == None:
            return -1

        return page - self.start_page_count_at_page + 1


