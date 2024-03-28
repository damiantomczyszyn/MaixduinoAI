"""Unittests for the big dict of dicts containing all emoji"""


import re
import emoji


def test_all_languages_list():
    """Compare all language keys in EMOJI_DATA with the emoji.LANGUAGES list"""

    langs = set()
    for item in emoji.EMOJI_DATA.values():
        langs.update(item.keys())
    all_languages = {lang for lang in langs if len(lang) == 2 and lang.lower() == lang}

    assert set(emoji.LANGUAGES) == all_languages


def test_emoji_versions():
    """Check that every emoji has a valid version"""
    for item in emoji.EMOJI_DATA.values():
        assert "E" in item
        v = item["E"]
        assert isinstance(v, (int, float))
        assert v >= 0.6


def check_duplicate_names(lang):
    """Check that there are no duplicate names in the fully_qualified except for different variants"""
    seen = {}
    for emj, item in emoji.EMOJI_DATA.items():
        if item["status"] > emoji.STATUS["fully_qualified"]:
            continue

        if lang not in item:
            continue

        name = item[lang]
        if name in seen and 'variant' in item:
            seen[name] += 1
        else:
            assert name not in seen
            seen[name] = 0


def test_duplicate_names():
    """Check that there are no duplicate names in the fully_qualified except for different variants"""
    for lang in emoji.LANGUAGES:
        check_duplicate_names(lang)


def test_name_valid():
    """Check that every name starts with colons and does not contain other colons or whitespace"""

    pattern = re.compile(r":[^:\s]+:")
    for item in emoji.EMOJI_DATA.values():
        for lang in emoji.LANGUAGES:
            if lang in item:
                name = item[lang]
                assert pattern.match(name)
