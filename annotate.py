import re
import sys
#for finite-state transducer (fallback processing)
import hfst
import codecs
#classes for random data selection and preprocessing
from preprocessing import selector, preprocessor
#linguistic rules and hierarchical FSAs for verse processing
from hAutomata import ruleset, HFSA13, HFSA14, HFSA15, HFSA16

####MAIN PROGRAM####	
	
infile = codecs.open(sys.argv[1], "r", "utf-8")
outfile = codecs.open(sys.argv[2], "w", "utf-8")

lines = infile.readlines()

#get a verse selector: use this to select and process a random subset of verses
#sel = selector()
#selection = sel.select(lines, 1)
#print(selection, file = outfile)

#get a preprocessor
prep = preprocessor()

hfsa13 = HFSA13('hfsa13')
hfsa14 = HFSA14('hfsa14')
hfsa15 = HFSA15('hfsa15')
hfsa16 = HFSA16('hfsa16')

#only for tracking number of lines with obviously erroneous syllabification
syll_counter = 0
#only for tracking number of short lines
short_counter = 0
#sentences with scansion annotation
scansion_counter = 0

for line in lines:
#for line in selection:
	scansion = ''
	
	vals = re.split(r'\t+', line.rstrip('\r?\n?'))
	
	#preprocessing
	text = prep.normalise(vals[1])
	#signal very short verses
	if prep.get_verse_length(text) < 4:
		short_counter+=1
	#selection of functions for syllabification
	##syllabified = prep.simple_syllabify(text)
	##syllabified = prep.vowel_syllabify(text)
	##syllabified = prep.cltk_syllabify(text)
	syllabified = prep.papakitsos_syllabify(text)
	syllable_count = prep.count_syllables(syllabified)
	
	#scansion annotation
	if syllable_count == 12:
		scansion = '-- -- -- -- -- -X'
		
	elif syllable_count == 13:
		scansion = 'one daktylus must be found'
		if hfsa13.state != 'waiting':
			hfsa13.to_waiting()
		hfsa13.set_text(syllabified)
		hfsa13.start_analysis()
		if hfsa13.state == 'daktylus_found':
			scansion = hfsa13.scansion
			scansion_counter += 1
		else:
			print('not found, fallback required')
			hfsa13.not_found()
		
	elif syllable_count == 14:
		scansion = 'two daktyles must be found'
		if hfsa14.state != 'waiting':
			hfsa14.to_waiting()
		hfsa14.set_text(syllabified)
		hfsa14.start_analysis()
		if hfsa14.state == 'found_two_daktyles':
			scansion = hfsa14.scansion
			scansion_counter += 1
		else:
			print('not found, fallback required')
			hfsa14.not_found()
	
	elif syllable_count == 15:
		scansion = 'two spondees must be found'
		if hfsa15.state != 'waiting':
			hfsa15.to_waiting()
		hfsa15.set_text(syllabified)
		hfsa15.start_analysis()
		if(hfsa15.state == 'found_two_spondees'):
			scansion = hfsa15.scansion
			scansion_counter += 1
		else:
			print('not found, fallback required')
			hfsa15.not_found()
		
	elif syllable_count == 16:
		scansion = 'one spondeus must be found'
		if hfsa16.state != 'waiting':
			hfsa16.to_waiting()
		hfsa16.set_text(syllabified)
		hfsa16.start_analysis()
		if(hfsa16.state == 'spondeus_found'):
			scansion = hfsa16.scansion
			scansion_counter += 1
		else:
			print('not found, fallback required')
			hfsa16.not_found()
		
	elif syllable_count == 17:
		scansion = '-** -** -** -** -** -X'
	
	else:
		print("WARNING: Incorrect syllable count: " + vals[0])
		syll_counter += 1
	
	#output
	print("{}\t{}\t{}\t{}".format(vals[0], vals[1], syllabified, scansion), file=outfile)

#log	
print(syll_counter, ' incorrectly syllabified verses')
print(short_counter, ' short verses')
print(scansion_counter, 'annotated verses')