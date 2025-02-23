#pip install marko reportlab
import logging
import os
import re
import tempfile
from html import escape

import reportlab.lib.colors as colors
from marko.element import Element
from marko.ext.gfm import gfm
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import get_lexer_by_name
from reportlab.lib.styles import StyleSheet1
from reportlab.lib.units import inch
from reportlab.platypus import (HRFlowable, ListFlowable,
                                ListItem, PageBreak, Paragraph, Spacer, Table,
                                XPreformatted)
from reportlab.platypus.tableofcontents import TableOfContents

from nicebook.components.better_image import BetterImage
from nicebook.components.rich_paragraph import RichParagraph
from nicebook.configs import Configs, Heading
from nicebook.nicebook_doc_template import NiceBookTemplate
from nicebook.reference_manager import ReferenceManager
from nicebook.styler import Styler
from nicebook.utils import number_to_letter, number_to_roman


class Generator:
    configs: Configs
    styles: StyleSheet1
    headings = [0,0,0,0,0,0]
    toc: TableOfContents
    image_toc: TableOfContents
    reference_manager: ReferenceManager

    def __init__(self, config_path:str=None):
        self.configs = Configs(config_path)
        self.styler = Styler(self.configs)
        self.styles = self.styler.stylesheet
        self.reference_manager = ReferenceManager()
        RichParagraph.styler = self.styler
        BetterImage.configs = self.configs

    a = None

    def __process_variables(self, text:str, filename:str):
        regex = re.compile(r"\$\{\{pdf\.(\w+)\}\}")

        def replacer(match):
            var = match.group(1)
            logging.info(f"Found variable '{var}' in file {filename}")

            if hasattr(self.configs.metadata, var):
                val = getattr(self.configs.metadata, var)
                logging.info(f"Replacing variable '{var}' with value '{val}'")
                return str(val)
            else:
                logging.warning(f"Variable '{var}' not found in metadata, fallback to original value")
                return match.group(0)

        return regex.sub(replacer, text)

    def generate(self, files: list[str], output_path:str="output.pdf"):

        mtd = self.configs.metadata
        doc:NiceBookTemplate = NiceBookTemplate(
            output_path,
            pagesize=self.configs.document.get_page_size(),
            topMargin=self.configs.document.margin.top * inch,
            bottomMargin=self.configs.document.margin.bottom * inch,
            leftMargin=self.configs.document.margin.left * inch,
            rightMargin=self.configs.document.margin.right * inch,
            title = mtd.title if mtd.title else None,
            author = mtd.author if mtd.author else None,
            subject = mtd.subject if mtd.subject else None,
            creator = mtd.creator if mtd.creator else None,
            producer = mtd.producer if mtd.producer else None,
            keywords = ",".join(mtd.keywords) if mtd.keywords else None,
            configs=self.configs
        )

        story = []

        story.extend(self.__process_title_page())

        if self.configs.document.toc.enabled:
            self.toc = self.__process_toc(doc)
            story.extend(self.toc)

        if self.configs.document.images.list_of_figures.enabled:
            self.image_toc = self.__process_image_toc(doc)
            story.extend(self.image_toc)

        if isinstance(files, str):
            files = [files]

        for (i, file) in enumerate(files):
            if i > 0 and self.configs.document.page_break_on_new_md_file:
                story.append(PageBreak())

            story.extend(self.__process_file(file))


        # TODO: see where the None comes from
        cleanup_story = []

        for item in story:
            if item is not None:
                cleanup_story.append(item)


        # Fallback in case an anchor is referenced but not defined
        # reportlab would through an error
        anchors_fallback = self.reference_manager.fail_safe()
        for a in anchors_fallback:
            cleanup_story.append(Paragraph(a))

        doc.multiBuild(cleanup_story, onFirstPage=doc.on_first_page, onLaterPages=doc.on_later_pages, maxPasses=100)

    def __process_file(self, file:str):
        self.reference_manager.current_file = file


        f = open(os.path.normpath(os.path.join(os.getcwd(), file)))
        md = f.read()
        f.close()

        md = self.__process_variables(md, file)

        parsed = gfm.parse(md)

        story = []

        # this anchor is used for when a link points to an entire markdown file
        a = self.reference_manager.generate_anchor(file, "")
        story.append(Paragraph(a))

        for child in parsed.children:
            el = self.__process_element(child)

            if isinstance(el, list):
                story.extend(el)
            else:
                story.append(el)

        return story

    def __process_toc(self, doc: NiceBookTemplate):
        story = []
        conf = self.configs.document.toc

        if conf.start_on_new_page:
            story.append(PageBreak())

        heading = Paragraph(conf.title, self.styles["TOCHeading"])
        story.append(heading)

        toc = TableOfContents()
        toc.levelStyles = [self.styles[f"TOCLevel{i}"] for i in range(1,7) ]
        doc.register_toc(toc)

        story.append(toc)

        if conf.page_break:
            story.append(PageBreak())


        return story

    def __process_image_toc(self, doc: NiceBookTemplate):
        story = []
        conf = self.configs.document.images.list_of_figures

        if conf.start_on_new_page:
            story.append(PageBreak())

        heading = Paragraph(conf.title, self.styles["ImageTOCHeading"])
        story.append(heading)

        toc = TableOfContents()
        toc.levelStyles = [self.styles[f"ImageTOCLevel{i}"] for i in range(1,7) ]
        doc.register_image_toc(toc)

        story.append(toc)

        if conf.page_break:
            story.append(PageBreak())

        return story

    def process_divider(self, element:Element):
        conf = self.configs.document.dividers

        ret = []

        ret.append(Spacer(0, conf.space_before * inch))

        #the spaceBefore and spaceAfter properties were not working
        #so we use spacers instead
        ret.append(HRFlowable(
            width=conf.width,
            thickness=conf.thickness*inch,
            lineCap='round',
            color=colors.HexColor(conf.color),
            hAlign=conf.alignment.upper(),
            vAlign='CENTER',
            dash=None)
        )

        ret.append(Spacer(0, conf.space_after * inch))

        return ret

    def __process_raw_text(self, element:Element):
        return escape(element.children)


    def __process_link(self, element:Element):
        text = escape(element.children[0].children)
        link = element.dest

        if "://" in link:
            return f"<a href='{link}'>{text}</a>"
        else:
            return self.reference_manager.generate_referencing_link(self.reference_manager.current_file, link, text)


    def __process_strong_emphasis(self, element:Element):
        text = escape(element.children[0].children)
        return f"<b>{text}</b>"

    def __process_emphasis(self, element:Element):
        s = element.children[0].children

        # for bold and italic ***text***
        if isinstance(s, str):
            text =  escape(s)
        else:
            text = "<b>" + escape(s[0].children) + "</b>"

        return f"<i>{text}</i>"

    def __process_line_break(self, element:Element=None):
        return "\n"

    def __process_code_span(self, element:Element):
        font = self.configs.document.code.font
        color = self.configs.document.code.color
        return f"<font color='{color}' face='{font}'>{escape(element.children)}</font>"

    def __process_paragraph_new(self, element:Element, extra_info: dict = None):

        ret = []

        p:RichParagraph = None

        for child in element.children:
            c_type = child.get_type()

            if p == None:
                p = RichParagraph("", extra_info)

            match c_type:
                case "RawText":
                    p.add_text(child.children)
                case "Link":
                    text = escape(child.children[0].children)
                    link = child.dest
                    p.add_link(link, text, self.reference_manager)
                case "StrongEmphasis":
                    p.add_bold_text(child.children[0].children)
                case "Emphasis":
                    s = child.children[0].children

                    # this is for bold and italic ***text***
                    if not isinstance(s, str):
                        p.add_bold_italic_text(s[0].children)
                    else:
                        p.add_italic_text(s)
                case "LineBreak":
                    p.add_new_line()
                case "CodeSpan":
                    p.add_code_text(child.children)
                case "InlineHTML":
                    logging.warning("Ignoring Inline HTML in paragraph")
                case "Image":
                    ret.append(p.process())
                    image_legend = child.children[0].children
                    img = BetterImage.resized_image(child.dest, image_legend)
                    ret.append(img)

                    if self.configs.document.images.show_legends:
                        p = RichParagraph(extra_info={"style": self.styler.stylesheet["ImageLegend"]})
                        p.add_italic_text(img.process_legend())
                        ret.append(p.process())

                    p = None
                case _:
                    logging.warning(f"Unknown paragraph type: {c_type}. If you see this message please report in Github with the markdown content that caused this.")

        if p != None:
            ret.append(p.process())

        return ret


    def __process_blank_line(self, element:Element):

        # Create a Paragraph object with the sample content and custom style
        return Spacer(0, self.configs.document.body.font_size)


    def __increment_heading(self, level):
        self.headings[level-1] += 1
        for i in range(level, len(self.headings)):
            self.headings[i] = 0

    def __heading_numbering_to_string(self, level:int):
        s = ""

        for i in range(1, level + 1):

            h:Heading = getattr(self.configs.document, f"heading{i}")
            heading_value = self.headings[i-1]

            if s != "":
                s = s + "."

            match h.numbering:
                case "roman":
                    s = s + number_to_roman(heading_value)
                case "arabic":
                    s = s + str(heading_value)
                case "letters":
                    s = s + number_to_letter(heading_value)

        return s

    def __process_heading(self, element:Element):
        ret = []

        level = element.level

        conf:Heading = getattr(self.configs.document, f"heading{level}")

        if conf.start_on_new_page:
            ret.append(PageBreak())

        raw_text = element.children[0]
        text = raw_text.children

        if not isinstance(text, str):
            text = text[0].children

        if conf.numbering:
            self.__increment_heading(level)

            numbering = self.__heading_numbering_to_string(level)
            text_final = f"{numbering} {text}"

        p = Paragraph(text_final, self.styles[f"heading{level}"])

        anchor = self.reference_manager.generate_anchor(self.reference_manager.current_file, text)
        ret.append(Paragraph(anchor))

        ret.append(p)

        if conf.start_content_on_new_page:
            ret.append(PageBreak())

        return ret

    def __process_quote(self, element:Element):
        children = element.children
        p = self.__process_paragraph_new(children[0], {"quote": True})
        return p

    def __process_table(self, element:Element):
        data = []

        for row in element.children:
            r_data = []
            for cell in row.children:
                cell_content = cell.children


                if len(cell_content) > 1:
                   # cell data doesn't come in paragraphs :(
                    # so we fake one :D
                    e = Element()
                    e.get_type = lambda: "Paragraph"
                    e.children = cell_content

                    # Using a KeepTogether break the execution inside the table cell,
                    # But we can send an array of flowables to the cell content
                    # so we just get the flowables from the KeepTogether instance
                    cell_content = self.__process_paragraph_new(e)
                else:
                    c = cell_content[0]
                    if c.get_type() == "RawText":
                        cell_content = Paragraph(c.children)
                    else:
                        # Don't know whats there... Try to process as a regular element
                        e = Element()
                        e.get_type = lambda: "Container"
                        e.children = cell_content
                        cell_content = self.__process_element(e)

                r_data.append(cell_content)

            data.append(r_data)

        t = Table(data)
        t.setStyle(self.styler.table_style)

        return t

    def __process_list(self, element:Element, nested=False, ordered=None):
        list_items = []
        # size = self.configs.document.body.font_size

        # style = self.styler.stylesheet["BodyText"]
        # style.leftIndent = size * 2

        # return [
        #     Checkbox(checked=False, style=),
        #     Spacer(0,-(size), True),
        #     Paragraph("asd", style)
        #     ]

        _ordered = ordered or (not nested and element.ordered == True)

        bullet_type = "1" if _ordered else "bullet"
        start = None
        color = None
        element_items = element.children # List -> ListItem[]

        for list_item in element_items:
            # TODO: there's a limitation here, we are only adding a 'checkbox' if the first element is a checkbox
            # we should add a checkbox for each element in the list
            # For that the current way this is implemented means that we need to create a new list, since check square that shows up is defined in the ListFlowable object
            # TODO support checked checkboxes :)
            # If first item has a checkbox, show a checkbox in all
            children = list_item.children
            if len(children) == 0:
                continue

            if hasattr(children[0], "checked"):
                start = "square"
                color = colors.HexColor("#DDDDDD")

            p = self.__process_paragraph_new(children[0])

            l = ListItem(p)


            if len(children) < 2:
                list_items.append(l)
            else:
                # TODO: There's a "hack" here where we only get the first element of the paragraph
                # It may have some issues
                list_items.append([p[0], self.__process_list(children[1], True, _ordered)])

        params = {
            "bulletType": bullet_type,
            "start": start,
            "spaceBefore": 0,
            "spaceAfter": 0,
            "bulletColor": color or "black"
        }

        return ListFlowable(list_items,  **params)

    def __process_code_block(self, element:Element):

        code = element.children[0].children
        lang = element.lang
        conf = self.configs.document.code_highlight

        if lang == '':
            lang = 'text'

        if conf.do_highlight:
            try:
                lexer = get_lexer_by_name(lang)
            except Exception as e:
                logging.warning(f"Failed to get lexer for language '{lang}', falling back to plain text")
                lexer = get_lexer_by_name("text")

            formatter = ImageFormatter(
                style=conf.theme,
                dpi=600, scale=1,
                line_numbers=conf.line_numbers,
                line_number_bg=None,
                font_size=self.configs.document.body.font_size,
                font_name=conf.font
            )

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
                highlight(code, lexer, formatter, outfile=f)
                s = Spacer(0, 0.1 * inch) # to give it some vertical spacing
                img = BetterImage.resized_image(f.name, None, code_snippet=True)

                return [s,img,s]

        else:
            ret = []
            for l in code.split("\n"):
                #XPreformatted will preserve trailing spaces, opposite to Paragraph
                ret.append(XPreformatted(escape(l), self.styles["Code"]))
            return ret

    def __process_element(self, element: Element, parent=None):
        type = element.get_type()

        match type:
            case "Paragraph":
                ##return self.__process_paragraph(element)
                return self.__process_paragraph_new(element)
            case "BlankLine":
                return self.__process_blank_line(element)
            case "Heading":
                return self.__process_heading(element)
            case "List":
                _list = self.__process_list(element)
                return _list
            case "Quote":
                return self.__process_quote(element)
            case "FencedCode":
                return self.__process_code_block(element)
            case "CodeBlock":
                return self.__process_code_block(element)
            case "HTMLBlock":
                logging.warning("Ignoring HTML block")
                return None # lets ignore html blocks for now. appear for exxample for comments
            case "Table":
                return self.__process_table(element)
            case "RawText":
                return self.__process_raw_text(element)
            case "Link":
                return self.__process_link(element)
            # case "StrongEmphasis":
            #     return self.__process_strong_emphasis(element)
            # case "Emphasis":
            #     return self.__process_emphasis(element)
            case "LineBreak":
                return self.__process_line_break(element)
            case "ThematicBreak":
                return self.process_divider(element)

            # Container does not exist in marko, this is a hack for us to fix table cell's data
            case "Container":
                res = []
                for c in element.children:
                    res.append(self.__process_element(c))
                return res
            case "CodeSpan":
                return Paragraph(self.__process_code_span(element))
            case _:
                logging.warning(f"Unknown type: {type}. If you see this message please report in Github with the markdown content that caused this.")
                return None

    def __process_title_page(self):
        components = []
        conf = self.configs.document.title_page


        if conf.title.show:
            components.append(Spacer(1, self.configs.document.title_page.title.space_before * inch))
            components.append(Paragraph(self.configs.metadata.title, self.styles["TitlePageTitle"]))

        if conf.subject.show:
            components.append(Paragraph(self.configs.metadata.subject, self.styles["TitlePageSubject"]))

        if conf.author.show:
            components.append(Paragraph(self.configs.metadata.author, self.styles["TitlePageAuthor"]))

        if conf.page_break:
            components.append(PageBreak())

        return components




