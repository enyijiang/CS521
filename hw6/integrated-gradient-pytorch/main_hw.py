import numpy as np
import torch
from torchvision import models
import cv2
import robustbench as rb
import torch.nn.functional as F
from utils import calculate_outputs_and_gradients, generate_entrie_images
from integrated_gradients import random_baseline_integrated_gradients
from visualization import visualize
import argparse
import os
from resnet import ResNet50

parser = argparse.ArgumentParser(description='integrated-gradients')
parser.add_argument('--cuda', action='store_true', help='if use the cuda to do the accelartion')
parser.add_argument('--model-path', type=str, default='resnet18_basic_training', help='the type of network')
# parser.add_argument('--img', type=str, default='01.jpg', help='the images name')

if __name__ == '__main__':
    args = parser.parse_args()
    # check if have the space to save the results
    if not os.path.exists('results/'):
        os.mkdir('results/')
    if not os.path.exists('results/' + args.model_path):
        os.mkdir('results/' + args.model_path)
    
    # start to create models...
    # model = ResNet50()
    # sd = torch.load(args.model_path, map_location=torch.device('cpu'))['model']
    # sd = {k[len('module.'):]:v for k,v in sd.items()}
    # model.load_state_dict(sd)
    model = rb.utils.load_model('Salman2020Do_R50', model_dir='.',
            dataset='imagenet', threat_model='Linf')
    model.eval()
    if args.cuda:
        model.cuda()
    # read the image
    files = os.listdir('examples')
    for f in files:
        img = cv2.imread('examples/' + f)
        # if args.model_type == 'inception':
            # the input image's size is different

        # img = cv2.resize(img, (32, 32))
        img = img.astype(np.float32) 
        img = img[:, :, (2, 1, 0)]
        # calculate the gradient and the label index
        gradients, label_index = calculate_outputs_and_gradients([img], model, None, args.cuda)
        gradients = np.transpose(gradients[0], (1, 2, 0))
        img_gradient_overlay = visualize(gradients, img, clip_above_percentile=99, clip_below_percentile=0, overlay=True, mask_mode=True)
        img_gradient = visualize(gradients, img, clip_above_percentile=99, clip_below_percentile=0, overlay=False)

        # calculae the integrated gradients 
        attributions = random_baseline_integrated_gradients(img, model, label_index, calculate_outputs_and_gradients, \
                                                            steps=50, num_random_trials=10, cuda=args.cuda)
        img_integrated_gradient_overlay = visualize(attributions, img, clip_above_percentile=99, clip_below_percentile=0, \
                                                    overlay=True, mask_mode=True)
        img_integrated_gradient = visualize(attributions, img, clip_above_percentile=99, clip_below_percentile=0, overlay=False)
        output_img = generate_entrie_images(img, img_gradient, img_gradient_overlay, img_integrated_gradient, \
                                            img_integrated_gradient_overlay)
        cv2.imwrite('results/' + args.model_path + '/' + f, np.uint8(output_img))
