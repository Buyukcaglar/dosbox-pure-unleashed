# Embedded archive development resource

`phase3-smoke.dosz` is a license-safe development fixture that can be embedded into the Visual Studio executable as `IDR_EMBEDDED_ARCHIVE` `RCDATA` resource 101.

The archive contains `DOSBOX.BAT` and a generated FAT12 floppy image named `DISK.IMA`. The batch file writes `PHASE3.OK`, mounts the image directly from inside the embedded DOSZ, checks for `A:\IMAGE.OK`, and writes `PHASE3.IMG` through DOSBox Pure's normal writable overlay when the image read succeeds.

`phase3-smoke.json` is the matching Phase 6 package metadata embedded as `IDR_EMBEDDED_METADATA` `RCDATA` resource 102. Its stable `package_id` selects persistence, its title brands the window, and its `archive_identity` binds the metadata to the exact fixture archive. Rebuilding or replacing the DOSZ requires updating the identity while retaining the package ID when saves should remain associated.

`phase3-smoke/make_floppy.py` reproducibly generates `DISK.IMA` from the license-safe `phase3-smoke/IMAGE.OK` sentinel. No third-party game or operating-system content is included.

Normal builds exclude the fixture and produce a clean runtime template. To build the development fixture explicitly, pass:

```powershell
MSBuild.exe DOSBoxPure-vs.vcxproj /p:Configuration=ReleaseGLCORE /p:Platform=x64 /p:EmbedDevelopmentPackage=true
```

The Phase 7 package builder adds a selected game archive and matching package metadata to the clean template. The opt-in fixture build remains available for embedded-resource and no-extraction regression testing.
