import os
import json
import pandas as pd

def sequence_metadata(data, version):
    seq_data = {
        "VERSION": version,
        "NUM_OF_FRAMES": data["NUM_OF_FRAMES"],
        "FPS": data["FPS"],
        "START_TIME": str(data["START_TIME"]),
        "END_TIME": str(data["END_TIME"]),
        "STAGE": data["STAGE"],
    }
    return seq_data

def scene_curation(data):
    scene_data = {
        "COUNTRY": data["COUNTRY"],
        "WEATHER": data["WEATHER"],
        "ILLUMINATION": data["ILLUMINATION"],
        "ROAD": data["ROAD"],
        "ROAD_SURFACE": data["ROAD_SURFACE"],
    }
    return scene_data

def convert_to_new_format(seq_data,sence_data):
        output_json = {
            "SEQUENCE_METADATA": seq_data,
            "SCENE_CURATION": sence_data
        }
        return output_json
