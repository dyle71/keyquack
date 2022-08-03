#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
# keyquack/__main__.py
#
# keyquack package startup.
#
# (C) Copyright 2022, see the 'LICENSE' file in the project root.
# Oliver Maurhart, headcode.space, https://headcode.space
# ------------------------------------------------------------

"""This is the keyquack package start script."""

import dataclasses
import os
import pathlib
import subprocess
import sys
import tempfile
from typing import Dict, Optional, Set, Tuple

import click
import pydub
import pydub.exceptions
import pydub.playback
import pydub.utils
import pynput


DEFAULT_SOUND: str = 'quack'

SoundDB = Dict[str, Tuple[pydub.AudioSegment, Optional[str]]]


def load_base_sounds() -> SoundDB:
    """Loads all base sounds.

    :return:    Dictionary of sound name to (sound audio segment, temp. WAV file path).
    """

    res: SoundDB = {}

    paths = search_paths()
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                sound_file = os.path.join(dirpath, filename)
                try:
                    sound = pydub.AudioSegment.from_file(sound_file)
                    sound_name = pathlib.Path(dirpath) / pathlib.Path(filename).stem
                    sound_name = pathlib.Path(sound_name).relative_to(path)
                    res[str(sound_name)] = (sound, None)

                except pydub.exceptions.CouldntDecodeError:
                    sys.stderr.write(f"Failed to load: {sound_file}.")

    return res


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.option('--list-only', '-l', is_flag=True, help='Only list current found base sounds.')
@click.option('--sound', '-s', type=str, default=DEFAULT_SOUND, show_default=True,
              help='Default base sound to load.')
@click.option('--version', '-v', is_flag=True, help='Show version and exit.')
def main(list_only=False, sound='', version=False) -> None:
    """Keyquack - annoy your colleagues while you type.

    Launch program, turn on your loudspeakers while in an open space,
    start typing and annoy everyone.
    """

    @dataclasses.dataclass
    class Quacker:

        default_sound: str
        sound_db: SoundDB
        temp_dir: str

        def on_key_press(self, key: pynput.keyboard.KeyCode) -> None:
            """A keyboard key has been pressed."""
            quack = f"{self.default_sound}_{key!s}"
            if quack not in self.sound_db:
                quack = self.default_sound
            play(sound=quack, sound_db=self.sound_db, temp_dir=self.temp_dir)

        def run(self):
            with pynput.keyboard.Listener(on_press=self.on_key_press) as listener:
                listener.join()

    if version:
        show_version()
        sys.exit(0)

    base_sounds = load_base_sounds()
    if list_only:
        print('Available sounds:')
        for sound_name in base_sounds:
            print(sound_name)
        sys.exit(0)

    if sound not in base_sounds:
        sys.stderr.write(f"Cannot find sound '{sound}' in base sounds.\n")
        sys.stderr.write('List available sounds with --list-only option.\n')
        sys.stderr.write('Please specify alternative with --sound option.\n')
        sys.exit(1)

    with tempfile.TemporaryDirectory() as temp_dir:
        quacker = Quacker(default_sound=sound, sound_db=base_sounds, temp_dir=temp_dir)
        quacker.run()


def play(sound: str, sound_db: SoundDB, temp_dir: str) -> None:
    """Plays the given audio file.

    :param sound:           The sound to play.
    :param sound_db:        The sound database play.
    :param temp_dir:        Path to temporary directory.
    """
    if sound not in sound_db:
        raise RuntimeError(f"Sound '{sound}' not found in sound database.")

    if sound_db[sound][1] is None:
        save_wav(sound=sound, sound_db=sound_db, temp_dir=temp_dir)

    player = pydub.utils.get_player_name()
    cmd = [player, "-nodisp", "-autoexit", "-hide_banner", sound_db[sound][1]]
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def save_wav(sound: str, sound_db: SoundDB, temp_dir: str) -> None:
    """Produces a WAV file of the given sound and stores it in the temporary directory.

    :param sound:           The sound to play.
    :param sound_db:        The sound database play.
    :param temp_dir:        Path to temporary directory.
    """

    if sound not in sound_db:
        raise RuntimeError(f"Sound '{sound}' not found in sound database.")

    wav_file_name = os.path.join(temp_dir, f"{sound}.wav")
    sound_db[sound][0].export(wav_file_name, "wav")
    sound_db[sound] = (sound_db[sound][0], wav_file_name)


def search_paths() -> Set[str]:
    """Get the system search paths where sound files *could* be found.

    :return:    Set of folders possible holding possible sound files.
    """
    res = set()

    keyquack_sounds = os.path.join('share', 'keyquack')
    res.add(os.path.join(sys.prefix, keyquack_sounds))

    if sys.platform in ['linux', 'aix', 'cygwin']:
        res.add(os.path.join('/usr', keyquack_sounds))
        res.add(os.path.join('/usr/local', keyquack_sounds))
        res.add(os.path.join('/var/lib', os.path.join('keyquack')))

    for folder in [folder for folder in sys.path if os.path.isdir(folder)]:
        if os.path.split(folder)[1] in ['site-packages', 'dist-packages']:
            prefix = pathlib.Path(folder).parents[2]
            res.add(os.path.join(prefix, keyquack_sounds))
        else:
            res.add(os.path.join(folder, keyquack_sounds))

    return res


def show_version():
    """Show program version and exit."""
    import keyquack.__about__
    click.echo(f"{keyquack.__about__.__title__} V{keyquack.__about__.__version__}")
    click.echo(f"{keyquack.__about__.__summary__}\n")
    click.echo(f"{keyquack.__about__.__author__}, {keyquack.__about__.__email__}")
    click.echo(keyquack.__about__.__uri__)
    sys.exit()


def speed_change(sound: pydub.AudioSegment, speed: float = 1.0) -> pydub.AudioSegment:
    """Increase speed of song therefore increase or decrease frequencies.

    :param sound:       The sound to modify.
    :param speed:       Speedup.
    :return:            Modified sound.
    """
    # Taken from https://stackoverflow.com/a/51434954/8754067
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


if __name__ == '__main__':
    main(prog_name='keyquack')
