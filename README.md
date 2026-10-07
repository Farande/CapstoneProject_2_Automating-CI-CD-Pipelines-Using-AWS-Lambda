# AWS Resource Automation Tool Using Python and Boto3

## 1. Project Title and Objective

**Project Title:** AWS Resource Automation Tool Using Python and Boto3

**Objective:**
This project is a Python-based command-line application that automates common AWS resource management tasks using **Boto3**, the AWS SDK for Python. Instead of performing operations manually through the AWS Management Console, users can manage **Amazon S3** and **Amazon EC2** resources from a simple CLI menu.

The project demonstrates:

- AWS automation with Python
- Boto3 SDK usage
- IAM permissions and secure credential handling
- Basic cloud resource lifecycle management

### Features

**Amazon S3**
- Create an S3 bucket
- List existing S3 buckets
- Upload files to an S3 bucket

**Amazon EC2**
- Launch an EC2 instance
- List EC2 instances
- Start an EC2 instance (and wait until it reaches the `running` state)
- Stop an EC2 instance
- Terminate an EC2 instance (with confirmation)

---

## 2. AWS Services Used

| Service | Purpose in this project |
|---|---|
| **Amazon S3** | Create buckets, list buckets, upload files |
| **Amazon EC2** | Launch, list, start, stop and terminate instances |
| **AWS IAM** | Controls which actions the application is allowed to perform |
| **AWS CLI** | Configures credentials and region used by Boto3 |

**Other technologies:** Python 3.x, Boto3

---

## 3. Architecture / Workflow

### Architecture

```
                         User
                           |
                           v
                Python CLI Application
                           |
                           v
                         Boto3
                           |
                           v
                       AWS IAM
                           |
                +----------+----------+
                |                     |
                v                     v
           Amazon S3              Amazon EC2
                |                     |
          +-----+-----+        +------+------+
          |     |     |        |      |      |
          v     v     v        v      v      v
       Create Upload List    Launch  Start  Stop
       Bucket  File   Buckets        /      /
                                  Terminate
```

### Workflow

```
Run Application
       |
       v
Create S3 Bucket --> Upload File --> List S3 Buckets
       |
       v
Launch EC2 Instance --> List EC2 Instances
       |
       v
Start EC2 Instance --> Stop EC2 Instance --> Terminate EC2 Instance
```

Each operation can be verified both from the CLI output and from the AWS Management Console.

### Project Structure

```
aws-resource-automation/
│
├── aws_automation.py
├── requirements.txt
├── .gitignore
└── screenshots/
    ├── 01-iam-permissions.png
    ├── 02-running-python-application.png
    ├── 03-s3-bucket.png
    ├── 04-s3-file-upload.png
    ├── 05-s3-list-buckets.png
    ├── 06-ec2-running.png
    └── 07-ec2-information.png
```

---

## 4. Implementation Steps

1. **Set up the environment** – Install Python, the AWS CLI, and create a virtual environment.
2. **Install Boto3** – Install the AWS SDK for Python and save dependencies to `requirements.txt`.
3. **Create an IAM identity** – Create an IAM user or role with the S3 and EC2 permissions listed below.
4. **Configure AWS credentials** – Use `aws configure` so credentials are never hard-coded in the code.
5. **Build the Python CLI** – Write `aws_automation.py` with a menu that calls Boto3 clients for S3 and EC2.
6. **Implement S3 operations** – Create bucket, upload file, list buckets.
7. **Implement EC2 operations** – Launch, list, start (with waiter), stop, and terminate (with confirmation prompt).
8. **Test and verify** – Run each operation and confirm the result in both the CLI output and the AWS Console.
9. **Secure the repository** – Add a `.gitignore` so secrets and unnecessary files are never committed.

### IAM Permissions

**Amazon S3**

```
s3:CreateBucket
s3:ListAllMyBuckets
s3:PutObject
```

**Amazon EC2**

```
ec2:RunInstances
ec2:DescribeInstances
ec2:StartInstances
ec2:StopInstances
ec2:TerminateInstances
```

> For production use, apply a more restrictive **least-privilege** IAM policy instead of granting unnecessary permissions.

---

## 5. Screenshots

### IAM Permissions
![IAM Permissions](Screenshot\01_IAM_Policy_Configuration.png)

### S3 Bucket Created
(!Screenshot\02_S3_Bucket_Creation.png)

### S3 File Upload
![S3 File Upload](Screenshot\03_S3_File_Upload_Terminal.png)

### S3 List Buckets
![S3 List Buckets](Screenshot\04_S3_List_Buckets_Terminal.png)

### EC2 Instance Running
![EC2 Running](Screenshot\08_EC2_Console_Instance_Running.png)

### EC2 Instance Information
![S3 upload Information](Screenshot\07_S3_Console_Upload_Verification.png)

---

## 6. How to Run or Deploy the Project

### Prerequisites

- Python 3.x
- AWS CLI
- An AWS account
- An IAM user or role with the required permissions
- Boto3

Verify installations:

```bash
python --version
aws --version
```

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Farande/aws-resource-automation.git
cd aws-resource-automation
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist yet:

```bash
pip install boto3
pip freeze > requirements.txt
```

### AWS Configuration

```bash
aws configure
```

Example input:

```
AWS Access Key ID: YOUR_ACCESS_KEY
AWS Secret Access Key: YOUR_SECRET_KEY
Default region name: ap-south-1
Default output format: json
```

Verify the configuration:

```bash
aws sts get-caller-identity
```

### Run the Application

```bash
python aws_automation.py
```

Menu:

```
========================================
       AWS RESOURCE AUTOMATION TOOL
========================================

1. Create S3 Bucket
2. Upload File to S3
3. List S3 Buckets
4. Launch EC2 Instance
5. List EC2 Instances
6. Start EC2 Instance
7. Stop EC2 Instance
8. Terminate EC2 Instance
9. Exit

Enter your choice:
```

### Usage Guide

#### Amazon S3

| Option | Action | Input required |
|---|---|---|
| 1 | Create S3 bucket | A globally unique bucket name (e.g. `automated-s3-bucket-2026`) |
| 2 | Upload file to S3 | Bucket name and complete file path (no quotation marks) |
| 3 | List S3 buckets | None |

Example upload:

```
Enter bucket name: automated-s3-bucket-2026
Enter complete file path: C:\Users\Nikhil Farande\Downloads\sample.pdf
```

#### Amazon EC2

| Option | Action | Input required |
|---|---|---|
| 4 | Launch instance | AMI ID, key pair name, security group ID |
| 5 | List instances | None |
| 6 | Start instance | Instance ID (waits until `running`) |
| 7 | Stop instance | Instance ID |
| 8 | Terminate instance | Instance ID and `yes` confirmation |

Example launch:

```
Enter AMI ID: ami-xxxxxxxxxxxxxxxxx
Enter key pair name: MySQL-key
Enter security group ID: sg-xxxxxxxxxxxxxxxxx
```

The AMI ID, key pair, and security group must exist in your AWS account and selected region.

Instance state transitions when stopping:

```
running -> stopping -> stopped
```

> ⚠️ **Warning:** EC2 termination is destructive. A terminated instance cannot normally be restarted.

### Security Best Practices

- Credentials are configured via AWS CLI and **never hard-coded**.
- Never commit AWS access keys, secret keys, `.pem` files, or `.env` files with secrets.
- Follow the principle of least privilege for IAM policies.
- Keep S3 buckets private unless public access is specifically required.
- Use appropriate security group rules for EC2 instances.
- Destructive operations (termination) require confirmation.

Recommended `.gitignore`:

```
venv/
__pycache__/
*.pyc
.env
*.pem
.aws/
```

---

## 7. Key Learnings

- **Boto3 fundamentals:** Using Boto3 clients to automate S3 and EC2 operations programmatically instead of through the console.
- **IAM and least privilege:** Understanding which specific permissions each action requires and why granting only those is safer.
- **Secure credential management:** Using the AWS CLI credential store rather than hard-coding secrets, and keeping sensitive files out of version control.
- **EC2 lifecycle management:** Working with instance states (`running`, `stopping`, `stopped`, `terminated`) and using waiters to wait for a desired state.
- **S3 constraints:** Bucket names are globally unique, and uploads need correct bucket names and file paths.
- **Safe automation:** Adding confirmation prompts for destructive actions such as instance termination.
- **Regional awareness:** AMIs, key pairs, and security groups are region-specific and must exist in the configured region.
- **CLI design in Python:** Building a simple, menu-driven interface that makes cloud operations accessible.

---

## 8. Future Enhancements

- Automatic AMI discovery
- Automatic key pair selection
- Automatic security group selection
- EC2 instance type selection
- EC2 instance tagging
- CloudWatch monitoring

---

## Conclusion

The **AWS Resource Automation Tool** shows how Python and Boto3 can automate everyday AWS tasks. It provides a practical foundation for building more advanced AWS automation and cloud management applications.