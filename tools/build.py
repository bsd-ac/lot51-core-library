import argparse
import compileall
import os
import pathlib
import shutil

parser = argparse.ArgumentParser(description="Build a Sims 4 mod")
parser.add_argument("--root", required=True, help="Root folder of the mod")
parser.add_argument("--name", required=True, help="Name of the mod")


PYTHON_MAGIC = ".cpython-37"
MOD_ROOT = "build"
MOD_CACHE = "build/cache"
MOD_FINAL = "build/mods"

def build():
    args = parser.parse_args()

    # compileall python files in root folder
    compileall.compile_dir(args.root, force=True)

    # create mod directory
    mod_dir = f"{MOD_CACHE}/{args.name}"
    os.makedirs(mod_dir, exist_ok=True)

    # copy all compiled files to mod directory with the directory structure but removing __pycache__
    for file in pathlib.Path(args.root).rglob("*.pyc"):
        dest = pathlib.Path(mod_dir) / file.relative_to(args.root)
        dest = dest.with_name(dest.name.replace(PYTHON_MAGIC, ""))
        # move one directory up to get rid of __pycache__
        dest = dest.parent.parent / dest.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(file, dest)

    # zip the files
    shutil.make_archive(f"{MOD_CACHE}/{args.name}", 'zip', mod_dir)
    # move the zip to the final mods folder
    os.makedirs(MOD_FINAL, exist_ok=True)
    shutil.move(f"{MOD_CACHE}/{args.name}.zip", f"{MOD_FINAL}/{args.name}.ts4script")

if __name__ == "__main__":
    build()
