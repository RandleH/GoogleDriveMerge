################################################################################################
# File: merge.py
#
#
# Author: Randle
#
# Copyright (c) 2024, Randle
#
################################################################################################

import os
import argparse
import logging
import sys
import tarfile
import zipfile
from logger import PrettyLogger



parser = argparse.ArgumentParser()
parser.add_argument("--dst", type=str, help="Destination Files", default="")
parser.add_argument("--logging", type=str, help="Verbose", default="info")
parser.add_argument(      "--no-keep", action="store_true", dest="no_keep", default=False, help="Do NOT keep any source files!! (Danger!!)")
parser.add_argument("-f", "--force",   action="store_true", dest="force", default=False, help="Skip the query!! (Danger!!)")


( args, unknown_args) = parser.parse_known_args()


DEFAULT_IGNORED_FILE = {
    ".DS_Store",
    ".git"
}


def validate(name):
    return name.replace(r"\\ ", " ").replace(r"\ ", " ").replace(" ", r"\ ").replace("(", r"\(").replace(")", r"\)").replace("&",r"\&")

def is_zip(file):
    try:
        with open(file, 'rb') as f:
            pass
        ext = [s.lower() for s in os.path.splitext(file)]
        if ext[1]==".zip":
            return True
        else:
            return False
    except FileNotFoundError as e:
        return e
    except IsADirectoryError:
        return False
    except Exception as e:
        return e

def query(msg):
    ans = input(f"{msg} [Y/N]? ")
    if ans=="Y":
        return True
    else:
        return False


class cmd:
        def merge( _from:str, _to:str, _copy:bool, _is_dir:bool):
            cmd = ""
            if _copy==True:
                cmd += "cp -RpP -a " if _is_dir==True else "cp -a"
            else:
                cmd += "mv "
            cmd += validate(_from)
            cmd += " "
            cmd += validate(_to)
            return cmd
        
        def copy(_from:str, _to:str):
            cmd = ""
            cmd += "cp -RpP -a " if os.path.isfile(_from)==False else "cp -a"
            cmd += validate(_from)
            cmd += " "
            cmd += validate(_to)
            return cmd
        
        def move(_from:str, _to:str):
            cmd = ""
            cmd += "mv "
            cmd += validate(_from)
            cmd += " "
            cmd += validate(_to)
            return cmd
        
        def remove(file):
            cmd = f"rm -rf {validate(file)}"
            return cmd
        
        def mkdir(dir):
            cmd = f"mkdir {validate(dir)}"
            return cmd
        
        def xtzip(zip_path, _to):
            if not os.path.exists(_to):
                cmd = f"mkdir {validate(_to)} && tar xzfC {validate(zip_path)} {validate(_to)}"
            else:
                cmd = f"tar xzfC {validate(zip_path)} {validate(_to)}"
            return cmd

class MergeUtility:
    
    def __init__(self, args):
        self.logger = PrettyLogger(self.__class__.__name__, level=logging.DEBUG if args.logging=="debug" else logging.INFO)
        self.args     = args
        self.logger.debug(f"ParsedArgs: \n\t\t{self.args}")
        self.logger.debug(f"UnknownArgs: \n\t\t{unknown_args}")
        self.logger.debug(f"SysArgs: \n\t\t{sys.argv}")
        self.itemlist = list(unknown_args)
        self.logger.info(f"Items in this batch:")
        for idx, item in enumerate(self.itemlist):
            if "comappleCloudDocs" in item:
                self.itemlist[idx] = item.replace("comappleCloudDocs", "com~apple~CloudDocs")
            self.logger.info(f"\t{self.itemlist[idx]}")
        if "comappleCloudDocs" in self.args.dst:
            self.args.dst = self.args.dst.replace("comappleCloudDocs", "com~apple~CloudDocs")

    def __exe__(self, cmd):
        ret = os.system(cmd)
        self.logger.debug(f"${cmd} | Return: {ret}")
        # self.logger.debug(f"${cmd} | Return: {0xFF}")
        
        if ret != 0:
            self.logger.error(f"Aborted as operation returned a none zero value. {ret=}")
            self.logger.error(f"${cmd}")
            sys.exit(1)

    def merge(self):
        if not os.path.exists(self.args.dst):
            self.__exe__(cmd.mkdir(self.args.dst))
        
        for idx, item in enumerate(self.itemlist):
            self.logger.info(f"Processing item[{idx+1}/{len(self.itemlist)}]: {item}...")
            if is_zip(item):
                self.submerge_from_zip(item, self.args.dst)
            else:
                self.submerge( item, self.args.dst, self.args.no_keep==False)

    def submerge(self, src, dst, copy:bool, trace_level=0):
        idx = 1 if copy==True else 0
        cmd_opt = [cmd.move, cmd.copy]

        # NOTE: 
        #   In case this function was NOT called from an upper recursive level.
        #   Double check if the source is a file.
        if os.path.isfile(src):
            self.__exe__(cmd_opt[idx](src, dst))
            return
        
        file_list = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src,f))]
        dir_list  = [d for d in os.listdir(src) if not os.path.isfile(os.path.join(src,d))]
        trace_prefix = "="*trace_level+"=>"
        
        self.logger.info(f"{trace_prefix} Prepare looping files in the directory {src}:")
        self.logger.info(f"{trace_prefix} {file_list=}")
        for f in file_list:
            src_file = os.path.join(src,f)
            if f in DEFAULT_IGNORED_FILE:
                continue
            
            if os.path.exists(os.path.join(dst,f)):
                self.logger.warning(f"Can NOT merge duplicated file: {src_file}")
                continue
            self.__exe__(cmd_opt[idx](src_file, dst))

        self.logger.info(f"{trace_prefix} Prepare looping folders in the directory {src}:")
        self.logger.info(f"{trace_prefix} {dir_list=}")
        for d in dir_list:
            src_dir = os.path.join(src,d)
            dst_dir = os.path.join(dst,d)
            if d in DEFAULT_IGNORED_FILE:
                continue
            if not os.path.exists(dst_dir):
                self.__exe__(cmd_opt[idx](src_dir, dst_dir))
            else:
                self.submerge( src_dir, dst_dir, copy, trace_level+1)
    
    def submerge_from_zip(self, zip_path, dst):
        top_level = None

        #########################################################################################
        # TODO: 
        #   Module <zipfile> doesn't perserve file info (eg: mdate/permission/cdate/...).
        #
        # NOTE: 
        #   <os.system()> treated needs all space charactor with an escape indicator "\"
        #   However <zipfile.ZipFile()> won't recognize the escape indicator "\" 
        #########################################################################################
        with zipfile.ZipFile(validate(zip_path).replace(r"\ ", " "), 'r') as zip_file:
            top_level = {item.split('/')[0] for item in zip_file.namelist()}
        
        try:
            tmp_path = os.path.join(dst, "__TEMP__")
            self.__exe__(cmd.xtzip(zip_path, tmp_path))
            
            if len(top_level)!=1:
                self.logger.warning(f"Top level in zip file is NOT unique. {top_level=}")
            
            for item in top_level:
                src_item = os.path.join(tmp_path,item)
                self.submerge( src_item, dst, False)
                self.__exe__(cmd.remove(src_item))
                
            self.__exe__(cmd.remove(tmp_path))
            
            if self.args.no_keep == True:
                if self.args.force == True or query(f"Remove the zip file {zip_path}?"):
                    self.__exe__(cmd.remove(zip_path))
            
        except Exception as e:
            self.logger.error(e)


    def submerge_from_tar(self, src, dst):
        raise NotImplementedError


if __name__=="__main__":
    m = MergeUtility(args)
    m.merge()
