from kovol_language_tools.verbs.kovol_verb import PredictedVerb


class HansenPredictedVerb(PredictedVerb):
    """Class to replace the standard method of predicting verbs with the Hansen alternative."""

    def __init__(self, future_3p, english=""):
        super(PredictedVerb, self).__init__(future1s="", english=english)
        self.future_3p = future_3p
        self.predict_root(rules="hansen")
        self.predict_verb()

    def predict_remote_past_tense(self):
        root = self.root  # save a copy of the root so we can alter it

        suffixes = {
            "1s": "om",
            "2s": "oŋ",
            "3s": "ot",
            "1p": "omuŋg",
            "2p": "omwa",
            "3p": "ɛmind",
        }
        last_vowel = self.get_last_root_vowel()
        if last_vowel == "ɛ":
            if (
                self.get_last_two_root_characters() == "ɛl"
                and self.get_vowel_n(-2) == "u"
            ):
                root = root.replace("ɛl", "ul")
            else:
                root = root.replace("ɛ", "o")
        elif last_vowel == "u":
            suffixes = {k: v.replace("o", "u") for (k, v) in suffixes.items()}

        for a in self.actors:
            setattr(self, f"remote_past_{a}", root + suffixes[a])

    def predict_recent_past_tense(self):
        suffixes = {
            "1s": "ogom",
            "2s": "ogoŋ",
            "3s": "ɛge",
            "1p": "oŋg",
            "2p": "agama",
            "3p": "ogond",
        }
        roots = {k: self.root for k in ["1s", "2s", "3s", "1p", "2p", "3p"]}
        last_vowel = self.get_last_root_vowel()
        last_character = self.get_last_root_character()

        if last_vowel == "ɛ":
            if self.get_last_two_root_characters() == "ɛl":
                # shorten root by two
                roots = {k: v[:-2] for (k, v) in roots.items()}
                if self.get_vowel_n(-2) == "u":
                    suffixes = {
                        "1s": "ugam",
                        "2s": "ugoŋ",
                        "3s": "uga",
                        "1p": "aŋg",
                        "2p": "uguma",
                        "3p": "ugand",
                    }
                else:
                    for r in ("1s", "3s", "1p", "2p", "3p"):
                        roots[r] = roots[r].replace("ɛ", "a")
                    roots["2s"] = roots["2s"].replace("ɛ", "o")

                    suffixes = {
                        "1s": "agam",
                        "2s": "ogoŋ",
                        "3s": "aga",
                        "1p": "aŋg",
                        "2p": "agama",
                        "3p": "agand",
                    }
            else:
                for r in ("1s", "2s", "1p", "3p"):
                    roots[r] = roots[r].replace("ɛ", "o")
                roots["2p"] = self.root.replace("ɛ", "a")

        elif last_vowel == "u":
            suffixes["1s"] = "ugum"
            suffixes["2s"] = "ugoŋ"
            suffixes["3s"] = "uge"
            suffixes["1p"] = "uŋg"
            suffixes["2p"] = "uguma"
            suffixes["3p"] = "ugund"
            if last_character == "m":
                suffixes["1s"] = "ogom"

        elif last_vowel == "i":
            suffixes["1s"] = "igom"
            suffixes["2s"] = "igoŋ"
            suffixes["3s"] = "ige"
            suffixes["2p"] = "igima"
            suffixes["3p"] = "igond"

        if last_character == "m":
            if (
                self.get_last_two_root_characters() == "um"
                or self.get_last_two_root_characters() == "ɛm"
            ):
                suffixes = {k: v[1:] for (k, v) in suffixes.items()}
                suffixes["1p"] = "oŋg"
                roots = {k: v[:-1] for (k, v) in roots.items()}
                roots["1p"] = self.root
                if self.get_last_two_root_characters() == "um":
                    suffixes["1p"] = "uŋg"
                elif self.get_last_two_root_characters() == "ɛm":
                    suffixes["1p"] = "oŋg"
            elif self.root[-2] == "u" or self.root[-2] == "ɛ":
                pass
            else:
                roots = {k: v[:-1] + "ŋ" for (k, v) in roots.items()}
                roots["1p"] = self.root
                suffixes = {k: v[1:] for (k, v) in suffixes.items()}
                suffixes["1p"] = "oŋg"

        elif last_character == "g":
            suffixes = {k: v[2:] for (k, v) in suffixes.items()}
            suffixes["1p"] = "oŋg"

        self.recent_past_1s = roots["1s"] + suffixes["1s"]
        self.recent_past_2s = roots["2s"] + suffixes["2s"]
        self.recent_past_3s = roots["3s"] + suffixes["3s"]
        self.recent_past_1p = roots["1p"] + suffixes["1p"]
        self.recent_past_2p = roots["2p"] + suffixes["2p"]
        self.recent_past_3p = roots["3p"] + suffixes["3p"]

    def predict_future_tense(self):
        suffixes = {
            "1s": "ɛnim",
            "2s": "ɛniŋ",
            "3s": "iŋ",
            "1p": "ug",
            "2p": "wa",
            "3p": "is",
        }
        roots = {k: self.root for k in ["1s", "2s", "3s", "1p", "2p", "3p"]}

        last_vowel = self.get_last_root_vowel()
        last_character = self.get_last_root_character()

        if last_vowel == "i" or last_vowel == "u" or last_character == "m":
            suffixes["1s"] = "inim"
            suffixes["2s"] = "iniŋ"
        elif self.get_last_two_root_characters() == "ɛl":
            suffixes["1s"] = suffixes["1s"][2:]
            suffixes["2s"] = suffixes["2s"][2:]
            suffixes["3s"] = "aŋ"
        elif last_vowel == "ɛ":
            roots["1p"] = roots["2p"] = self.root.replace("ɛ", "o")

        self.future_1s = roots["1s"] + suffixes["1s"]
        self.future_2s = roots["2s"] + suffixes["2s"]
        self.future_3s = roots["3s"] + suffixes["3s"]
        self.future_1p = roots["1p"] + suffixes["1p"]
        self.future_2p = roots["2p"] + suffixes["2p"]
        # self.future_3p = roots["3p"] + suffixes["3p"]
        # 3PF given as starting data

    def predict_imperative(self):
        suffixes = {"sing_imp": "ɛ", "pl_imp": "as"}
        root = self.root
        if self.get_last_root_vowel() == "ɛ":
            root = root.replace("ɛ", "a")
        if self.get_last_root_character() == "g":
            suffixes["sing_imp"] = "u"
            suffixes["pl_imp"] = "was"
        else:
            root = self.root
        self.singular_imperative = root + suffixes["sing_imp"]
        self.plural_imperative = root + suffixes["pl_imp"]
