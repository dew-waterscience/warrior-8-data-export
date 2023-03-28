# warrior-8-data-export

How do I export array datasets (such as full-waveform sonic logs) from Warrior 8 in a way that allows archiving of data without relying on proprietary file formats?

This repository has a [notebook](https://github.com/dew-waterscience/warrior-8-data-export/blob/main/Extracting%20Hunting-Titan%20CBL%20data%20from%20LIS%20file%20created%20by%20Warrior%208.ipynb) and script (essentially the same code in both) that allows this in a two-step process:

1. Export from Warrior 8 as a LIS file
2. Read the LIS file using [TotalDepth](https://github.com/paulross/TotalDepth), a GPL-licensed Python library. I don't know how to install this on Windows, but it runs fine on WSL (Windows Subsystem for Linux).
3. Write the curve datasets out as a LAS file, and the array/waveform datasets out as WellCAD-compatible ASCII files (WAF). The latter are easily importable into WellCAD, but are also simple ASCII files, easily readable using Python or any other software (see [wellcadformats](https://github.com/dew-waterscience/wellcadformats)).

## Usage

See the [notebook](https://github.com/dew-waterscience/warrior-8-data-export/blob/main/Extracting%20Hunting-Titan%20CBL%20data%20from%20LIS%20file%20created%20by%20Warrior%208.ipynb) or use the script [cbl_to_waf.py](cbl_to_waf.py):

```
$ cbl_to_waf.py single_log_pass_example.tap
```

The script is not general-purpose - it is hard-coded to handle the logs I am including in my LIS exports. However, it should be simple for you to follow the notebook and adjust as needed - or to produce a more general-purpose script.

