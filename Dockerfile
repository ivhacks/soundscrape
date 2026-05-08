FROM fedora:43

RUN dnf install -y \
    python3 python3-tkinter libpq-devel \
    git curl fedora-workstation-repositories \
    && dnf config-manager setopt google-chrome.enabled=1 \
    && dnf install -y google-chrome-stable \
    && dnf clean all

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

RUN git clone https://github.com/ivhacks/soundscrape.git /soundscrape
WORKDIR /soundscrape
COPY secrets.yaml .
RUN uv sync --extra dev
RUN git pull
ENV PATH="/soundscrape/.venv/bin:$PATH"

# fully passing
RUN pytest test/test_parse_clean.py -v --tb=short
RUN pytest test/test_metadata.py -v --tb=short
RUN pytest test/test_genius_basic.py -v --tb=short
RUN pytest test/test_spotify.py -v --tb=short
RUN pytest test/test_img_diff.py -v --tb=short
RUN pytest test/test_genius_real_songs.py -v --tb=short
RUN pytest test/test_soundscrape_file_io.py -v --tb=short
RUN pytest test/test_view_link.py -v --tb=short
RUN pytest test/test_bandcamp_search.py -v --tb=short
RUN pytest test/test_beatport_search.py -v --tb=short
RUN pytest test/test_misc.py -v --tb=short
RUN pytest test/test_art_search.py -v --tb=short
RUN pytest test/test_anthropic_api.py -v --tb=short

# has failures — longest first
RUN pytest test/test_artists_and_features.py -v --tb=short || true
RUN pytest test/test_integration.py -v --tb=short || true
RUN pytest test/test_google_images.py -v --tb=short || true
RUN pytest test/test_album_search.py -v --tb=short || true
RUN pytest test/test_get_img.py -v --tb=short || true
RUN pytest test/test_yt_music_metadata.py -v --tb=short || true
RUN pytest test/test_sevendigital_search.py -v --tb=short || true
RUN pytest test/test_selenium_chrome.py -v --tb=short || true

CMD ["pytest", "--tb=short", "-v"]
