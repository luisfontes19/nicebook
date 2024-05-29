# import enum
# from typing import Union

# from reportlab.lib.styles import ParagraphStyle
# from reportlab.platypus import Flowable


# class ListBulletType(enum):
#     NONE = 0
#     BULLET = 1
#     NUMBER = 2
#     CHECKBOX = 3

# # list = List()

# # list.add_item("aisuhd")
# # sublist = List()
# # sublist.add_item("")
# # list.add_item(sublist)




# # size = self.configs.document.body.font_size
# #                 style = self.styler.stylesheet["BodyText"]
# #                 style.leftIndent = size * 2

# #                 ret.append(Checkbox(checked=children[0].checked, style=style))
# #                 ret.append(Spacer(0,-(size), True))

# class List:

#     indexes:dict
#     items: list["ListItem" | "List"]

#     def __init__(self, items):
#         self.items = []

#     def add_item(self, item: Union["ListItem", "List"]):
#         self.items.append(item)

#     def process(self, nested_list=None, level=0):
#         items = self.items if nested_list is None else nested_list
#         level += 1

#         for item in items:
#             index = 0
#             if isinstance(item, List):
#                 self.process(item, level)
#                 level -= 1
#             else:
#                 index += 1



#     def __process_item(self, item: "ListItem"):
#         item.process()
#         return item

# class ListItem:
#     def __init__(self, flowables: list[Flowable], bullet_type: ListBulletType = ListBulletType.BULLET, bullet: str = None, level=0, style=None):
#         self.flowables = flowables
#         self.bullet_type = bullet_type
#         self.bullet = bullet
#         self.level = level
#         self.style = style

#         if style is None:
#             self.style = ParagraphStyle(name='paragraphImplicitDefaultStyle')



#     def get_number(self, level):
#         if level in self.indexes:
#             self.indexes[level] += 1

#         return self.bullet
