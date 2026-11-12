# SkyBlaze - sound playback.
# (lines 29-32 and 119-143 of SkyBlaze_test_1.py, copied unchanged)

import os
import subprocess
import sys

try:                                    # sound on Windows
    import winsound
except ImportError:                     # Linux / macOS
    winsound = None

from helpers import asset


_sound_procs = []
_sound_enabled = True


def play_sound(name):
    """Play a wav file asynchronously on Windows / macOS / Linux (never crashes)."""
    global _sound_enabled
    if not _sound_enabled:
        return
    path = asset(name)
    if not os.path.exists(path):
        return
    try:
        if winsound is not None:
            winsound.PlaySound(path, winsound.SND_ASYNC | winsound.SND_FILENAME)
            return
        _sound_procs[:] = [p for p in _sound_procs if p.poll() is None]  # reap
        if len(_sound_procs) > 8:
            return
        player = "afplay" if sys.platform == "darwin" else "aplay"
        args = [player, path] if player == "afplay" else [player, "-q", path]
        _sound_procs.append(subprocess.Popen(
            args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    except Exception:
        _sound_enabled = False          # no audio player available
