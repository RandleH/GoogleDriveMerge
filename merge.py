
import os
import argparse
import logging
import sys
import tarfile
from logger import PrettyLogger



parser = argparse.ArgumentParser()
parser.add_argument("--dst", type=str, help="Instagram Account Name", default="")
parser.add_argument("--logging", type=str, help="Print More Message", default="info")
parser.add_argument("--copy", type=bool, help="Copying files instead of moving", default=False)
( args, unknown_args) = parser.parse_known_args()


DEFAULT_IGNORED_FILE = {
    ".DS_Store",
    ".git"
}


def exe(cmd):
    return os.system(cmd)
    # return 0

def validify(name):
    return name.replace(" ", r"\ ").replace("(", r"\(").replace(")", r"\)")

def is_zip(file):
    try:
        with open(file, 'rb') as f:
            pass
        ext = [s.lower() for s in os.path.splitext(file)]
        if ext[1]==".zip" or ext[1]==".tar" or ext[1]==".rar":
            return True
        else:
            return False
    except FileNotFoundError as e:
        return e
    except IsADirectoryError:
        return False
    except Exception as e:
        return e
    


class MergeUtility:
    def __init__(self, args):
        self.logger = PrettyLogger(self.__class__.__name__, level=logging.DEBUG if args.logging=="debug" else logging.INFO)
        self.args     = args
        self.logger.debug(f"ParsedArgs: \n\t\t{self.args}")
        self.logger.debug(f"UnknownArgs: \n\t\t{unknown_args}")
        self.logger.debug(f"SysArgs: \n\t\t{sys.argv}")
        self.itemlist = list(unknown_args)
        self.logger.info(f"ItemList:")
        for idx, item in enumerate(self.itemlist):
            if "comappleCloudDocs" in item:
                self.itemlist[idx] = item.replace("comappleCloudDocs", "com~apple~CloudDocs")
            self.logger.info(f"\t{self.itemlist[idx]}")
        if "comappleCloudDocs" in self.args.dst:
            self.args.dst = self.args.dst.replace("comappleCloudDocs", "com~apple~CloudDocs")

    def merge(self):
        if not os.path.exists(self.args.dst):
            cmd = f"mkdir {validify(self.args.dst)}"
            self.logger.debug(f"=> ${cmd} Returned:{exe(cmd)}")
        
        for idx, item in enumerate(self.itemlist):
            self.submerge( item, self.args.dst)

    def __cmd_merge__(self, _from:str, _to:str, _is_dir:bool) -> str:
        cmd = ""
        _is_zip = is_zip(_from)

        if self.args.copy==True:
            if _is_zip==True:
                cmd += "tar -zxvf "
            else:
                cmd += "cp -rf " if _is_dir==True else "cp "
        else:
            if _is_zip==True:
                cmd += "tar -zxvf "
            else:
                cmd += "mv "
            pass
        cmd += validify(_from)
        cmd += " "
        cmd += validify(_to)

        return cmd


    def submerge(self, src, dst, trace_level=0):
        file_list = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src,f))]
        dir_list  = [d for d in os.listdir(src) if not os.path.isfile(os.path.join(src,d))]
        trace_prefix = "="*trace_level+"=>"
        self.logger.info(f"{trace_prefix} {file_list=} {dir_list=}")
        for f in file_list:
            src_file = os.path.join(src,f)
            if f in DEFAULT_IGNORED_FILE:
                continue
            
            if os.path.exists(os.path.join(dst,f)):
                self.logger.warning(f"Can NOT merge duplicated file: {os.path.join(src,f)}")
                continue

            cmd = self.__cmd_merge__(src_file, dst, False)
            self.logger.debug(f"{trace_prefix} ${cmd} Returned:{exe(cmd)}")

        for d in dir_list:
            src_dir = os.path.join(src,d)
            dst_dir = os.path.join(dst,d)
            if d in DEFAULT_IGNORED_FILE:
                continue
            if not os.path.exists(dst_dir):
                cmd = self.__cmd_merge__(src_dir, dst_dir, True)
                self.logger.debug(f"{trace_prefix} ${cmd} Returned:{exe(cmd)}")
            else:
                self.submerge( src_dir, dst_dir, trace_level+1)


if __name__=="__main__":
    m = MergeUtility(args)
    m.merge()



