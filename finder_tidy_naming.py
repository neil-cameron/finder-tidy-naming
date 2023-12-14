import argparse
import os
import re
import string
from ast import mod

from words import (
    del_delims,
    delims,
    examples,
    ignore_filenames,
    lowercase_words,
    unmodified_words,
)

parser = argparse.ArgumentParser()

# Arguments
parser.add_argument(
    "-f",
    "--front",
    type=int,
    help="The number of characters to delete from the front of each file or directory name",
)
parser.add_argument(
    "-e",
    "--end",
    type=int,
    help="The number of characters to delete from the end of each file or directory name",
)
parser.add_argument(
    "-p",
    "--path",
    nargs="+",
    type=str,
    help="A full or relative path to a file, several files, a directory, or several directories of items to rename",
)

args = parser.parse_args()

# Parse arguments
front = 0
end = 0
list_of_paths = []

if args.front:
    front = args.front

if args.end:
    end = args.end

if args.path:
    [list_of_paths.append(individual_path) for individual_path in args.path]


def process_title(title, **kwargs):
    front = kwargs.pop("front", 0)
    end = kwargs.pop("end", 0)

    # Trim from front and back
    if (len(title) - front - end) > 0:
        title = title[front:]
        title = title[: ((len(title)) - end)]
    else:
        print(
            "Too many characters requested to be removed"
            # f"Too many characters requested to be removed from {title}. This action would result in no file name at all. This file has been skipped."
        )
        return

    # Pad delimeters
    for delim in delims:
        title = title.replace(delim, " " + delim + " ")

    # Delete bad characters
    # title = title.replace(u"\u2018", "'").replace(u"\u2019", "'")

    # Split
    individual_words = title.split(" ")

    # Neaten and remove bad delimeters
    individual_words = [word for word in individual_words if word not in del_delims]

    # Capitalisation loop through words
    capitalised_words = []
    for position, word in enumerate(individual_words):
        mod_word = string.capwords(word)
        if position != 0:
            previous_word = individual_words[position - 1]
            if word.lower() in lowercase_words:
                if previous_word.isdigit():
                    mod_word = word.title()
                elif previous_word in delims:
                    mod_word = word.title()
                else:
                    mod_word = word.lower()
            if word in unmodified_words:
                mod_word = word
            if word == ".":
                if previous_word.isdigit():
                    mod_word = ""  # "."  # Special tweak to no longer keep decimal points as decimal points because of titles like 07.F1.2023.Round.23.Abu.Dhabi.mkv
                else:
                    mod_word = ""

        # Special tweak just to deal with the fact that opening '(' is attached to the word so the next letter after is not capitalised
        if len(mod_word) >= 2:
            if mod_word[0] == "(":
                mod_word_chars = []
                for position, character in enumerate(mod_word):
                    if position != 1:
                        mod_word_chars.append(character)
                    else:
                        mod_word_chars.append(character.capitalize())
                mod_word = "".join(mod_word_chars)

        # Special tweak just to deal with season and episode codes
        if len(mod_word) >= 2:
            if re.match(r"[sS][0-9]{2}[eE][0-9]{2}", mod_word):
                mod_word_chars = []
                for character in mod_word:
                    if character.isdigit():
                        mod_word_chars.append(character)
                    else:
                        mod_word_chars.append(character.capitalize())
                mod_word = "".join(mod_word_chars)

        capitalised_words.append(mod_word)

    # Reinstate spaces
    processed_title = " ".join(capitalised_words)
    processed_title = " ".join(
        processed_title.split()
    )  # Second pass to fix double spaces
    processed_title = processed_title.split(" . ")  # Fix for dots together with numbers
    processed_title = ".".join(processed_title)

    return processed_title


# Test
# for item in examples:
#     print(process_title(item))


def rename_file(dir_path, file_name, front, end):
    if not file_name in ignore_filenames:
        if not file_name.startswith("."):
            file_name_root, file_extension = os.path.splitext(file_name)
            new_name = process_title(file_name_root, front=front, end=end)
            new_name_plus_ext = new_name + file_extension.lower()

            file_path_old_name = os.path.join(dir_path, file_name)
            file_path_new_name = os.path.join(dir_path, new_name_plus_ext)
            os.rename(file_path_old_name, file_path_new_name)


def rename_dir(dir_path, dir_name, dirs_to_rename, front, end):
    if not dir_name.startswith("."):
        new_name = process_title(dir_name, front=front, end=end)
        dir_path_old_name = os.path.join(dir_path, dir_name)
        dir_path_new_name = os.path.join(dir_path, new_name)
        dirs_to_rename.append((dir_path_old_name, dir_path_new_name))


def rename_dirs_and_files(path_to_process, front, end):
    dirs_to_rename = []  # This list is processed after the files are done
    if os.path.isdir(path_to_process):  # Directory
        for dir_path, dir_names, file_names in os.walk(path_to_process):
            for file_name in file_names:
                rename_file(dir_path, file_name, front, end)
            for dir_name in dir_names:
                rename_dir(dir_path, dir_name, dirs_to_rename, front, end)

        # Rename the root folder too
        root_dir_path = os.path.dirname(path_to_process)
        root_dir_name = os.path.basename(os.path.normpath(path_to_process))
        rename_dir(root_dir_path, root_dir_name, dirs_to_rename, front, end)
    else:  # File
        dir_path, file_name = os.path.split(path_to_process)
        rename_file(dir_path, file_name, front, end)

    # Rename the directories last
    for dir_tuple in dirs_to_rename:
        os.rename(dir_tuple[0], dir_tuple[1])


# Test
# test_dir = "/Users/neil/Downloads/Renaming Test Folder"
# rename_dirs_and_files(test_dir)


# Run the script
for individual_path in list_of_paths:
    rename_dirs_and_files(individual_path, front, end)
