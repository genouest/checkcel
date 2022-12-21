# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This changelog was started for release 0.0.3.

## [0.0.3] - 21/11/2022

### Added

- empty_ok_if key for validator & templates
- empty_ok_unless key for validator & templates
- readme key for validator
- unique key for validator
- expected_rows key for templates
- logs parameters for templates
- na_ok key for validators & templates
- skip_generation key for validators & templates
- skip_validation key for validators & templates

### Fixed

- Bug for setValidator when using number values
- Fixed regex for GPS

### Changed

- Better validation for integers
- Refactor validation in excel for most validators (to include unique & na_ok)
