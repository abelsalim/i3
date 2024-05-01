from types import SimpleNamespace

from i3py.constants.constants import i3, monitor
from i3py.utils.funcoes import stdout_run, no_stdout_run


class Monitor:

    def __init__(self):
        self._monitors_active = SimpleNamespace()
        self._monitors_connected = SimpleNamespace()
        self._xrandr_exec = ''
        self.atributos = [
            self._monitors_active,
            self._monitors_connected
        ]

    def restar_i3(self):
        no_stdout_run(i3.restart)

    def search_dict_primary(self):
        primary = next(
            filter(
                lambda x: x.get('primary'), self._monitors_connected.monitors
            )
        )

        self._xrandr_exec = monitor.sync_main_monitors.format(
            primary.get('monitor'),
            primary.get('resolution')
        )

    def get_resolution(self, displays, primary):
        lista_monitors = []

        for display in displays:
            # Captura resolução máxima dos dispositivos
            resolution = stdout_run(monitor.reolution.format(display))

            # Captura localização do monitor
            localizacao = stdout_run(monitor.localizacao.format(display))

            lista_monitors.append(
                {
                    'monitor': display,
                    'resolution': resolution.replace('\n', ''),
                    'localizacao': localizacao.replace('\n', ''),
                    'primary': True if display in primary else False
                }
            )

        return lista_monitors

    def search_monitors(self):
        for atributo, command in zip(self.atributos, monitor.commands):
            # Captura dispositivos conectados
            monitors = stdout_run(command)

            # Gera lista com nome dos dispositivos
            monitors = monitors.strip().split('\n')

            if command == monitor.active:
                primary = monitors[0]

            # Quantidade de monitores
            atributo.number = len(monitors)
            # Dicionario dos monitores e resoluções
            atributo.monitors = self.get_resolution(monitors, primary)

    def _aplica_logica_condicional_nos_monitores(self):
        for index, dicionario in enumerate(self._monitors_connected.monitors):
            # Entra se for o primeiro índice
            if not index:
                # Nesse ponto estamos pegando o primeiro monitor visando a
                # usabilidade em notbook, pois o monitor embutido não
                # necessariamente é o primário, mas sempre será é o primeiro
                # listado pelo xrandr.
                # Nota: O padão eDP-1 não é levado em consideração pois
                # adaptadores usb-c ficam contém a mesma nomenclatura.
                self._xrandr_exec += monitor.sync_main_monitors.format(
                    dicionario.get('monitor'),
                    dicionario.get('resolution')
                )
                continue

            valor_logico = (
                self._monitors_active.number - self._monitors_connected.number
            )

            # Se >= -1 (True), então ativa (monitor.sync_secondary_monitors)
            # Se = 0 (False) então desativa (monitor.disable_secondary_monitors)
            self._xrandr_exec += (
                monitor.sync_secondary_monitors.format(
                    dicionario.get('monitor'),
                    dicionario.get('resolution')
                )
                if (
                    valor_logico or
                    not valor_logico and dicionario.get('localizacao') != '00'
                )
                else monitor.disable_secondary_monitors.format(
                    dicionario.get('monitor')
                )
            )

    def active_disable(self):
        self.search_monitors()
        self._xrandr_exec = ''

        # Aplica lógica dos monitores
        self._aplica_logica_condicional_nos_monitores()

        # Ativa monitores e reinia i3
        no_stdout_run(self._xrandr_exec)
        self.restar_i3()
