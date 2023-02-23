# pardisc
This is the repository for pardisc (lowercase), a Discord bot for the party games you can't do because you're not in the same place. This README is "under construction" (meaning, I don't know if I'm going to share this repo with anyone else, so I don't know if I need it), so things might be weird, but hopefully fixed in future commits.

## Things

* Limit line length to 100 characters.

## Version Numbers
* **Major** version numbers (e.g. ***2***.3.7) signify major feature releases. Usually, these also contain bug fixes. An example of a major release changelog could be:
```
- Add game 1
- Add gamemode 1 for game 2
- Fix issue with game 3
- Fix issue with command 8
```
* **Minor** version numbers (e.g. 2.***3***.7) signify either a collection of bug fixes or a small feature release. An example of a minor release changelog could be:
```
- Add setting 7 for game 1
- Fix issue with game 10
- Fix issue with command 2
```
* **Patch** version numbers (e.g. 2.3.***7***) signify small bug fixes or patches. An example of a minor release changelog could be:
```
- Fix issue with setting 3 not working
- Fix ambiguous wording in prompt 324
```

### Version Modifiers
* A version suffix of `-dev` signifies a pre-release, unstable, usually not working version. This is the tag used when a version is in development.
* A version suffix of `-beta` (for example, "2.3.7-beta") signifies a pre-release, unstable, but generally working version.
* A version suffix of `-rc-x` or `-release-candidate-x` indicates a release **candidate**. For example, there could be two ways something could work, and two versions could be developed. This suffix should be used with something other than `-stable`, usually `-dev`. This suffix is not used as often as the others. 
* A version suffix of `-stable` indicates a stable release. If not specified, versions have this suffix implicitly.

### 0.x.y Versions
If the major version number is 0, the version is more unstable than a normal version starting with 1, or 2, or etc. Features may be added or removed at any time. Even if a version has the `-stable` tag, the version is not generally reliable. Things may work, but the project is in development.