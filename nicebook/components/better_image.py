from reportlab.lib.units import inch
from reportlab.platypus import Image

from nicebook.configs import Configs
from nicebook.utils import number_to_roman


class BetterImage(Image):
    legend: str

    configs: Configs = None
    image_number: int
    code_snippet: bool # if code_snippet is True, we do not use the legend numbering as markdown code has no legend

    LAST_INDEX = 0

    def __init__(self, filename, width=None, height=None, kind='direct', mask='auto', lazy=1, legend=None, code_snippet=False):
        super().__init__(filename, width, height, kind, mask, lazy)
        self.legend = legend
        self.code_snippet = code_snippet

        if not code_snippet:
            BetterImage.LAST_INDEX += 1
            self.image_number = BetterImage.LAST_INDEX

    def process_legend(self):
        text = ""
        configs = BetterImage.configs.document.images

        if configs.list_of_figures.prefix:
            text += f"{configs.list_of_figures.prefix}"

        if configs.list_of_figures.numbering:
            n = self.image_number
            if configs.list_of_figures.numbering == "roman":
                n = number_to_roman(n)
            else :
                n = str(n)

            text += n

        text += ": " + self.legend if self.legend else f": [No legend]"
        return text

    @staticmethod
    def resized_image(image_path, legend="", code_snippet: bool=False) -> "BetterImage":
        configs = BetterImage.__get_configs()

        doc_width = configs.document.get_page_size()[0]
        max_width = doc_width - configs.document.margin.left * inch - configs.document.margin.right * inch

        image = Image(image_path)

        if image.imageWidth > max_width:
            aspect_ratio = image.imageWidth / image.imageHeight
            height = max_width / aspect_ratio
            return BetterImage(image_path, max_width, height, legend=legend,code_snippet=code_snippet)
        else:
            return BetterImage(image_path, legend=legend,code_snippet=code_snippet)


    def __get_configs():
        if not BetterImage.configs :
            raise Exception("Configs not set for BetterImage")

        return BetterImage.configs
