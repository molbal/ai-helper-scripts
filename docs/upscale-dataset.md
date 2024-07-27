## Upscale
The script is designed to upscale images within a specified directory that have dimensions 
smaller than or equal to a given size. It leverages the ComfyUI backend and two separate
upscale models to achieve this. 

### Dependencies

The script requires several Python libraries: tqdm, Pillow, comfy_api_simplified, and websockets.
```sh
pip install tqdm Pillow comfy_api_simplified websockets
```

### Usage

```sh
python ./data-prep/upscale-dataset.py /path/to/your/directory --max-size 256
```

### CLI Parameters

| Flag         | Type | Description                                                                                                                                   | Default | Example Usage                                                                  |
|--------------|------|-----------------------------------------------------------------------------------------------------------------------------------------------|---------|--------------------------------------------------------------------------------|
| `directory`  | str  | The path to the directory containing the images you want to upscale.                                                                          | N/A     | `python ./data-prep/upscale-dataset.py /path/to/your/directory`                |
| `--max-size` | int  | The maximum size of the smaller dimension of the images. Images with either width or height less than or equal to this size will be upscaled. | 256     | `python ./data-prep/upscale-dataset.py /path/to/your/directory --max-size 512` |

