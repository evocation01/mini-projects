Here is a list of the nine labs that you need to have completed and downloaded as preparation for your submission. Ensure that you have completed the tasks listed under each lab.

Question 1. Refer to the following tasks of the lab “Comparison of Memory-Based and Generator-Based Data Loading” in Module 1. (10 points)

    Task 1: Determine the shape (dimensions) of a single image stored in the image_data variable.

    Task 2: Display the first four images in './images_dataSAT/class_0_non_agri/' directory.

    Task 3: Create a list named agri_images_paths that contains the full file paths of all images located in the dir_agri directory. Sort the list before saving it.

    Task 4: Determine the number of images of agricultural land that exist in the './images_dataSAT/class_1_agri/' directory.

Question 2. Refer to the following tasks of the lab “Data Loading and Augmentation Using Keras” in Module 1. (8 points)

    Task 1: Create the list all_image_pathscontaining paths of files from both folders: class_0_non_agri and class_1_agri.

    Task 2: Create a temporary list temp by binding image paths and labels. Print 5 random samples.

    Task 3: Generate a data batch (batch size = 8) using the custom_data_generator function.

    Task 4: Create validation data using a batch size of 8.

Question 3. Refer to the following tasks of the lab “Data Loading and Augmentation Using PyTorch” lab in Module 1. (10 points)

    Task 1: Define a transformation pipeline custom_transform including:

    image size = 64 x 64 pixels

    RandomHorizontalFlip probability 0.5

    RandomVerticalFlip probability 0.2

    RandomRotation of 45 degrees

    Task 2: Load dataset using datasets.ImageFolder with custom_transform.

    Task 3: Print class names and indices from imagefolder_dataset.

    Task 4: Retrieve and display image shapes from a batch in imagefolder_loader.

    Task 5: Display images in the custom loader batch.

Question 4. Refer to the following tasks of the lab “Train and Evaluate a Keras-Based Classifier” in Module 2. (12 points)

    Task 1: Walk through dataset_path to create list fnames of all image files.

    Task 2: Create validation_generator.

    Task 3: Count the total number of CNN model layers.

    Task 4: Create and compile a CNN with 4 Conv2D and 5 Dense layers.

    Task 5: Define a checkpoint callback with max accuracy.

    Task 6: Plot training and validation loss.

Question 5. Refer to the following tasks of the lab “Implement and Test a PyTorch-Based Classifier” in Module 2. (20 points)

    Task 1: Explain the usefulness of random initialization.

    Task 2: Define train_transform pipeline.

    Task 3: Define the val_transform pipeline.

    Task 4: Create val_loader for the validation dataset.

    Task 5: Purpose of tqdm.

    Task 6: Explain why train_loss, train_correct, and train_total are reset every epoch.

    Task 7: Why use torch.no_grad() in the validation loop?

    Task 8: List two metrics used to evaluate training performance.

    Task 9: Plot model training loss.

    Task 10: Retrieve predictions all_preds and ground truth all_labels from val_loader.

Question 6. Refer to the following tasks of the lab “Comparative Analysis of Keras and PyTorch Models” in Module 2. (10 points)

    Task 1: What does preds > 0.5 do in line: preds = (preds > 0.5).astype(int).flatten()?

    Task 2: Print Keras model metrics using print_metrics.

    Task 3: Explain the significance of the F1-score.

    Task 4: Print PyTorch model metrics using print_metrics.

    Task 5: Count false negatives in the PyTorch confusion matrix.

Question 7. Refer to the following tasks of the lab “Vision Transformers in Keras” in Module 3. (10 points)

    Task 1: Load and summarize a pre-trained CNN model using load_model() and summary().

    Task 2: Identify the feature extraction layer in feature_layer_name.

    Task 3: Define the hybrid model using build_cnn_vit_hybrid.

    Task 4: Compile the hybrid_model.

    Task 5: Set training configuration.

Question 8. Refer to the following tasks of the lab “Vision Transformers in PyTorch” in Module 3. (12 points)

    Task 1: Define train_transform.

    Task 2: Define val_transform.

    Task 3: Create train_loader and val_loader.

     Task 4: Train CNN-ViT model with parameters: epochs=5, attn heads=12, embed_dim=768, transformer block depth = 12.

    Task 5: Plot validation loss comparison between model and model_test.

    Task 6: Plot training time comparison.

Question 9. Refer to the following tasks of the lab “Land Classification: CNN-Transformer Integration Evaluation” in Module 3. (8 points)

    Task 1: Define dataset directory, data loader, and model hyperparameters.

    Task 2: Instantiate the PyTorch model.

    Task 3: Print evaluation metrics for the KerasViT model (label: "Keras CNN-ViT Hybrid Model").

    Task 4: Print evaluation metrics for the PyTorchViT model (label: "PyTorch CNN-ViT Hybrid Model").
