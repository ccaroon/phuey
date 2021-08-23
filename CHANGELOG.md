# CHANGELOG

## 0.0.5 - 2021-08-23
### CLI
* Each command is now a separate module in the new `cli` dir
* Added `init` command.
* Added `light` commands (get, set, list).
  * Now requires a config file. See `phuey init`.

### Library
* Added `get_lights` method to HueBridge
  - Updated `get_light` to use `get_lights`

## 0.0.4 - 2021-08-22
* Added `--version` flag to CLI

## 0.0.3 - 2021-08-22
* Fixed bug in HueBridge caused by changing the params to the `error` method
  on last commit.

## 0.0.2 - 2021-08-22
* HueBridge: Added ability to generate a username (token)
* Added simple CLI: `phuey -h`
  - Currently only supports one action: `create-username`

## 0.0.1 - 2021-08-21
* Initial Release
