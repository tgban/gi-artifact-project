# Genshin Impact artifact detection and scoring project
## Introduction
Farming for Genshin Impact artifact is known to be quite time-consuming, and even more so when the right ones is harder to come by with RNG involved. Filtering through them manually to get rid of many of them gets tiring, so this project aims to alleviate the burden of such task. This project detects a 5-star artifact on screen and outputs a score based on the artifact stats, type, and set.

## Dependencies
PyTesseract, OpenCV-Python, PIL, numpy

### Input
Screenshot from game:

![Artifact Image](https://github.com/tgban/gi-artifact-project/assets/38060917/d206b912-c1df-4a13-b650-169fc569b34c)

### Output
Screenshot from console log (interactive):

![Console Image](https://github.com/tgban/gi-artifact-project/assets/38060917/2c70c29d-8697-41b3-a140-4ccf4768e7c2)

## Artifact Detection
### Cascade Classifier
From [Open-CV Documentation of Cascade Classifier](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html):
> Object Detection using Haar feature-based cascade classifiers is an effective object detection method proposed by Paul Viola and Michael Jones in their paper, "Rapid Object Detection using a Boosted Cascade of Simple Features" in 2001. It is a machine learning based approach where a cascade function is trained from a lot of positive and negative images. It is then used to detect objects in other images.

### Early Implementation
A cascase classifier was trained with 88 positive images (images from game with artifact item marked with surrounding box) and used to detect Genshin artifact images, which resulted in more than 90% of real-time artifacts being detected. The detection purely from the cascade classifier was imperfect since there were multiple boxes, or regions of interest (ROIs):

![Early Detection Image, Multiple Boxes](https://github.com/tgban/gi-artifact-project/assets/38060917/914693e4-45cf-45eb-8c5e-788a58baaac3)

Therefore, to filter out which of the detected ROIs is the correct region(s), an extra method was introduced and implemented: PyTesseract.

### PyTesseract
From [PyTesseract project description page](https://pypi.org/project/pytesseract/):
> Python-tesseract is an optical character recognition (OCR) tool for python. That is, it will recognize and “read” the text embedded in images.
>
> Python-tesseract is a wrapper for Google’s Tesseract-OCR Engine. It is also useful as a stand-alone invocation script to tesseract, as it can read all image types supported by the Pillow and Leptonica imaging libraries, including jpeg, png, gif, bmp, tiff, and others. Additionally, if used as a script, Python-tesseract will print the recognized text instead of writing it to a file.

### Second Implementation
After ROIs are detected, each of them are fed through the image-to-text detection and check against the local Genshin artifact strings to match set, type, and stats by checking the Levenshtein distance, which is the difference between 2 string using only character changes and addition. If one is missing, that is not considered a correct ROI and dismissed, while the correct ROI will be put through PyTesseract to retrieve lines of text (in Vietnamese).

### Testing
The project was put to a test using the original 88 images with artifacts at different locations on the screen as well as the real-time Genshin artifact display, and it has to output to console the right information as well as the correct approximate ROI boundary:

![td](https://github.com/tgban/gi-artifact-project/assets/38060917/f5090568-57cb-48a1-97ac-65501d4e2ccf)

It is to note that while real-time Genshin artifacts are being detected with ease, with one mistook the main stat of "Tấn công" (Atk) for "HP", the original 88 images needs some form of image manipulation (zoom in/out, changing image size and position) for it to detect. Since this project is intended to be used in real-time, the accuracy will only consist of the tests conducted on real-time artifacts, which is more than 90% accuracy.

### Note
While the accuracy of the current detection is more than 90%, there are a few edge cases to be addressed. One of which was mentioned in [Testing](#testing): the "Tấn công" (Atk) was mistaken for "HP". This happens mainly for main stat since the text for main stat is in gray color, and it is hard for PyTesseract to pick up this text correctly at times, resulting it sometimes having a Levenshtein distance closer to "HP" due to its length. Artifact string matching might need to be changed in the future to counter such edge cases.

## Artifact Scoring
### v1
In the first scoring implementation, it looks at the set, stat, and whether any pairs or trios of stats are hindering each other. For example, "HP", "Tấn công" (Atk), and "Phòng ngự" (Def) are the trio where, ideally, only one is needed. If two or more exists in an artifact, points will be deducted. Another such pair is "Phòng ngự" (Def) and "Tinh Thông Nguyên Tố" (Elemental Mastery, or EM for short), where no in-game character needs at this point in time.
Aside from point deduction, point addition is done if the stats are preferred by a set. For example, "Phiến Đá Lâu Đời" has a 2x set effect where it increases Geo damage, and "Tăng ST Nguyên Tố Nham" (Geo DMG Bonus) is a great line to combo with the set. CRIT rate and CRIT DMG lines are needed by a lot of characters, so more points are added. This is the same for ER lines.

### Testing v1
v1 scoring implementation was tested on the original 88 artifacts (through image manipulation for automatic data collection), and the results are in [this sheet, Sheet1 page](https://docs.google.com/spreadsheets/d/1D6Xf-Wp5CQNxEpSPHQQ8hxvj5gj_WLRcjb94unVRKfU/edit?usp=sharing). The first column determines whether the artifact is worth saving or getting rid of (personally). The last column depicts the score output from the scoring implementation. When plotted together:

![Graph depicting relationship between v1 scores and personal pass/fail. No clear threshold can be seen.](https://github.com/tgban/gi-artifact-project/assets/38060917/fdf54f4a-d978-48dc-81f2-7dc61d20f892)

As seen in the plot (x-axis being the index of the datapoint, y-axis being the v1 score of the datapoint, and the color represents personal pass/fail flag for the datapoint), no clear threshold can be seen, which prompts for a v2 implementation.
### v2
The score is divided into 3 categories:
- Attack score: Mainly prioritize Atk, HP, Elemental DMG Bonus, and CRIT lines.
- Defense score: Mainly prioritize Def and CRIT lines. EM lines are discouraged.
- Support score: Mainly prioritize Atk, HP, EM, ER (Energy Recharge), or Healing Bonus. CRIT lines are not as prioritized.
Score addition and subtraction is done pretty similarly to v1, except different categories might add or subtract scores differently. Then, the highest score of the 3 will become the v2 score.

### Testing v2
v2 scoring implementation was tested on 101 randomly picked artifacts from in-game, and the results are in [this sheet, Test Data page](https://docs.google.com/spreadsheets/d/1D6Xf-Wp5CQNxEpSPHQQ8hxvj5gj_WLRcjb94unVRKfU/edit?usp=sharing). The first column determines whether the artifact is worth saving or getting rid of (personally). The last column depicts the score output from the scoring implementation. When plotted together:

![Graph depicting relationship between v1 scores and personal pass/fail. Some clear threshold can be seen.](https://github.com/tgban/gi-artifact-project/assets/38060917/0286bbaa-b152-4159-9fbb-74892ac2472b)

When a threshold for pass/fail of 7.5 is set, the correct rate (calculated from counting true positive and true negative values) is more than 80%:

![Threshold set at 7.5 and correct rate.](https://github.com/tgban/gi-artifact-project/assets/38060917/0c677d88-4594-4c6d-90a0-56cfe5de44d8)

### Note
While testing, sometimes the detection system mistook artifact type and artifact stat, for example from a hat to a sandglass, or from Hydro DMG Bonus to Electro DMG Bonus. Further implementation changes to string matching might be needed to prevent such edge cases and improve accuracy. Also, characters are still being added in the future, so scoring algorithm might need to be updated in the future to keep up with artifact stats combinations and set.

## Finally
While at the current state of the project, the accuracy for detecting and scoring Genshin artifact is quite good, edge cases are still a problem to resolve, and future changes are still needed to keep up with new Genshin content.
