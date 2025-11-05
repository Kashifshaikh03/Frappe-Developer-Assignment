# ERPNext v15 Setup & Frappe Developer Assignment

This repository provides a complete guide to set up **ERPNext Version 15** on **Ubuntu 22.04**, along with a detailed **Frappe Developer Assignment** focusing on HRMS, Recruitment, Payroll, and Taxation modules.

---

## System Setup (Brief)

### **Prerequisites**

| Type | Requirement |
|------|--------------|
| OS | Ubuntu 22.04 |
| User | A user with sudo privileges |
| Python | v3.10+ |
| Node.js | v18 |
| RAM | 4GB Minimum |
| Storage | 40GB Minimum |

---

### **Step 1: Update and Upgrade**
```bash
sudo apt-get update -y
sudo apt-get upgrade -y

Step 2: Create Bench User
sudo adduser frappe
sudo usermod -aG sudo frappe
su frappe
cd /home/frappe

Step 3: Install Dependencies
Install Required Packages
sudo apt-get install git python3-dev python3.10-dev python3-setuptools python3-pip python3-distutils python3.10-venv software-properties-common -y

Install MariaDB & Redis
sudo apt install mariadb-server mariadb-client redis-server -y

Configure MariaDB
sudo mysql_secure_installation
sudo nano /etc/mysql/my.cnf


Add:

[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4


Then restart:

sudo service mysql restart

Step 4: Install Node.js, NPM, and Yarn
sudo apt install curl -y
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
source ~/.profile
nvm install 18
sudo apt-get install npm -y
sudo npm install -g yarn

Step 5: Install wkhtmltopdf
sudo apt-get install xvfb libfontconfig wkhtmltopdf libmysqlclient-dev -y

Step 6: Install Frappe Bench
sudo pip3 install frappe-bench


Initialize Frappe Bench:

bench init --frappe-branch version-15 frappe-bench
cd frappe-bench


Give permission:

chmod -R o+rx /home/frappe

Step 7: Create a New Site
bench new-site test.localhost

Step 8: Install ERPNext and Custom App
Get ERPNext App
bench get-app --branch version-15 erpnext

Get Your Custom App
bench get-app my_custom_app

Install on Site
bench --site test.localhost install-app erpnext
bench --site test.localhost install-app my_custom_app

 Frappe Developer Assignment

This assignment demonstrates the ability to customize and extend ERPNext (v15) using the Frappe Framework — covering HRMS, recruitment workflows, payroll, and taxation.

Part 1 – HRMS & Recruitment
1. Recruitment Workflow

Workflow:
Job Opening → Application → Screening → Interview → Offer → Hired

Roles and Permissions:

HR Manager – Create and manage job openings.

Interviewer – Evaluate during the screening and interview stages.

Hiring Manager – Final approval and offer stage.

Add Custom Field:

Field Name: source_of_application

Label: Source of Application

Options: LinkedIn, Referral, Job Portal, Others.

Doctype: Job Applicant

Create a Report/Dashboard:

Title: Applicants by Source

Displays a count of applicants grouped by “Source of Application”.

 Part 2 – Employee Lifecycle
1. Lifecycle Events

Employee stages: Joining → Probation → Confirmation → Exit

2. Automations

On Confirmation:

Automatically update employee status to “Confirmed”.

On Exit:

Automatically generate an Experience Letter (PDF).

Attach generated PDF to the employee record.

3. Implementation Details

Add date fields:

probation_end_date

confirmation_date

relieving_date

Create a server script or hook:

Trigger on before_save or on_update.

Check lifecycle dates and update status.

Generate PDF using frappe.attach_print.

Part 3 – Salary Structure & Payroll
1. Salary Structure

Create salary structure with:

Earnings:

Basic

HRA

Special Allowance

Deductions:

PF

Professional Tax

2. Payroll Entry

Process salary for multiple employees.

Ensure each salary slip includes earning/deduction details.

3. Custom Salary Slip Print Format

Add company branding and logo.

Include:

Employee Info

Earnings & Deductions Table

Department & Designation

Attendance Summary

Ensure Net Pay = Gross Pay consistency.

Part 4 – Tax Regime Implementation
Objective

Support both Old and New tax regimes within Payroll.

Steps

Create two Salary Structures:

Old Regime Structure

New Regime Structure

Add a field in Employee Doctype:

tax_regime_preference (Select: Old Regime / New Regime)

On Payroll Generation:

System automatically selects the correct salary structure.

Create a Comparison Report:

Columns:

Employee

Gross Salary

Old Regime Tax

New Regime Tax

Tax Savings (Difference)

Part 5 – Customization: Investment Declaration
Doctype: Employee Investment Declaration
Field	Label	Description
section_80c	Section 80C	LIC, PPF, ELSS, etc.
section_80d	Section 80D	Medical Insurance
other_exemptions	Other Exemptions	HRA, LTA, etc.
Integration with Payroll

Link this Doctype to Employee.

During tax calculation, include declared exemptions to reduce taxable income.

Git & Version Control Process
Repository Setup
# Initialize a new Git repository
git init

# Add remote origin
git remote add origin https://github.com/Kashifshaikh03/Frappe-Developer-Assignment.git

# Verify remote
git remote -v

Branch Creation
# Create and switch to a new feature branch
git checkout -b new-feature

Add and Commit Changes
# Add all files
git add .

# Commit Part 1
git commit -m "Part 1: Implemented Recruitment Workflow with Job Applicant source field and Applicants by Source report"

# Commit Part 2
git commit -m "Part 2: Automated employee lifecycle with confirmation update and Experience Letter generation"

# Commit Part 3
git commit -m "Added Payroll setup and Tax Regime implementation"

# Commit Part 4
git commit -m "Added Employee Investment Declaration Doctype and linked with Payroll for tax calculations"

Push to GitHub
# Push branch to remote
git push origin new-feature
