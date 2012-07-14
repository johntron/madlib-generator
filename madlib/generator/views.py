from __future__ import with_statement
from types import *
from copy import copy
import string
import cPickle
import itertools
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.forms.util import ErrorList
from madlib.generator.models import Madlib, MarkupException
from madlib.generator.forms import GeneratorForm
from madlib.generator.tokenizer import MadlibTokenizer
from madlib.settings import DATA_DIR

def edit ( request, id=False ) :
	if request.method == 'POST':
		req = copy( request.POST )
		req['titles'] = req.getlist( 'titles' )
		form = GeneratorForm( req )
		if ( form.is_valid() ):
		
			# Save form data
			data = copy( form.cleaned_data )
			with open("%s/formdata.txt" % DATA_DIR, 'wb' ) as f:
				cPickle.dump( data, f, cPickle.HIGHEST_PROTOCOL )
				
			# Number of articles to generate
			num_articles = int( form.cleaned_data[ 'limit' ] )
			
			# Generate the bodies
			try:
				madlib = Madlib()
				madlib.parse( form.cleaned_data[ 'madlib' ] )
				bodies = []
				while len(bodies) < num_articles:
					bodies.append( madlib.generate() )
	
				# Generate the titles
				titles = []
				it = itertools.cycle( form.data['titles'] )
				while len(titles) < num_articles:
					madlib = Madlib()
					madlib.parse( it.next() )
					titles.append( madlib.generate() )
	
				# Compile results
				results = []
				for i in range(0, num_articles):
					results.append( ( titles[i], bodies[i] ) )
			except MarkupException as e:
				return HttpResponse( e )
			# Show madlibs
			return render_to_response( 'results.html', { 'results': results, 'form': form.cleaned_data, 'encode_html': form.cleaned_data[ 'encode_embedded_HTML' ] }, mimetype="text/plain" )
		else:
			raise Exception( "Uh oh, John didn't account for something" )
	else:
		initial = {}
		with open("%s/formdata.txt" % DATA_DIR, 'rb' ) as f:
			try:
				initial = cPickle.load( f )
			except:
				pass
		form = GeneratorForm(initial=initial)

	return render_to_response( 'generator.html', { 'form': form } )
