import json
from pathlib import Path

from utils import read_json_file, write_json_file

def has_particle(word):
    pass

def get_valid_word(word):
    if word:
        syls = word.split('་')
        if len(syls) < 6:
            if has_particle(word):
                return None
            return word
    else:
        return None

def get_monlam_word_list(monlam_dict_dir):
    monlam_word_list = []
    monlam_dict_file_paths = list(monlam_dict_dir.iterdir())
    for monlam_dict_file_path in monlam_dict_file_paths:
        monlam_dict = read_json_file(monlam_dict_file_path)
        for monlam_word_info in monlam_dict['rows']:
            monlam_word = monlam_word_info[1]
            if monlam_word := get_valid_word(monlam_word):
                monlam_word_list.append(monlam_word)
    monlam_word_list = list(set(monlam_word_list))
    return monlam_word_list

if __name__ == '__main__':
    monlam_dict_dir = Path('data/monlam/')
    monlam_word_list = get_monlam_word_list(monlam_dict_dir)
    write_json_file('data/monlam/monlam_word_list.json', monlam_word_list)