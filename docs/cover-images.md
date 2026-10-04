# Cover images and work links

Cover originals are configured in `SOURCE_WORK_OVERRIDES` in
`tools/build_quotes_project.py`. When adding a work, select its correct edition
or screen adaptation, then run:

```sh
python3 tools/cache_cover_images.py
python3 tools/build_quotes_project.py
```

Commit `site/assets/ai-dystopia-quotes/covers/` together with the generated
outputs. The cache manifest retains original image URLs, source pages, retrieval
dates and SHA-256 hashes. Images remain copyrighted by their respective owners;
caching is not a grant of redistribution rights. Review source-page usage terms
before adding or publishing new artwork.

Normal builds are offline. They use only verified local cache files, with a
placeholder for missing artwork rather than a fragile hotlink. `--refresh`
explicitly re-fetches images; failures never replace a good cached image.
The download command requires `curl` and uses its platform TLS trust store.

The publisher copies only covers referenced by approved records to the shared
public repository under `assets/ai-dystopia-quotes/covers/`. Relative asset URLs
work both locally and below the GitHub Pages `/public/` prefix. Include these
files in the public-repository commit along with its HTML and JSON exports.

Film and television catalog buttons use IMDb. Written works use explicitly
labelled Amazon.ca searches by title and author, not unverified product IDs or
claims of stock availability. Citation and metadata links remain unchanged.

## October 4 audit

Replaced eight dead image URLs (Dune, Westworld TV, First Contact, Moon,
Automata, Portal, TRON and Chappie), using their current Wikipedia work pages.
Added previously absent artwork for Westworld (film), M3GAN, Nineteen Eighty-Four
and Avengers: Age of Ultron. The cache holds 35 images (about 3 MB).
The Evitable Conflict, With Folded Hands and The Machine Stops intentionally
retain placeholders until suitable edition artwork is selected.

Corrected film-to-novel catalog mismatches for 2001, Colossus and Demon Seed,
and added IMDb links for Avengers, Portal and Mass Effect 3. Across 47 quote
records, 38 now link to IMDb and nine written-work records link to Amazon.ca
searches. No verified Amazon.ca edition/product availability is claimed.

Run offline regression checks with `python3 tools/test_cover_images.py`.
