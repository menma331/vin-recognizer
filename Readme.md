# VIN Recognizer

VIN Recognizer is a system designed to automatically extract Vehicle Identification Numbers (VIN) from various types of images. The system accelerates the customer service process by automating VIN recognition, even for images with rotated or angled VINs, and provides explanations if a VIN cannot be identified.

## Business Context

The system is developed for a company specializing in car parts. It addresses the challenge of manually recognizing VINs from images provided by customers. The system ensures efficiency, transparency, and accuracy in VIN recognition.

## Features

- **VIN Extraction**: Automatically extracts VIN codes from images, even those rotated, angled, or inverted.
- **Error Explanation**: Provides reasons why a VIN code is not present or identifiable in an image.
- **Accuracy Handling**: Ensures transparency in recognition accuracy, avoiding false positives and detailing potential errors.
- **Multi-context Support**: Supports VIN recognition from diverse contexts such as documents, handwritten notes, car hoods, and even screenshots.

## Requirements

### System Requirements
- **Python**: 3.10 or higher.
- **Dependencies**:
  - `qwen2.5-7B-VL` for VIN recognition.

### Dataset
- The system is tested and trained with a dataset comprising:
  - Images of handwritten VINs.
  - Photos of VINs on car hoods.
  - Screenshots of VIN codes.
  - Images without VINs (e.g., parts or unrelated items).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/menma331/vin-recognizer.git
   cd vin-recognizer
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Environment Variables**:
   Create a `.env` file with the following:
   ```env
   MODEL_PATH=path_to_qwen_model
   ```

4. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

1. **Input**: Upload an image containing a VIN code.
2. **Process**: The system extracts the VIN or provides an explanation for its absence.
3. **Output**: The VIN code or an error message.

### Examples:

- **Input**: A photo of a car hood with a VIN.
  - **Output**: "VIN: 1HGCM82633A123456"
- **Input**: An image without a VIN.
  - **Output**: "Reason: This appears to be an image of a manual, not a VIN."

## Architecture

The system is composed of the following components:

1. **Image Preprocessing**:
   - Rotates and aligns images to detect VIN codes at various angles.
2. **VIN Recognition Model**:
   - Utilizes `qwen2.5-7B-VL` for OCR-based VIN recognition.
3. **Error Handling Module**:
   - Identifies and categorizes images without VIN codes, providing a human-understandable explanation.
4. **Accuracy Management**:
   - Ensures a false-positive rate below 20% by validating results with defined thresholds.

## Evaluation and Metrics

The system's performance is evaluated based on:
- **Accuracy**: Correct identification of VIN codes.
- **False Positives**: Instances where non-VIN data is incorrectly identified as a VIN.
- **Processing Time**: Speed of recognition and response.

## Contribution

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Ensure your code adheres to the project standards and includes appropriate tests.

## Future Plans

- Explore alternative models to `qwen2.5-7B-VL` for cost-effectiveness.
- Enhance recognition accuracy for handwritten and obscured VINs.
- Integrate with customer support systems for seamless operation.

## Contact

For questions or feedback, contact the repository owner:
- GitHub: [menma331](https://github.com/menma331)