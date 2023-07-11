import imgaug.augmenters as iaa
import cv2
import os
import glob



# 1.) Load Dataset
images = []
images_path = glob.glob("images/*.jpeg")
for img_path in images_path:
    img = cv2.imread(img_path)
    images.append(img)

#2.) Image Augmentation

augmentation = iaa.Sequential([
    #A. Rotate
    # iaa.Rotate((-30, 30))
    #B. Flip
    iaa.Fliplr(0.5),
    iaa.Flipud(0.5),

    #C. Affine
    iaa.Affine(translate_percent={"x": (-0.5, 0.5), "y": (-0.5, 0.5)},
               rotate=(-30, 30),
               scale=(0.5, 1.5),
               ),
    #D. Multiply -- which makes the image brighter or darker
    iaa.Multiply((0.8, 1.2)),

    #E Linear Contrast
    iaa.LinearContrast((0.6, 1.4)),

    #Perform the below messages only sometime
    iaa.Sometimes(0.5, 
        #F. gaussian blur
        iaa.GaussianBlur((0.0, 3.0)),
                  
                  )


    

])

#3.) show images
# while True:
#     augmented_images = augmentation(images=images)
#     for img in augmented_images:
#         cv2.imshow("Image", img)
#         cv2.waitKey(0)

# 3.) Generate & Save Images
output_dir = "/Users/foreveroptimist/Desktop/new_images"
os.makedirs(output_dir, exist_ok=True) #create the output of the directory if it doesnt exist

amount_augmented_images = 20 # number of augmented images per input image

for idx, img in enumerate(images):
    for aug_idx in range(amount_augmented_images):
        augmented_img = augmentation.augment_image(img)

        # Apply cropping to remove black space
        # cropped_img = augmented_img.copy()
        # gray = cv2.cvtColor(augmented_img, cv2.COLOR_BGR2GRAY)
        # _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # if len(contours) > 0:
        #     x, y, w, h = cv2.boundingRect(contours[0])
        #     cropped_img = cropped_img[y:y + h, x:x + w]


        output_path = os.path.join(output_dir, f"augmented_{idx}_{aug_idx}.jpeg")
        cv2.imwrite(output_path, augmented_img)


cv2.destroyAllWindows()