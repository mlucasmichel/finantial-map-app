# Manual Testing Procedures

This document outlines the manual testing steps performed to ensure the functionality, usability, and responsiveness of the application.

## 1. Authentication

*   **Objective:** Verify user registration, login, and logout flows.
*   **Steps:**
    1.  Navigate to `/accounts/signup/`.
    2.  Attempt to register with valid credentials. Verify successful registration and redirection to login/dashboard.
    3.  Attempt to register with existing username/email. Verify appropriate error messages.
    4.  Navigate to `/accounts/login/`.
    5.  Attempt to log in with valid credentials. Verify successful login and redirection to dashboard.
    6.  Attempt to log in with invalid credentials. Verify appropriate error messages.
    7.  Click the "Logout" option in the navbar dropdown. Verify successful logout and redirection to login page.
    8.  Attempt to access authenticated pages (e.g., `/accounts/`) while logged out. Verify redirection to login page.

## 2. Account Management (CRUD)

*   **Objective:** Verify creation, viewing, updating, and deletion of user accounts.
*   **Steps:**
    1.  Log in as a test user.
    2.  Navigate to the Accounts List (`/accounts/`).
    3.  Click "Add Account".
    4.  Submit the form with valid data (e.g., "Checking Account", "500.00"). Verify account appears in the list and current balance on dashboard is updated.
    5.  Submit the form with invalid data (e.g., negative balance). Verify error messages.
    6.  Click "Edit" next to an existing account. Update its name and balance. Verify changes are reflected in the list and dashboard.
    7.  Click "Delete" next to an existing account. Confirm deletion. Verify account is removed from the list and total balance is updated.

## 3. Category Management (Implied by Transactions/Budgets)

*   **Objective:** Verify categories are available and correctly used.
*   **Steps:**
    1.  Ensure default categories are loaded (e.g., by creating a transaction and checking category dropdown).

## 4. Transaction Management (CRUD)

*   **Objective:** Verify creation, viewing, updating, and deletion of transactions, and their impact on account balances.
*   **Steps:**
    1.  Log in as a test user.
    2.  Navigate to the Records List (`/transactions/`).
    3.  Click "Add Record" (from sidebar or navbar).
    4.  Submit form with valid data (Account, Category, Amount, Date, Description). Verify transaction appears in the list and the linked Account's balance on dashboard is updated.
    5.  Submit form with invalid data (e.g., missing fields). Verify error messages.
    6.  Click "Edit" next to an existing transaction. Update amount, category, or account. Verify changes are reflected in the list and all relevant Account balances are correctly updated.
    7.  Click "Delete" next to an existing transaction. Confirm deletion. Verify transaction is removed from the list and the linked Account's balance is reverted.

## 5. Budget Management (CRUD)

*   **Objective:** Verify creation, viewing, updating, and deletion of monthly budgets.
*   **Steps:**
    1.  Log in as a test user.
    2.  Navigate to the Budgets List (`/budgets/`).
    3.  Click "Set New Budget".
    4.  Submit form with valid data (Category, Limit, Month, Year). Verify budget appears in the list.
    5.  Submit form with invalid data (e.g., duplicate budget for same category/month/year). Verify error messages.
    6.  Click "Edit" next to an existing budget. Update its limit. Verify changes are reflected.
    7.  Click "Delete" next to an existing budget. Confirm deletion. Verify budget is removed from the list.

## 6. Dashboard & Filtering

*   **Objective:** Verify the dashboard displays correct summaries and filters work as expected.
*   **Steps:**
    1.  Log in as a test user with some existing accounts and transactions.
    2.  Navigate to the Dashboard (`/dashboard/`).
    3.  Verify:
        *   Total balance across accounts is correct.
        *   Expense Structure chart, Cash Flow Summary, and Monthly Budgets (if set) display accurate data for the selected month/year.
        *   Balance Trend chart is visible and appears correct.
    4.  Use the month/year filters at the top of the dashboard. Verify all charts and summaries update correctly.
    5.  Navigate to Records List (`/transactions/`).
    6.  Use the sidebar filter form (Accounts, Categories, Start Date, End Date). Verify that the transaction list updates to show only matching transactions.
    7.  Click "Clear Filters". Verify the full list of transactions is restored.

## 7. Responsive Design

*   **Objective:** Verify the application's layout and functionality across various screen sizes.
*   **Tools:** Browser developer tools (toggle device toolbar) or actual mobile devices.
*   **Checklist:**
    *   **Navbar:** Collapses correctly, menu items are accessible.
    *   **Dashboard:** Cards and charts resize and stack appropriately.
    *   **Forms:** Input fields are well-aligned and usable.
    *   **Lists (Accounts, Records, Budgets):** Tables (if used) are responsive or switch to card-like layouts. Sidebar filters are accessible.
    *   **Overall:** No horizontal scrolling is needed. All content is visible and interactive.