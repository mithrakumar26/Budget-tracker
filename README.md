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
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
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
![Login Page](path/to/login_screenshot.png)

### Dashboard
![Dashboard](path/to/dashboard_screenshot.png)

## License

This project is licensed under the MIT License.
```

### Notes:
1. Replace the placeholders for the screenshots (`path/to/login_screenshot.png` and `path/to/dashboard_screenshot.png`) with the actual paths.
2. Add a `requirements.txt` file that lists all the dependencies used in the project for installation.
