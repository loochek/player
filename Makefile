MIDIS=$(wildcard midis/*.mid)
ROLLS=${MIDIS:midis/%.mid=rolls/%.roll}

all: ${ROLLS}

rolls/%.roll: midis/%.mid
	./mid2roll.py $< $@
