# I don't know if you can source environment.sh from here.
# You'd save on repetitions if you could.

all: clean v4l2grab

clean:
	rm -f out/v4l2grab

clean-data: remove-all-photos remove-all-photosets remove-all-photos clean clear-last-photo

remove-all-photos:
	rm -f out/photos/*.jpg
remove-all-photosets:
	rm -f out/photosets/*.jpg
clear-photoset-queue:
	rm -f out/photoset_queue.csv
clear-last-photo:
	rm -f out/last_captured.txt

v4l2grab: src/v4l2grab.c
	mkdir -p out
	gcc $^ -o out/v4l2grab -Wall -ljpeg -DIO_READ -DIO_MMAP -DIO_USERPTR
