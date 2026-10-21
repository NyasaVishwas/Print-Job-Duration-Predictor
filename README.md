# Print Job Duration Predictor

A Python-based machine learning application that predicts the estimated duration of a print job using **Linear Regression**. The project uses **MongoDB** for storing print jobs, printer details, and prediction history. It also demonstrates schema validation, CRUD operations, and MongoDB aggregation pipelines.

## Features

- **Print Duration Prediction:** Estimates printing time based on page count, number of copies, print mode, binding type, and printer speed.
- **MongoDB Integration:** Stores and retrieves print-job data using PyMongo.
- **Schema Validation:** Enforces data validation rules for print-job documents.
- **CRUD Operations:** Create, read, update, and delete print jobs.
- **Aggregation Reports:** Analyzes average duration by print mode, job counts by status, total pages by binding type, and the five slowest completed jobs.
- **Prediction History:** Saves predictions in MongoDB for later retrieval.
- **Model Evaluation:** Evaluates the Linear Regression model using MAE, RMSE, and R².

## Technologies Used

- Python
- MongoDB
- PyMongo
- pandas
- NumPy
- scikit-learn
- joblib

## Project Structure

```text
Print Job Duration Predictor/
├── database.py
├── seed_data.py
├── train_model.py
├── predict.py
├── validation.py
├── operations.py
├── aggregations.py
├── main.py
├── requirements.txt
├── models/
│   └── linear_regression.joblib
└── README.md
```

## Prerequisites

- Python 3.10 or later
- MongoDB Community Server
- pip

The project was developed and tested using Python 3.13 and a local MongoDB instance.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/NyasaVishwas/Print-Job-Duration-Predictor.git
cd "Print Job Duration Predictor"
```

Replace `<your-repository-url>` with your GitHub repository URL.

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start MongoDB

Ensure the MongoDB server is running locally and accessible at:

```text
mongodb://localhost:27017/
```

The application uses the MongoDB database named `printpulse`.

### 5. Generate sample data

```bash
python seed_data.py
```

This script generates 300 synthetic print-job records and prepares three printer records. If print jobs already exist, the script skips inserting another batch of jobs.

### 6. Configure schema validation

```bash
python validation.py
```

This configures MongoDB JSON Schema validation for the `print_jobs` collection and tests rejection of an invalid document.

### 7. Train the machine learning model

```bash
python train_model.py
```

The script retrieves completed print jobs from MongoDB, prepares input features, trains a Linear Regression model, evaluates performance, and saves the trained model to:

```text
models/linear_regression.joblib
```

### 8. Run the application

```bash
python main.py
```

The menu provides options to predict print duration, manage print jobs, view aggregation reports, and view prediction history.

## Machine Learning Approach

The project uses **Linear Regression**, a supervised learning algorithm suitable for predicting continuous numerical values.

### Input Features

- `page_count`: Number of pages in a document.
- `copies`: Number of copies to print.
- `print_mode`: Black-and-white or color printing.
- `binding_type`: None, staple, or spiral binding.
- `printer_speed_ppm`: Printer speed in pages per minute.

### Feature Engineering

The model uses the following engineered features:

- **Effective pages:** Page count multiplied by copies and divided by printer speed.
- **Color pages:** Effective pages for color printing; zero for black-and-white printing.
- **Binding type:** Converted into numerical features using one-hot encoding.

The data is divided into 80% training data and 20% testing data. The trained preprocessing and regression pipeline is saved using joblib and reused for predictions.

## Model Performance

The following results were observed during a training run:

| Metric | Result |
|---|---:|
| Training records | 240 |
| Testing records | 60 |
| Mean Absolute Error (MAE) | 0.452 minutes |
| Root Mean Squared Error (RMSE) | 0.507 minutes |
| R² Score | 0.9993 |

- **MAE** measures the average absolute difference between predicted and actual durations.
- **RMSE** measures prediction error while penalizing larger errors more heavily.
- **R²** measures how well the model explains variation in the target values relative to a mean baseline.

**Important:** The dataset is synthetically generated using a duration formula with random noise. These metrics demonstrate performance on simulated data and do not establish accuracy on real printing-shop data.

## MongoDB Collections

### `print_jobs`

Stores print-job details, including page count, copies, print mode, binding type, printer speed, actual duration, creation time, and job status.

### `printers`

Stores printer information, including printer ID, name, speed, supported modes, binding support, and availability status.

### `prediction_history`

Stores prediction inputs and the corresponding estimated print duration. Each prediction is recorded as a separate document.

## MongoDB Aggregation Reports

The application demonstrates four aggregation pipelines:

1. **Average Duration by Print Mode:** Calculates the average duration and number of completed jobs for each print mode.
2. **Job Count by Status:** Counts jobs grouped by their current status.
3. **Total Pages by Binding Type:** Calculates total printed pages, accounting for copies, grouped by binding type.
4. **Five Slowest Completed Jobs:** Retrieves the five completed jobs with the longest recorded durations.

## Example Prediction

**Input:**

```text
Page count: 50
Copies: 2
Print mode: color
Binding type: spiral
Printer speed: 25 pages/min
```

**Observed output:**

```text
Predicted duration: 11.96 minutes
```

The prediction is also stored in the `prediction_history` collection.

## Limitations and Future Improvements

- Train and evaluate the model using real print-job measurements.
- Compare Linear Regression with other regression algorithms.
- Add features such as paper type, printer condition, and queue waiting time.
- Add automated unit tests and more comprehensive input validation.
- Extend validation rules to printer and prediction-history documents.
- Develop a web interface or API for easier integration with printing systems.

## Conclusion

The Print Job Duration Predictor demonstrates how MongoDB, Python, PyMongo, and machine learning can be combined in a backend application. It integrates document storage, schema validation, CRUD operations, aggregation-based analytics, model evaluation, and prediction history into one runnable project.

## Author

**Name:** Nyasa Vishwas

**Project:** Print Job Duration Predictor
