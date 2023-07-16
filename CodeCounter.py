import os
import sys
import logging
import colorlog
from typing import Iterable
from tqdm import tqdm

# Create a custom formatter with colors
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG': 'light_green',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red'
    }
)

# Create a handler and set the formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Create the logger and add the handler
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# list of supported languages
LANGUAGE_LIST = (
    "ActionScript", "Ada", "Assembler",
    "Basic", "C", "C header",
    "C++", "C++ header",
    "C#", "CSS", "Cg",
    "Cobol", "CoffeeScript", "Coq",
    "CUDA", "D", "Dart",
    "ECMAScript", "Erlang", "F#",
    "Fortran", "Go", "GLSL",
    "Groovy", "Haskell", "HLSL",
    "HTML", "Java", "JavaScript",
    "JSON", "Kotlin", "LaTeX",
    "Lisp", "Lua", "Objective-C",
    "OCaml", "OpenCL", "Pascal",
    "Perl", "Perl 6", "PHP",
    "PostScript", "Python", "Q",
    "Q#", "Ruby", "Rust",
    "Scala", "Swift", "TypeScript"
)
# initialize every language with an empty list to hold all files and an empty line count
counter_dict = {language:{"files": [], "line-count": 0} for language in LANGUAGE_LIST}

# file extensions for every programming language
# file extensions must be on the same index as language listed
# above in LANGUAGE_LIST
FILE_EXTENSION_LIST = (
    ('.as'), ('.adb', 'ads'), ('.asm', '.masm', '.nasm'),
    ('.bas'), ('.c'), ('.h'),
    ('.cpp', '.cxx', '.c++', '.cc'), ('.hpp', '.hxx', '.h++', '.hh'),
    ('.cs'), ('.css'), ('.cg'),
    ('.cbl', '.cob', '.cpy'), ('.coffee', '.litcoffee'), ('.v'),
    ('.cu', '.cuh', '.cuda'), ('.d'), ('.dart'),
    ('.es'), ('.erl', '.hrl'), ('.fs', '.fsi', '.fsx'),
    ('fsscript'), ('.f', '.for', '.f90'), ('.go'),
    ('.glsl'), ('.groovy'), ('.hs', '.lhs'),
    ('.hlsl'), ('.html'), ('.java'),
    ('.js', '.mjs'), ('.json'), ('.kt', '.kts'),
    ('.tex'), ('.lsp'), ('.lua'), ('.m', '.mm'),
    ('.ml', '.mli'), ('.cl'), ('.pp', '.pas'),
    ('.pl', '.pm', '.t', '.pod'), ('.p6', '.pl6', '.pm6'), ('.php', '.phtml', '.php3'),
    ('.php4', '.php5', '.php7'), ('.phps', '.php-s', '.pht'), ('.ps'),
    ('.py'), ('.q'), ('.qs'),
    ('.rb'), ('.rs', '.rlib'), ('.sc', '.scala'),
    ('.swift'), ('.ts', '.tsx')
)

def add_extension_ref(extension_dict: dict, extensions: Iterable, language_ref: dict):
    """
    To avoid later iterating over every language and their file extension
    we add a reference from every file extension as a key referring
    to the same language, so we just have to access a single dict

    Args:
        extension_dict (dict): the extension_dict with all references
        extensions (tuple): the file extensions of this language
        language_ref (dict): a reference to the languages counter
    """
    for extension in extensions:
        extension_dict[extension] = language_ref["files"]

# initialize a reference table to refer to a specific programming language based on the file extension
extension_dict = {}
for extensions, language in zip(FILE_EXTENSION_LIST, counter_dict.values()):
    add_extension_ref(extension_dict, extensions, language)


def check_directory_paths(args: Iterable) -> list:
    """
    Check all given paths in the folder
    if the folder is empty return an empty list
    if one of the given paths is invalid it will show an error and `sys.exit`
    otherwise it will return a new list with paths

    Args:
        args (Iterable): a list with paths to check

    Returns:
        list: a copy of the given path list
    """
    folders_list = []

    if len(args) == 0:
        return []

    for folder_name in args:
        if os.path.isdir(folder_name):
            folders_list.append(folder_name)
            continue

        logging.critical(f"{folder_name} is not a directory")
        sys.exit()

    return folders_list

def FilesInFolder(path: str, recursive: bool) -> list:
    """
    Return a list with exact paths to every file in the given path
    if the recursive flag is set to `True`, it will search the full directory
    otherwise just the given path without any sub-folders

    Args:
        path (str): the path where to search in
        recursive (bool): search only given path or search the given directory

    Returns:
        list: all files whether only this path or the whole directory
    """
    files_list = []

    if recursive is True:
        for root, dirs, files in tqdm(os.walk(path), desc=f"Finding files in {path}:", unit="file"):
            for filename in files:
                files_list.append(os.path.join(root, filename))
    else:
        files_list = os.listdir(path)

    return files_list

def LinesInLang(lang: dict):
    """
    Count the lines of every file that's listed in the files list of the given
    counter ref and save the sum into line-count

    Args:
        lang (dict): a reference to the language counter
    """
    for file in tqdm(lang["files"], desc="Counting...", unit="Files"):
        try:
            lang["line-count"] += sum(1 for line in open(file, "r", errors="ignore"))
        except UnicodeDecodeError:
            logging.error(f"there was an error reading: {file}")

arguments = sys.argv[1:]  # read user args

logging.info("Validate input")
folders = check_directory_paths(arguments)  # check the folders

for folder in folders:
    logging.info(f"Start counting files for dir {folder}")
    files = FilesInFolder(folder, True)
    skipped_extensions = set()

    for file in files:
        file_split = file.split(".")
        if len(file_split) <= 1:
            continue
        extension = "." + file_split[-1]
        extension_dict_ref = extension_dict.get(extension)
        if extension_dict_ref is None:
            logging.warning(f"skipping extension {extension}: {file}")
            skipped_extensions.add(extension)
        else:
            logging.info(f"Found extension {extension}: {file}")
            extension_dict_ref.append(file)

    total_lines = 0
    successfully_counted = []

    for lang in counter_dict:
        logging.info(f"counting lines for {lang}")
        counter_ref = counter_dict[lang]
        LinesInLang(counter_ref)

        total_lines += counter_ref["line-count"]

        if counter_ref["line-count"] != 0:
            successfully_counted.append(f"{lang}: {counter_ref['line-count']} lines")

    logging.warning(f"\nSkipped extensions:\n{', '.join(sorted(skipped_extensions))}")
    logging.info(f"\n" + "\n".join(successfully_counted))
    logging.info(f'Total:{total_lines}')
