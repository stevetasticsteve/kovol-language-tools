from kovol_language_tools.verbs.kovol_verb import PredictedVerb


class StanleyPredictedVerb(PredictedVerb):
    """Initialise a verb with the remote past 1s and recent past 1s and predict an entire paradigm from that."""

    def __init__(self, remote_past_1s: str, recent_past_1s: str, english=""):
        super().__init__(
            future1s="", english=english
        )  # optionally pass through english parameter
        self.remote_past_1s = remote_past_1s
        self.recent_past_1s = recent_past_1s

        self.predict_root()
        self.predict_verb()

    def predict_future_tense(self) -> None:
        """Assign future tense attributes. Called during __init__"""
        root = self.root
        suffixes = {
            "1s": "inim",
            "2s": "iniŋ",
            "3s": "iŋ",
            "1p": "ug",
            "2p": "wa",
            "3p": "is",
        }

        # 1.
        if self.get_last_root_character() == "a":
            # "a" causes assimilation
            for a in ("1s", "2s", "3s"):
                suffixes[a] = "a" + suffixes[a].lstrip("i")

        elif self.get_last_root_character() == "l":
            # special rule, roots ending in "l" have unique suffixes and vowel replacement
            root = self.root[:-2]
            suffixes = {
                "1s": "ɛnim",
                "2s": "ɛniŋ",
                "3s": "aŋ",
                "1p": "olug",
                "2p": "wa",
                "3p": "ɛlis",
            }

        if self.root_ending() == "V":
            # roots ending in V reduce
            root = self.root[:-1]

        for a in self.actors:
            setattr(self, f"future_{a}", root + suffixes[a])
        # no modification to 2sf
        setattr(self, "future_2s", self.root + suffixes["2s"])

    def predict_recent_past_tense(self) -> None:
        """Assign recent past tense attributes. Called during __init__."""
        root = root_1p = self.root
        suffixes = {
            "1s": "gɔm",
            "2s": "gɔŋ",
            "3s": "ge",
            "1p": "ɔŋg",
            "2p": "gɔma",
            "3p": "gɔnd",
        }

        if (
            self.get_last_root_character() == "u"
            or self.get_last_two_root_characters() == "um"
        ):
            # "u" causes assimilation
            for a in ("1s", "1p", "2p", "3p"):
                suffixes[a] = suffixes[a].replace("ɔ", "u")

        elif self.get_last_root_vowel() == "i":
            # "i" causes assimilation, stretches over morpheme boundary
            suffixes["2p"] = "gima"

        elif (
            self.get_last_root_character() == "a"
            or self.get_last_root_character() == "l"
        ):
            # "a" causes assimilation
            suffixes = {
                "1s": "gam",
                "2s": "gɔŋ",
                "3s": "ga",
                "1p": "aŋg",
                "2p": "gama",
                "3p": "gand",
            }
            if self.get_last_root_character() == "l" and len(self.verb_vowels()) == 1:
                # special rule, single syllable roots ending in "l" cause vowel replacement in root
                root = self.root.replace("ɔ", "a")

        if self.root_ending() == "C":
            # roots ending in C reduce
            if (
                self.get_last_root_character() == "m"
                and self.get_last_root_character() != "um"
            ):
                # special rule, "m" assimilates to "ŋ"
                # unless root ends in "um", then it doesn't
                root = root[:-1] + "ŋ"
                root_1p = self.root

            else:
                # roots ending in C reduce
                root = root[:-1]
                if self.get_last_root_character() == "l":
                    # special rule for "l", root is reduced for "-ɔŋg" use reduced root for 1p
                    root_1p = self.root[:-2]
                else:
                    # no assimilation or reduction for "-ɔŋg"  use normal root for 1p
                    root_1p = self.root

        # Assign recent past attributes
        for a in self.actors:
            if a == "1p":
                setattr(self, f"recent_past_{a}", root_1p + suffixes[a])
            else:
                setattr(self, f"recent_past_{a}", root + suffixes[a])

    def predict_remote_past_tense(self) -> None:
        """Assign remote past tense attributes. Called during __init__"""
        root = self.root
        suffixes = {
            "1s": "ɔm",
            "2s": "ɔŋ",
            "3s": "ɔt",
            "1p": "omuŋg",
            "2p": "omwa",
            "3p": "ɛmind",
        }

        # 'u' in the root can cause assimilation
        if self.get_last_root_character() == "u":
            # if the root ends in 'u' there is assimilation
            suffixes = {k: "u" + v[1:] for (k, v) in suffixes.items()}

        elif self.get_last_two_root_characters() == "um":
            # if the root ends in 'uC' there is weak assimilation
            for a in ("1s", "2s", "3s"):
                suffixes[a] = "u" + suffixes[a][1:]

        if self.root_ending() == "V":
            # roots ending in V reduce
            root = root[:-1]

        for a in self.actors:
            setattr(self, f"remote_past_{a}", root + suffixes[a])

    def predict_imperative(self) -> None:
        """Assign imperative attributes. Called during __init__.
        The two stages are:
        1. figure out suffixes to use
        2. add them to root."""
        # 1.
        if self.root[-1] == "g":
            # special rule, "g" has it's own suffixes
            suffixes = ["u", "as"]
        else:
            # standard suffixes
            suffixes = ["e", "as"]

        # 2.
        if self.root_ending() == "V":
            # roots ending in V reduce
            imperatives = [self.root[0:-1] + sfx for sfx in suffixes]
        else:
            # roots ending in C just add suffix to root
            imperatives = [self.root + sfx for sfx in suffixes]

        # Assign imperative attributes
        self.singular_imperative = imperatives[0]
        self.plural_imperative = imperatives[1]
