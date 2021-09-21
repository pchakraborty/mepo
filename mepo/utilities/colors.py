try:
    import colorama
    from colorama import Fore, Back, Style

    RED    = Fore.RED
    BLUE   = Fore.BLUE
    CYAN   = Fore.CYAN
    GREEN  = Fore.GREEN
    YELLOW = Fore.YELLOW
    RESET  = Style.RESET_ALL
except ImportError:
    RED    = "\x1b[1;31m"
    BLUE   = "\x1b[1;34m"
    CYAN   = "\x1b[1;36m"
    GREEN  = "\x1b[1;32m"
    YELLOW = "\x1b[1;33m"
    RESET  = "\x1b[0;0m"
