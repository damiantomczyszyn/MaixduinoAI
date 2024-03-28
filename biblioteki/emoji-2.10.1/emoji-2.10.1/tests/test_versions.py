"""Unittests for versions in EMOJI_DATA"""

import emoji
import pytest


def test_emoji_versions_complete_emojize():
    # Check that every emoji has a valid version
    replacement = "<3"
    for lang_code, emoji_pack in emoji.unicode_codes._EMOJI_UNICODE.items():
        for name in emoji_pack.keys():
            version = []

            def f(e, d):
                v = d['E']
                n = d[lang_code]
                assert n == name
                assert isinstance(v, (int, float))
                assert v >= 0.6
                version.append(v)
                return replacement
            r = emoji.emojize(name, language=lang_code,
                              version=0.0, handle_version=f)
            assert len(version) == 1
            assert r == replacement


def test_emoji_versions_complete_demojize():
    # Check that every emoji has a valid version
    for lang_code, emoji_pack in emoji.unicode_codes._EMOJI_UNICODE.items():
        for name in emoji_pack.keys():
            version = []

            def f(e, d):
                v = d['E']
                assert isinstance(v, (int, float))
                assert v >= 0.6
                version.append(v)
                return ''
            emoji.demojize(emoji.emojize(name, language=lang_code),
                           language=lang_code, version=0.0, handle_version=f)
            if len(version) != 1:
                print(name)
                print(emoji.emojize(name, language=lang_code).encode("unicode-escape").decode("utf-8"))
                print(emoji.demojize(emoji.emojize(name, language=lang_code), language=lang_code).encode("unicode-escape").decode("utf-8"))
            assert len(version) == 1


def test_method_version():
    # Test method "emoji.version()"

    assert emoji.version(":snake:") == 0.6
    assert emoji.version("\U0001F40D") == 0.6

    assert emoji.version(":brain:") == 5
    assert emoji.version("\U0001F9E0") == 5
    assert emoji.version(":cerebro:") == 5

    assert emoji.version("prefix :people_hugging: suffix") == 13
    assert emoji.version("prefix \U0001FAC2 suffix") == 13

    assert emoji.version("\U0001F611") == 1
    assert emoji.version(":expressionless_face:") == 1
    assert emoji.version(":expressionless:") == 1

    assert emoji.version("':pouring_liquid::people_hugging:") == 14
    assert emoji.version("\U0001FAD7\U0001FAC2") == 14

    assert emoji.emojize(':123:', version=5, variant="text_type") == ':123:'

    with pytest.raises(ValueError):
        emoji.version("test")

    with pytest.raises(ValueError):
        emoji.version("':snak:")


def test_method_replace_version():
    # Test method "emoji.replace_emoji(string, version=X.Y)"

    assert emoji.replace_emoji("\U0001F40D\U0001F9E0\U0001FAC2\U0001FAD7\U0001FAC2", version=6) == "\U0001F40D\U0001F9E0"

    assert emoji.replace_emoji('Hi, I am fine. 😁', version=0) == 'Hi, I am fine. '
    assert emoji.replace_emoji('Hi', version=0) == 'Hi'
    assert emoji.replace_emoji('Hello 🇫🇷👌', version=0) == 'Hello '
    assert emoji.replace_emoji('Hello 🇫🇷👌', 'x', version=0,) == 'Hello xx'
    assert emoji.replace_emoji('Hello 🇫🇷👌', 'x', version=1,) == 'Hello 🇫🇷👌'

    def replace(emj, data):
        assert emj in ["🇫🇷", "👌"]
        return 'x'
    assert emoji.replace_emoji('Hello 🇫🇷👌', replace, version=0.1) == 'Hello xx'

    assert emoji.replace_emoji('A 🦖 is eating a 🥐', replace='', version=5.0) == 'A 🦖 is eating a 🥐'
