# Expense Tracker

Expense Tracker is a web application built using Dash and Flask that helps users manage their income and expenses efficiently. It features user authentication, dynamic transaction management, and visual income vs. expense comparisons. Users can add, delete, filter, and download their transaction history.

## Features

- **User Authentication**: Secure login using Flask-Login.
- **Transaction Management**: Add, edit, and delete transactions.
- **Income vs Expense Visualization**: Bar chart for comparing income and expenses.
- **Downloadable Data**: Export your transaction history as a CSV file.
- **Dynamic DataTable**: Filter and sort transaction records directly from the app.

## Tech Stack

- **Frontend**: Dash (Plotly), HTML, Bootstrap components
- **Backend**: Flask (with Flask-Login for authentication)
- **Database**: In-memory storage for user-specific transactions
- **Visualization**: Plotly for charts

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mithrakumar26/Budget-tracker.git
   cd Budget-tracker
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Open your browser and go to `http://127.0.0.1:8050/`.

## Usage

1. **Login**: Use the default credentials to log in:
   - Username: `admin`
   - Password: `1234`

2. **Add Transaction**: Enter a transaction description, category, amount (negative for expenses, positive for income), and date.

3. **View and Filter**: See your transactions in the table and use sorting/filtering options to manage them.

4. **Download**: Click "Download History" to export your transactions as a CSV file.

## Screenshots

### Login Page
![image](https://github.com/user-attachments/assets/cad3f164-2402-4279-aabc-9b55ae718877)


### Dashboard
![image](https://github.com/user-attachments/assets/8ad0b0ee-660a-4e38-8a74-b9afb0449623)
![image](https://github.com/user-attachments/assets/26d0adc3-e430-41a3-940d-7c0c6eb84c90)


