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
        """Assign future tense attributes. Called during __init__.
        The two stages are:
        1. figure out suffixes to use
        2. add them to root."""
        root = self.root

        # 1.
        if self.get_last_root_character() == "a":
            # "a" causes assimilation
            suffixes = {
                "1s": "anim",
                "2s": "aniŋ",
                "3s": "aŋ",
                "1p": "ug",
                "2p": "wa",
                "3p": "is",
            }
        elif self.get_last_root_character() == "l":
            # special rule, roots ending in "l" have unique suffixes and vowel replacement
            suffixes = {
                "1s": "ɛnim",
                "2s": "ɛniŋ",
                "3s": "aŋ",
                "1p": "olug",
                "2p": "wa",
                "3p": "ɛlis",
            }
        else:
            # standard suffixes
            suffixes = {
                "1s": "inim",
                "2s": "iniŋ",
                "3s": "iŋ",
                "1p": "ug",
                "2p": "wa",
                "3p": "is",
            }

        # 2.
        if self.get_last_root_character() == "l":
            # special rule, "l" vowel replacement
            root = self.root[:-2]
        elif self.root_ending() == "V":
            # roots ending in V reduce
            root = self.root[:-1]

        for a in self.actors:
            setattr(self, f"future_{a}", root + suffixes[a])
        # no modification to 2sf
        setattr(self, "future_2s", self.root + suffixes["2s"])

    def predict_recent_past_tense(self) -> None:
        """Assign recent past tense attributes. Called during __init__.
        The two stages are:
        1. figure out suffixes to use
        2. add them to root."""
        root = self.root  # variable to handle special rule changing the root

        # 1.
        # if root[-2:] == "um":
        #     suffixes = ["gum", "gɔŋ", "ge", "guŋg", "guma", "gund"]
        if root[-1] == "u" or root[-2:] == "um":
            # "u" causes assimilation
            suffixes = ["gum", "gɔŋ", "ge", "uŋg", "guma", "gund"]

        elif self.verb_vowels()[-1] == "i":
            # "i" causes assimilation, stretches over morpheme boundary
            suffixes = ["gɔm", "gɔŋ", "ge", "ɔŋg", "gima", "gɔnd"]
        elif root[-1] == "a":
            # "a" causes assimilation
            suffixes = ["gam", "gɔŋ", "ga", "aŋg", "gama", "gand"]
        elif root[-1] == "l":
            # special rule, roots ending in "l" have unique suffixes
            suffixes = ["gam", "gɔŋ", "ga", "aŋg", "gama", "gand"]
            # special rule, single syllable roots ending in "l" cause vowel replacement in root
            if len(self.verb_vowels()) == 1:
                root = self.root.replace("ɔ", "a")
        else:
            # standard suffixes
            suffixes = ["gɔm", "gɔŋ", "ge", "ɔŋg", "gɔma", "gɔnd"]

        # 2.
        if self.root_ending() == "C":
            # roots ending in C reduce
            if root[-1] == "m" and root[-2:] != "um":
                # special rule, "m" assimilates to "ŋ"
                # unless root ends in "um", then it doesn't
                past_tense = [root[:-1] + "ŋ" + sfx for sfx in suffixes]
                past_tense[3] = root + suffixes[3]  # "-ɔŋg" doesn't assimilate
            else:
                # roots ending in C reduce
                past_tense = [root[:-1] + sfx for sfx in suffixes]
                if root[-1] == "l":
                    # special rule for "l", root is reduced for "-ɔŋg"
                    past_tense[3] = root[:-2] + suffixes[3]
                else:
                    # no assimilation or reduction for "-ɔŋg"
                    past_tense[3] = root + suffixes[3]
        else:
            # roots ending in V just add suffix to root
            past_tense = [root + sfx for sfx in suffixes]
            past_tense[3] = root[:-1] + suffixes[3]

        # Assign recent past attributes
        # No need to predict 1s, user gave it to class
        self.recent_past_2s = past_tense[1]
        self.recent_past_3s = past_tense[2]
        self.recent_past_1p = past_tense[3]
        self.recent_past_2p = past_tense[4]
        self.recent_past_3p = past_tense[5]

    def predict_remote_past_tense(self) -> None:
        """Assign remote past tense attributes. Called during __init__.
        The two stages are:
        1. figure out suffixes to use
        2. add them to root."""
        # 1.

        # 'u' in the root can cause assimilation
        # if self.verb_vowels()[-1] == "u":
        if self.root[-1] == "u":
            # if the root ends in 'u' there is assimilation
            suffixes = ["um", "uŋ", "ut", "umuŋg", "umwa", "umind"]
        elif self.root[-2:] == "um":
            # if the root ends in 'uC' there is weak assimilation
            suffixes = ["um", "uŋ", "ut", "omuŋg", "omwa", "ɛmind"]
        else:
            # standard suffixes
            suffixes = ["ɔm", "ɔŋ", "ɔt", "omuŋg", "omwa", "ɛmind"]

        # 2.
        if self.root_ending() == "V":
            # roots ending in V reduce
            remote_past = [self.root[:-1] + sfx for sfx in suffixes]
        else:
            # roots ending in C just add suffix to root
            remote_past = [self.root + sfx for sfx in suffixes]

        # Assign remote past attributes
        # No need to predict 1s, user gave it to class
        self.remote_past_2s = remote_past[1]
        self.remote_past_3s = remote_past[2]
        self.remote_past_1p = remote_past[3]
        self.remote_past_2p = remote_past[4]
        self.remote_past_3p = remote_past[5]

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
