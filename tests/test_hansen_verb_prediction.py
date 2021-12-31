from kovol_language_tools.verbs import HansenPredictedKovolVerb as HV

test_verb = "amis"


def test_past_prediction():
    v = HV(test_verb)
    assert v.future_1s == "aminim"
    assert v.remote_past_1s == "amom"
    assert v.recent_past_1s == "aŋgom"
