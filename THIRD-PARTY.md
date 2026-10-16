third party bits archon calls, not bundled:

- clamav (`clamscan`, `freshclam`) - GPLv2, by Cisco Talos. archon just runs the binary you installed. bases belong to their owners.
- yara (`yara` binary or `yara-python`) - Apache 2.0 / BSD style depending on build. rules in `rules/` are ours.
- unofficial sigs if you add them - check their own license before sharing.

if you ship an exe, ship these notes with it and point people at upstream sources.
