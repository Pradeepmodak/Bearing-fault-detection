# Project Walkthrough And Viva Preparation

## Problem Statement

Bearings are essential parts of rotating machines. If a bearing develops an inner race, outer race, or ball defect, the vibration pattern changes. Detecting these changes early helps avoid serious machine failure and supports predictive maintenance.

In simple terms:

- healthy bearings produce a more regular vibration pattern
- faulty bearings create abnormal vibration signatures
- machine learning can learn those signatures and classify the fault type

## Approach

### 1. Acquire Vibration Data

The project uses the CWRU bearing dataset, which contains vibration signals from a motor-bearing test rig under different health conditions.

### 2. Segment The Signal

Each long vibration signal is divided into smaller windows. This creates many training samples and helps the model learn local patterns associated with faults.

### 3. Extract Features

The project computes informative signal features instead of feeding raw waveforms directly into classical ML models.

Time-domain examples:

- mean
- RMS
- standard deviation
- skewness
- kurtosis
- crest factor

Frequency-domain examples:

- FFT spectrum
- dominant frequency
- spectral mean
- spectral energy
- frequency variance

### 4. Train Machine Learning Models

Two models are trained:

- Support Vector Machine
- Random Forest

They are compared using:

- accuracy
- precision
- recall
- F1-score

### 5. Deploy With GUI

A Streamlit interface allows the user to:

- load a signal
- inspect waveform and FFT plots
- see the predicted fault class
- view prediction confidence
- examine extracted features

## Results

The project produces:

- a trained reusable model artifact
- a confusion matrix
- a feature importance plot
- a live prediction dashboard

This makes the project valuable for:

- mechanical engineering project evaluation
- ML interview discussion
- live technical demonstrations

## Simple Viva Explanation

"We used vibration data from the CWRU bearing dataset, segmented the signals, extracted time-domain and frequency-domain features, trained SVM and Random Forest models, compared their performance, and deployed the best model in a Streamlit GUI for fault prediction."

## Possible Viva Questions With Answers

### Why use the CWRU dataset?

It is one of the most widely used benchmark datasets for bearing fault diagnosis and is accepted in academic and applied condition-monitoring work.

### Why use vibration signals?

Bearing defects directly change mechanical vibration, so vibration analysis is one of the most practical ways to detect faults.

### Why use FFT?

FFT transforms the signal into the frequency domain, where fault-related frequency patterns are easier to analyze.

### What is RMS?

RMS measures the overall energy level of the vibration signal. Faulty bearings often increase vibration energy.

### Why use feature extraction?

Classical ML models work well on compact numerical features. Features also make the pipeline easier to explain during a presentation.

### Why use two models?

Comparing two models shows a proper engineering workflow instead of assuming one algorithm is automatically best.

### What is a confusion matrix?

It is a table showing true classes versus predicted classes, which helps explain where the model performs well and where mistakes happen.

### What are the current limitations?

- the local sample set is smaller than the full CWRU collection
- the current workflow uses segment-level splitting
- the app expects CSV input rather than direct sensor streaming

### How can the project be improved?

- add more operating loads and fault cases
- use 1D CNN or other deep learning approaches
- connect to live sensor acquisition
- deploy as an online predictive maintenance dashboard

## Interview Talking Points

- end-to-end ownership from data to deployment
- combination of mechanical knowledge and ML implementation
- explainability through confusion matrix and feature importance
- strong demo story through the Streamlit interface
