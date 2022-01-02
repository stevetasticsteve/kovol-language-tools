from kovol_language_tools.verbs.csv_reader import get_data_from_csv
from kovol_language_tools.verbs.hansen_predicted_verb import HansenPredictedVerb as HV
test_csv = "tests/test_data.csv"

def verb1():
    v = get_data_from_csv(test_csv)[0]
    hv = HV(v.future_3p)
    return (v, hv)

def verb2():
    v = get_data_from_csv(test_csv)[1]
    hv = HV(v.future_3p)
    return (v, hv)

def test_hansen_verb_init():
    v = HV("asis")
    assert v.future_3p == "asis"
    assert v.root == "as"

def test_hansen_prediction():
    """Test a conjugation from each tense"""
    _, hv = verb1()
    assert hv.remote_past_1s == 'pigom'
    assert hv.recent_past_1s == 'pigom'
    assert hv.future_1s == 'piginim'
    assert hv.future_3p == 'pigis'

    _, hv2 = verb2()
    assert hv2.remote_past_1s == 'tolom'
    assert hv2.recent_past_1s == 'tagam'
    assert hv2.future_1s == 'tɛlim' # that will get corrected
    assert hv2.future_3p == 'tɛlis'

    

def test_hansen_verb_errors():
    v, hv = verb1()
    # always gonna be wrong compared to this test data
    assert hv.get_prediction_errors(v) == {'remote_past_1s': ('pigɔm', 'pigom'), 'remote_past_2s': ('pigɔŋ', 'pigoŋ'), 'remote_past_3s': ('pigɔt', 'pigot'), 'recent_past_1s': ('pigɔm', 'pigom'), 'recent_past_2s': ('pigɔŋ', 'pigoŋ'), 'recent_past_1p': ('pigɔŋg', 'pigoŋg'), 'recent_past_3p': ('pigɔnd', 'pigond'), 'plural_imperative': ('pigas', 'pigwas')}
    
