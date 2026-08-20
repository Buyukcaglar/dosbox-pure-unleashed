# Embedded archive development resource

`phase3-smoke.dosz` is a license-safe development fixture embedded into the Visual Studio executable as `RCDATA`.

The archive contains `DOSBOX.BAT` and a generated FAT12 floppy image named `DISK.IMA`. The batch file writes `PHASE3.OK`, mounts the image directly from inside the embedded DOSZ, checks for `A:\IMAGE.OK`, and writes `PHASE3.IMG` through DOSBox Pure's normal writable overlay when the image read succeeds.

`phase3-smoke/make_floppy.py` reproducibly generates `DISK.IMA` from the license-safe `phase3-smoke/IMAGE.OK` sentinel. No third-party game or operating-system content is included.

The fixture is temporary development packaging content. A later package-builder phase will replace it with a selected game archive and package metadata.
