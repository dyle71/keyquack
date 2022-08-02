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

import os
import pathlib
import sys
from typing import Set

import click
import pydub


def show_version(ctx, param, value):

    if not value or ctx.resilient_parsing:
        return

    import keyquack.__about__
    click.echo(f"{keyquack.__about__.__title__} V{keyquack.__about__.__version__}")
    click.echo(keyquack.__about__.__author__)
    click.echo(keyquack.__about__.__uri__)
    ctx.exit()


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.option('--version', '-v', is_flag=True, help='Show version and exit.')
def main(version=False) -> None:
    """Keyquack - annoy your colleagues while you type.

    Launch program, turn on your loudspeakers while in an open space,
    start typing and annoy everyone.
    """

    if version:
        show_version()
        sys.exit(0)

    print('blah')


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
