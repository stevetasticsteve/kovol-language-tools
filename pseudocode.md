# Hansen verb prediction
Predictions generated from 3PP

---

## predict_root
- root =  3PP - "is"

---
## predict_remote_past_tense
- suffixes = "om", "oŋ", "ot", "omuŋg", "omwa", "ɛmind"
- if last vowel = "ɛ"
  - replace "ɛ" in root with "o"
- else if last vowel = "u"
  - suffixes = normal suffixes, but replace "o" with "u"

- **Result = root + suffix**

---

## predict_recent_past_tense
- suffixes = "ogom", "ogoŋ", "ɛge", "oŋg", "agama", "ogond"
- if last vowel = "ɛ"
  - root for 1s, 2s, 1p, 3p = replace "ɛ" in root with "o"
  - root for 2p = replace "ɛ" in root with "a"
  - (root for 3s remains normal root)
- else if last vowel = "u"
  - suffixes = "ugum, "ugoŋ", "uge", "uŋg", "uguma", ugund"
  - if last character = m
    - 1s suffix = "ogom"
- else if last vowel = i
  - suffixes = "igom", "igoŋ", "ige", "oŋg", "igima", "igond"

- if last character = "m"
  - if last 2 characters of root = "um" or "ɛm"
    - short all suffixes by removing 1st character
    - 1p suffix = "oŋg"
  - else if penultimate character = "u" or "ɛ"
    - do nothing (avoids the else statement following this)
  - else
    - replace 'm' with "ŋ" in root
    - 1p root = normal root
    - shorten all suffixes by removing 1st character
    - 1p suffix = "oŋg"
- else if last character = "g"
  - shorten suffixes by removing first 2 characters
  - 1p suffix = "oŋg"

- **Result = root + suffix**

---

## predict_future_tense
- suffixes = "ɛnim", "ɛniŋ", "iŋ", "ug", "wa", "is"
- if last vowel = "i" or "u"
  - 1s suffix = "inim"
  - 2s suffix = "iniŋ"
- else if last vowel = "ɛ"
  - replace "ɛ" with "o" in 1p and 2p root

- **Result = root + suffix**

---

## predict imperative
- suffixes = "ɛ", "as"
- if last vowel = "ɛ"
  - replace "ɛ" with "o" in root

- **Result = root + suffix**