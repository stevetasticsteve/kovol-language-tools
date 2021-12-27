# Hansen verb prediction
Predictions generated from 3PF

---

## predict_root
- root =  3PF - "is" or subtract "js"

---
## predict_remote_past_tense
- suffixes = "om", "oŋ", "ot", "omuŋg", "omwa", "ɛmind"
- if last vowel = "ɛ"
  - if last 2 characters = "ɛl" AND the preceding verb = "u"
    - last 2 characters = "ul"
  - else 
    - suffixes = normal suffixes -else replace "ɛ" in root with "o"
- elif last vowel = "u"
  - suffixes = normal suffixes, but replace "o" with "u"

- **Result = root + suffix**

---

## predict_recent_past_tense
- suffixes = "ogom", "ogoŋ", "ɛge", "oŋg", "agama", "ogond"
  
- if last vowel = "ɛ"
  - if last 2 characters are "ɛl"
    - shorten suffixes by removing first 2 characters
    - if preceded by "u" in previous syllable
      - suffixes = "ugam", "ugoŋ", "uga", "aŋg", "uguma", "ugand"
    - else 
        - change "ɛ" to "a" in root for 1s, 3s, 1p, 2p, 3p
        - change "ɛ" to "o" in root for 2s
        - suffixes = "agam", "ogoŋ", "aga", "aŋg", "agama", "agand"
  - else 
    - root for 1s, 2s, 1p, 3p = replace "ɛ" in root with "o"
    - root for 2p = replace "ɛ" in root with "a"
   
- elif last vowel = "u"
  - suffixes = "ugum, "ugoŋ", "uge", "uŋg", "uguma", ugund"
  - if last character = m
    - 1s suffix = "ogom"
- elif last vowel = i
  - suffixes = "igom", "igoŋ", "ige", "oŋg", "igima", "igond"

- if last character = "m"
  - if last 2 characters of root = "um" or "ɛm"
    - shorten all suffixes by removing 1st character
    - if last 2 characters of root = "um"
      - 1p suffix = "uŋg"
    - if last 2 characters of root = "ɛm"
      - 1p suffix = "oŋg"
  - elif penultimate character = "u" or "ɛ"
    - do nothing (avoids the else statement following this)
  - else
    - replace 'm' with "ŋ" in root
    - 1p root = normal root
    - shorten all suffixes by removing 1st character
    - 1p suffix = "oŋg"
- elif last character = "g"
  - shorten suffixes by removing first 2 characters
  - 1p suffix = "oŋg"



- **Result = root + suffix**

---

## predict_future_tense
- suffixes = "ɛnim", "ɛniŋ", "iŋ", "ug", "wa", "is"
- if last vowel = "i" or "u" or last character = "m"
  - 1s suffix = "inim"
  - 2s suffix = "iniŋ"
- elif last 2 characters are "ɛl"
  - shorten suffixes by removing 2 initial characters in 1s, 2s
  - 3s suffix = "aŋ"
- elif last vowel = "ɛ"
  - replace "ɛ" with "o" in 1p and 2p root


- **Result = root + suffix**

---

## predict imperative
- suffixes = "ɛ", "as"
- if last vowel = "ɛ"
  - replace "ɛ" with "a" in 2p root
- if last character = "g"
  - 2s suffix = "u"
  - 2p suffix = "was"

- **Result = root + suffix**