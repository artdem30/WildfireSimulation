import os
import cv2
import building_recognition.mask_conversion as mc
import building_recognition.augmentations as aug
from building_recognition.load_data import BuildingDataset
import torch
import segmentation_models_pytorch as smp

input_dir = 'building_recognition/input/'
output_dir = 'building_recognition/output/'

ENCODER = 'resnet50'
ENCODER_WEIGHTS = 'imagenet'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
preprocessing_fn = smp.encoders.get_preprocessing_fn(ENCODER, ENCODER_WEIGHTS)

best_model = torch.load('building_recognition/best_model6.pth', map_location=torch.device(DEVICE))

def predict():
    if len(os.listdir(input_dir)) == 0:
        raise Exception("No images in input directory!")
    else:
        # create test dataset
        test_dataset = BuildingDataset(
            input_dir,
            input_dir,
            augmentation=aug.get_validation_augmentation(),
            preprocessing=aug.get_preprocessing(preprocessing_fn)
        )

        test_dataset_vis = BuildingDataset(
            input_dir, input_dir, augmentation=aug.get_validation_augmentation())

        n = 0
        image_vis = test_dataset_vis[n][0].astype('uint8')
        image, _ = test_dataset[n]
        image_tensor = torch.from_numpy(image).to(DEVICE).unsqueeze(0)
        pr_mask = best_model.predict(image_tensor)
        image_vis, boxes = mc.generate_bbox(image_vis, pr_mask)
        cv2.resize(image_vis, (1000,1000))
        cv2.imwrite(output_dir + "output.png", image_vis)
        return boxes
