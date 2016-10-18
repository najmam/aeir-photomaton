# environment variables should be correctly set for this script to run
# cf run_photomaton.sh

datetime=`date +%Y-%m-%d_%Hh%Mm%Ss`
filename_for_this_image=${PHOTOMATON_PHOTOS_DIR}/${PHOTOMATON_PHOTO_PREFIX}${datetime}.jpg

$(${PHOTOMATON_COMMAND_FOR_PLAYING_COUNTDOWN_SFX})

${PHOTOMATON_OUT_DIR}/v4l2grab \
	-d ${PHOTOMATON_VIDEO_DEVICE} \
	-q 100 \
	-W ${PHOTOMATON_WEBCAM_PHOTO_WIDTH} \
	-H ${PHOTOMATON_WEBCAM_PHOTO_HEIGHT} \
	-o ${filename_for_this_image} \
&& echo ${filename_for_this_image} > ${PHOTOMATON_LAST_CAPTURED_TEXT_PATH}
