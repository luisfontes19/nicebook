import os
import unittest

from nicebookconfigs import Configs
from nicebookgenerator import Generator
from pdf2image import convert_from_path
from PIL import Image, ImageChops


class TestPdfGeneration(unittest.TestCase):

    tmp_folder = os.path.join(os.path.dirname(__file__), "..", "tmp")
    test_files_folder = os.path.join(os.path.dirname(__file__), "test_files", "test_pdf_generation")

    def setUp(self):
        self.conf_file = os.path.join(self.tmp_folder, "test.yml")
        configs = Configs(None)
        configs.document.title_page.cover_image = os.path.join(self.test_files_folder, "cover.jpg")

        Configs.generate_config_file(configs, self.conf_file)

    def test_pdf_generation(self):

        generator = Generator(self.conf_file)
        f1 = os.path.join(self.test_files_folder, "test.md")
        f2 = os.path.join(self.test_files_folder, "test2.md")
        o = os.path.join(self.tmp_folder, "test.pdf")
        generator.generate([f1,f2], o)

        images = convert_from_path(o)
        for i in range(len(images)):
            image_name = f"page_{i}.jpg"
            image = images[i]
            image.save(os.path.join(self.tmp_folder, image_name))

            generated_image = Image.open(os.path.join(self.tmp_folder, image_name))
            expected_image = Image.open(os.path.join(self.test_files_folder, image_name))
            diff = ImageChops.difference(generated_image, expected_image)
            self.assertFalse(diff.getbbox(), f"PDF page {i} differs from the expected image")



        # with(Image(filename=o, resolution=120)) as source:
        #     for i, image in enumerate(source.sequence):
        #         newfilename = os.path.join(self.tmp_folder, f"page_{i}.jpg")
        #         Image(image).save(filename=newfilename)

        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
