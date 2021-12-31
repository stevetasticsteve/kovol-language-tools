from kovol_language_tools.verbs.csv_reader import get_data_from_csv
from kovol_language_tools.verbs.hansen_predicted_verb import HansenPredictedVerb as HV
test_csv = "tests/test_data.csv"

def verb1():
    return get_data_from_csv(test_csv)[0]

def verb2():
    return get_data_from_csv(test_csv)[1]

def test_hansen_verb_init():
    v = HV("asɔm", "asogɔm")
    assert v.future_3p == "asɔm"
    assert v.root == "as"
