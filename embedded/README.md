# Embedded archive development resource

`phase3-smoke.dosz` is a license-safe development fixture embedded into the Visual Studio executable as `RCDATA`.

The archive contains only `DOSBOX.BAT`, built from `phase3-smoke/DOSBOX.BAT`. The batch file writes `PHASE3.OK` through DOSBox Pure's normal writable overlay and exits. This provides a deterministic Phase 3 runtime test without bundling third-party game content.

The fixture is temporary development packaging content. A later package-builder phase will replace it with a selected game archive and package metadata.
