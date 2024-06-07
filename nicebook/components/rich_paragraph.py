import logging
from html import escape

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

from nicebook.configs import Configs
from nicebook.reference_manager import ReferenceManager
from nicebook.styler import Styler


# https://docs.reportlab.com/reportlab/userguide/ch6_paragraphs/#the-outermost-para-tag
class RichParagraph():

    styler: Styler
    styler_warning: bool = False

    def __init__(self, text="", extra_info: dict = None):
        self.text = self.sanitize(text)
        self.extra_info = extra_info


    def add_text(self, text):
        self.text = self.text + self.sanitize(text)


    def add_link(self, link, text, reference_manager: ReferenceManager):
        ##
        # an instance of ReferenceManager is required in case its an internal link

        text = self.sanitize(text)
        style = self.__get_styler().configs.document.links

        if self.styler.configs.document.links.underline:
            text = f"<u>{text}</u>"

        if "://" in link:
            self.text = self.text + f"<a href='{link}' color='{style.color}'>{text}</a>"
        else:
            self.text = self.text + reference_manager.generate_referencing_link(reference_manager.current_file, link, text)

    # def add_checkbox(self, checked: bool):
    #     c = "☑" if checked else "☐"
    #     self.text = self.text + f"""<span fontname='Roboto-Regular'>{c}</span>"""

    def add_bold_text(self, text):
        text = self.sanitize(text)
        self.text = self.text + f"<b>{text}</b>"

    def add_italic_text(self, text):
        text = self.sanitize(text)
        self.text = self.text + f"<i>{text}</i>"

    def add_underline_text(self, text):
        text = self.sanitize(text)
        self.text = self.text + f"<u>{text}</u>"

    def add_strikethrough_text(self, text):
        text = self.sanitize(text)
        self.text = self.text + f"<strike>{text}</strike>"

    def add_bold_italic_text(self, text):
        text = self.sanitize(text)
        self.text = self.text + f"<b><i>{text}</i></b>"

    def add_superscript(self, text):
        text = self.sanitize(text)
        self.text = self.text + f"<sup>{text}</sup>"

    def add_subscript_text(self, text):
        text = self.sanitize(text)
        self.text = self.text + f"<sub>{text}</sub>"

    def add_code_text(self, code):
        #code = self.escape(code)
        code_style = self.__get_styler().configs.document.code


        self.text = self.text + f"""<span
            backColor='{code_style.background_color}'
            fontSize='{code_style.font_size}'
            fontname='{code_style.font}'
            color='{code_style.color}'
            >
                <pre>{code}</pre>
            </span>"""


    def add_new_line(self):
        self.text = self.text + "\n"

    # def add_raw_text_unsafe(self, text):
    #     """
    #     Every other method applies sanitization to prevent html injection.
    #     This method won't. Be careful
    #     It can be used in case you need more control of the content, you can inject RML tags directly through here
    #     """
    #     self.text = self.text + text


    def __get_styler(self):
        if not RichParagraph.styler and not RichParagraph.styler_warning:
            logging.warning("Styler not set, creating styler with default configs. To fix this do RichParagraph.styler = Styler(configs) before using RichParagraph.")
            RichParagraph.styler_warning = True
            RichParagraph.styler = Styler(Configs())

        return RichParagraph.styler

    def process(self):
        if not self.extra_info:
            self.extra_info = {}

        is_block_quote = self.extra_info.get("quote", False) == True
        style = None

        if is_block_quote:
            s:ParagraphStyle = self.__get_styler().stylesheet['Blockquote']
            style = s
        else:
            style = self.extra_info.get("style", None)

        return Paragraph(self.text, style, encoding="unicode")



    def sanitize(self, text):
        # TODO
        # reportlab has its paid library to do this...
        # Basically it convers html to safe RML (the language they use to generate pdfs)

        #return escape(text)
        return text
        #return f"<![CDATA[{text}]]>" # breaks inline code
