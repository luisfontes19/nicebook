from reportlab.lib.colors import green, tan
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus.flowables import Flowable


class Checkbox(Flowable):

    def __init__(self, checked:bool, style=None):

        self.checked = checked

        if style is None:
            style = ParagraphStyle(name='paragraphImplicitDefaultStyle')

        self.size=style.defaults["fontSize"]
        self.width = self.size
        self.height = self.size

        self.color = style.defaults["textColor"]
        #self.xoffset = 0

        # normal size is 4 inches
        self.scale = self.size/(4.0*inch)

    # def wrap(self, *args):
    #     return (self.xoffset, self.size)

    def draw(self):
        self.canv.setLineWidth(self.size/10)

        self.canv.setStrokeColor(self.color)
        self.canv.rect(0, 0, self.size,self.size)

        a_fourth = self.size/4
        margin = self.size/6

        if self.checked:
            self.canv.line(0 + margin, a_fourth + margin, a_fourth + margin, 0 + margin)
            self.canv.line(a_fourth + margin, 0 + margin, self.size - margin,self.size - margin)
