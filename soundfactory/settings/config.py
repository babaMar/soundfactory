from pathlib import Path

this_folder = Path(__file__).resolve().parent

BUILDER_CACHE_PATH = str(this_folder / "builder_cache.pickle")
