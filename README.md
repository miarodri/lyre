# lyre

## Description

`Lyre` is a python package that can read `.lyre` files and pass the notes to the currently running Genshin Impact instance. The program will pull up the lyre, play the song (possibly indefinitely), and close the lyre.

## Usage

### Running Lyre

`Lyre` requires Python 3.6^. The easiest way to run this is through [Poetry](https://python-poetry.org/). Using this, the package can be run with the following command:

```cmd
poetry run python -m lyre {.lyre file}
```

This package is not currently on PyPI.

At any point during execution, you can press `ctrl+c` on the terminal to prematurely end the performance.

### .lyre Files

`.lyre` files have a specific format, and are split into 2 parts:

* Header
  * One line at the top of the file
  * `{BPM} [loop]`
  * Example: `120 loop`
  * The BPM sets how much delay there is between full beats (set to `60_000 / BPM` ms)
  * `loop` is optional. Setting it will cause Lyre to repeat the song endlessly

* Body
  * Each line is a single chord played on the harp
  * `{Beats since last chord} {Notes in chord}`
  * Example: `1      C3  E3  G3`
  * Notes are written in standard notation
  * Valid notes are C3 - B6
  * No accidentals
  * The number of beats since the last chord is a float; 0.333 is a valid value

See the [examples](./examples) folder for and idea of what this looks like.

## Contributing

No plans for now. Message me if you want to add something.
