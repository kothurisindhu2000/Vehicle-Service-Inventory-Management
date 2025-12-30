## Project Overview

The Vehicle Service & Inventory Management System is a desktop application designed to help a vehicle service garage manage customer service bookings, mechanic workflows, and parts/tools inventory from a single platform.

This project was developed for the **BIS 698 – Information System Project** course at **Central Michigan University** by **Group 6**.

The system supports three user roles:
- **Customer** – Books services and tracks vehicle service status
- **Admin** – Manages services, mechanics, payments, inventory, and suppliers
- **Mechanic** – Views assigned services and updates service progress

All data is stored in a **MySQL** database, and the application is built using **Python with Tkinter**.

---

## Application Features

### Customer
- Register and log in to the system
- Schedule services (e.g., Oil Change, Seat Covers Change) with notes
- View previous service history (date, amount, status)
- Track current service status and expected delivery date
- Submit ratings and feedback after service completion

### Admin
- View dashboard metrics (customers, mechanics, service statuses)
- View all service requests and filter unassigned or completed services
- Assign mechanics to service requests using dropdown selection
- Update payment status for completed services
- Add new services with pricing
- Add new mechanics with login credentials
- Manage parts/tools inventory
- Track tools used per service
- Maintain supplier contact information

### Mechanic
- Log in to a mechanic dashboard
- View assigned services with request details
- Update service status and delivery dates
- View completed services with customer feedback
- View tools inventory and usage per service

---

## Technologies Used
- **Language:** Python
- **GUI Framework:** Tkinter, tkcalendar
- **Database:** MySQL
- **Connector:** mysql-connector-python

---

## Running the Application

### Development Mode
python Login.py

##  System Architecture
Authentication & Role Detection
Users log in with a username/email and password
The system determines the user role by querying the database
Based on the role, the appropriate dashboard is loaded:
AdminDashboard
CustomerDashboard
MechanicDashboard

##  Database Design
The application uses the following core tables:
- **CUSTOMER** – Customer details and login credentials
- **MECHANIC** – Mechanic profiles and credentials
- **SERVICE_REQUEST** – Service bookings, status, dates, and mechanic assignments
- **PARTS** – Parts and tools inventory
- **PARTS_USED** – Tools used per service request
- **SUPPLIERS** – Supplier contact information
- **FEEDBACK** – Customer ratings and comments

## Development Details
- **Customer Module** - 
Creates new service requests in SERVICE_REQUEST.
Retrieves service history and current service status.
Inserts customer feedback into FEEDBACK.

- **Admin Module** - 
Assigns mechanics by updating SERVICE_REQUEST.Mechanic_ID.
Updates payment status.
Adds new records to PARTS, SUPPLIERS, SERVICES, and MECHANIC.

- **Mechanic Module** - 
Retrieves services assigned to the logged-in mechanic.
Updates service status and delivery dates.
Displays customer feedback.
Displays tools usage by joining PARTS_USED and PARTS.

- **Testing & Packaging** - 
Tested all user roles independently.
Verified service booking, mechanic assignment, status updates, payments, and feedback.
Packaged as a standalone executable (Login.exe) to run without a Python environment.
