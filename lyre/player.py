from datetime import timedelta
from enum import Enum
import logging
from types import TracebackType
from pywinauto.controls.hwndwrapper import DialogWrapper  # type: ignore
import re
import time
from typing import Iterable, List, NamedTuple, Optional, Sequence, Type

_moduleLogger = logging.getLogger(__name__)
_moduleLogger.addHandler(logging.NullHandler())


class NoteType(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6


class Note(NamedTuple):
    note: NoteType
    octave: int

    _PATTERN = re.compile(r"([a-zA-Z])([0-9])")

    @classmethod
    def from_str(cls, text: str) -> Iterable["Note"]:
        for match in cls._PATTERN.finditer(text):
            note, octave = match.groups()
            try:
                yield Note(NoteType[note.upper()], int(octave))
            except Exception:
                _moduleLogger.error(f"Unable to parse {note}{octave}")
                pass


_KEYBOARD = {
    Note(NoteType.C, 3): "z",
    Note(NoteType.D, 3): "x",
    Note(NoteType.E, 3): "c",
    Note(NoteType.F, 3): "v",
    Note(NoteType.G, 3): "b",
    Note(NoteType.A, 4): "n",
    Note(NoteType.B, 4): "m",
    Note(NoteType.C, 4): "a",
    Note(NoteType.D, 4): "s",
    Note(NoteType.E, 4): "d",
    Note(NoteType.F, 4): "f",
    Note(NoteType.G, 4): "g",
    Note(NoteType.A, 5): "h",
    Note(NoteType.B, 5): "j",
    Note(NoteType.C, 5): "q",
    Note(NoteType.D, 5): "w",
    Note(NoteType.E, 5): "e",
    Note(NoteType.F, 5): "r",
    Note(NoteType.G, 5): "t",
    Note(NoteType.A, 6): "y",
    Note(NoteType.B, 6): "u",
}


def _get_keys(notes: Sequence[Note]) -> str:
    keys: List[str] = []
    for note in notes:
        key = _KEYBOARD.get(note, None)
        if key is None:
            _moduleLogger.warn(f"Cannot get key for {note}")
        else:
            keys.append(key)
    return "".join(keys)


class Chord(NamedTuple):
    time: float
    notes: str

    @classmethod
    def from_str(cls, tempo: timedelta, text: str) -> Optional["Chord"]:
        strings = text.split()
        time = strings[0]
        notes = strings[1:]
        _moduleLogger.debug(f"Matched time={time} notes={notes}")
        try:
            time = float(time)
            notes = Note.from_str("".join(notes))
            return Chord((tempo * time).total_seconds(), _get_keys(notes))
        except Exception:
            _moduleLogger.exception("")
        _moduleLogger.error(f"Unable to parse {text}")
        return None


class Player(object):
    def __init__(self, wrapper: DialogWrapper, loop: bool = False):
        self.wrapper = wrapper
        self.loop = loop

    def __enter__(self) -> "Player":
        self.wrapper.send_keystrokes("z")  # type: ignore
        time.sleep(1)
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        time.sleep(1)
        self.wrapper.send_keystrokes("{VK_ESCAPE}")  # type: ignore

    def play(self, chords: Sequence[Chord]):
        last_length = 0
        play = True
        while play:
            for chord in chords:
                _moduleLogger.debug(
                    f"Sleeping {chord.time} ms then playing {chord.notes}"
                )
                time.sleep(chord.time - (last_length * 0.02))
                last_length = len(chord.notes)
                if last_length > 0:
                    self.wrapper.send_keystrokes(chord.notes)  # type: ignore

            play = self.loop
