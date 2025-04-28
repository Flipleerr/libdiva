# libdiva
library with tools to manipulate file formats found in Project Diva

## installation
open a terminal session and install using pip:

`pip install libdiva`

alternatively, clone the repo and install locally:

```
git clone https://github.com/Flipleerr/libdiva
cd libdiva
pip install . (add the -e flag if you'd like to contribute)
```

libdiva should now be installed. test by running `libdiva --help`.

## usage
libdiva supports the following options:

- `--write`: create a fresh DLT file with the contents of your choice
- `--read`: print an existing DLT file
- `--encrypt`: encrypt a file using DIVAFILE
- `--decrypt`: decrypt a file encrypted with DIVAFILE
- `--extract`: extract a FARC archive

some example of using the CLI tool:

`libdiva --encrypt file.txt`
`libdiva --extract file.farc extracted`

> [!TIP]
> you can also use libdiva like a proper library by entering `import libdiva` in your script.

## to-do
- [ ] FARC support (extract and repack)
- [ ] DLT boilerplate
- [ ] support for other Project Diva formats (`.cpk`, Dreamy Theater and F files, etc.)
- [ ] proper documentation or wiki
- [ ] a verbose option (-v or --verbose)

> [!NOTE]
> feel free to try your hand at any of these issues - any improvements help!

## contributing
all contributions to libdiva are welcome! to start:
1. fork the repo
2. clone it using `git clone https://github.com/USERNAME/libdiva (REPLACE 'USERNAME' WITH YOUR OWN!)`
3. create a new branch in the repo
4. make your changes

then submit a pull request!

> [!IMPORTANT]
> keep in mind that **GitHub Actions will automatically lint your code** when creating a pull request. if pylint fails, you'll be asked to fix the issues before merging. you can run pylint locally to check before pushing.
