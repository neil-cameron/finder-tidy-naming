#!/usr/bin/python
# -*- coding: latin-1 -*-

# These are the words that will remain lowercase, unless they begin or end the title.
lowercase_words = [
    "a",
    "an",
    "and",
    "at",
    "but",
    "by",
    "for",
    "in",
    "nor",
    "of",
    "on",
    "or",
    "so",
    "the",
    "to",
    "with",
]
# Optional additional words: "amid", "anti", "as", "down", "into", "like", "near", "off", "onto", "out", "over", "past", "per", "plus", "save", "some", "than", "till", "up", "upon", "via", "yet"

# These are the words that won't be modified at all. It's a good place to put all-uppercase words.
unmodified_words = [
    "FM",
    "USA",
    "WDPK",
    "OYFN",
    "UR",
    "TV",
    "MGM",
    "DVD",
    "ABC",
    "CD",
    "USSR",
    "CA",
    "WA",
    "NY",
    "NYC",
    "LP",
    "EP",
    "VHS",
    "UK",
    "GB",
    "'Bout",
    "'Cause",
    "o'",
    "'n'",
    "n'",
    "McCartney",
    "vs.",
    "de",
    "feat.",
    "Pi-hsien",
    "von",
    "van",
    "HBR",
    "CRC",
    "DOE",
    "ANSYS",
    "ASM",
    "BBC",
    "NPR",
]

# Delimeters to pad
delims = []
[
    delims.append(item) for item in "_%&/=¿?¡|¢∞*-+•«»—ºª…;."
]  #'_!"$%&/()=¿?@¡|#¢∞“”[]{}*-+•«»—´`ºª…:;.,']

# Delimeters to delete
del_delims = [
    ";",
    "_",
    "~",
    "",
]

# File names to ignore
ignore_filenames = [
    ".DS_Store",
]

# Example file names for testing
examples = [
    "armathwaite-guide.pdf",
    "How_to_Network_Effectively_-_Scripts_Templates_and_Tips.pdf",
    "97575_00_00_MM01_what Is_AFTerfx.mov",
    "01_Understanding the Event Library.mov",
    "82541_02_02_SC11_library.mp4",
    "bar_chord_rhythm#1_BD.mp3",
    "title_-_episode.S01E01.mp4",
    "(brian)_iss.2-[vol 3]",
    "en.1993.1.5.2006.pdf",
    "A; more,    common&example *with {some} brackets_McCartney.pdf",
    "1.0 G.R.R.Martin. Martin TM. Lewin",
    "WeWork.or.The.Making.and.Breaking.of.a.47.Billion.Unicorn.2021.720p.WEBRip.800MB.x264-GalaxyRG",
    "04 - Alice's Essential Kitchen Tools - Alice Waters Teaches the Art of Home Cooking.mp4",
    "05 - a Well - Stocked Pantry - Alice Waters Teaches the Art of Home Cooking",
    "16 - the Power of Food the Edible Schoolyard - Alice Water's Teaches the Art of Home Cooking",
    "15.12.21 the Power of Food",
    "hello (the full picture)",
    "Title - s01e02",
]