# Project-Phishing
Research project - Phishing Simulation Web Application

## Introduction
This reposiroty contains a Flask web application designed to simulate phishing and genuine email challenges for educational and training purposes.
The application provides two questionnaire forms to be completed before and after the simulation. The simulation provides users with six different emails related to a secondary school environment. In each email scenario, users must decide whether the email is genuine, phishing or unsure. They will also be required to rate their confidence (low, medium or high) and have the option to provide a reason for their decisions. Scoring is based on duration of decision making and accuracy of identification of the emails. Following completion of the pre-simulation questionnaire, phishing simulation and post-simulation questionnaire, users are redirected to an overall score and grade level that includes tips to support their learning in cyber awareness.

## Features
- User registration and authentication system.
- Pre-simulation questionnaire to assess user's initial awareness.
- Six email challenges to identify.
- Post-simulation questionnaire to measure the change in user awareness.

## Prerequisites
The following requirements are needed before you begin:
- Python 3
- Virtualenv for python packages

## Installation
To install please follow these steps:

```bash
git clone https://github.com/jj-call/Project-Phishing.git
cd Project-Phishing.git
pipenv install or use
pip install -r requirements.txt

## Configuration
Create a .env file in the root directory of the project with:

FLASK_APP=my_app
FLASK_ENV=development
DB_USERNAME=root
DB_PASSWORD=
DB_NAME=
SECRET_KEY=
DB_HOST=localhost
DB_PORT=3306

Running from Windows from the downloaded directory:
Change to the downloaded directory
```
.\venv\Scripts\activate
set FLASK_APP=my_app.py
set FLASK_ENV=development
flask db upgrade
flask run
```

The application will be available at 'http://localhost:5000' or 127.0.0.1

## Using the application
Register as a new user with username and password to make a user account. A progress log is created for training perodically.
When entering the base page follow the instructions and steps. 
After completing the steps in sequence, a final page will provide a score, grade and information on awareness.

## Database setup
Using a console PHP My Admin either web or localhost 127.0.0.1

Database query:
Code to seed the Phishing Challenges Table


```
CREATE TABLE `phishing_challenges` (
  `id` varchar(36) NOT NULL,
  `subject` varchar(512) DEFAULT NULL,
  `sender` varchar(512) DEFAULT NULL,
  `content` text NOT NULL,
  `is_phishing` enum('genuine','phishing','unsure') NOT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `phishing_challenges`
--

INSERT INTO `phishing_challenges` (`id`, `subject`, `sender`, `content`, `is_phishing`, `timestamp`) VALUES
('084d88c8-d4a8-46a9-9d03-35f34997af4d', 'Congratulations you are a winner!', 'principal3897@abc_high_school.com', '<p>Dear Student,</p> <p>I am pleased to inform you that due to your excellent high scores in your subjects, you have won a $1000 HKD voucher and a chance to enter the schools lucky draw.</p> <p>In the lucky draw all participants have the chance to win computers, electronic devices and many more...</p> <p>However you only have until Monday to download the attachment pdf form, complete and return the school office.</p> <p>If there are any issues completing the form please contact us using the link below.</p> <p>Regards, Ms. Honey.<br>Principal.<br> ABC High School.<br> Tel:+852 10101010.<br> http://www.abc_highschool.com</p>', 'phishing', '2023-08-16 13:23:27'),
('1b59784d-aaf4-4385-bede-159d6d45152a', 'Reactivate account', 'schoolsecurity96389@info_seek.com', '<p>Dear User, we have detected unusual activity on your school account. As a security measure, your account has been temporarily locked.</p> <p>To verify your identity and regain access to your account, please click the link https://www.letmein27834.com/verify.</p> <p>If you did not request this security check, please ignore this email. Best Regards, School Security Team.</p>', 'phishing', '2023-08-16 13:23:27'),
('2266ffaa-13d2-4ad2-a573-d12d0b5c41fb', 'Print Credit Balance', 'noreply@abchighschoolaccountdepartment.edu.com', '<p>Dear Student (Account No. 117263894),</p> <p>Please be aware that your avaliable balance for printing credit is now $0 HKD.</p> <p>Please top up your balance using the link below or visiting the General Office to update your funds so that you have printing availability in School. If there is an error on your account please visit the school accounts department.</p> <p>This is a system generated message and do not reply to this email.</p>', 'genuine', '2023-08-16 22:40:30'),
('3852741c-9bc1-4c5d-a670-71059ed5dbc2', 'Hope for the future', 'Smith, James <jamessmith2023@email.com>', '<p>You were referred to us with other selected students for a financial grant as an asipring academic student to further your studies.</p> <p>students were chosen based on criteria and information off the school. A student will be given $6000 each.</p> <p>all stduents are to send text to the treasurer on +8521029293 for further information and collection.</p> <p>Regards, James.</p>', 'phishing', '2023-08-16 22:40:30'),
('53f590ea-a406-4adb-9cef-5e2f1e915290', 'Overdue book loan', 'noreply@schoollibraryteam.org', '<p>Dear Student,</p> your book loan has been overdue.</p> <p>Please update your book loan status by clicking the link or you will incur an additional fine.</p> <p>Regards, School Library Team.</p>', 'phishing', '2023-08-16 22:40:30'),
('75542f20-1cb7-4f92-a264-d0fb3d2307d4', 'Outstanding achievement', 'principal@abchighschool.edu.com', '<p>I am pleased to inform you that due to your excellent high attainment grades across all your school subjects, you have been awarded a $250 HKD book coupon.</p> <p>Your continued effort and performance has not gone unnoticed by your teachers and to support your learning further please go to the General Office from next Monday onwards to find out more regarding the prize. <p>Well done and keep up the great work!</p> <p>Best regards,</p> <p>Ms. Honey.<br> Principal.<br> ABC High School.<br> Tel: +852 10101010.<br> https://www.abchighschool.com.</p>', 'genuine', '2023-08-16 13:23:27');
```

## Testing
Tests can be run using the following commands
```
pytest
```

