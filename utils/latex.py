import os

import jinja2
from jinja2 import Template

latex_jinja_env = jinja2.Environment(
    block_start_string="\BLOCK{",
    block_end_string="}",
    variable_start_string="\VAR{",
    variable_end_string="}",
    comment_start_string="\#{",
    comment_end_string="}",
    line_statement_prefix="%%",
    line_comment_prefix="%#",
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.abspath(".")),
)


def create_latex_file(name):
    """
    Creates a .tex file in the current directory.
    """
    f = open(f"{name}.tex", "w", encoding="utf-8")
    f.write(r"\input{preamble.tex}" + "\n")
    f.write(r"\begin{document}" + "\n")
    f.close()


def append_to_latex_file(name, data):
    f = open(f"{name}.tex", "a", encoding="utf-8")
    f.write(str(data) + "\n")
    f.close()


def output_latex_file(name):
    f = open(f"{name}.tex", "a", encoding="utf-8")
    f.write(r"\end{document} " + "\n")
    f.close()
    os.system(f"xelatex -interaction nonstopmode --shell-escape {name}.tex")


def appened_using_template(method):
    """
    A method decorator used to append to the latex file created by the instance
    using a latex template with the name of the given method.
    """

    def inner(instance, *args, **kwargs):
        f = open(f"{instance.__name__}.tex", "a", encoding="utf-8")
        template = latex_jinja_env.get_template(f"{method.__name__}.tex")
        output = method(instance, *args, **kwargs)
        result = template.render(instance=instance, output=output, **kwargs)
        f.write(result)
        f.close()
        return method(instance, *args, **kwargs)

    return inner


def latexfy(obj):
    """
    When used on an object, each method will write how the calculation is done
    to a tex file which can be compiled then.
    """

    object_methods = [
        method_name for method_name in dir(obj) if callable(getattr(obj, method_name))
    ]
    object_methods = [m for m in object_methods if not m.startswith("__")]
    for method in object_methods:
        setattr(obj, method, appened_using_template(getattr(obj, method)))
    return obj
