archon - deep scan for packed stuff.

built on clamav + own yara, focused on nested archives and autostart traces. no scareware, just shows what found and where.

install:
- python 3.11+
- install clamav and make sure `clamscan` and `freshclam` are in PATH
- optional: `yara` binary or `yara-python` for own rules
- pip install -e .

use:
- `python -m archon.cli some/folder` - scan folder, archives included
- `python -m archon.cli some/file.zip --depth 8 --max-mb 1024` - deeper for big packs
- `python -m archon.cli some/folder --exclude node_modules --exclude .git` - skip trash
- `python -m archon.cli some/folder --json > out.json` - for scripts, exit 1 if hits
- `python -m archon.cli --hashes some/folder` - list sha256
- `python -m archon.cli --autoruns` - show run keys + startup
- `python -m archon.cli --update` - refresh clamav bases via freshclam
- `python -m archon.cli some/folder --quarantine ./q` - move hits aside
- `python -m archon.cli some/folder --yara` - also run rules/
- `python -m archon.cli some/folder --log scan.log` - append result to file
- `python -m archon.cli --rescan ./q` - recheck quarantine
- copy `archon.toml.example` to `archon.toml` for defaults, allow_sha256 skips known clean

notes:
- big archives are cut by depth/size/timeout, tune flags if needed
- yara rules live in `rules/`, add your own
- windows first, python cross-platform where possible
