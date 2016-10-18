# -*- coding: utf-8 -*-
# NB: we're not reading the CSV file written during execution of the booth program.
#     Instead, we assume that photos in photosets are correctly ordered in
#     the photos directory. This assumption will turn out to be wrong if you put
#     photos in that directory without using the booth program, if you rename
#     existing photos or change their alphabetical order, or if you remove photos.

import os, sys
import pygame

PHOTOS_PATH = os.getenv('PHOTOMATON_PHOTOS_DIR')
PHOTOSETS_PATH = os.getenv('PHOTOMATON_PHOTOSETS_DIR')
PHOTOSET_PREFIX = os.getenv('PHOTOMATON_PHOTOSET_PREFIX')
PHOTO_WIDTH, PHOTO_HEIGHT = [int(os.getenv(e)) for e in ['PHOTOMATON_WEBCAM_PHOTO_WIDTH', 'PHOTOMATON_WEBCAM_PHOTO_HEIGHT']]

PHOTOSET_SIZE = (PHOTO_WIDTH*2, PHOTO_HEIGHT*2)

def run():
	pygame.init()
	
	photosets = []
	cur_photoset = []
	cur_photoset_count = 0
	
	# you could shorten this using a procedure that looks like:
	# partition : (List, Integer) -> List
	#             ([1,2,3,4,5,6], 2) -> [[1,2], [3,4], [5,6]]
	paths_to_photos = [os.path.join(PHOTOS_PATH, e) for e in os.listdir(PHOTOS_PATH)]
	paths_to_photos.sort()
	for photo_path in paths_to_photos:
		cur_photoset.append(photo_path)
		cur_photoset_count += 1
		if cur_photoset_count == 4:
			photosets.append(cur_photoset)
			cur_photoset = []
			cur_photoset_count = 0
	
	# you could also write
	# for i, paths in zip(range(len(photosets)), photosets):
	i = 1
	for paths in photosets:
		dest = pygame.surface.Surface(PHOTOSET_SIZE)
		surfaces = [pygame.image.load(p) for p in paths]
		dest.blit(surfaces[0], (0, 0))
		dest.blit(surfaces[1], (PHOTO_WIDTH, 0))
		dest.blit(surfaces[2], (0, PHOTO_HEIGHT))
		dest.blit(surfaces[3], (PHOTO_WIDTH, PHOTO_HEIGHT))
		
		photoset_path = os.path.join(PHOTOSETS_PATH, "%s%d.jpg" % (PHOTOSET_PREFIX, i))
		pygame.image.save(dest, photoset_path)
		i += 1

if __name__ == '__main__':
	run()
