import re


def clean_title(title):
    no_explicit = remove_explicit(title)

    no_parens = re.sub("\(.*\)", "", no_explicit)
    no_brackets = re.sub("\[.*\]", "", no_parens)
    no_ft = no_brackets.split("ft.")[0]
    no_feat = no_ft.split("feat.")[0]
    no_Feat = no_feat.split("Feat.")[0]

    return no_Feat.strip()


def clean_artist(artist):
    no_semicolons = artist.replace(";", "")
    no_commas = no_semicolons.replace(",", "")
    return no_commas.strip()


def remove_explicit(input: str) -> str:
    no_parens = re.sub(r"\(explicit\)", "", input, flags=re.IGNORECASE).strip()
    no_brackets = re.sub(r"\[explicit\]", "", no_parens, flags=re.IGNORECASE).strip()
    no_explicit = re.sub(r"\bexplicit$", "", no_brackets, flags=re.IGNORECASE).strip()
    return no_explicit
