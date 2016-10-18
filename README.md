### Installation

You'll need :
- a machine that runs Linux (either 32- or 64-bit)
- Python 2.7.x
- the Pygame library for Python. Install it with `sudo pip2 install pygame`
- `sox`, which provides the `play` binary for playing audio files.  
	You can change the command used to play audio files in `src/environment.sh`.
  If you only need to play WAV files, you can use `aplay`, which is installed
  by default on some Linux distributions.
- GCC, for compiling `src/v4l2grab.c` for your architecture.

### Configuration

- edit `src/environment.sh`. Make sure the widths and heights match
  those of your screen and video capture device
- `cd` into the directory that contains `README.txt`
- run `make`

### How to run

- make sure to give `booth` a run before the event, on the exact same hardware
you'll be using during the event
- during the event, run `./booth`. The photos will be stored in `out/photos`
- after the event, run `./pack_photos_by_four_into_photosets` and look at the result in `out/photosets`

### Caveats

- not tested when the aspect ratio of the webcam doesn't match that of the screen

### References

- `v4l2grab.c` comes from [here](http://www.twam.info/linux/v4l2grab-grabbing-jpegs-from-v4l2-devices)

### Authors

- 2012 : Naji Mammeri `naji@pascience.net`

### License

Public domain
