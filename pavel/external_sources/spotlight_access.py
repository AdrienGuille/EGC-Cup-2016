__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'
LANG_PORTS = {
    "en": '2222',
    "german": '2226',
    "dutch": '2232',
    "hungarian": '2229',
    "fr": '2225',
    "portuguese": '2228',
    "italian": '2230',
    "russian": '2227',
    "turkish": '2235',
    "spanish": '2231'
}


def get_spotlight_annotation(text, lang="fr"):
    import spotlight
    try:
        annotations = spotlight.annotate('http://spotlight.sztaki.hu:{}/rest/annotate'.format(LANG_PORTS[lang]),
                                         text, confidence=0.6, support=20, spotter='Default')

    except:
        print "could not get info from spotlight"
        print text
        return []
    return annotations
