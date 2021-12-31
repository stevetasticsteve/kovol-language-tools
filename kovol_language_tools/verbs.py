# This file contains classes and functions for retrieving verb data and putting it into a Verb object.
# Also handles verb prediction.

import csv

from tabulate import tabulate

from kovol_language_tools.facts import phonetic_vowels


def get_data_from_csv(csv_file, format="object") -> list:
    """reads a csv file and outputs a list of KovolVerb objects.
    Can accept 'list' as format to return a list of listed dict entries instead"""
    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(
            file,
            delimiter=",",
            fieldnames=["actor", "tense", "mode", "kov", "eng", "checked"],
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


class KovolVerb:
    """A class to represent a Kovol verb defining the conjugations of it as attributes with methods for retrieving
    those conjugations and printing to screen."""

    vowels = phonetic_vowels  # Vowels in Kovol language
    actors = ("1s", "2s", "3s", "1p", "2p", "3p")
    tenses = ("remote_past", "recent_past", "future")

    def __init__(self, future1s: str, english: str):
        # Meta data
        self.kovol = future1s
        self.english = english
        self.tpi = ""  # Tok pisin
        self.author = ""  # Who entered the data
        self.errors = []  # used for PredictedVerb subclass,
        # defined here to maintain template compatibility

        # Set a blank string for actor/tense combinations
        for t in self.tenses:
            for a in self.actors:
                setattr(self, f"{t}_{a}", "")

        self.future_1s = future1s

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

    def predict_root(self, rules="stanley") -> str:
        """Find the verb root. Can take a keyword argument to change how it's predicted."""

        if rules == "hansen":
            self.root = self.future_3p[:-2]
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
        try:
            v = [c for c in self.root if c in self.vowels]
        except AttributeError:
            self.predict_root()
            v = [c for c in self.root if c in self.vowels]
        v = "".join(v)
        return v

    def get_vowel_n(self, n) -> str or None:
        """Return the nth vowel, or None"""
        v = self.verb_vowels()
        if not v:
            return None
        else:
            try:
                return v[n]
            except IndexError:
                return None

    def get_last_root_vowel(self) -> str or None:
        """Returns last vowel of root, or None"""
        v = self.verb_vowels()
        if not v:
            return None
        else:
            return v[-1]

    def get_last_root_character(self) -> str or None:
        """Returns last character of root, or None"""
        try:
            return self.root[-1]
        except IndexError:
            return None
        except AttributeError:
            self.predict_root()
            return self.root[-1]

    def get_last_two_root_characters(self) -> str or None:
        """Returns the last two characters of the root, or None"""
        try:
            return self.root[-2:]
        except IndexError:
            return None
        except AttributeError:
            self.predict_root()
            return self.root[-2:]

    def get_remote_past_tense(self) -> tuple:
        """Return a tuple of remote past conjugations."""
        return tuple([getattr(self, f"remote_past_{a}") for a in self.actors])

    def get_recent_past_tense(self) -> None:
        """Return a tuple of recent past tense conjugations."""
        return tuple([getattr(self, f"recent_past_{a}") for a in self.actors])

    def get_future_tense(self) -> tuple:
        """Return a tuple of future tense conjugations."""
        return tuple([getattr(self, f"future_{a}") for a in self.actors])

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
        self.predict_remote_past_tense()
        self.predict_imperative()

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


class HansenPredictedKovolVerb(PredictedKovolVerb):
    """Class to replace the standard method of predicting verbs with the Hansen alternative."""

    def __init__(self, future_3p, english=""):
        super(PredictedKovolVerb, self).__init__(future1s="", english=english)
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
