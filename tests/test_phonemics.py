import pytest
import kovol_language_tools.phonemics

test_data = (
    # Phonetics, interpreted, analysed, orthography
    # 184 "front"
    ("ɑβɑgɑm", "ɑβɑgɑm", "ɑβɑgɑm", "avagam"),
    # 163 "rotten"
    ("pjɑg", "pjɑg", "pjɑg", "pyag"),
    # 166 "serrated"
    ("ʔigɑbulo", "ʔigɑbulo", "ʔigɑbulo", "kigabulo"),
    # 131 "ancestor"
    ("iguβɑsɑβɑs", "iguβɑsɑβɑs", "iguβɑsɑβɑs", "iguvasavas"),
    # 128 "unmarried man"
    ("meⁱ", "mej", "mej", "mey"),
    # 266 "cucumber"
    ("ʔɔsoβiɑg", "ʔɔsoβjɑg", "ʔosoβjɑg", "kosovyag"),
    # 266 "cucumber" (spelling variant to check a allowed)
    ("ʔɔsoβiag", "ʔɔsoβjag", "ʔosoβjag", "kosovyag"),
    # 318 "sore"
    ("wɑⁱgɔm", "wɑⁱgɔm", "wɑⁱgom", "waigom"),
    # 286 "smoke"
    ("ʔoᵘg", "ʔowg", "ʔowg", "kowg"),
    # 207 "rafter"
    ("tɑŋgɑŋgi", "tɑŋgɑŋgi", "tɑŋgɑŋgi", "tangangi"),
    # 207 "rafter" (spelling variation to check ng handled correctly)
    ("tɑŋɑŋgi", "tɑŋɑŋgi", "tɑŋɑŋgi", "tangangi"),
)

invalid_characters = (
    "siv",
    "səbə",
)


def test_check_phonetic_inventory():
    # test good data
    for t in test_data:
        assert kovol_language_tools.phonemics.check_phonetic_inventory(t[0]) == []

    # test bad data with soft fail
    for t in invalid_characters:
        assert (
            kovol_language_tools.phonemics.check_phonetic_inventory(t, hard_fail=False)
            != []
        )

    # test bad data with hard fail
    for t in invalid_characters:
        with pytest.raises(ValueError):
            kovol_language_tools.phonemics.check_phonetic_inventory(t)


def test_interpret_phonetics():
    for t in test_data:
        assert kovol_language_tools.phonemics.interpret_phonetics(t[0])[0] == t[1]


def test_analyse_phonetics():
    for t in test_data:
        assert kovol_language_tools.phonemics.analyse_phonetics(t[1]) == t[2]


def test_use_orthography():
    for t in test_data:
        assert kovol_language_tools.phonemics.use_orthography(t[2]) == t[3]


def test_phonetics_to_orthography():
    for t in test_data:
        assert kovol_language_tools.phonemics.phonetics_to_orthography(t[0]) == t[3]
