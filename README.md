# archon

digs through archives and finds the nasty bits. clamav inside, own yara on top, no scare tactics - just what, where and why.

![ci](https://github.com/palychdev/archon/actions/workflows/test.yml/badge.svg)

## why another scanner

most scanners either scream at everything or hide what they do. archon shows the file, the inner file if it was packed, and the sig name. packed-but-clean stuff gets a calm `high-entropy` note instead of a red alert.

## 30 seconds start

```sh
git clone https://github.com/palychdev/archon
cd archon
pip install -e .
python -m archon.cli --setup
python -m archon.cli --gui
```

no terminal mood? `--menu` walks you through, `--gui` is a plain window: pick folder, tick boxes, hit scan.

## what it does

- nested packs: zip/rar/7z/iso, depth/size/timeout guards so one monster archive can't hang the box
- clamav bases via freshclam, user-local config so no admin dance
- own `rules/` for miners and stealers, runs via yara lib or binary
- entropy flag for packed unknowns
- autostart list + snapshot diff (`--snap-save base.json`, `--snap-diff base.json`)
- quarantine move + restore + rescan
- json out + log file + exit 1 on hits, scripts love it
- watch mode for drop folders, parallel yara/entropy with `--workers`

## honest limits

- needs clamav binaries, they're big and bases update daily
- full `C:\` scan is slow, start with downloads
- heuristics can false-positive on packed games and installers, allowlist them by sha256 in `archon.toml`

## credits

engine: clamav by Cisco Talos (GPLv2, you install it, we just call it). yara rules here are ours. see THIRD-PARTY.md.
