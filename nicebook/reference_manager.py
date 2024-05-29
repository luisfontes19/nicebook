import logging
import os
import random
import re
import string


class Reference:
    absolute_file_path: str
    hash: str
    ref_value: str

    def __init__(self, absolute_file_path:str):
        self.absolute_file_path = absolute_file_path
        self.hash = self.random_hash()


    def random_hash(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


class ReferenceManager:
    """"
    We may need to resolve cross references between files.
    Since we may have multiple files or headers with the same name we need to ensure every anchor has a unique identifier
    This class will manage random hashes as anchor prefixes so that we don't leak file paths in the final PDF.

    """
    file_references: list[Reference]

    # if an reference cannot be resolved reportlab will fail
    # so we log all created references and if one is missing we create a dummy anchor
    created_references = []
    created_anchors = []

    current_file: str

    def __init__(self):
        self.file_references = []
        self.created_references = []
        self.created_anchors = []
        current_file = None

    def resolve_absolute_file_path(self, file:str, current_md_file=None):
        # Get absolute file paths, gets tricky when a markdown file is referencing another
        # Example:
        # File A/some.md references ../B/other.md
        # We need to resolve the full path so we can always compare the same file path
        if current_md_file:
            current_md_file_path = os.path.abspath(os.path.dirname(current_md_file))
            file = os.path.join(current_md_file_path, file) # (A, ../B/other.md) => A/../B/other.md => B/other.md

        return os.path.abspath(file)


    def add_reference(self, file:str)->str|None:
        file = self.resolve_absolute_file_path(file)
        ref = self.get_reference(file)
        if not ref:
            ref = Reference(file)
            self.file_references.append(ref)
            logging.debug(f"Adding reference for file: {file}. Hash: {ref.hash}")

        return ref

    def get_reference(self, file:str):
        file = self.resolve_absolute_file_path(file)
        for reference in self.file_references:
            if reference.absolute_file_path == file:
                return reference


        return None

    def get_or_create_reference(self, file:str):
        ref = self.get_reference(file)
        if not ref:
            ref = self.add_reference(file)

        return ref


    def generate_anchor(self, current_md_file:str, heading:str) -> str:
        ref = self.add_reference(current_md_file)
        r = self.calculate_reference_value(ref, heading)
        self.created_anchors.append(r)

        return f"<a name='{r}'></a>"

    def calculate_reference_value(self, ref:Reference, heading:str) -> str:
        h = self.string_to_md_anchor(heading)
        return f"{ref.hash}-{h}"



    def generate_referencing_link(self, current_md_file, md_link:str, text:str):
        href = ""
        l = ""

        if md_link.startswith("#"):
            ref = self.get_or_create_reference(current_md_file)
            l = self.calculate_reference_value(ref, md_link[1:])
            href = f"document:{l}"
        elif "#" in md_link: # references another file: some_file#some_heading
            file, heading = md_link.split("#")
            target_file = self.resolve_absolute_file_path(file, current_md_file)
            ref = self.get_or_create_reference(target_file)

            l = self.calculate_reference_value(ref, heading)
            href = f"document:{l}"
        else:
            # assuming is a link to another file
            target_file = self.resolve_absolute_file_path(md_link, current_md_file)
            ref = self.add_reference(current_md_file)
            l = self.calculate_reference_value(ref, "")
            href = f"document:{l}"

        self.created_references.append(l)

        return f"<a href='{href}'>{text}</a>"

    def string_to_md_anchor(self, string:str):

        string = re.sub('[^A-Za-z0-9 \-\_]+', '', string)
        return string.lower().replace(' ', '-')


    def fail_safe(self) -> list[str]:
        extra_anchors = []
        for reference in self.created_references:
            if reference not in self.created_anchors:
                logging.debug(f"Missing anchor for reference: {reference}")
                extra_anchors.append(f"<a name='{reference}'></a>")

        return extra_anchors

