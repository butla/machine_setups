import logging
from pathlib import Path
import platform


CONFIG_TEMPLATE = """
font:
  size: {font_size}
"""

MACHINE_SPECIFIC_CONFIG_LOCATION = Path('~/.config/alacritty/machine-specific.yml').expanduser()

FONT_SIZE_OVERRIDES = {
    'bl': 13
}
DEFAULT_FONT_SIZE = 11.5

log = logging.getLogger(__name__)


def setup():
    current_host = platform.node()
    config = CONFIG_TEMPLATE.format(
        font_size=FONT_SIZE_OVERRIDES.get(current_host, DEFAULT_FONT_SIZE)
    )

    current_config = ''
    if MACHINE_SPECIFIC_CONFIG_LOCATION.exists():
        current_config = MACHINE_SPECIFIC_CONFIG_LOCATION.read_text()

    if config == current_config:
        log.info("%s doesn't need updating.", MACHINE_SPECIFIC_CONFIG_LOCATION)
    else:
        MACHINE_SPECIFIC_CONFIG_LOCATION.write_text(config)
        log.info(
            'Alacritty machine specific config (%s) is set to:\n%s',
            MACHINE_SPECIFIC_CONFIG_LOCATION,
            config,
        )
