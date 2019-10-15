from pathlib import Path
import shutil
import re
import os


def find_show_name(episode_name: str) -> str:
    idx = re.search("([sS][0-9][0-9][eE][0-9][0-9])", episode_name).start()
    show_name = episode_name[:idx-1]
    try:
        idx2 = re.search("(.[0-9][0-9][0-9][0-9])", show_name).start()
    except:
        pass
    else:
        show_name = show_name[:idx2].replace(".", " ")
        if (show_name == "S W A T"):
            show_name = "S.W.A.T."

    return str(show_name)


def deposit_files(path: Path):
    for p in path.iterdir():
        if p.is_dir():
            p.cwd()
            dld_episode_dir = Path(p)
            for dep in dld_episode_dir.iterdir():
                if (dep.suffix == ".mkv"):
                    src_name = str(dep)
                    # Throw away any obfuscation
                    episode_name = dep.parts[-2]
                    show_name = find_show_name(episode_name)
                    # print("show_name = " + show_name)
                    dst_directory = Path(tv_dowloads_root + sep + show_name)
                    if not dst_directory.exists():
                        try:
                            os.mkdir(dst_directory)
                        except:
                            print(
                                "Unable to make destination directory" + dst_directory)
                            exit

                    dst_name = str(dst_directory) + sep + \
                        episode_name + dep.suffix
                    try:
                        shutil.copy(src_name, dst_name)
                    except (shutil.Error, OSError, IOError):
                        print("Could not move file \n\"" +
                              src_name + "\"\nto\n\"" + dst_name + "\"")
                    else:
                        pass
                        # shutil.rmtree(dld_episode_dir)


complete_dir = Path(
    "/Users/tspgallagher/Projects/Python/TV-Show-Parser/complete")
torrents_dir = Path(
    "/Users/tspgallagher/Projects/Python/TV-Show-Parser/Torrents")
tv_dowloads_root = "/Users/tspgallagher/Projects/Python/TV-Show-Parser/TVDownloads"
sep = "/"

tvd_path = Path(tv_dowloads_root)

if not(tvd_path.is_dir() and tvd_path.exists):
    tvd_path.mkdir()

for path in [complete_dir, torrents_dir]:
    if not(path.is_dir() and path.exists):
        exit
    deposit_files(path)
