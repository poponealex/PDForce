<pre>
 ______ _____  _______                        
|   __ \     \|    ___|.-----.----.----.-----.
|    __/  --  |    ___||  _  |   _|  __|  -__|
|___|  |_____/|___|    |_____|__| |____|_____|
</pre>

## Lightweight PDF password cracker (bruteforce).

### REQUIREMENTS
- __PYTHON 3__

__You can find a `requirements.txt` file in this repository.__

> `pip install -r requirements.txt`

### USAGE
> `pdforce.py [-p <pdf>] [-w <wordlist>] [-e <encoding>] [-o <output>] [-c] [-v] [-h/--help]`
#### [-p <pdf>] - PDF FILE
> Path to the pdf file.
#### [-w <wordlist>] - WORDLIST
> Path to the wordlist.
#### [-e <encoding>] - ENCODING
> Specify an encoding for the wordlist (https://docs.python.org/3/library/codecs.html#standard-encodings). The default encoding is platform dependent. Use 'iso8859_2' for rockyou.
#### [-o <output>] - OUTPUT
> Output the cracked password to a new file.
#### [-c] - COPY
> Copy the password to the clipboard.
#### [-v] - VERBOSE
> Display additional information.
#### [-h/--help] - HELP
> Display help.

![PDForce](/misc/screenshot.png)

# ENJOY

## DISCLAIMER: USE FOR LEGAL INTENTS ONLY. YOU ARE SOLELY RESPONSIBLE FOR ANY MISUSE / ILLEGAL INTENT.
