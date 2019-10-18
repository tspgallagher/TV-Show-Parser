from pathlib import Path
import shutil
import re
import os


def copy_file(src, dst, buffer_size=10485760, preserve_file_date=True):
    """
    Copies a file to a new location.
    Much faster performance than Apache Commons due to use of larger buffer.

    :param src:    Source file path
    :param dst:    Destination file path
    :param buffer_size:    Buffer size to use during copy
    :param preserve_file_date:    Preserve the original file date
    """

    # Optimize the buffer for small files
    buffer_size = min(buffer_size, os.path.getsize(src))
    if buffer_size == 0:
        buffer_size = 1024

    if shutil._samefile(src, dst):
        raise shutil.Error(
            "`{0}` and `{1}` are the same file".format(src, dst))
    for fn in [src, dst]:
        try:
            st = os.stat(fn)
        except OSError:  # File most likely does not exist
            pass
        else:  # XXX What about other special files? (sockets, devices...)
            if shutil.stat.S_ISFIFO(st.st_mode):
                raise shutil.SpecialFileError(
                    "`{}` is a named pipe".format(fn))
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            shutil.copyfileobj(fsrc, fdst, buffer_size)

    if preserve_file_date:
        shutil.copystat(src, dst)


def find_show_name(episode_name: str) -> str:
    """
    Sucks out show_name from episode_name
    So if episode_name was "Blue.Bloods.S10E03.1080p.WEB.H264-AMCON[rarbg]" then
    show_name would result in "Blue Bloods"
    The show "S.W.A.T." is a special case

    :param  episode_name:   String containing episode name pulled from source directory
    """

    idx = re.search("([sS][0-9][0-9][eE][0-9][0-9])", episode_name).start()
    show_name = episode_name[:idx-1]
    try:
        idx2 = re.search("(.[0-9][0-9][0-9][0-9])", show_name).start()
    except:
        show_name = show_name[:idx].replace(".", " ")
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
                        #    shutil.copy(src_name, dst_name)
                        copy_file(src_name, dst_name)

                    except (shutil.Error, OSError, IOError):
                        print("Could not move file \n\"" +
                              src_name + "\"\nto\n\"" + dst_name + "\"")
                    else:
                        shutil.rmtree(dld_episode_dir)


complete_dir = Path(
    "/Users/tspgallagher/Projects/Python/TV-Show-Parser/complete")
torrents_dir = Path(
    "/Users/tspgallagher/Projects/Python/TV-Show-Parser/Torrents")
tv_dowloads_root = "/Users/tspgallagher/Projects/Python/TV-Show-Parser/TVDownloads"

#complete_dir = Path("/Volumes/Plex Content/complete")
#torrents_dir = Path("/Volumes/Plex Content/Torrents")
#tv_dowloads_root = "/Volumes/Plex Content/TV Downloads"

sep = "/"
tvd_path = Path(tv_dowloads_root)

if not(tvd_path.is_dir() and tvd_path.exists):
    tvd_path.mkdir()

for dld_path in [complete_dir, torrents_dir]:
    if not(dld_path.is_dir() and dld_path.exists):
        exit
    deposit_files(dld_path)
