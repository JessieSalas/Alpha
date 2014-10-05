#!/usr/bin/env python
import happyfuntokenizing
import numpy as np 
import pandas as pd


def feature_weights(msg):
	if type(msg)!=dict:
		msg = pd.DataFrame.from_dict(msg)
	
