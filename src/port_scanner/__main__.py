import socket, sys, re
from typing import Any

from pyflags.flag import Flags
import Adonis

RANGE_DEFAULT = [x for x in range(0, 80)]
PORT_DEFAULT = [53, 80, 443]


def is_ipAddress(input: str) -> bool:

    if re.match(
        "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        input,
    ):
        return True
    else:
        return False


def cli() -> Flags:
    flags = Flags()

    flags.add(
        ["--range"],
        "The range of ports that should be scanned",
        list[int],
        default=RANGE_DEFAULT,
        custom_parse=lambda x: int(x),
        validator=lambda x: x <= 65535,
    )
    flags.add(
        ["--ports"],
        "The list of ports that should be scanned",
        list[int],
        default=PORT_DEFAULT,
        custom_parse=lambda x: int(x),
        validator=lambda x: x <= 65535,
    )
    flags.add(["--ip"], "The ip to be scanned", str, validator=is_ipAddress)
    flags.add(
        ["--timeout"],
        "the number of seconds before the scan should time out",
        float,
        default=0.2,
    )
    flags.add(
        ["--ip-range"], "The ip range to be scanned", list[str], validator=is_ipAddress
    )

    flags.add(["--help", "-h"], "give me a help menu", bool)
    flags.add(["--verbose"], "Print out everything", bool, False)

    flags.parse_and_resolve(sys.argv[1:])

    return flags


def is_port_open(host: str, port: int, flag: Flags) -> dict[str, Any]:
    """
    determine whether `host` has the `port` open
    """
    # creates a new socket
    s = socket.socket()
    try:
        # make timeout if you want it a little faster ( less accuracy )
        s.settimeout(flag.timeout)

        # tries to connect to host using that port
        s.connect((host, port))
    except Exception as e:
        # cannot connect, port is closed
        # return false
        return {"open": False, "reason": str(e)}
    else:
        # the connection was established, port is open!
        return {"open": True, "reason": ""}
    finally:
        s.close()


def print_port_results(ip, port, flags):
    response = is_port_open(ip, port, flag=flags)
    print(VERBOSE)
    if response["open"]:
        Adonis.PrintInfo(f"\n[+] {ip}:{port} is open", end="\n")
        SEEN = True
    elif "timed out" in response["reason"]:
        Adonis.PrintWarning(
            f"\x1b[2K[!] {ip}:{port} timedout {response['reason']}",
            end="\n" if VERBOSE else "\r",
        )
    else:
        Adonis.PrintWarning(
            f"\x1b[2K[!] {ip}:{port} is closed {response['reason']}",
            end="\n" if VERBOSE else "\r",
        )


def scan_ports(ip, flags):

    default_range = flags.range == RANGE_DEFAULT
    default_port = flags.ports == PORT_DEFAULT

    # If the range isn't the deafult ports is
    if not default_range and default_port:
        for port in range(min(flags.range), max(flags.range) + 1):
            print_port_results(ip, port, flags)

    # Ports isn't just the default
    elif not default_port:
        for port in flags.ports:
            print_port_results(ip, port, flags)

    else:
        for port in range(min(flags.range), max(flags.range) + 1):
            print_port_results(ip, port, flags)


def main():
    flags = cli()
    # iterate over ports, from 1 to 1024

    VERBOSE = flags.verbose

    if flags.help:
        print(flags.help_text_ordered())
        exit(0)

    if flags.ip is None and flags.ip_range is None:
        Adonis.PrintError("No ip addresses found in the input")
        print(flags.help_text_ordered())
        exit(1)

    if flags.ip_range:
        for idx in range(0, len(flags.ip_range)):
            ip = flags.ip_range[idx]
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                print(f"Looking at: {hostname}")
            except:
                pass
            scan_ports(ip, flags)
    else:
        try:
            hostname = socket.gethostbyaddr(flags.ip)[0]
            print(f"Looking at: {socket.gethostbyaddr(flags.ip)[0]}")
        except:
            pass

        scan_ports(flags.ip, flags)

    if not SEEN:
        print(f"{Adonis.Ansi.reset}No open ports found: {flags.ip}")


if __name__ == "__main__":
    SEEN = False
    VERBOSE = False
    main()
