import re


def clean_title(title):

    # https://medium.com/@georgelgore/using-regex-to-remove-brackets-and-parentheses-from-a-string-3a6067155d74

    no_parens = re.sub("\(.*\)", "", title)
    no_brackets = re.sub("\[.*\]", "", no_parens)
    no_ft = no_brackets.split("ft.")[0]
    no_feat = no_ft.split("feat.")[0]
    no_Feat = no_feat.split("Feat.")[0]

    return no_Feat.strip()


def clean_artist(artist):
    no_semicolons = artist.replace(";", "")
    no_commas = no_semicolons.replace(",", "")
    return no_commas.strip()
