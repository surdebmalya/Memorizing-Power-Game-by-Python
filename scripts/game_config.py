import os

IMAGE_SIZE=128
SCREEN_SIZE=512
NUM_TILES_SIDE=4
NUM_TILES_TOTAL=16
MARGIN=4

BUTTON_WIDTH=500
BUTTON_HEIGHT=60

PROFILE_WIDTH=400
PROFILE_HEIGHT=385

INITIAL_POSITION_X=500
INITIAL_POSITION_Y=100

ASSET_DIR='assets'
ASSET_FILES=[x for x in os.listdir(ASSET_DIR) if x[-3:].lower()=='png']

assert len(ASSET_FILES)==8
#Checks the ASSET_FILES has 8 images or not
