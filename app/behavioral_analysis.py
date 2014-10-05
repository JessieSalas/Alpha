#!/usr/bin/env python
import happyfuntokenizing
from happyfuntokenizing import * 
import numpy as np 
import pandas as pd


def count_pos(tagged_words):
	"""return counts of each part of speech"""
	pos = {}
	for word in tagged_words:
		try:
			pos[word[1]] = pos[word[1]] + 1
		except KeyError:
			pos[word[1]] = 1
	return pos



def read_list(filename):
	lines = []
	with open(filename,'rb') as f:
		lines = [line.strip().lower() for line in f.readlines()]
	return lines

def count_words(msg):
	"""return dict of word counts in msg
	At this point not worth using sklearn data structs..."""
	counts = {}
	tokenizer = Tokenizer(preserve_case=False)
	toks = tokenizer.tokenize(msg)
	for word in toks:
		try:
			counts[word] = counts[word] + 1
		except KeyError:
			counts[word] = 1
	return counts


def count_trait_words(word_freqs, trait_words):
	"""given dict of word frequences, and a list of words representative
	of a trait, return percentage of words in msg that are relevant to trait"""
	# I think this should be frequencies, but if we primarily want something for
	# a graphic at this point I think we might need to do counts...
	total_words = sum(word_freqs.values())
	relevant_words = 0.0
	for word in trait_words:
		try:
			relevant_words += word_freqs[word]
		except KeyError:
			pass
	return relevant_words/total_words


def big_five(msg):
	"""
	calculate rough estimate on this based on occurrence of most relevant
	words according to 
	http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3783449/#pone.0073791.s002
	"Personality, Gender, and Age in the Language of Social Media: The Open-Vocabulary Approach"
	"""
	PATH = "big_five/"
	freqs = count_words(msg)
	files = ["agreeableness.txt", "disagreeable.txt", "open.txt", "closed.txt",
	"extraversion.txt", "introversion.txt", "unconscientious.txt", "conscientious.txt", 
	"neurotic.txt", "stability.txt"]
	traits = ["agreeable", "disagreeable", "open", "closed", "extraversion",
	"introversion", "unconscientious", "conscientious", "neurotic", "stability"]
	trait_words = {}
	for i in range(len(traits)):
		trait_words[traits[i]] = read_list(PATH + files[i])
	five = {}
	for trait in traits:
		five[trait] = count_trait_words(freqs,trait_words[trait])
	return five


def display_five(data):
	"""Creates graph of data"""
	pass


def features(msg):
	"""return dict of stats about msg
	msg is a string of all of a user's messages"""
	from nltk import word_tokenize, pos_tag
	hedges = ["i think", "kind of", "kinda", "i suppose", "sort of", "seems to me", 
	"i fancy", "somewhat", "apparent", "apparently", "alleged", "allegedly",
	"perhaps" ]
	self_ref = ["I", "me"] # use pure count? otherwise we'd need to find the threshold

	tagged = pos_tag(word_tokenize(msg['message']))
	pos_counts = count_pos(tagged)

	# introvert or extrovert features based on
	# https://www.aaai.org/Papers/JAIR/Vol30/JAIR-3012.pdf


	# postitive or negative sentiment
	# need to find corpus