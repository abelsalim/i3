from types import SimpleNamespace

i3 = SimpleNamespace()
monitor = SimpleNamespace()


# Relacionado a utilização do i3
i3.restart = 'i3-msg restart'


# Relacionado a utilização do xrandr
monitor.connected = "xrandr --verbose|grep connected|awk '{print $1}'"
monitor.active = (
    "xrandr --listactivemonitors|grep -v Monitors|awk '{print $4}'"
)
monitor.reolution = (
    "xrandr -q | grep '{}' -A1 | tail -n1 | awk '{{print $1}}'"
)
monitor.localizacao = (
    "xrandr -q | awk '/{}/' | awk -F '[ +]' '{{print $4 $5}}'"
)
monitor.dimension = (
    "xrandr|grep {}|awk '{{print $3}}'|awk -F + '{{print $2 $3}}'"
)
monitor.sync_main_monitors = (
    'xrandr --output {} --primary --mode {} --pos 0x768 --rotate normal'
)
monitor.sync_secondary_monitors = (
    ' --output {} --mode {} --pos 0x0 --rotate normal'
)
monitor.disable_secondary_monitors = ' --output {} --off'

# listas relacionadas ao xrandr
monitor.labels = ['active', 'connected']
monitor.commands = [monitor.active, monitor.connected]
