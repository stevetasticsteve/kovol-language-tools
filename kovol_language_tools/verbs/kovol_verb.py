from tabulate import tabulate

from kovol_language_tools.facts import phonetic_vowels


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


class PredictedVerb(KovolVerb):
    def __str__(self):
        string = self.get_string_repr()
        return f"Predicted Kovol verb: {string['future_1s']}, \"{string['english']}\""

    def __repr__(self):
        return self.__str__()

    def predict_verb(self) -> None:
        """A method to call all prediction methods together. Called during __init__."""
        self.predict_future_tense()
        self.predict_recent_past_tense()
        self.predict_remote_past_tense()
        self.predict_imperative()

    def root_ending(self) -> str:
        """Returns whether the root ends in a Vowel "V" or Consonant "C".
        Called during __init__."""
        if self.root[-1] in self.vowels:
            return "V"
        else:
            return "C"

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
        order = [f"{t}_{a}" for t in self.tenses for a in self.actors] + ["singular_imperative", "plural_imperative"]
       
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
