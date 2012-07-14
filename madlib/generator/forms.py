from django import forms


class MultipleTextWidget(forms.TextInput):
	def render( self, name, value, attrs=None ):

		html = '<ol id="oldTitles">'
		for i,title in enumerate( value ):
			if i is len(value) - 1:
				html += '<li id="adder"><input type="text" name="%s" value="%s" id="id_%s" /></li>' % (name, title, name)
			else:
				html += '<li id="title_%d"><input type="text" name="%s" value="%s" /><button class="remove_title image" type="button" id="remove_title_%d" ><img src="/media/images/subtract.gif" id="remove_title_%d" /></button></li>' % (i,name, title, i, i)
		return html + '</ol>'

class MultipleTextField(forms.Field):
	def clean( self, value ):
		return value
		

class GeneratorForm(forms.Form):
	limit = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'short' }), initial=3, error_messages={'required': 'Please enter a limit' },  )
	encode_embedded_HTML = forms.BooleanField(required=False)
	campaign_name = forms.CharField(initial='Test campaign', required=False)
	description = forms.CharField(widget=forms.Textarea(attrs={'class': 'small'}), initial='This is a test campaign to demonstrate the madlib generator', required=False )
	
	titles = MultipleTextField(widget=MultipleTextWidget, initial='First {test|scenario}', error_messages={'required': 'Please enter at least one title' })
	madlib = forms.CharField(widget=forms.Textarea(attrs={'class': 'large'}), error_messages={'required': 'Please enter a madlib' }, initial='Madlib text for first {test|scenario}' )
	
	tags = forms.CharField(initial='awesome, amazing, nifty', required=False)
	excerpt = forms.CharField(widget=forms.Textarea(attrs={'class': 'small'}), initial="The first test of the madlib generator", required=False )
	categories = forms.CharField(initial="testing, generated data", required=False)