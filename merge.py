
import os
import argparse
import logging
import sys
from logger import PrettyLogger



parser = argparse.ArgumentParser()
parser.add_argument("--dst", type=str, help="Instagram Account Name", default="")
parser.add_argument("--logging", type=str, help="Print More Message", default="info")
parser.add_argument("--copy", type=bool, help="Copying files instead of moving", default=False)
( args, unknown_args) = parser.parse_known_args()


DEFAULT_IGNORED_FILE = {
    ".DS_Store"
}

def exe(cmd):
    return os.system(cmd)
    # return 0

def validify(name):
    return name.replace(" ", r"\ ").replace("(", r"\(").replace(")", r"\)")


class MergeUtility:
    def __init__(self, args):
        self.logger = PrettyLogger(self.__class__.__name__, level=logging.DEBUG if args.logging=="debug" else logging.INFO)
        self.args     = args
        self.logger.debug(f"ParsedArgs: \n\t\t{self.args}")
        self.logger.debug(f"UnknownArgs: \n\t\t{unknown_args}")
        self.logger.debug(f"SysArgs: \n\t\t{sys.argv}")
        self.itemlist = list(unknown_args)
        self.logger.info(f"ItemList:")
        for item in self.itemlist:
            if "comappleCloudDocs" in item:
                item = item.replace("comappleCloudDocs", "com~apple~CloudDocs")

            self.logger.info(f"\t{item}")
        
        self.file_operation = "cp" if args.copy==True else "mv"
        self.dir_operation  = "cp -rf "if args.copy==True else "mv"

    def merge(self):
        if not os.path.exists(self.args.dst):
            cmd = f"mkdir {validify(self.args.dst)}"
            self.logger.debug(f"=> ${cmd} Returned:{exe(cmd)}")
        
        for idx, item in enumerate(self.itemlist):
            self.submerge( item, self.args.dst)


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

            cmd = f"{self.file_operation} {validify(src_file)} {validify(dst)}"
            self.logger.debug(f"{trace_prefix} ${cmd} Returned:{exe(cmd)}")

        for d in dir_list:
            src_dir = os.path.join(src,d)
            dst_dir = os.path.join(dst,d)
            if not os.path.exists(dst_dir):
                cmd = f"{self.dir_operation} {validify(src_dir)} {validify(dst_dir)}"
                self.logger.debug(f"{trace_prefix} ${cmd} Returned:{exe(cmd)}")
            else:
          