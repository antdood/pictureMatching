# pictureMatching

Given a folder, finds visually similar images and sorts them into subfolders. Complexity seems to be roughly n * 1.005^n.

Uses basic histogram matching of colours. Variables can be tweaked in histogramImageComparer.py but I've found these to be most successful in my limited testing. Seems to be quite robust against upscaled/downscaled images as well. 

Increasing the threshold will help with matching cropped images, but may also result in more false positives. 
