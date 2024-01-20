import argparse

from subprocess import run, PIPE


def stdout_run(command):
    return run(
        command,
        shell=True,
        stdout=PIPE,
        universal_newlines=True
    ).stdout


def no_stdout_run(command):
    return run(
        command,
        shell=True,
    ).stdout


def argumentos_monitor():
    parser = argparse.ArgumentParser(
        description='Monta xml Security Odoo'
    )

    parser.add_argument(
        '-a',
        '--active',
        action='store_true',
        help='Conectar monitores externos'
    )

    parser.add_argument(
        '-d',
        '--disable',
        action='store_true',
        help='Desconectar monitores externos'
    )

    args = parser.parse_args()

    return (args.active, args.disable)
