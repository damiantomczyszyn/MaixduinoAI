"""Unittests for emoji.core"""

import random
import re
import emoji
import pytest
import unicodedata

# Build all language packs (i.e. fill the cache):
emoji.emojize("", language="alias")
for lang_code in emoji.LANGUAGES:
    emoji.emojize("", language=lang_code)


def ascii(s):
    # return escaped Code points \U000AB123
    return s.encode("unicode-escape").decode()


def all_language_and_alias_packs():
    yield ('alias', emoji.unicode_codes.get_aliases_unicode_dict())

    for lang_code in emoji.LANGUAGES:
        yield (lang_code, emoji.unicode_codes.get_emoji_unicode_dict(lang_code))


def normalize(form, s):
    return unicodedata.normalize(form, s)


def test_emojize_name_only():
    # Check that the regular expression emoji.core._EMOJI_NAME_PATTERN contains all the necesseary characters
    from emoji.core import _EMOJI_NAME_PATTERN

    pattern = re.compile('[^%s]' % (_EMOJI_NAME_PATTERN, ))

    for lang_code, emoji_pack in all_language_and_alias_packs():
        for name_in_db in emoji_pack.keys():

            pairs = [
                ('Form from EMOJI_DATA', name_in_db),
                ('NFKC', normalize('NFKC', name_in_db)),
                ('NFKD', normalize('NFKD', name_in_db)),
                ('NFD', normalize('NFD', name_in_db)),
                ('NFC', normalize('NFC', name_in_db))
            ]
            for form, name in pairs:
                actual = emoji.emojize(name, language=lang_code)
                expected = emoji_pack[name_in_db]

                if expected != actual:
                    print("Regular expression is missing a character:")
                    print("Emoji name %r in form %r contains:" % (name, form))
                    print("\n".join(["%r (%r) is not in the regular expression" % (x, x.encode('unicode-escape').decode()) for x in pattern.findall(name[1:-1])]))

                assert expected == actual, '%s != %s' % (expected, actual)
                assert pattern.search(name[1:-1]) is None


def test_regular_expression_minimal():
    # Check that the regular expression emoji.core._EMOJI_NAME_PATTERN only contains the necesseary characters
    from emoji.core import _EMOJI_NAME_PATTERN

    pattern_str = '[^%s]' % (_EMOJI_NAME_PATTERN, )
    i = 2
    while i < len(pattern_str) - 1:
        c = pattern_str[i]
        if c == '\\':
            i += 2
            continue
        pattern = re.compile(pattern_str.replace(c, ''))
        failed = False
        for lang_code, emoji_pack in all_language_and_alias_packs():
            for name_in_db in emoji_pack.keys():
                name_in_db = name_in_db[1:-1]
                names = [
                    name_in_db,
                    normalize('NFKC', name_in_db),
                    normalize('NFKD', name_in_db),
                    normalize('NFD', name_in_db),
                    normalize('NFC', name_in_db)
                ]
                for str in names:
                    if pattern.search(str):
                        failed = True
                        break
            if failed:
                break
        if not failed:
            assert failed, "char: %r is not necessary in regular expression" % (c, )

        i += 1


def test_emojize_complicated_string():
    # A bunch of emoji's with UTF-8 strings to make sure the regex expression is functioning
    name_code = {
        ':flag_for_Ceuta_&_Melilla:': '\U0001F1EA\U0001F1E6',
        ':flag_for_St._Barthélemy:': '\U0001F1E7\U0001F1F1',
        ':flag_for_Côte_d’Ivoire:': '\U0001F1E8\U0001F1EE',
        ':flag_for_Åland_Islands:': '\U0001F1E6\U0001F1FD',
        ':flag_for_São_Tomé_&_Príncipe:': '\U0001F1F8\U0001F1F9',
        ':flag_for_Curaçao:': '\U0001F1E8\U0001F1FC'
    }
    string = ' complicated! '.join(list(name_code.keys()))
    actual = emoji.emojize(string)
    expected = string
    for name, code in name_code.items():
        expected = expected.replace(name, code)
    expected = emoji.emojize(actual)
    assert expected == actual, '%s != %s' % (expected, actual)


def test_emojize_languages():
    for lang_code, emoji_pack in emoji.unicode_codes._EMOJI_UNICODE.items():
        for name, emj in emoji_pack.items():
            assert emoji.emojize(name, language=lang_code) == emj


def test_demojize_languages():
    for lang_code, emoji_pack in emoji.unicode_codes._EMOJI_UNICODE.items():
        for name, emj in emoji_pack.items():
            assert emoji.demojize(emj, language=lang_code) == name


def test_emojize_variant():
    def remove_variant(s): return re.sub('[\ufe0e\ufe0f]$', '', s)

    assert emoji.emojize(
        ':Taurus:', variant=None) == emoji.unicode_codes._EMOJI_UNICODE['en'][':Taurus:']
    assert emoji.emojize(':Taurus:', variant=None) == emoji.emojize(':Taurus:')
    assert emoji.emojize(':Taurus:', variant='text_type') == remove_variant(
        emoji.unicode_codes._EMOJI_UNICODE['en'][':Taurus:']) + '\ufe0e'
    assert emoji.emojize(':Taurus:', variant='emoji_type') == remove_variant(
        emoji.unicode_codes._EMOJI_UNICODE['en'][':Taurus:']) + '\ufe0f'

    assert emoji.emojize(
        ':admission_tickets:', variant=None) == emoji.unicode_codes._EMOJI_UNICODE['en'][':admission_tickets:']
    assert emoji.emojize(':admission_tickets:', variant=None) == emoji.emojize(
        ':admission_tickets:')
    assert emoji.emojize(':admission_tickets:', variant='text_type') == remove_variant(
        emoji.unicode_codes._EMOJI_UNICODE['en'][':admission_tickets:']) + '\ufe0e'
    assert emoji.emojize(':admission_tickets:', variant='emoji_type') == remove_variant(
        emoji.unicode_codes._EMOJI_UNICODE['en'][':admission_tickets:']) + '\ufe0f'

    with pytest.raises(ValueError):
        emoji.emojize(':admission_tickets:', variant=False)

    with pytest.raises(ValueError):
        emoji.emojize(':admission_tickets:', variant=True)

    with pytest.raises(ValueError):
        emoji.emojize(':admission_tickets:', variant='wrong')

    assert emoji.emojize(":football:") == ':football:'
    assert emoji.emojize(":football:", variant="text_type") == ':football:'
    assert emoji.emojize(":football:", language="alias") == '\U0001F3C8'
    assert emoji.emojize(":football:", variant="emoji_type", language="alias") == '\U0001F3C8'


def test_demojize_removes_variant():
    # demojize should remove all variant indicators \ufe0e and \ufe0f from the string
    text = "".join([emoji.emojize(':Taurus:', variant='text_type'),
                    emoji.emojize(':Taurus:', variant='emoji_type'),
                    emoji.emojize(':admission_tickets:', variant='text_type'),
                    emoji.emojize(':admission_tickets:', variant='emoji_type'),
                    emoji.emojize(':alien:', variant='text_type'),
                    emoji.emojize(':alien:', variant='emoji_type'),
                    emoji.emojize(':atom_symbol:', variant='text_type'),
                    emoji.emojize(':atom_symbol:', variant='emoji_type')])

    for lang_code in emoji.LANGUAGES:
        result = emoji.demojize(text, language=lang_code)
        assert '\ufe0e' not in result
        assert '\ufe0f' not in result


def test_emojize_invalid_emoji():
    string = '__---___--Invalid__--__-Name'
    assert emoji.emojize(string) == string

    string = ':: baby:: :_: : : :  : :-: :+:'
    assert emoji.emojize(string) == string


def test_emojize_version():
    assert emoji.emojize("Flags like :Belgium: are in version 2.0", version=1.0) == "Flags like  are in version 2.0"
    assert emoji.emojize("Flags like :Belgium: are in version 2.0", version=1.9) == "Flags like  are in version 2.0"
    assert emoji.emojize("Flags like :Belgium: are in version 2.0", version=2.0) == "Flags like 🇧🇪 are in version 2.0"
    assert emoji.emojize("Flags like :Belgium: are in version 2.0", version=3.0) == "Flags like 🇧🇪 are in version 2.0"
    assert emoji.emojize("Boxing gloves :boxing_glove: are in version 3.0", version=0) == "Boxing gloves  are in version 3.0"
    assert emoji.emojize("Boxing gloves :boxing_glove: are in version 3.0", version=1) == "Boxing gloves  are in version 3.0"
    assert emoji.emojize("Boxing gloves :boxing_glove: are in version 3.0", version=2) == "Boxing gloves  are in version 3.0"
    assert emoji.emojize("Boxing gloves :boxing_glove: are in version 3.0", version=3) == "Boxing gloves 🥊 are in version 3.0"
    assert emoji.emojize("Boxing gloves :boxing_glove: are in version 3.0", version=4) == "Boxing gloves 🥊 are in version 3.0"

    assert emoji.emojize("Biking :man_biking: is in 4.0", version=3.0, handle_version='<emoji>') == "Biking <emoji> is in 4.0"
    assert emoji.emojize("Biking :man_biking: is in 4.0", version=3.0, handle_version=lambda e, data: '<emoji>') == "Biking <emoji> is in 4.0"
    assert emoji.emojize("Biking :man_biking: is in 4.0", version=3.0, handle_version=lambda e, data: data["fr"]) == "Biking :cycliste_homme: is in 4.0"

    def f(emj, data):
        assert data['E'] == 5

    assert emoji.emojize(':bowl_with_spoon:', version=-
                         1, handle_version=f) == ''
    assert emoji.emojize(':bowl_with_spoon:') == '\U0001F963'
    assert emoji.emojize(':bowl_with_spoon:', version=4) == ''
    assert emoji.emojize(':bowl_with_spoon:', version=4.9) == ''
    assert emoji.emojize(':bowl_with_spoon:', version=5) == '\U0001F963'
    assert emoji.emojize(':bowl_with_spoon:', version=5.1) == '\U0001F963'
    assert emoji.emojize(':bowl_with_spoon:', version=6) == '\U0001F963'
    assert emoji.emojize(':bowl_with_spoon:', version=4,
                         handle_version='abc') == 'abc'
    assert emoji.emojize(':bowl_with_spoon:', version=4,
                         handle_version=None) == ''
    assert emoji.emojize(':bowl_with_spoon:', version=4,
                         handle_version='') == ''
    assert emoji.emojize(':bowl_with_spoon:', version=4,
                         handle_version=lambda e, d: str(d['E'])) == '5'


def test_demojize_version():

    assert emoji.emojize('A :T-Rex: is eating a :croissant:', version=3.0) == 'A  is eating a 🥐'

    assert emoji.emojize('A :T-Rex: is eating a :croissant:', version=3.0, handle_version='[Unsupported emoji]') == 'A [Unsupported emoji] is eating a 🥐'

    assert emoji.demojize('A 🦖 is eating a 🥐', version=3.0) == 'A  is eating a :croissant:'

    assert emoji.demojize('A 🦖 is eating a 🥐', handle_version='X', version=3.0) == 'A X is eating a :croissant:'

    assert emoji.demojize('A 🦖 is eating a 🥐', handle_version='X', version=5.0) == 'A :T-Rex: is eating a :croissant:'


def test_alias():
    # When lanugage != "alias" aliases should be passed through untouched
    assert emoji.emojize(':soccer:') == ':soccer:'
    assert emoji.emojize(':soccer:', language="alias") == '\U000026BD'
    assert emoji.emojize(':football:') == ':football:'
    assert emoji.emojize(':football:', language="alias") == '\U0001F3C8'
    # Multiple aliases for one emoji:
    assert emoji.emojize(':thumbsup:', language="alias") == emoji.emojize(
        ':+1:', language="alias")
    assert emoji.emojize(':thumbsup:', language="alias") == emoji.emojize(
        ':thumbs_up:', language="alias")
    assert emoji.emojize(':thumbsup:', language="alias") == '\U0001f44d'

    thumbsup = '\U0001f44d'
    assert emoji.demojize(thumbsup, language="alias") != thumbsup
    assert emoji.demojize(thumbsup, language="alias") != ':thumbs_up:'
    assert emoji.demojize(thumbsup, language="alias") != emoji.demojize(thumbsup)

    thailand = '🇹🇭'
    assert emoji.demojize(thailand, language="alias") != thailand
    assert emoji.demojize(thailand, language="alias") != ':Thailand:'
    assert emoji.demojize(thailand, language="alias") != emoji.demojize(thailand)
    assert emoji.demojize(thailand, language="alias", version=1.0) != emoji.demojize(
        thailand, language="alias")

    # No alias
    for emj, emoji_data in emoji.EMOJI_DATA.items():
        if emoji_data['status'] != emoji.STATUS['fully_qualified']:
            continue
        if 'alias' not in emoji_data:
            assert emoji.emojize(emoji_data['en'], language="alias") != emoji_data['en']
            assert emoji.demojize(emj, language="alias") == emoji_data['en']


def test_invalid_alias():
    # Invalid aliases should be passed through untouched
    assert emoji.emojize(':tester:', language="alias") == ':tester:'
    assert emoji.emojize(':footbal:', language="alias") == ':footbal:'
    assert emoji.emojize(':socer:', language="alias") == ':socer:'
    assert emoji.emojize(':socer:', language="alias",
                  variant="text_type") == ':socer:'


def test_demojize_name_only():
    for emj, item in emoji.EMOJI_DATA.items():
        if item['status'] != emoji.STATUS['fully_qualified']:
            continue
        for lang_code in emoji.LANGUAGES:
            if not lang_code in item:
                continue
            name = item[lang_code]
            oneway = emoji.emojize(name, language=lang_code)
            assert oneway == emj
            roundtrip = emoji.demojize(oneway, language=lang_code)
            assert name == roundtrip, '%s != %s' % (name, roundtrip)


def test_demojize_complicated_string():
    constructed = 'testing :baby::emoji_modifier_fitzpatrick_type-3: with :eyes: :eyes::eyes: modifiers :baby::emoji_modifier_fitzpatrick_type-5: to symbols ヒㇿ'
    emojid = emoji.emojize(constructed)
    destructed = emoji.demojize(emojid)
    assert constructed == destructed, '%s != %s' % (constructed, destructed)


def test_demojize_delimiters():
    for e in ['\U000026BD', '\U0001f44d', '\U0001F3C8']:
        for d in [(":", ":"), ("}", "}"), ("!$", "!!$"), ("[123", "456]"), ("😁", "👌"), ("[", "]")]:
            s = emoji.demojize(e, delimiters=d)
            assert s.startswith(d[0])
            assert s.endswith(d[1])

    text = "Example with an emoji%sin a sentence and %s %s %s %s multiple emoji %s%s%s%s%s in a row"
    for e in ['\U000026BD', '\U0001f44d', '\U0001F3C8']:
        for d in [(":", ":"), ("{", "}"), ("!$", "$!"), (":", "::"), ("::", "::"), ("😁", "👌"), ("[", "]")]:
            print("delimiter: %s" % (d, ))
            text_with_unicode = text % ((e, ) * 10)
            demojized_text = emoji.demojize(text_with_unicode, delimiters=d)
            assert text_with_unicode != demojized_text, (text_with_unicode, demojized_text)
            assert e not in demojized_text
            assert emoji.emojize(demojized_text, delimiters=d) == text_with_unicode
            de = emoji.demojize(e, delimiters=d)
            text_with_emoji = text % ((de, ) * 10)
            assert demojized_text == text_with_emoji
            assert emoji.emojize(text_with_emoji, delimiters=d) == text_with_unicode


def test_emoji_list():
    assert emoji.emoji_list('Hi, I am 👌 test')[0]['match_start'] == 9
    assert emoji.emoji_list('Hi') == []
    if len('Hello 🇫🇷👌') < 10:  # skip these tests on python with UCS-2 as the string length/positions are different
        assert emoji.emoji_list('Hi, I am fine. 😁') == [
            {'match_start': 15, 'match_end': 16, 'emoji': '😁'}]
        assert emoji.emoji_list('Hello 🇫🇷👌') == [
            {'emoji': '🇫🇷', 'match_start': 6, 'match_end': 8}, {'emoji': '👌', 'match_start': 8, 'match_end': 9}]


def test_distinct_emoji_list():
    assert emoji.distinct_emoji_list('Hi, I am fine. 😁') == ['😁']
    assert emoji.distinct_emoji_list('Hi') == []
    assert set(emoji.distinct_emoji_list('Hello 🇫🇷👌')) == {'🇫🇷', '👌'}
    assert emoji.distinct_emoji_list('Hi, I am fine. 😁😁😁😁') == ['😁']


def test_emoji_count():
    assert emoji.emoji_count('Hi, I am fine. 😁') == 1
    assert emoji.emoji_count('Hi') == 0
    assert emoji.emoji_count('Hello 🇫🇷👌') == 2
    assert emoji.emoji_count('Hello 🇵🇱🍺🇵🇱', unique=True) == 2


def test_replace_emoji():
    assert emoji.replace_emoji('Hi, I am fine. 😁') == 'Hi, I am fine. '
    assert emoji.replace_emoji('Hi') == 'Hi'
    assert emoji.replace_emoji('Hello 🇫🇷👌') == 'Hello '
    assert emoji.replace_emoji('Hello 🇫🇷👌', 'x') == 'Hello xx'

    def replace(emj, data):
        assert emj in ["🇫🇷", "👌"]
        return 'x'
    assert emoji.replace_emoji('Hello 🇫🇷👌', replace) == 'Hello xx'


def test_is_emoji():
    assert emoji.is_emoji('😁')
    assert not emoji.is_emoji('H')
    assert emoji.is_emoji('🇫🇷')
    assert not emoji.is_emoji('🇫🇷🇫🇷')
    assert not emoji.is_emoji('\ufe0f')  # variation selector


def test_long_emoji():
    assert emoji.demojize('This is \U0001F9D1\U0001F3FC\U0000200D\U0001F37C example text') == 'This is :person_feeding_baby_medium-light_skin_tone: example text'
    assert emoji.demojize('This is \U0001f468\U0001f3ff\u200d\u2764\ufe0f\u200d\U0001f468\U0001f3ff example text \U0001F469\U0001F3FB\U0000200D\U0001F91D\U0000200D\U0001F468\U0001F3FF') == 'This is :couple_with_heart_man_man_dark_skin_tone: example text :woman_and_man_holding_hands_light_skin_tone_dark_skin_tone:'
    assert emoji.demojize('This is \U0001f468\U0001f3ff\u200d\u2764\ufe0f\u200d\U0001f468\U0001f3ff\U0001f468\U0001f3ff\u200d\u2764\ufe0f\u200d\U0001f48b\u200d\U0001f468\U0001f3ff example text \U0001F469\U0001F3FB\U0000200D\U0001F91D\U0000200D\U0001F468\U0001F3FF') == 'This is :couple_with_heart_man_man_dark_skin_tone::kiss_man_man_dark_skin_tone: example text :woman_and_man_holding_hands_light_skin_tone_dark_skin_tone:'
    assert emoji.demojize('\U0001F46B\U0001F3FB This is \U0001f468\U0001f3ff\U0001f468\U0001f3ff\u200d\u2764\ufe0f\u200d\U0001f468\U0001f3ff\U0001f468\U0001f3ff\u200d\u2764\ufe0f\u200d\U0001f48b\u200d\U0001f468\U0001f3ff example text \U0001F469\U0001F3FB\U0000200D\U0001F91D\U0000200D\U0001F468\U0001F3FF') == ':woman_and_man_holding_hands_light_skin_tone: This is :man_dark_skin_tone::couple_with_heart_man_man_dark_skin_tone::kiss_man_man_dark_skin_tone: example text :woman_and_man_holding_hands_light_skin_tone_dark_skin_tone:'
    assert emoji.demojize('\U0001F46B\U0001F3FB\U0001F46B\U0001F3FB\U0001F469\U0001F3FB\U0000200D\U0001F91D\U0000200D\U0001F468\U0001F3FF\U0001FAF1\U0001F3FD\U0001FAF1\U0001F3FD\U0000200D\U0001FAF2\U0001F3FF') == ':woman_and_man_holding_hands_light_skin_tone::woman_and_man_holding_hands_light_skin_tone::woman_and_man_holding_hands_light_skin_tone_dark_skin_tone::rightwards_hand_medium_skin_tone::handshake_medium_skin_tone_dark_skin_tone:'
    s = ":crossed_fingers_medium-light_skin_tone::crossed_fingers::crossed_fingers_dark_skin_tone:"
    assert emoji.demojize(emoji.demojize(s)) == s


def test_untranslated():
    for emj, item in emoji.EMOJI_DATA.items():
        if item['status'] != emoji.STATUS['fully_qualified']:
            continue
        if 'es' not in item:
            # untranslated
            value = emoji.emojize(item['en'], language='en')
            roundtrip = emoji.demojize(value, language='es')
            assert roundtrip == value, '%s != %s (from %s)' % (ascii(roundtrip), ascii(value), item['en'])
        else:
            # translated
            value = emoji.emojize(item['en'], language='en')
            roundtrip = emoji.demojize(value, language='es')
            assert roundtrip == item['es'], '%s != %s' % (roundtrip, item['es'])


def test_text():
    UCS2 = len('Hello 🇫🇷👌') > 9  # don't break up characters on python with UCS-2

    text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat in reprehenderit in cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
Stróż pchnął kość w quiz gędźb vel fax myjń.
Høj bly gom vandt fræk sexquiz på wc.
Съешь же ещё этих мягких французских булок, да выпей чаю.
За миг бях в чужд плюшен скърцащ фотьойл.
هلا سكنت بذي ضغثٍ فقد زعموا — شخصت تطلب ظبياً راح مجتازا
שפן אכל קצת גזר בטעם חסה, ודי
ऋषियों को सताने वाले दुष्ट राक्षसों के राजा रावण का सर्वनाश करने वाले विष्णुवतार भगवान श्रीराम, अयोध्या के महाराज दशरथ के बड़े सपुत्र थे।
とりなくこゑす ゆめさませ みよあけわたる ひんかしを そらいろはえて おきつへに ほふねむれゐぬ もやのうち
視野無限廣，窗外有藍天
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""

    def add_random_emoji(text, lst, select=lambda emj_data: emj_data['en']):

        emoji_list = []
        text_with_unicode = ""
        text_with_placeholder = ""
        for i in range(0, len(text), 10):
            while True:
                emj, emj_data = random.choice(lst)
                placeholder = select(emj_data)
                if placeholder:
                    break

            if UCS2:
                j = text.find(" ", i, i + 10)
                if j == -1:
                    continue
            else:
                j = random.randint(i, i + 10)

            text_with_unicode += text[i:j]
            text_with_unicode += emj
            text_with_unicode += text[j:i + 10]

            text_with_placeholder += text[i:j]
            text_with_placeholder += placeholder
            text_with_placeholder += text[j:i + 10]

            emoji_list.append(emj)

        return text_with_unicode, text_with_placeholder, emoji_list

    def clean(s):
        return s.replace('\u200d', '').replace('\ufe0f', '')

    all_emoji_list = list(emoji.EMOJI_DATA.items())
    qualified_emoji_list = [(emj, item) for emj, item in emoji.EMOJI_DATA.items() if item['status'] == emoji.STATUS['fully_qualified']]

    # qualified emoji
    text_with_unicode, text_with_placeholder, emoji_list = add_random_emoji(text, qualified_emoji_list)
    assert emoji.demojize(text_with_unicode) == text_with_placeholder
    assert emoji.emojize(text_with_placeholder) == text_with_unicode
    if not UCS2:
        assert emoji.replace_emoji(text_with_unicode, '') == text
    assert set(emoji.distinct_emoji_list(text_with_unicode)) == set(emoji_list)
    for i, lis in enumerate(emoji.emoji_list(text_with_unicode)):
        assert lis['emoji'] == emoji_list[i]

    # qualified emoji from "es"
    selector = lambda emoji_data: emoji_data["es"] if "es" in emoji_data else False
    text_with_unicode, text_with_placeholder, emoji_list = add_random_emoji(text, qualified_emoji_list, selector)
    assert emoji.demojize(text_with_unicode, language="es") == text_with_placeholder
    assert emoji.emojize(text_with_placeholder, language="es") == text_with_unicode
    if not UCS2:
        assert emoji.replace_emoji(text_with_unicode, '') == text
    assert set(emoji.distinct_emoji_list(text_with_unicode)) == set(emoji_list)
    for i, lis in enumerate(emoji.emoji_list(text_with_unicode)):
        assert lis['emoji'] == emoji_list[i]

    # qualified emoji from "alias"
    selector = lambda emoji_data: emoji_data["alias"][0] if "alias" in emoji_data else False
    text_with_unicode, text_with_placeholder, emoji_list = add_random_emoji(text, qualified_emoji_list, selector)
    assert emoji.demojize(text_with_unicode, language="alias") == text_with_placeholder
    assert emoji.emojize(text_with_placeholder, language="alias") == text_with_unicode
    if not UCS2:
        assert emoji.replace_emoji(text_with_unicode, '') == text
    assert set(emoji.distinct_emoji_list(text_with_unicode)) == set(emoji_list)
    for i, lis in enumerate(emoji.emoji_list(text_with_unicode)):
        assert lis['emoji'] == emoji_list[i]

    # all emoji
    text_with_unicode, text_with_placeholder, emoji_list = add_random_emoji(text, all_emoji_list)
    assert emoji.demojize(text_with_unicode) == text_with_placeholder
    assert clean(emoji.emojize(text_with_placeholder)) == clean(text_with_unicode)
    if not UCS2:
        assert emoji.replace_emoji(text_with_unicode, '') == text
    assert set(emoji.distinct_emoji_list(text_with_unicode)) == set(emoji_list)
    for i, lis in enumerate(emoji.emoji_list(text_with_unicode)):
        assert lis['emoji'] == emoji_list[i]


def test_text_multiple_times():
    # Run test_text() multiple times because it relies on a random text
    for i in range(100):
        test_text()


def test_invalid_chars():
    invalidchar = "\U0001F20F"
    assert emoji.demojize(invalidchar) == invalidchar, "%r != %r" % (ascii(emoji.demojize(invalidchar)), ascii(invalidchar))
    assert emoji.demojize(invalidchar) == invalidchar, "%r != %r" % (ascii(emoji.demojize(invalidchar)), ascii(invalidchar))

    invalidchar = "u\2302 ⌂"
    assert emoji.demojize(invalidchar) == invalidchar, "%r != %r" % (ascii(emoji.demojize(invalidchar)), ascii(invalidchar))
    assert emoji.demojize(invalidchar) == invalidchar, "%r != %r" % (ascii(emoji.demojize(invalidchar)), ascii(invalidchar))


def test_combine_with_component():
    text = "Example of a combined emoji%sin a sentence"

    combined = emoji.emojize(text % ":woman_dark_skin_tone:")
    separated = emoji.emojize(text % ":woman::dark_skin_tone:")
    assert combined == separated,  "%r != %r" % (ascii(combined), ascii(separated))

    combined = emoji.emojize(text % ":woman_dark_skin_tone_white_hair:")
    separated = emoji.emojize(text % ":woman::dark_skin_tone:\u200d:white_hair:")
    assert combined == separated,  "%r != %r" % (ascii(combined), ascii(separated))


purely_emoji_testdata = [
    ('\U0001f600\ufe0f', True),
    ('\U0001f600', True),
    ('\U0001f600\U0001f600\U0001f600', True),
    ('abc', False),
    ('abc\U0001f600', False),
    ('\U0001f600c', False),
    ('\u270a\U0001f3fe', True),
]


@pytest.mark.parametrize("string,expected", purely_emoji_testdata)
def test_purely_emoji(string: str, expected: bool):
    assert emoji.purely_emoji(string) == expected
