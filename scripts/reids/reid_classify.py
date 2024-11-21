import os
import shutil
import torch
from torchreid.utils import FeatureExtractor
from tqdm import tqdm  # 用于显示进度条

# Initialize the feature extractor with a pretrained model
extractor = FeatureExtractor(
    model_name='osnet_x1_0',
    model_path='/home/mount_point_one/ssx/workspace/deep-person-reid/torchreid/models/checkpoints/20241111osnet_x1_0.pth.tar-50',
    device='cuda'  # or 'cpu'
)

def extract_feature(image_path):
    features = extractor([image_path])
    return features[0]

def compare_images(image_path1, image_path2):
    features1 = extract_feature(image_path1)
    features2 = extract_feature(image_path2)
    similarity = torch.nn.functional.cosine_similarity(features1, features2, dim=0)
    return similarity.item()

def main(directory_a, delete_folder, normal_folder, threshold=0.85):
    # Ensure the delete and normal folders exist
    os.makedirs(delete_folder, exist_ok=True)
    os.makedirs(normal_folder, exist_ok=True)

    # Get sorted list of image files in directory A
    image_files = sorted([f for f in os.listdir(directory_a) if f.endswith(('.jpg', '.png', '.jpeg'))])

    # Set the initial baseline frame without moving it
    if len(image_files) > 0:
        baseline_image_path = os.path.join(directory_a, image_files[0])

        # Iterate over the remaining images starting from the second one
        zuididefen = 100.0
        name_zuidi = "None"

        for image_file in tqdm(image_files[1:], desc="Processing images"):
            current_image_path = os.path.join(directory_a, image_file)

            # Compare current image with the baseline
            similarity_score = compare_images(baseline_image_path, current_image_path)

            # Move based on similarity score
            if similarity_score > threshold:
                print(f"similar (score: {similarity_score}) {baseline_image_path} and {current_image_path}, moving {image_file} to delete.")
                shutil.move(current_image_path, delete_folder)
            else:
                print(f"different (score: {similarity_score})  {baseline_image_path} and {current_image_path}  , moving {image_file} to normal.")
                shutil.move(current_image_path, normal_folder)
                # Update baseline image after moving the current non-similar image
                baseline_image_path = os.path.join(normal_folder, image_file)
            if similarity_score < zuididefen:
                zuididefen = similarity_score
                name_zuidi = current_image_path
        print(zuididefen)
        print(name_zuidi)

if __name__ == "__main__":
    id_path_name = "0050"
    directory_a = '/home/indemind/nfs_1/reid_datas/reid_dataset_1104/{}'.format(id_path_name)
    delete_folder = '/home/indemind/nfs_1/reid_datas/reid_dataset_1104/{}/repeat'.format(id_path_name)
    normal_folder = '/home/indemind/nfs_1/reid_datas/reid_dataset_1104/{}/normal_0.85'.format(id_path_name)
    # normal_folder = '/home/indemind/nfs_1/reid_datas/reid_dataset_1104/0004/half'

    main(directory_a, delete_folder, normal_folder)
