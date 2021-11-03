# This file contains classes and functions for retrieving verb data and putting it into a Verb object.
# Also handles verb prediction.

import csv

from tabulate import tabulate


class KovolVerb:
    """A class to represent a Kovol verb defining the conjugations of it as attributes with methods for retrieving
    those conjugations and printing to screen."""

    vowels = (
            "i",
            "e",
            "ɛ",
            "a",
            "ə",
            "u",
            "o",
            "ɔ",
      )  # Vowels in Kovol language

    def __init__(self, future1s: str, english: str):
        # Meta data
        self.kovol = future1s
        self.english = english
        self.tpi = ""  # Tok pisin
        self.author = ""  # Who entered the data
        self.errors = []  # used for PredictedVerb subclass,
        # defined here to maintain template compatibility

        # Remote past tense
        self.remote_past_1s = ""
        self.remote_past_2s = ""
        self.remote_past_3s = ""
        self.remote_past_1p = ""
        self.remote_past_2p = ""
        self.remote_past_3p = ""

        # Recent past tense
        self.recent_past_1s = ""
        self.recent_past_2s = ""
        self.recent_past_3s = ""
        self.recent_past_1p = ""
        self.recent_past_2p = ""
        self.recent_past_3p = ""

        # Future tense
        self.future_1s = future1s
        self.future_2s = ""
        self.future_3s = ""
        self.future_1p = ""
        self.future_2p = ""
        self.future_3p = ""

        # Imperative forms
        self.singular_imperative = ""
        self.plural_imperative = ""

        # Other forms
        self.short = ""

        

    def __str__(self):
        string = self.get_string_repr()
        return f"Kovol verb: {string['future_1s']}, \"{string['english']}\""

    def __repr__(self):
        return self.__str__()

    # Methods to call several attributes together in groups
    def get_string_repr(self) -> str:
        """Get an up to date string representation."""
        return {"future_1s": self.future_1s, "english": self.english}
        
        
    def predict_root(self, rules="steve") -> str:
        """Find the verb root. Can take a keyword argument to change how it's predicted."""

        if rules == "philip":
            self.root = self.remote_past_3p[:-5]
        else:
            remote_past_tense = self.remote_past_1s[0:-2]  # strip -om
            past_tns = self.recent_past_1s[0:-3]  # strip -gom

            if len(past_tns) > len(remote_past_tense):
                self.root = past_tns
            elif len(past_tns) == len(remote_past_tense):
                self.root = remote_past_tense
            else:
                self.root = remote_past_tense

    def verb_vowels(self) -> str:
            """Returns a string containing just the vowels of the root."""
            v = [c for c in self.root if c in self.vowels]
            v = "".join(v)
            return v


    def get_remote_past_tense(self) -> tuple:
        """Return a tuple of remote past conjugations."""
        remote_past_tense = (
            self.remote_past_1s,
            self.remote_past_2s,
            self.remote_past_3s,
            self.remote_past_1p,
            self.remote_past_2p,
            self.remote_past_3p,
        )
        return remote_past_tense

    def get_recent_past_tense(self) -> None:
        """Return a tuple of recent past tense conjugations."""
        recent_past_tense = (
            self.recent_past_1s,
            self.recent_past_2s,
            self.recent_past_3s,
            self.recent_past_1p,
            self.recent_past_2p,
            self.recent_past_3p,
        )
        return recent_past_tense

    def get_future_tense(self) -> tuple:
        """Return a tuple of future tense conjugations."""
        future_tense = (
            self.future_1s,
            self.future_2s,
            self.future_3s,
            self.future_1p,
            self.future_2p,
            self.future_3p,
        )
        return future_tense

    def get_imperatives(self) -> tuple:
        """Return a tuple of imperative conjugations."""
        return (self.singular_imperative, self.plural_imperative)

    def get_all_conjugations(self) -> tuple:
        """Return a tuple of all conjugations for easily comparing verbs."""
        return (
            self.get_remote_past_tense()
            + self.get_recent_past_tense()
            + self.get_future_tense()
            + self.get_imperatives()
        )

    def print_paradigm(self) -> None:
        """Use tabulate to print a nice paradigm table to the terminal."""
        table = [
            ["1s", self.remote_past_1s, self.recent_past_1s, self.future_1s, ""],
            [
                "2s",
                self.remote_past_2s,
                self.recent_past_2s,
                self.future_2s,
                self.singular_imperative,
            ],
            ["3s", self.remote_past_3s, self.recent_past_3s, self.future_3s, ""],
            ["1p", self.remote_past_1p, self.recent_past_1p, self.future_1p, ""],
            [
                "2p",
                self.remote_past_2p,
                self.recent_past_2p,
                self.future_2p,
                self.plural_imperative,
            ],
            ["3p", self.remote_past_3p, self.recent_past_3p, self.future_3p, ""],
        ]
        headers = [
            "",
            "Remote past tense",
            "Recent past tense",
            "Future tense",
            "Imperative",
        ]
        print('\n {sing}, "{eng}"'.format(sing=self.future_1s, eng=self.english))
        print(tabulate(table, headers=headers, tablefmt="rst"))
        print("Short form: {short}".format(short=self.short))


class PredictedKovolVerb(KovolVerb):
    """Initialise a verb with the remote past 1s and recent past 1s and predict an entire paradigm from that."""

    def __init__(self, remote_past_1s: str, recent_past_1s: str, english=""):
        super().__init__(
            future1s="", english=english
        )  # optionally pass through english parameter
        self.remote_past_1s = remote_past_1s
        self.recent_past_1s = recent_past_1s

        self.predict_root()
        self.predict_verb()

    def __str__(self):
        string = self.get_string_repr()
        return f"Predicted Kovol verb: {string['future_1s']}, \"{string['english']}\""

    def __repr__(self):
        return self.__str__()

    def root_ending(self) -> str:
        """Returns whether the root ends in a Vowel "V" or Consonant "C".
        Called during __init__."""
        if self.root[-1] in self.vowels:
            return "V"
        else:
            return "C"

    def predict_verb(self) -> None:
        """A method to call all prediction methods together. Called during __init__."""
        self.predict_future_tense()
        self.predict_recent_past_tense()
        self.predict_remote_past()
        self.predict_imperative()

    def predict_future_tense(self) -> None:
        """Assign future tense attributes. Called during __init__.
        The two stages are:
        1. figure out suffixes to use
        2. add them to root."""
        # 1.
        if self.root[-1] == "a":
            # "a" causes assimilation
            suffixes = ["anim", "aniŋ", "aŋ", "ug", "wa", "is"]
        elif self.root[-1] == "l":
            # special rule, roots ending in "l" have unique suffixes and vowel replacement
            suffixes = ["ɛnim", "ɛniŋ", "aŋ", "olug", "wa", "ɛlis"]
        else:
            # standard suffixes
            suffixes = ["inim", "iniŋ", "iŋ", "ug", "wa", "is"]

        # 2.
        if self.root[-1] == "l":
            # special rule, "l" vowel replacement
            future_tense = [self.root[:-2] + sfx for sfx in suffixes]
        elif self.root_ending() == "V":
            # roots ending in V reduce
            future_tense = [self.root[:-1] + sfx for sfx in suffixes]
        else:
            # roots ending in C just add suffix to root
            future_tense = [self.root + sfx for sfx in suffixes]
        # no assimilation or reduction for future 2p "-wa"
        future_tense[4] = self.root + suffixes[4]

        # Assign attributes
        self.future_1s = future_tense[0]
        self.future_2s = future_tense[1]
        self.future_3s = future_tense[2]
        self.future_1p = future_tense[3]
        self.future_2p = future_tense[4]
        self.future_3p = future_tense[5]

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

    def predict_remote_past(self) -> None:
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

    def print_with_kovol_verb(self, kovol_verb: KovolVerb) -> None:
        """Use the parent class' print_paradigm method to print both predicted and actual paradigm."""
        print("Actual verb:")
        kovol_verb.print_paradigm()
        print("\nPredicted verb:")
        self.print_paradigm()

    def get_prediction_errors(self, kovol_verb: KovolVerb) -> dict:
        """Compare predicted Kovol verb to the actual one, returning a dict of differences. The key for the dict
        is the tense and actor (as a string) and the value is the tuple (actual data, predicted data).
        Also asigns this return value to self.errors."""
        diff = {}
        # explicitly define order of conjugations
        order = [
            "remote_past_1s",
            "remote_past_2s",
            "remote_past_3s",
            "remote_past_1p",
            "remote_past_2p",
            "remote_past_3p",
            "recent_past_1s",
            "recent_past_2s",
            "recent_past_3s",
            "recent_past_1p",
            "recent_past_2p",
            "recent_past_3p",
            "future_1s",
            "future_2s",
            "future_3s",
            "future_1p",
            "future_2p",
            "future_3p",
            "singular_imperative",
            "plural_imperative",
        ]
        predicted = self.get_all_conjugations()
        actual = kovol_verb.get_all_conjugations()

        for o, p, a in zip(order, predicted, actual):
            # o=order (label), p=predicted, a=actual
            if o == "future_2s" or o == "future_2p":
                # ignore data that has " ig" on the end, sometimes entered by users
                if a.endswith(" ig"):
                    a = a[:-3]  # strip ig off of the comparison
            if a != p:
                # add non matching prediction to errors
                diff[o] = (a, p)
        self.errors = diff
        return self.errors


def get_data_from_csv(csv_file, format="object") -> list:
    """reads a csv file and outputs a list of KovolVerb objects.
    Can accept 'list' as format to return a list of listed dict entries instead"""
    with open(csv_file, newline="") as file:
        reader = csv.DictReader(
            file, delimiter=",", fieldnames=["actor", "tense", "mode", "kov", "eng", "checked"]
        )
        data = [r for r in reader]
        if "actor" in data[0]:
            data.pop(0)  # Remove header

    # Get a list of the unique verbs (identified by English translation)
    eng = set([v["eng"] for v in data])
    # Get list of all data where each index is a list of dict items for each translation
    verb_data = [[d for d in data if d["eng"] == e] for e in eng]

    if format == "list":
        return verb_data
    elif format == "object":
        return csv_data_to_verb_object(verb_data)


def csv_data_to_verb_object(verb_data: list) -> list:
    """Take a list of dicts representing a verb and return a list of Verb objects instead."""
    verbs = []
    for d in verb_data:
        eng = d[0]["eng"]  # every row item contains this info
        v = KovolVerb("", eng)  # init obj with temp 1s_future

        future_tense = [v for v in d if v["tense"].lower() == "future"]
        for t in future_tense:
            if t["actor"].lower() == "1s":
                v.future_1s = t["kov"]
            elif t["actor"].lower() == "2s":
                if not t["mode"] == "imperative":
                    v.future_2s = t["kov"]
            elif t["actor"].lower() == "3s":
                v.future_3s = t["kov"]
            elif t["actor"].lower() == "1p":
                v.future_1p = t["kov"]
            elif t["actor"].lower() == "2p":
                if not t["mode"] == "imperative":
                    v.future_2p = t["kov"]
            elif t["actor"].lower() == "3p":
                v.future_3p = t["kov"]

        recent_past_tense = [v for v in d if v["tense"].lower() == "recent past"]
        for t in recent_past_tense:
            if t["actor"].lower() == "1s":
                v.recent_past_1s = t["kov"]
            elif t["actor"].lower() == "2s":
                v.recent_past_2s = t["kov"]
            elif t["actor"].lower() == "3s":
                v.recent_past_3s = t["kov"]
            elif t["actor"].lower() == "1p":
                v.recent_past_1p = t["kov"]
            elif t["actor"].lower() == "2p":
                v.recent_past_2p = t["kov"]
            elif t["actor"].lower() == "3p":
                v.recent_past_3p = t["kov"]

        remote_past_tense = [v for v in d if v["tense"].lower() == "remote past"]
        for t in remote_past_tense:
            if t["actor"].lower() == "1s":
                v.remote_past_1s = t["kov"]
            elif t["actor"].lower() == "2s":
                v.remote_past_2s = t["kov"]
            elif t["actor"].lower() == "3s":
                v.remote_past_3s = t["kov"]
            elif t["actor"].lower() == "1p":
                v.remote_past_1p = t["kov"]
            elif t["actor"].lower() == "2p":
                v.remote_past_2p = t["kov"]
            elif t["actor"].lower() == "3p":
                v.remote_past_3p = t["kov"]

        imperatives = [v for v in d if v["mode"]]
        for t in imperatives:
            if t["actor"].lower() == "2s":
                v.singular_imperative = t["kov"]
            elif t["actor"].lower() == "2p":
                v.plural_imperative = t["kov"]
            elif t["mode"].lower() == "short":
                v.short = t["kov"]

        verbs.append(v)
    verbs = sorted(verbs, key=lambda x: x.future_1s)
    return verbs
