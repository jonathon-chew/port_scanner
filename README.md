# Port Scanner

I built this project as a small command-line network diagnostic tool that checks whether ports are open on one or more hosts and reports the results clearly.

It is designed to be simple to run, easy to read in the terminal, and useful as a quick first-pass check when I want to understand what a machine is exposing on the network.

## What It Does

- scans a host across a range of ports
- reports ports as open, closed, or timed out
- supports a configurable timeout
- accepts either a single IP or a list of IPs
- provides straightforward CLI output

## Why I Built It

I wanted to practice socket programming, CLI design, and error handling in a way that felt practical. This project let me explore how connection timeouts behave, how to present scan results clearly, and how to structure a small Python package that can be installed and run from the command line.

## How To Run It

Install the project locally:

```bash
pip install -e .
```

Show the available options:

```bash
port-scanner --help
```

Scan a single host:

```bash
port-scanner --ip 127.0.0.1
```

Scan a list of hosts:

```bash
port-scanner --ip-range 192.168.1.10 192.168.1.11
```

Set a custom timeout:

```bash
port-scanner --ip 127.0.0.1 --timeout 0.5
```

Scan a custom list of ports:

```bash
port-scanner --ip 127.0.0.1 --ports 22 80 443
```

## What I Learned

- how socket connections behave under success, refusal, and timeout conditions
- how to turn low-level network logic into a usable CLI
- how to package a Python project with a console entry point
- how to make terminal output readable and useful in practice

## Future Improvements

- threaded scanning for faster results
- service name lookup
- banner grabbing
- UDP scanning exploration
