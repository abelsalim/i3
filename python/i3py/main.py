from i3py.models.monitor import Monitor
from i3py.utils.funcoes import argumentos_monitor


def main(active, disable):
    monitor = Monitor()

    if active:
        monitor.active()

    elif disable:
        monitor.disable()


if __name__ == '__main__':
    main(*argumentos_monitor())