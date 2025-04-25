# Google Drive Merge Tool



## Do you know...

Google drive automatically compress your files in a batch while you are downloading a folder from the server. However this may cause the problem leaving you a stack of files in pieces. 

<p align="center"><img src="asset/1.jpg" alt="rdme_clk_panel" ;" /></p>



## How to use

We are here to help!



Clone the repository

```bash
git clone https://github.com/RandleH/GoogleDriveMerge.git
cd GoogleDriveMerge
```



Merge your files

```bash
python merge.py --dst <your_destination_folder> <source_folder1> <source_folder2> ...
```

> Tips: You can drag the folder to the terminal. It will automatically convert to a string.



Below is the full command usage:

```bash
python merge.py --dst <your_destination_folder> --logging <debug|[info]> --copy <[0]|1> <source_folder1> <source_folder2> ...
```



## Example

For demonstration, inside this repository, I provided some dummy files in the `example` folder.

The directory tree looks like this:

<img src="/Users/randleh/Library/Mobile Documents/com~apple~CloudDocs/GitHub/GoogleDriveMerge/asset/2.png" alt="3" style="zoom:30%;" />

Then you may run this command

```bash
python merge.py --dst dummy --copy 0 example/dummy1 example/dummy2 example/dummy3
```

> - Move the original files meaning there will be empty folders remaining.
> - The destination folder is `dummy`. It is at `${YOUR_REPO_DIR}/dummy`
> - The folders to be triaged are `example/dummy1` `example/dummy2` `example/dummy3`



Finally, the result directory tree will be like this:

<img src="/Users/randleh/Library/Mobile Documents/com~apple~CloudDocs/GitHub/GoogleDriveMerge/asset/3.png" alt="3" style="zoom:30%;" />

On the leftside, every original folders became empty and the rightride is your ordered google drive content.





