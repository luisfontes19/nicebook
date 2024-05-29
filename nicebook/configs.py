import logging
import re
from typing import Literal

import yaml

Font = Literal['Courier', 'Courier-Bold', 'Courier-Oblique', 'Courier-BoldOblique', 'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 'Helvetica-BoldOblique', 'Times-Roman', 'Times-Bold', 'Times-Italic', 'Times-BoldItalic', 'Symbol','ZapfDingbats']
Alignment = Literal["left", "center", "right", "justify"]

class Metadata:

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)


class TextBasics:
    font_size: float
    font: Font
    leading: float
    alignment: Alignment
    space_before: float
    space_after: float
    color: str


    def __init__(self, **kwargs):
        self.font = kwargs.get("font", "Helvetica")
        self.font_size = kwargs.get("font_size", 10)
        self.leading = kwargs.get("leading", self.font_size * 1.2)
        self.alignment = kwargs.get("alignment", "left").lower()
        self.space_before = kwargs.get("space_before", 0)
        self.space_after = kwargs.get("space_after", 0)
        self.color = kwargs.get("color", "#000000")

class HeaderFooterSide(TextBasics):
    enabled: bool
    text: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enabled = kwargs.get("enabled", True)
        self.text = kwargs.get("text", "")
        self.color="#AAAAAA"

class HeaderFooter:
    odd: HeaderFooterSide
    even: HeaderFooterSide
    all: HeaderFooterSide
    start_at_page: int

    def __init__(self, **kwargs):
        self.all = HeaderFooterSide(**kwargs.get("all", {}))
        self.odd = HeaderFooterSide(**kwargs.get("all", {}))
        self.even = HeaderFooterSide(**kwargs.get("all", {}))

        keys = ["odd", "even"]

        for key in keys:
            obj = getattr(self, key)
            odd = kwargs.get(key, {})
            for key in odd.keys():
                setattr(obj, key, odd[key])

        self.start_at_page = kwargs.get("start_at_page", 2)



class Body(TextBasics):
    font: Font
    font_size: float
    leading: float
    space_before: float
    alignment: Alignment

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Margin:
    top: float
    bottom: float
    left: float
    right: float

    def __init__(self, **kwargs):
        self.top = kwargs.get("top", 1)
        self.bottom = kwargs.get("bottom", 1)
        self.left = kwargs.get("left", 1)
        self.right = kwargs.get("right", 1)

class Heading(TextBasics):
    start_on_new_page: bool
    start_content_on_new_page: bool

    numbering: Literal["none", "roman","letters", "arabic"]


    def __init__(self, **kwargs):
        if "space_before" not in kwargs:
            kwargs["space_before"] = 0.2

        if "space_after" not in kwargs:
            kwargs["space_after"] = 0.1


        super().__init__(**kwargs)
        self.start_on_new_page = kwargs.get("start_on_new_page", False)
        self.start_content_on_new_page = kwargs.get("start_content_on_new_page", False)
        self.numbering = kwargs.get("numbering", "arabic")


class CodeHighlight():
    theme: str
    line_numbers: bool
    do_highlight: bool

    def __init__(self, **kwargs):
        self.theme = kwargs.get("theme", "monokai")
        self.line_numbers = kwargs.get("line_numbers", True)
        self.do_highlight = kwargs.get("do_highlight", True)

class Code():
    background_color:str
    color: str
    font: Font
    font_size: float


    def __init__(self, **kwargs):
        self.background_color = kwargs.get("background_color", "#DDDDDD")
        self.color = kwargs.get("color", "#333333")
        self.font = kwargs.get("font", "Courier")
        self.font_size = kwargs.get("font_size", 10)


class TitlePageSubject(TextBasics):
    show: bool

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.show = kwargs.get("show", True)
        self.font_size = kwargs.get("font_size", 20)
        self.alignment = kwargs.get("alignment", "center")
        self.space_before = kwargs.get("space_before", 1)


class TitlePageTitle(TextBasics):
    show: bool

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.show = kwargs.get("show", True)
        self.font_size = kwargs.get("font_size", 50)
        self.alignment = kwargs.get("alignment", "center")
        self.space_before = kwargs.get("space_before", 1)

class TitlePageAuthor(TextBasics):
    show: bool

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.show = kwargs.get("show", True)
        self.alignment = kwargs.get("alignment", "center")
        self.space_before = kwargs.get("space_before", 1)

class TitlePage():
    cover_image: str
    title: TitlePageTitle
    subject: TitlePageSubject
    author: TitlePageAuthor
    page_break: bool


    def __init__(self, **kwargs):
        self.enabled = kwargs.get("enabled", True)
        self.show_author = kwargs.get("show_author", True)
        self.show_title = kwargs.get("show_title", True)
        self.cover_image = kwargs.get("cover_image", "")
        self.title = TitlePageTitle(**kwargs.get("title", {}))
        self.author = TitlePageAuthor(**kwargs.get("author", {}))
        self.subject = TitlePageSubject(**kwargs.get("subject", {}))
        self.page_break = kwargs.get("page_break", True)

class Dividers:
    color: str
    width: str
    thickness:float
    space_before:float
    space_after:float
    alignment:Alignment

    def __init__(self, **kwargs):
        self.color = kwargs.get("color", "#000000")
        self.width = kwargs.get("width", "100%")
        self.thickness = kwargs.get("thickness", 0.01)
        self.space_before = kwargs.get("space_before", 0.2)
        self.space_after = kwargs.get("space_after", 0.2)
        self.alignment = kwargs.get("alignment", "center")

class ToC:
    enabled: bool
    title: str
    depth: int
    heading_font: Font
    heading_font_size: float
    heading_color: str
    start_on_new_page: bool
    page_break: bool
    leading: float
    indentation:int


    def __init__(self, **kwargs):
        self.enabled = kwargs.get("enabled", True)
        self.title = kwargs.get("title", "Table of Contents")
        self.depth = kwargs.get("depth", 3)
        self.heading_font = kwargs.get("heading_font", "Helvetica")
        self.heading_font_size = kwargs.get("heading_font_size", 10)
        self.heading_color = kwargs.get("heading_color", "#000000")
        self.start_on_new_page = kwargs.get("start_on_new_page", False)
        self.leading = kwargs.get("leading", self.heading_font_size * 1.4)
        self.page_break = kwargs.get("page_break", True)
        self.indentation = kwargs.get("indentation", 0.1)

class TableHeader:
    font: Font
    font_size: float
    background_color: str
    text_alignment: Alignment

    def __init__(self, **kwargs):
        self.font = kwargs.get("font", "Helvetica")
        self.font_size = kwargs.get("font_size", 10)
        self.background_color = kwargs.get("background_color", "#f0f0f0")
        self.text_alignment = kwargs.get("text_alignment", "center")


class Tables:
    header: TableHeader
    border_color: str
    style: Literal["list", "grid", "grid_inner"]
    text_alignment: Alignment

    def __init__(self, **kwargs):
        self.header = TableHeader(**kwargs.get("header", {}))
        self.border_color = kwargs.get("border_color", "#d0d0d0")
        self.style = kwargs.get("style", "list")
        self.text_alignment = kwargs.get("text_alignment", "left")

class Links:
    color: str
    underline: bool

    def __init__(self, **kwargs):
        self.color = kwargs.get("color", "#0000FF")
        self.underline = kwargs.get("underline", True)


class ImageToc(ToC):
    numbering: Literal["none", "roman","arabic"]
    prefix: str
    title: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numbering = kwargs.get("numbering", "roman")
        self.prefix = kwargs.get("prefix", "Figure ")
        self.title = kwargs.get("title", "List of Figures")

class Images:
    show_legends: bool
    list_of_figures: ImageToc

    def __init__(self, **kwargs):
        self.show_legends = kwargs.get("show_legends", True)
        self.list_of_figures = ImageToc(**kwargs.get("list_of_figures", {}))




class Document:
    page_size: Literal["A0","A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","B0","B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","C0","C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","LETTER","LEGAL","ELEVENSEVENTEEN","JUNIOR_LEGAL","HALF_LETTER","GOV_LETTER","GOV_LEGAL","TABLOID","LEDGER"]
    body: Body
    margin: Margin
    heading1: Heading
    heading2: Heading
    heading3: Heading
    heading4: Heading
    heading5: Heading
    heading6: Heading
    code: Code
    title_page: TitlePage
    header: HeaderFooter
    footer: HeaderFooter
    toc: ToC
    background_image: str
    page_break_on_new_md_file: bool
    tables: Tables
    links: Links
    dividers: Dividers
    code_highlight: CodeHighlight
    fonts: list[str]
    images: Images

    start_page_count_at_page: int
    start_page_count_on_first_header: bool

    def __init__(self, metadata, **kwargs):
        self.page_size = kwargs.get("page_size", "A4")
        self.margin = Margin(**kwargs.get("margin", {"top": 1, "bottom": 1, "left": 1, "right": 1}))

        for i in range(1,7):
            setattr(self, f"heading{i}", Heading(**kwargs.get(f"heading{i}", {"font_size": 10 * ((7-i)/2)})))

        self.body = Body(**kwargs.get("body", {}))
        self.code = Code(**kwargs.get("code", {}))
        self.title_page = TitlePage(**kwargs.get("title_page", {}))
        self.header = HeaderFooter(**kwargs.get("header", {"all": {"text": metadata.title, "space_before": 0.5}}))
        self.footer = HeaderFooter(**kwargs.get("footer", {"all": {"text": "${{page_number}}", "space_after": 0.5, "alignment": "right"}}))
        self.start_page_count_at_page = kwargs.get("start_page_count_at_page", 1)
        self.start_page_count_on_first_header = kwargs.get("start_page_count_on_first_header", True)
        self.toc = ToC(**kwargs.get("toc", {}))
        self.background_image = kwargs.get("background_image", "")
        self.page_break_on_new_md_file = kwargs.get("page_break_on_new_md_file", False)
        self.tables = Tables(**kwargs.get("tables", {}))
        self.links = Links(**kwargs.get("links", {}))
        self.dividers = Dividers(**kwargs.get("dividers", {}))
        self.code_highlight = CodeHighlight(**kwargs.get("code_highlight", {}))
        self.fonts = kwargs.get("fonts", [])
        self.images = Images(**kwargs.get("images", {}))


    def get_page_size(self):
        import reportlab.lib.pagesizes as pagesizes
        return  getattr(pagesizes, self.page_size)

class Settings:
    empty_line_in_text_only: bool

    def __init__(self, **kwargs):
        self.empty_line_in_text_only = kwargs.get("empty_line_in_text_only", False)



class Configs:

    metadata: Metadata
    document: Document
    settings: Settings

    DEFAULT_FILE_NAME = "nicebook.yml"

    def __init__(self, path):

        if path:
            configs = yaml.safe_load(open(path, 'r'))
            configs = self.__process_config_variables(configs)
        else:
            logging.warning(f"No config file found, using default values")
            configs = {
                "metadata": {
                    "title": "My Book",
                    "author": "John Doe",
                    "subject": "A book about nothing",
                    "keywords": "book, nothing, john doe",
                    "creator": "John Doe",
                    "producer": "John Doe",
                    "version": "1.0",
                },
                "document": {}
            }

        self.metadata = Metadata(**configs["metadata"])
        self.document = Document(self.metadata, **configs["document"])


    @staticmethod
    def generate_default_config_file(path: str):
        c = Configs(None)
        Configs.generate_config_file(c, path)

    @staticmethod
    def generate_config_file(c: "Configs", path:str):

        del c.document.header.odd
        del c.document.header.even
        del c.document.footer.odd
        del c.document.footer.even

        def recursive(field, key_path=""):
            d = {}
            for key, value in field.__dict__.items():

                # we add a unique id to each key so we can do find and replace
                # to add comments with documentation
                full_key = key_path + "." + key

                if value is None:
                    d[full_key] = None
                    continue


                t = type(value).__name__
                if t not in ('str', 'int', 'float', 'bool', 'list', 'dict','tuple'):
                    d[full_key] = recursive(value, full_key)
                else:
                    d[full_key] = value
            return d

        d = recursive(c)
        content = yaml.dump(d, indent=2)

        # No need to worry with adding spaces to match identation or adding comment sign on new line.
        # Just right the text, the code takes care of the rest
        # Third param set to True means we are commenting the option
        replacements = [
            ("    .document.code_highlight.do_highlight", "if  set to true an image will be generated with highlighted code, otherwise a text block is used"),
            ("    .document.code_highlight.theme", "Any theme available in https://pygments.org/styles/"),
            ("  .document.page_size", "values can be found at https://hg.reportlab.com/hg-public/reportlab/file/tip/src/reportlab/lib/pagesizes.py"),
            ("  .document.header", "can have either the 'all' property or the 'odd'/'even' properties. The nested properties are exactly the same. You should use odd/even if you want to have different headers/footers depending for odd and even page\n You can use the ${{page_number}} variable in the text"),
            ("  .document.footer", "can have either the 'all' property or the 'odd'/'even' properties. The nested properties are exactly the same. You should use odd/even if you want to have different headers/footers depending for odd and even page\n You can use the ${{page_number}} variable in the text"),
            ("    .document.title_page.cover_image", "Path to the cover image"),
            ("    .document.tables.style", "list, grid or grid_inner"),
            (".metadata", "In the 'document' properties of this file you can reference to metadata variables using the syntax ${{property_name}}\n You can add your own variables here as well. \nAlso on the markdown files you can reference to this variables with ${{pdf.YOUR_VARIABLE}}'.\nThese will be replaced in the pdf with the value defined in this file. Note that you cannot have spaces"),
            ("  .document.start_page_count_at_page", "if you change this property, this will only impact the numbering shown in the document, this means for the purpose of this configuration odd and even page numbers are related to the page order in the document, and not the page shown based on this index ", True),
            ("    .document.images.show_legends", "Will use the alt text of the image as a legend"),
            ("    .document.images.list_of_figures", "Will use the same settings as the toc"),
            ("    .document.images.start_page_count_on_first_header", "If set to true start_page_count_at_page will be ignored"),
        ]


        for r in replacements:
            k = f"{r[0]}:"
            n_spaces = len(k) - len(k.lstrip())
            spaces = " " * n_spaces
            comment:str = r[1]
            processed_lines = [f"{spaces}# {c.strip()}" for c in comment.split("\n")]
            final_comment = "\n".join(processed_lines)

            comment_property = "# " if len(r)==3 and r[2] == True else ""

            final_content = f"\n{final_comment}\n{spaces}{comment_property}{k.lstrip()}"
            content = content.replace(k, final_content)


        remove_full_key_regex = re.compile(r"((\.\w+)+)\.")
        remove_full_key_regex2 = re.compile(r"^\.", re.MULTILINE)
        content = re.sub(remove_full_key_regex, "", content)
        content = re.sub(remove_full_key_regex2, "", content)

        header = """# Fonts
# =====
# Out of the box fonts:
# 'Courier', 'Courier-Bold', 'Courier-Oblique', 'Courier-BoldOblique', 'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 'Helvetica-BoldOblique', 'Times-Roman', 'Times-Bold', 'Times-Italic', 'Times-BoldItalic', 'Symbol','ZapfDingbats'
#
# To add new fonts use the document.fonts property. Each font should be a path to a  .ttf file
# When adding a new fonts, it can be referenced across the document with the same name as the filename (without the extension)
#
# Fonts are measured in pt,

"""

        final_content = header + content

        with open(path, "w") as f:
            f.write(final_content)




    def __process_config_variables(self, configs: dict):

        var_regex = re.compile(r"\$\{\{(\w+)\}\}")

        def process_value(value:str):
            finds = var_regex.findall(value)

            if not finds:
                return value

            for f in finds:
                # We process this one in the header and footer sections
                if f == "page_number":
                    continue

                s = "${{" + f + "}}"
                value = value.replace(s, str(configs["metadata"][f]))

            return value


        def recursive_dict_update(d):
            for key, value in d.items():

                if isinstance(value, dict):
                    d[key] = recursive_dict_update(value)
                if isinstance(value, list):
                    l = []
                    for v in value:
                        l.append(process_value(v) if isinstance(v, str) else v)
                    d[key] = l
                elif isinstance(value, str):
                    d[key] = process_value(value)
                else:
                    # Update the value using the update function
                    d[key] = value

            return d

        return recursive_dict_update(configs)
