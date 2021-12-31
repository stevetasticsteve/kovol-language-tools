from kovol_language_tools.verbs.csv_reader import get_data_from_csv
from kovol_language_tools.verbs.kovol_verb import KovolVerb
from kovol_language_tools.verbs.stanley_predicted_verb import StanleyPredictedVerb as SV
test_csv = "tests/test_data.csv"

def verb1():
    p = SV("pigɔm" ,"pigɔm")
    return get_data_from_csv(test_csv)[0], p

def verb2():
    return get_data_from_csv(test_csv)[1]

def test_stanley_verb_init():
    v = SV("asɔm", "asogɔm")
    assert v.remote_past_1s == "asɔm"
    assert v.recent_past_1s == "asogɔm"
    assert v.root == "aso"

def test_stanley_errors():
    """verb1 should predict correctly. partial verb shouldn't"""
    v, p = verb1()
    assert p.get_prediction_errors(v) == {}
    assert p.get_prediction_errors(KovolVerb("piginim", "")) != {}
