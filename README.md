archon - deep scan for packed stuff.

built on clamav + own yara, focused on nested archives and autostart traces. no scareware, just shows what found and where.

install:
- python 3.11+
- install clamav and make sure `clamscan` and `freshclam` are in PATH
- pip install -e .

use:
- `python -m archon.cli some/folder` - scan folder, archives included
- `python -m archon.cli some/file.zip --depth 8 --max-mb 1024` - deeper for big packs
- `python -m archon.cli some/folder --exclude node_modules --exclude .git` - skip trash
- `python -m archon.cli some/folder --json > out.json` - for scripts
- `python -m archon.cli --hashes some/folder` - list sha256
- `python -m archon.cli --autoruns` - show run keys + startup
- `python -m archon.cli --update` - refresh clamav bases via freshclam
- `python -m archon.cli some/folder --quarantine ./q` - move hits aside

notes:
- big archives are cut by depth/size/timeout, tune flags if needed
- yara rules live in `rules/`, add your own
- windows first, python cross-platform where possible
