# Nicebook

This is a tool to convert markdown files into well formatted pdfs with a lot of customizations through a simple yet powerful config file. No need to work with latex templates or Lua scripts.

## Usage

```bash
nicebook -i file1.md file2.md folder_with_md -o output.pdf -c nicebook.yml
```

If you want to generate a default config so that you can customize it, you can use the following command

```bash
nicebook -g
```

This will generate a file nicebook.yml that you can then tweak for your needs

## Security implications

Text input is not sanitized before writing to pdf which means that you need to do this on your side in case the text comes from an unstrusted source or HTML will potentially be injected and rendered into the PDF

Also, the configurations are assumed as safe so they are not escaped either.

## Contributing

### Running Tests

```bash
python -m unittest
python -m nicebook.cli -i tests/test_files/complex.md -o tmp/output.pdf
``````
