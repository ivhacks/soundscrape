from PIL import Image


def _perceptual_hash(image: Image.Image, hash_size: int = 8) -> str:
    """Generate a perceptual hash for an image"""
    # Resize to hash_size x hash_size and convert to grayscale
    image = image.resize((hash_size, hash_size), Image.Resampling.LANCZOS).convert("L")

    # Get pixel values as list
    pixels = list(image.getdata())

    # Calculate average pixel value
    avg = sum(pixels) / len(pixels)

    # Create hash based on whether pixels are above or below average
    return "".join("1" if pixel > avg else "0" for pixel in pixels)


def _hamming_distance(hash1: str, hash2: str) -> int:
    """Calculate hamming distance between two hash strings"""
    if len(hash1) != len(hash2):
        return len(hash1)  # Maximum distance if lengths differ

    return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))


def _histogram_similarity(image1: Image.Image, image2: Image.Image) -> float:
    """Calculate histogram similarity between two images"""
    # Convert both images to RGB to ensure consistent histograms
    img1_rgb = image1.convert("RGB")
    img2_rgb = image2.convert("RGB")

    # Get histograms for each channel
    hist1_r = img1_rgb.histogram()[0:256]
    hist1_g = img1_rgb.histogram()[256:512]
    hist1_b = img1_rgb.histogram()[512:768]

    hist2_r = img2_rgb.histogram()[0:256]
    hist2_g = img2_rgb.histogram()[256:512]
    hist2_b = img2_rgb.histogram()[512:768]

    # Calculate correlation for each channel
    def correlation(hist1, hist2):
        # Normalize histograms
        total1 = sum(hist1)
        total2 = sum(hist2)
        if total1 == 0 or total2 == 0:
            return 0.0

        hist1_norm = [x / total1 for x in hist1]
        hist2_norm = [x / total2 for x in hist2]

        # Calculate correlation coefficient
        mean1 = sum(i * h for i, h in enumerate(hist1_norm)) / len(hist1_norm)
        mean2 = sum(i * h for i, h in enumerate(hist2_norm)) / len(hist2_norm)

        num = sum(
            (i - mean1) * (j - mean2) * h1 * h2
            for i, (h1, h2) in enumerate(zip(hist1_norm, hist2_norm))
            for j in [i]
        )

        den1 = sum((i - mean1) ** 2 * h for i, h in enumerate(hist1_norm))
        den2 = sum((i - mean2) ** 2 * h for i, h in enumerate(hist2_norm))

        if den1 == 0 or den2 == 0:
            return 0.0

        return num / (den1 * den2) ** 0.5

    # Simple intersection method instead of correlation (more reliable)
    def intersection(hist1, hist2):
        return sum(min(h1, h2) for h1, h2 in zip(hist1, hist2)) / max(
            sum(hist1), sum(hist2), 1
        )

    # Calculate intersection for each channel
    r_sim = intersection(hist1_r, hist2_r)
    g_sim = intersection(hist1_g, hist2_g)
    b_sim = intersection(hist1_b, hist2_b)

    # Return average similarity across channels
    return (r_sim + g_sim + b_sim) / 3.0


def same_images(image1: Image.Image, image2: Image.Image) -> float:
    """
    Calculate similarity between two images.
    Returns a float between 0.0 and 1.0, where 1.0 means identical.
    """
    # Handle identical image objects
    if image1 is image2:
        return 1.0

    # Generate perceptual hashes with different sizes for better discrimination
    hash1_8 = _perceptual_hash(image1, 8)
    hash2_8 = _perceptual_hash(image2, 8)
    hash1_16 = _perceptual_hash(image1, 16)
    hash2_16 = _perceptual_hash(image2, 16)

    # Calculate hash similarities
    hash_distance_8 = _hamming_distance(hash1_8, hash2_8)
    hash_similarity_8 = 1.0 - (hash_distance_8 / len(hash1_8))

    hash_distance_16 = _hamming_distance(hash1_16, hash2_16)
    hash_similarity_16 = 1.0 - (hash_distance_16 / len(hash1_16))

    # Average the hash similarities
    hash_similarity = (hash_similarity_8 + hash_similarity_16) / 2.0

    # Calculate histogram similarity
    hist_similarity = _histogram_similarity(image1, image2)

    # Apply more aggressive weighting - structural similarity is more important
    # and use a non-linear combination to emphasize when both metrics agree
    if hash_similarity > 0.8 and hist_similarity > 0.6:
        # Both high - likely same image
        combined_similarity = (hash_similarity * 0.7) + (hist_similarity * 0.3)
    elif hash_similarity < 0.4 or hist_similarity < 0.3:
        # Either very low - likely different images, reduce score more aggressively
        combined_similarity = (hash_similarity * hist_similarity) ** 0.5
    else:
        # Mixed signals - standard weighting
        combined_similarity = (hash_similarity * 0.8) + (hist_similarity * 0.2)

    return max(0.0, min(1.0, combined_similarity))
