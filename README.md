# 📂 Sorted

I have always struggled and have seen other students struggle while organizing a bunch of files in a folder , it has always been a waste of time for me to sit and manually organize the files. Now people don't have to go through the struggle I went through because of SORTED.

Sorted is a web-application which organizes your files for you by the help of machine learning algorithm , it stores files based on the text inside the files , it scans the text and then defines it under a category based on the data it was trained on.

It is a very simple yet efficient web-app in which we have used flask as the backend and basic html and css for the frontend , the algorithm used in the machine learning is naive bayes, and custom data on which it was trained on .

Well some challenges were that we did not have data to start with and still there is some files that it has trouble reading from and also because of lack of data it was difficult to train the model and get a good accuracy score.

even after all these challenges we got a 0.87 accuracy which we are certainly proud of and also the UI which is minimal yet engaging , and we tested this with many of my friends and we got a great response.

We are certainly gonna scale it and also going to train the model on more data so the minor errors that we are facing right now will be eliminated.

---

## 🚀 Features

- 📄 Upload multiple PDF files at once
- 🧠 Uses a trained ML model to predict categories
- 🗃️ Automatically organizes PDFs into categorized folders
- 🧼 Skips corrupted or empty PDFs and stores them separately
- 📦 Downloads sorted PDFs as a ZIP archive
- 🧹 Clear results button and scrollable interface for many files

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Python, Flask  
- **ML Model**: Naive Bayes (Scikit-learn)  
- **PDF Parsing**: `PyMuPDF` or `pdfminer.six`

