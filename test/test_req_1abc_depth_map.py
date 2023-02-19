import cv2
import torch
import subprocess
import depth_estimation

# Download MiDaS (models: DPT_Large, DPT_Hybrid, MiDaS_small).
midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small', trust_repo=True)
midas.to('cpu')
midas.eval()

# Input transformation pipeline.
transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
transform = transforms.small_transform 

# Take photo.
#subprocess.call("libcamera-still -o image.jpg", shell=True) # 2592x1944
subprocess.call("libcamera-still --width 1296 --height 972 -o image.jpg", shell=True)

# Read image.
img_original = cv2.imread('image.jpg')
img_original = cv2.rotate(img_original, cv2.ROTATE_90_CLOCKWISE)
img_original = cv2.rotate(img_original, cv2.ROTATE_90_CLOCKWISE)
#img_original = cv2.imread('depth_maps/image00.jpg')

# Transform input for MiDaS. 
img = cv2.cvtColor(cv2.resize(img_original, (480, 270)), cv2.COLOR_BGR2RGB)
imgbatch = transform(img).to('cpu')

# Generate depth map.
with torch.no_grad(): 
    prediction = midas(imgbatch)
    prediction = torch.nn.functional.interpolate(
        prediction.unsqueeze(1),
        size = img.shape[:2], 
        mode='bicubic', 
        align_corners=False
    ).squeeze()

    output = prediction.cpu().numpy()
    #print(output)
    cv2.imwrite('depth.jpg', output)

# Evaluate depth map.
dmap = cv2.imread('depth.jpg')
depth_estimation.print_map(dmap)
dmap_eval = depth_estimation.sample(dmap)
print(depth_estimation.evaluate(dmap_eval))

print('Done.')
