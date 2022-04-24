import os, sys, signal, time, argparse
from pikepdf import Pdf
from pathlib import Path
from pyperclip import copy
from typing import Union


TITLE = """
     ______ _____  _______                        
    |   __ \     \|    ___|.-----.----.----.-----.
    |    __/  --  |    ___||  _  |   _|  __|  -__|
    |___|  |_____/|___|    |_____|__| |____|_____|
 """


########################################################################################################### CLI, Misc ###########################################################################################################


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
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=f"\n{Color.DETAIL}pdforce.py [-p <pdf>] [-w <wordlist>] [-e <encoding>] [-o <output>] [-c] [-h/--help]{Color.END}",
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

    return parser.parse_args()


#################################################################################################################################################################################################################################


def get_valid_path(file_path: Path, prompt_title: str="PATH TO FILE") -> Path:
    """GET A VALID FILE'S POSIX PATH

    Parameters:
        - path: if not set, the user will be prompted to enter the file's path.
        - prompt_title: emphasised string to be displayed before the prompt, default is 'PATH TO FILE'.

    Returns a file's PosixPath.
    """

    print(f"{Color.EMPHASIS}{prompt_title}{Color.END}")
    while True:
        if file_path.exists() and file_path.is_file():
            return file_path
        else:
            file_path = Path(input(f"{Color.INFORMATION}Enter the file's path: {Color.END}"))


def bruteforce_pdf(pdf_file_path: Path, wordlist: list) -> Union[str, None]:
    """CRACK THE PDF FILE'S PASSWORD

    Parameters:
        - pdf_file_path: path to the pdf file.
        - wordlist: path to the wordlist.
    
    If the file is unencrypted a message will be displayed stating so.\n
    If the password is not in the wordlist a message will be displayed stating so.\n
    Returns the password and displays it if found.
    """

    start_time = time.time()
    for word in [""] + wordlist:
        try:
            with Pdf.open(pdf_file_path, password=word):
                if not word:
                    return print(f"\n{Color.EMPHASIS}The PDF file provided is not encrypted.{Color.END}")
                print(f"\n\n{Color.INFORMATION}Password is: {Color.EMPHASIS}{word}{Color.END}")
                print(f"\n\n{Color.DETAIL}Found at index: {wordlist.index(word) + 1}\n")
                print(f"{Color.DETAIL}Time elapsed: {(time.time() - start_time):.3f} secs{Color.END}")
                return word
        except:
            print(f"{Color.INFORMATION} Trying: {Color.FAIL}{word}{Color.END}", end="\r")
    return print(f"\n\n{Color.EMPHASIS}No password matched from the provided wordlist.{Color.END}")


def run():
    os.system("color")
    args = cli_arguments()
    print(f"{Color.EMPHASIS}{TITLE}{Color.END}".center(500))
    pdf_path = get_valid_path(file_path=Path(args.pdf), prompt_title="PATH TO PDF")
    print(pdf_path, end="\n\n")
    wordlist_path = get_valid_path(file_path=Path(args.wordlist), prompt_title="PATH TO WORDLIST")
    print(wordlist_path)
    wordlist = wordlist_path.read_text(encoding=args.encoding).split("\n")
    print(f"\n{Color.DETAIL}Total wordcount: {len(wordlist)}{Color.END}")
    result = bruteforce_pdf(pdf_path, wordlist)
    if result:
        if args.output:
            Path(args.output).write_text(result)
        if args.copy:
            copy(result)


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"{Color.FAIL}<{e}> was raised!{Color.END}")
    close()