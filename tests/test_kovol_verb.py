# tests for csv reader, KovolVerb and PredictedVerb

from kovol_language_tools.verbs.kovol_verb import KovolVerb as KV
from kovol_language_tools.verbs.csv_reader import get_data_from_csv
test_csv = "tests/test_data.csv"

def test_get_data_from_csv():
    data = get_data_from_csv(test_csv)
    assert type(data) == list
    assert len(data) == 3
    obj = data[0]
    assert type(obj) == KV
    assert str(obj) == 'Kovol verb: piginim, "to put"'


def test_get_data_as_list():
    data = get_data_from_csv(test_csv, format="list")
    assert type(data[0]) == list


###
# Class tests


def init_verb1():
    v = KV("aminim", "to speak")
    v.remote_past_1s = "amɔm"
    v.recent_past_1s = "aŋgɔm"
    v.future_3p = "amis"
    return v


def init_verb2():
    v = KV("asinim", "to jab")
    v.remote_past_1s = "asɔm"
    v.recent_past_1s = "asogɔm"
    v.future_3p = "asis"
    return v


def init_verb3():
    return get_data_from_csv(test_csv)[0]


def test_kovol_verb_init():
    v = KV("aminim", "to speak")
    assert type(v) == KV
    assert v.future_1s == "aminim"
    assert v.english == "to speak"
    assert v.future_1p == ""
    assert v.errors == []
    assert v.recent_past_1s == ""
    assert v.remote_past_1s == ""


def test_stanley_root_prection():
    """Simple root tests to make sure it functions, not that it's always correct"""
    v1 = init_verb1()
    v1.predict_root(rules="stanley")
    assert v1.root == "am"

    v2 = init_verb2()
    v2.predict_root(rules="stanley")
    assert v2.root == "aso"


def test_hansen_root_prection():
    v1 = init_verb1()
    v1.predict_root(rules="hansen")
    assert v1.root == "am"

    v2 = init_verb2()
    v2.predict_root(rules="hansen")
    assert v2.root == "as"


def test_verb_vowels():
    v1 = init_verb1()
    assert v1.verb_vowels() == "a"
    v2 = init_verb2()
    assert v2.verb_vowels() == "ao"


def test_get_vowel_n():
    v2 = init_verb2()
    assert v2.get_vowel_n(0) == "a"
    assert v2.get_vowel_n(1) == "o"


def test_get_last_root_vowel():
    v2 = init_verb2()
    assert v2.get_last_root_vowel() == "o"
    v1 = init_verb1()
    assert v1.get_last_root_vowel() == "a"


def test_get_last_root_character():
    v1 = init_verb1()
    assert v1.get_last_root_character() == "m"
    v2 = init_verb2()
    assert v2.get_last_root_character() == "o"


def test_get_last_two_root_characters():
    v1 = init_verb1()
    assert v1.get_last_two_root_characters() == "am"
    v2 = init_verb2()
    assert v2.get_last_two_root_characters() == "so"


def test_get_remote_past_tense():
    v1 = init_verb1()
    assert v1.get_remote_past_tense() == ("amɔm", "", "", "", "", "")
    v3 = init_verb3()
    assert v3.get_remote_past_tense() == (
        "pigɔm",
        "pigɔŋ",
        "pigɔt",
        "pigomuŋg",
        "pigomwa",
        "pigɛmind",
    )


def test_get_recent_past_tense():
    v1 = init_verb1()
    assert v1.get_recent_past_tense() == ("aŋgɔm", "", "", "", "", "")
    v3 = init_verb3()
    assert v3.get_recent_past_tense() == (
        "pigɔm",
        "pigɔŋ",
        "pige",
        "pigɔŋg",
        "pigima",
        "pigɔnd",
    )


def test_get_future_tense():
    v1 = init_verb1()
    assert v1.get_future_tense() == ("aminim", "", "", "", "", "amis")
    v3 = init_verb3()
    assert v3.get_future_tense() == (
        "piginim",
        "piginiŋ ig",
        "pigiŋ",
        "pigug",
        "pigwa ig",
        "pigis",
    )

