"""Sound playback that works on Windows, macOS and Linux without extra packages.

Windows uses the standard-library ``winsound``; macOS and Linux shell out to
``afplay`` / ``aplay`` when available. If no backend exists, or a sound file is
missing, the game runs silent instead of crashing.
"""

import logging
import shutil
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

_warned = set()


def _select_backend():
    """Return a ``play(path)`` callable for this platform, or None."""
    if sys.platform == "win32":
        import winsound

        def play_with_winsound(path):
            winsound.PlaySound(str(path), winsound.SND_ASYNC)

        return play_with_winsound

    command = "afplay" if sys.platform == "darwin" else "aplay"
    executable = shutil.which(command)
    if executable is None:
        logger.info("No sound player (%s) found; running without sound.", command)
        return None

    extra_args = ["-q"] if command == "aplay" else []

    def play_with_command(path):
        subprocess.Popen(
            [executable, *extra_args, str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    return play_with_command


_backend = _select_backend()


def _warn_once(key, message, *args):
    # A missing file would otherwise log on every shot.
    if key not in _warned:
        _warned.add(key)
        logger.warning(message, *args)


def play(path):
    """Play ``path`` asynchronously. Audio problems are logged, never raised."""
    if _backend is None:
        return
    path = Path(path)
    if not path.is_file():
        _warn_once(path, "Sound file not found: %s", path)
        return
    try:
        _backend(path)
    except (OSError, RuntimeError) as error:
        _warn_once(path, "Could not play %s: %s", path, error)
