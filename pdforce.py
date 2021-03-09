import os, sys, signal, time, argparse
from pikepdf import Pdf
from pathlib import Path
from pyperclip import copy

TITLE = """
     ______ _____  _______                        
    |   __ \     \|    ___|.-----.----.----.-----.
    |    __/  --  |    ___||  _  |   _|  __|  -__|
    |___|  |_____/|___|    |_____|__| |____|_____|
 """


class Color:
    """ANSI COLORS

    Color.FAIL --> Bold red.\n
    Color.INFORMATION --> Bold blue.\n
    Color.EMPHASIS --> Bold cyan.\n
    Color.DETAIL --> Yellow.\n
    """

    FAIL = "\033[91m\033[1m"
    INFORMATION = "\033[94m\033[1m"
    EMPHASIS = "\033[96m\033[1m"
    DETAIL = "\033[93m"
    END = "\033[0m"


def close(signum="", frame=""):
    print(f"\n{Color.INFORMATION}BYE!{Color.END}")
    sys.exit(0)
signal.signal(signal.SIGINT, close)


def cli_arguments():
    """CLI ARGUMENTS

    All arguments are optional.\n
    If the PDF and wordlist arguments are not set a prompt will let the user enter these values.\n
    The encoding argument lets the user set an encoding type for the wordlist. Refer to https://docs.python.org/3/library/codecs.html#standard-encodings.\n
    The verbose argument will display all the attempted passwords and some additional information after the password is found.
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=f"\n{Color.DETAIL}pdforce.py [-p <pdf>] [-w <wordlist>] [-e <encoding>] [-o <output>] [-c] [-v] [-h/--help]{Color.END}",
        description=f"{Color.EMPHASIS}{TITLE}\nLightweight PDF password cracker. USE FOR LEGAL INTENTS ONLY.{Color.END}",
        epilog=f"{Color.EMPHASIS}Made by @poponealex - https://github.com/poponealex{Color.END}",
    )

    parser.add_argument(
        "-p",
        "--pdf",
        type=str,
        help=f"{Color.INFORMATION}Path to the pdf file.{Color.END}",
        action="store",
        default="",
    )

    parser.add_argument(
        "-w",
        "--wordlist",
        type=str,
        help=f"{Color.INFORMATION}Path to the wordlist.{Color.END}",
        action="store",
        default="",
    )

    parser.add_argument(
        "-e",
        "--encoding",
        type=str,
        help=f"{Color.INFORMATION}Specify an encoding for the wordlist (https://docs.python.org/3/library/codecs.html#standard-encodings). The default encoding is platform dependent. Use 'iso8859_1' for rockyou. {Color.END}",
        action="store",
        default=None,
    )

    parser.add_argument(
        "-o",
        "--output",
        help=f"{Color.INFORMATION}Output the cracked password to a new file.{Color.END}",
        action="store",
    )

    parser.add_argument(
        "-c",
        "--copy",
        help=f"{Color.INFORMATION}Copy the password to the clipboard.{Color.END}",
        action="store_true",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help=f"{Color.INFORMATION}Display additional information.{Color.END}",
        action="store_true",
        default=False,
    )

    return parser.parse_args()


def return_valid_path(file_path, file_extension=""):
    """PATH VALIDATOR

    Parameters:
        - file_path: the path (as a string) to be validated and returned (as a Path object).
        - file_extension: to check that file_path leads to a file with the right extension.
    Errors:
        - An Exception is raised if the provided path is invalid (file not found).
        - An Exception is raised if the provided path's file's suffix doesn't match file_extension (if set).

    Returns the validated path of a file as a pathlib.Path() object.
    """

    path = Path.cwd() / Path(file_path) if not Path(file_path).is_absolute() else Path(file_path)
    if not path.exists():
        raise Exception(f"Invalid path, couldn't find: {path}")
    if file_extension and not path.suffix.replace(".", "") == file_extension:
        raise Exception(f"Invalid file format, has to be: {file_extension}")
    return path


def get_path(path="", prompt_title="PATH TO FILE", file_extension=""):
    """GET A FILE'S PATH

    Parameters:
        - path: if not set, the user will be prompted to enter the file's path to be validated.
        - prompt_title: emphasised string to be displayed before the prompt, default is 'PATH TO FILE'.
        - file_extension: to check that the path leads to a file with the right extension.

    If the the path provided isn't validated, the user will be prompted to enter a new one.\n
    Returns a file's path after validation by return_valid_path().
    """

    file_path = ""
    print(f"{Color.EMPHASIS}{prompt_title}{Color.END}")
    while True:
        try:
            file_path = (
                return_valid_path(input(f"{Color.INFORMATION}Enter an absolute or relative path from current working directory:{Color.END}\n"), file_extension)
                if not path
                else return_valid_path(path, file_extension)
            )
            return file_path
        except Exception as e:
            path = ""
            print(f"{Color.FAIL}{e}{Color.END}")


def load_wordlist(wordlist_path, encoding=None):
    """LOAD EVERY OCCURENCES FROM A WORDLIST

    Parameters:
        - wordlist_path: the provided wordlist has to be newline-delimited.
        - encoding: Default is platform dependent, refer to https://docs.python.org/3/library/codecs.html#standard-encodings for valid encodings.
    
    Returns a list object."""

    with open(wordlist_path, "r", encoding=encoding) as f:
        return f.read().splitlines()


def save_output(output, file_name=""):
    with open(file_name, "w") as f:
        f.write(output)


def bruteforce_pdf(pdf_file_path, wordlist, verbose=False):
    """CRACK THE PDF FILE'S PASSWORD

    Parameters:
        - pdf_file_path: path to the pdf file.
        - wordlist: path to the wordlist.
        - verbose: if True additional info will be displayed such as time elapsed and password position in the wordlist.
    
    If the file is unencrypted a message will be displayed stating so.\n
    If the password is not in the wordlist a message will be displayed stating so.\n
    Returns the password and displays it if found.
    """

    if verbose:
        start_time = time.time()

    for word in [""] + wordlist:
        try:
            with Pdf.open(pdf_file_path, password=word):
                if not word:
                    return print(f"\n{Color.EMPHASIS}The PDF file provided is not encrypted.{Color.END}")
                print(f"\n\n{Color.INFORMATION}Password is:{Color.END} {Color.EMPHASIS}{word}{Color.END}")
                if verbose:
                    print(f"\n\n{Color.DETAIL}Found at index: {wordlist.index(word) + 1}\nTime elapsed: {(time.time() - start_time):.3f} secs{Color.END}")
                return word
        except:
            sys.stdout.write(f"{Color.INFORMATION} Trying:{Color.END} {Color.FAIL}{word}{Color.END}\r") if verbose else sys.stdout.write(f"\r{Color.DETAIL}Searching...{Color.END}")
    return print(f"\n\n{Color.EMPHASIS}No password matched with the provided wordlist.{Color.END}")


def run():
    args = cli_arguments()
    print(f"{Color.EMPHASIS}{TITLE}{Color.END}".center(500))
    pdf_path = get_path(path=args.pdf, prompt_title="PATH TO PDF", file_extension="pdf")
    print(f"{pdf_path}\n")
    wordlist_path = get_path(path=args.wordlist, prompt_title="PATH TO WORDLIST")
    print(wordlist_path)
    wordlist = load_wordlist(wordlist_path, encoding=args.encoding)
    if args.verbose:
        print(f"\n{Color.DETAIL}Total wordcount: {len(wordlist)}{Color.END}")
    result = bruteforce_pdf(pdf_path, wordlist, verbose=args.verbose)
    if result:
        if args.output:
            save_output(result, file_name=args.output)
        if args.copy:
            copy(result)
    

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"{Color.FAIL}<{e}> was raised!{Color.END}")
    close()