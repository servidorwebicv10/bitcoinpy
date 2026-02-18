# Bitcoin Data Visualization Web App

A Flask-based web application that analyzes and visualizes Bitcoin price data using Python, Pandas, and Matplotlib.

This project loads historical Bitcoin data from a CSV file and generates multiple interactive visualizations displayed through a web interface.

---

## Features

- Load and process Bitcoin historical data from CSV
- Generate multiple data visualizations
- Display charts dynamically using Flask templates
- Clean project structure following Flask best practices

---

## Technologies Used

- Python 3
- Flask
- Pandas
- Matplotlib
- HTML5
- CSS3

---

## Project Structure
```
bitcoinpy/
│
├── app.py
├── bitcoin.csv
├── requirements.txt
├── static/
│ ├── styles.css
│ └── generated charts (.png)
│
├── templates/
│ ├── index.html
│ ├── grafica1.html
│ ├── grafica2.html
│ ├── grafica3.html
│ └── grafica4.html
```


---

## Installation

Clone the repository:

```bash
git clone https:(URL)
cd bitcoinpy
```
Install dependencies:

pip install -r requirements.txt

---

## Run the Flask application:

python app.py

## Then open your browser and go to:

http://127.0.0.1:5000/

---

## Visualizations Included

 - Price trend over time

 - Statistical analysis of price behavior

 - Multiple comparative graphs

 - Dynamic image rendering with Matplotlib

## Future Improvements

 - Add real-time Bitcoin API integration

 - Improve UI/UX design

 - Deploy to cloud (Render, Railway, or Heroku)

 - Add user interaction filters

---

# Author

Iván David Caro Vargas  
Aspiring Full Stack Developer  

