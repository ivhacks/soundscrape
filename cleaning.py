import re
from typing import List


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


def find_features(input: str) -> List[str]:
    features = []

    # Pattern 1: (feat. Artist) or (Feat. Artist) or (ft. Artist) or (featuring Artist)
    paren_feature = re.search(
        r"\((feat\.|Feat\.|ft\.|featuring)\s+(.+?)\)", input, re.IGNORECASE
    )
    if paren_feature:
        features.append(paren_feature.group(2).strip())

    # Pattern 2: Title feat./ft./featuring Artist (same variants as parenthesized)
    non_paren_feature = re.search(
        r"\s(feat\.|Feat\.|ft\.|featuring)\s+(.+)$", input, re.IGNORECASE
    )
    if non_paren_feature and not paren_feature:
        features.append(non_paren_feature.group(2).strip())

    return features
