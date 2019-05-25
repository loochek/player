MIDIS=$(wildcard *.mid)
CSVS=${MIDIS:%.mid=%.json}
JSONS=${MIDIS:%.mid=%.json}

all: ${JSONS}

%.json: %.csv
	py translator.py $< $@
	
%.csv: %.mid
	Midicsv.exe $< $@