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
