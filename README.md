# ECS-271 Project | Winter 2022 | UC Davis

## Team Members
- Shivam Pandey
- Michael Yang
- Aniket Banginwar

## Supervisor
- Prof. Hamed Pirsiavash (Department of Computer Science, UC Davis)

## References

- https://towardsdatascience.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5
- IAM Dataset

## How to Run

- To run the model, clone/download this repo.
- Download the word model from https://drive.google.com/drive/folders/1Mr0f6xURIt8wUtctTUayUyeaH8gjwRMb?usp=sharing, and unzip the word-model.zip.
- Get into the root directory of the cloned repository, and then copy all the contents of word-model.zip into the /Our Code/model directory present in the root directory.
- Get into the /Our Code/src directory from the root directory.
- To run and check the output of Phase-1, get into the /Our Code/src and run the command: *python3 SiLiHaSeR_phase1_image_preprocess.py test2.png* . This command will run the Phase-1 code for test2.png, and produce the individual word images in the same directory.
- To run and check the output of Phase-1 + Phase-2 combined, run the command in /Our Code/src directory: *python3 SiLiHaSeR_phase2_sentence_recognizer test2.png* . This will run the SiLiHaSeR model (Phase-1+Phase-2) and produce the desired machine-printed text as output in the terminal for test2.png.
- To run the model on all 34 custom sentence images and calculate the accuracy, run the command in /Our Code/src directory: *python3 SiLiHaSeR_accuracy_over_test_data.py*. This should output the predicted sentence for all test images along with the accuracies as explained in the report.

## Project Report

- Report can be found in /Report directory.
