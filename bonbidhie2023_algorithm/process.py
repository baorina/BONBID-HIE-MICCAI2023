# Copyright 2023 Radboud University Medical Center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# codes written by Rina Bao (rina.bao@childrens.harvard.edu) for BONBID-HIE MICCAI 
# Challenge 2023 (https://bonbid-hie2023.grand-challenge.org/). 
# Demo of Algorithm docker


import json
from dataclasses import dataclass, make_dataclass
from enum import Enum
from typing import Any, Dict
from pathlib import Path
import torch
import torch.nn as nn
import numpy as np
import SimpleITK
import os
INPUT_PREFIX = Path("/input")
OUTPUT_PREFIX = Path("/output")




class IOKind(str, Enum):
    JSON = "JSON"
    IMAGE = "Image"
    FILE = "File"


class InterfaceKind(str, Enum):
    # TODO taken from https://github.com/comic/grand-challenge.org/blob/ffbae21af534caed9595d9bc48708c5f753b075c/app/grandchallenge/components/models.py#L69
    #      would be better to get this directly from the schema

    def __new__(cls, value, annotation, io_kind):
        member = str.__new__(cls, value)
        member._value_ = value
        member.annotation = annotation
        member.io_kind = io_kind
        return member

    STRING = "String", str, IOKind.JSON
    INTEGER = "Integer", int, IOKind.JSON
    FLOAT = "Float", float, IOKind.JSON
    BOOL = "Bool", bool, IOKind.JSON
    ANY = "Anything", Any, IOKind.JSON
    CHART = "Chart", Dict[str, Any], IOKind.JSON

    # Annotation Types
    TWO_D_BOUNDING_BOX = "2D bounding box", Dict[str, Any], IOKind.JSON
    MULTIPLE_TWO_D_BOUNDING_BOXES = "Multiple 2D bounding boxes", Dict[str, Any], IOKind.JSON
    DISTANCE_MEASUREMENT = "Distance measurement", Dict[str, Any], IOKind.JSON
    MULTIPLE_DISTANCE_MEASUREMENTS = "Multiple distance measurements", Dict[str, Any], IOKind.JSON
    POINT = "Point", Dict[str, Any], IOKind.JSON
    MULTIPLE_POINTS = "Multiple points", Dict[str, Any], IOKind.JSON
    POLYGON = "Polygon", Dict[str, Any], IOKind.JSON
    MULTIPLE_POLYGONS = "Multiple polygons", Dict[str, Any], IOKind.JSON
    LINE = "Line", Dict[str, Any], IOKind.JSON
    MULTIPLE_LINES = "Multiple lines", Dict[str, Any], IOKind.JSON
    ANGLE = "Angle", Dict[str, Any], IOKind.JSON
    MULTIPLE_ANGLES = "Multiple angles", Dict[str, Any], IOKind.JSON
    ELLIPSE = "Ellipse", Dict[str, Any], IOKind.JSON
    MULTIPLE_ELLIPSES = "Multiple ellipses", Dict[str, Any], IOKind.JSON

    # Choice Types
    CHOICE = "Choice", int, IOKind.JSON
    MULTIPLE_CHOICE = "Multiple choice", int, IOKind.JSON

    # Image types
    IMAGE = "Image", bytes, IOKind.IMAGE
    SEGMENTATION = "Segmentation", bytes, IOKind.IMAGE
    HEAT_MAP = "Heat Map", bytes, IOKind.IMAGE

    # File types
    PDF = "PDF file", bytes, IOKind.FILE
    SQREG = "SQREG file", bytes, IOKind.FILE
    THUMBNAIL_JPG = "Thumbnail jpg", bytes, IOKind.FILE
    THUMBNAIL_PNG = "Thumbnail png", bytes, IOKind.FILE
    OBJ = "OBJ file", bytes, IOKind.FILE
    MP4 = "MP4 file", bytes, IOKind.FILE

    # Legacy support
    CSV = "CSV file", str, IOKind.FILE
    ZIP = "ZIP file", bytes, IOKind.FILE

@dataclass
class Interface:
    slug: str
    relative_path: str
    kind: InterfaceKind

    @property
    def kwarg(self):
        return self.slug.replace("-", "_").lower()

    def load(self):
        if self.kind.io_kind == IOKind.JSON:
            return self._load_json()
        elif self.kind.io_kind == IOKind.IMAGE:
            return self._load_image()
        elif self.kind.io_kind == IOKind.FILE:
            return self._load_file()
        else:
            raise AttributeError(f"Unknown io kind {self.kind.io_kind!r} for {self.kind!r}")

    def save(self, *, data):
        if self.kind.io_kind == IOKind.JSON:
            return self._save_json(data=data)
        elif self.kind.io_kind == IOKind.IMAGE:
            return self._save_image(data=data)
        elif self.kind.io_kind == IOKind.FILE:
            return self._save_file(data=data)
        else:
            raise AttributeError(f"Unknown io kind {self.kind.io_kind!r} for {self.kind!r}")

    def _load_json(self):
        with open(INPUT_PREFIX / self.relative_path, "r") as f:
            return json.loads(f.read())

    def _save_json(self, *, data):
        with open(OUTPUT_PREFIX / self.relative_path, "w") as f:
            f.write(json.dumps(data))

    def _load_image(self):
        input_directory = INPUT_PREFIX / self.relative_path

        mha_files = {f for f in input_directory.glob("*.mha") if f.is_file()}

        if len(mha_files) == 1:
            mha_file = mha_files.pop()
            return SimpleITK.ReadImage(mha_file)
        elif len(mha_files) > 1:
            raise RuntimeError(
                f"More than one mha file was found in {input_directory!r}"
            )
        else:
            raise NotImplementedError

    def _save_image(self, *, data):
        output_directory = OUTPUT_PREFIX / self.relative_path

        output_directory.mkdir(exist_ok=True, parents=True)
        print (data.GetSpacing())
        file_save_name=output_directory / "overlay.mha"
        print (file_save_name)

        SimpleITK.WriteImage(data, file_save_name)
        check_file = os.path.isfile(file_save_name)
        print ("check file", check_file)

    @property
    def _file_mode_suffix(self):
        if self.kind.annotation == str:
            return ""
        elif self.kind.annotation == bytes:
            return "b"
        else:
            raise AttributeError(f"Unknown annotation {self.kind.annotation!r} for {self.kind!r}")

    def _load_file(self):
        with open(INPUT_PREFIX / self.relative_path, f"r{self._file_mode_suffix}") as f:
            return f.read()

    def _save_file(self, *, data):
        with open(OUTPUT_PREFIX / self.relative_path, f"w{self._file_mode_suffix}") as f:
            f.write(data)

INPUT_INTERFACES = [
    Interface(slug="z-score-apparent-diffusion-coefficient-map", relative_path="images/z-score-adc", kind=InterfaceKind.IMAGE),
    Interface(slug="skull-stripped-adc", relative_path="images/skull-stripped-adc-brain-mri", kind=InterfaceKind.IMAGE),
]

OUTPUT_INTERFACES = [
    Interface(slug="hypoxic-ischemic-encephalopathy-lesion-segmentation", relative_path="images/hie-lesion-segmentation", kind=InterfaceKind.SEGMENTATION),
]

Inputs = make_dataclass(cls_name="Inputs", fields=[(inpt.kwarg, inpt.kind.annotation) for inpt in INPUT_INTERFACES])

Outputs = make_dataclass(cls_name="Outputs", fields=[(output.kwarg, output.kind.annotation) for output in OUTPUT_INTERFACES])

def load() -> Inputs:
    return Inputs(
        **{interface.kwarg: interface.load() for interface in INPUT_INTERFACES}
    )



def get_default_device():
    ######## set device#########
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')

class BaseNet(nn.Module):
    def __init__(self,):
        super().__init__()

    def forward(self,x):
        out=torch.where(x<-2,1,0)
        return out



def predict(*, inputs: Inputs) -> Outputs:
    z_adc = inputs.z_score_apparent_diffusion_coefficient_map
    adc_ss = inputs.skull_stripped_adc

    # Do your segmentation here, for now just copy over one of the inputs
    #hie_segmentation = SimpleITK.BinaryThreshold(
    #        image1=z_adc, lowerThreshold=-2, insideValue=1, outsideValue=0)
    with torch.no_grad():
       z_adc=SimpleITK.GetArrayFromImage(z_adc)
       z_adc_input=torch.from_numpy(z_adc.astype(np.float32))

       z_adc_input=z_adc_input[None,...].to(get_default_device())

       net=BaseNet()
       net=net.to(get_default_device())   

       out=net(z_adc_input)

       out=out.detach().cpu().numpy().squeeze().astype(np.uint8)

        
    hie_segmentation=SimpleITK.GetImageFromArray(out)    

    outputs = Outputs(
        hypoxic_ischemic_encephalopathy_lesion_segmentation = hie_segmentation
    )
    return outputs

    #raise NotImplementedError

def save(*, outputs: Outputs) -> None:
    for interface in OUTPUT_INTERFACES:
        interface.save(data=getattr(outputs, interface.kwarg))

def main() -> int:
    inputs = load()
    outputs = predict(inputs=inputs)
    save(outputs=outputs)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

