# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- The chart unit test snapshots match the chart again. They recorded a rendering that is several chart
  changes old, so both suites failed: the identity file path, the two volume `secretName` values and the
  container resource limits had all moved on without the snapshots. Nothing in the repository ran
  `helm unittest`, so no build reported it.


- The `helm.sh/chart` label is valid for long chart versions: the 63-character cut trims the whole trailing run of `-`, `.` and `_`.

- initial commits for first release

[Unreleased]: https://github.com/giantswarm/teleport-event-handler/tree/main
