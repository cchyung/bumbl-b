from __future__ import unicode_literals
from api.models import Snippet

def create_snippet(word, url, starttime, endtime):
  new_Snippet = Snippet(word=word, start=starttime, end=endtime, url=url)
  new_Snippet.save()
  print("Saved \"%s\" Snippet to database" % word)


