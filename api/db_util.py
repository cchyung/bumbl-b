from api.models import Snippet, Word, Audio
from api import models


def create_snippet(word, rawUrl, url, starttime, endtime):
    try:
        word_object = Word.objects.get(value=word)
    except models.Word.DoesNotExist:
        word_object = Word(value=word)
        word_object.save()

    audio_object = Audio.objects.get(url=rawUrl)
    new_Snippet = Snippet(word=word_object, audio=audio_object, start=starttime, end=endtime, url=url)
    new_Snippet.save()
    print "Saved \"%s\" Snippet to database" % word


def create_audio(name, url, description):
    audio = Audio(name=name, url=url, description=description)
    audio.save()

    print "Saved Audio \"%s\" to database" % audio
