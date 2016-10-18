# -*- coding: utf-8 -*-
import os, sys, commands, csv, datetime
import pygame

SHOULD_RUN_FULLSCREEN = os.getenv('PHOTOMATON_SHOULD_RUN_FULLSCREEN') == '1'
PATH_TO_LAST_CAPTURED_PHOTO = os.getenv('PHOTOMATON_LAST_CAPTURED_TEXT_PATH')
PATH_TO_PHOTOSETS_CSV = os.getenv('PHOTOMATON_PHOTOSETS_CSV_PATH')
COMMAND_FOR_TAKING_A_PHOTO = os.getenv('PHOTOMATON_COMMAND_FOR_TAKING_A_PHOTO') 
COMMAND_FOR_PLAYING_SUCCESS_SFX = os.getenv('PHOTOMATON_COMMAND_FOR_PLAYING_SUCCESS_SFX')
PATH_TO_BACKGROUND_IMAGE = "%s/background.png" % os.getenv('PHOTOMATON_RESOURCES_DIR')
PATH_TO_DEFAULT_QUADRANT_IMAGE = "%s/default.png" % os.getenv('PHOTOMATON_RESOURCES_DIR')
WINDOW_CAPTION = os.getenv('PHOTOMATON_WINDOW_CAPTION')
RENDERER_WIDTH, RENDERER_HEIGHT = [int(os.getenv(e)) for e in ['PHOTOMATON_UI_SCREEN_WIDTH', 'PHOTOMATON_UI_SCREEN_HEIGHT']]

# -----------------------------------------

QUADRANT_SIZE = QUADRANT_WIDTH, QUADRANT_HEIGHT = RENDERER_WIDTH/2, RENDERER_HEIGHT/2
QUADRANT_POSITIONS = [
	(0, 0),
	(QUADRANT_WIDTH, 0),
	(0, QUADRANT_HEIGHT),
	(QUADRANT_WIDTH, QUADRANT_HEIGHT),
]

def ptm_load_image_and_scale_into_quadrant(path):
	surface = pygame.image.load(path)
	scaled_surface = pygame.transform.scale(surface, QUADRANT_SIZE)
	return (path, scaled_surface)

SURFACE_FOR_DEFAULT_QUADRANT = ptm_load_image_and_scale_into_quadrant(PATH_TO_DEFAULT_QUADRANT_IMAGE)
SURFACE_FOR_BACKGROUND = pygame.transform.scale(pygame.image.load(PATH_TO_BACKGROUND_IMAGE), (RENDERER_WIDTH, RENDERER_HEIGHT))

# ----------------------------------------- state

# what to display on the next frame
# - 'idle' displays a background image
# - 'show_quadrants' displays the last 4 captured images
ptm_current_mode = 'idle'

# holds the 4 latest captured image as (path, pygame surface) tuples
ptm_quadrants = [SURFACE_FOR_DEFAULT_QUADRANT]*4

# -----------------------------------------

def ptm_last_captured_image_path():
	f = open(PATH_TO_LAST_CAPTURED_PHOTO, 'r')
	last_image_path = f.readline().strip()
	f.close()
	return last_image_path

def ptm_take_photo_then_display_into_quadrant(index_into_ptm_quadrants):
	output = commands.getstatusoutput(COMMAND_FOR_TAKING_A_PHOTO)
	if output[0] != 0:
		print("Error: failed to take a photo because this command failed : '%s'" % COMMAND_FOR_TAKING_A_PHOTO)
		print("stderr for that command:\n%s" % output[1])
		sys.exit(1)
	path = ptm_last_captured_image_path()
	ptm_quadrants[index_into_ptm_quadrants] = ptm_load_image_and_scale_into_quadrant(path)

def ptm_reset_quadrant(index):
	ptm_quadrants[index] = SURFACE_FOR_DEFAULT_QUADRANT

def ptm_write_photoset_filenames_into_csv():
	f = open(PATH_TO_PHOTOSETS_CSV, 'a+')
	writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow([os.path.basename(e[0]) for e in ptm_quadrants])
	f.close()
	print("[%s] Photoset successfully saved" % datetime.datetime.now().strftime('%H:%M:%S'))
	output = commands.getstatusoutput(COMMAND_FOR_PLAYING_SUCCESS_SFX)

def ptm_run():
	pygame.init()
	screen = pygame.display.set_mode((RENDERER_WIDTH, RENDERER_HEIGHT), pygame.FULLSCREEN if SHOULD_RUN_FULLSCREEN else 0, 32)
	pygame.display.set_caption(WINDOW_CAPTION)
	clock = pygame.time.Clock()
	
	def render():
		if ptm_current_mode == 'show_quadrants':
			for ptm_image, pos in zip(ptm_quadrants, QUADRANT_POSITIONS):
				path, image = ptm_image
				screen.blit(image, pos)
		elif ptm_current_mode == 'idle':
			screen.blit(SURFACE_FOR_BACKGROUND, (0,0))
		pygame.display.flip()

	def capture_one_photoset_then_revert_to_default_state():
		global ptm_current_mode
		ptm_current_mode = 'show_quadrants'
		render()
		for i in [0,1,2,3]:
			ptm_take_photo_then_display_into_quadrant(i)
			render()
		ptm_write_photoset_filenames_into_csv()

		for i in [0,1,2,3]:
			ptm_reset_quadrant(i)
		ptm_current_mode = 'idle'

	while True:
		clock.tick(40) # fps
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				capture_one_photoset_then_revert_to_default_state()
			elif event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key in [pygame.K_q, pygame.K_ESCAPE]):
				sys.exit(0)
		pygame.event.clear()
		render()

if __name__ == '__main__':
	ptm_run()
