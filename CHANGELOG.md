# changelog

## 0.13.0
- user writable base config, no admin needed

## 0.12.0
- auto setup via winget

## 0.11.0
- console menu and simple window, no flags needed

## 0.10.0
- parallel yara and entropy, tui progress
- live eicar parse check passed

## 0.9.0
- watch mode for new files
- clear hint when engine missing
- working exe build, tested on windows

## 0.8.0
- entropy flag for packed files
- autoruns snap diff, quarantine restore
- unofficial sigs option, ci, eicar tests

## 0.7.0
- fixed FOUND parse, added tests
- mit license + third party notes
- exe build script

## 0.6.0
- working yara run via lib or binary
- toml config, allowlist by sha256
- log file, exit 1 on hits, rescan flag

## 0.5.0
- base updater via freshclam
- quarantine move for hits
- second yara rule, readme with usage

## 0.4.0
- timeout guard against huge archives
- exclude dirs for scan

## 0.3.0
- json output for scripts
- sha256 listing for files

## 0.2.0
- clamscan wrapper with archive flags
- text report, autostart listing
- first yara rule for miners

## 0.1.0
- project skeleton, readme only
- engine plan: clamav + unofficial sigs + own yara
