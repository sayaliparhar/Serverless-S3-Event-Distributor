# Serverless S3 Event Distributor

A cloud-native, event-driven automation tool that processes S3 bucket metadata in real-time and alerts subscribers via Amazon SNS.

---
## Project Overview
This project demonstrates a serverless workflow where file uploads to an **Amazon S3** bucket act as a trigger. An **AWS Lambda** function (Python) intercepts the event, extracts critical metadata (Filename, Bucket Name, File Size), and publishes a formatted alert to an **Amazon SNS** topic for instant notification.

This project shows how to build a lightweight automation pipeline without servers.

---

## 🛠️ AWS Services Used

- **Cloud**: AWS (S3, Lambda, SNS, IAM, CloudWatch)

- **Language**: Python 3.x (Boto3 SDK)

---
## Architecture

1. **S3 Bucket**: Acts as the event source (ObjectCreated)

2. **IAM Role**: Provides the Lambda function with **"Least Privilege"** permissions (sns:Publish and logs:CreateLogGroup).

3. **AWS Lambda**: The compute layer that parses the JSON event sent by S3.

4. **Amazon SNS**: The distribution layer that sends emails to subscribed users.

5. **CloudWatch**: Used for real-time monitoring and debugging.

![Serverless-S3-Event-Distributor](Architecture/Serverless-S3-Event-Distributor.png)

---

## Prerequisites
- AWS Account

- Verified email address in Amazon SNS
---

## 🛠️ Step-by-Step Implementation

### 1. Messaging Layer (SNS)
* Create an SNS Standard Topic named `s3-upload-notify-topic`.
* Create an Email Subscription and confirm it via the verification link sent to your inbox.

<p align="center">
  <img width="750" alt="SNS-Topic" src="TestCases/SNS-Topic.png" />
</p>

### 2. Security & Permissions (IAM)
* Create an IAM Execution Role for Lambda.
* Attach the `AWSLambdaBasicExecutionRole` policy for CloudWatch Logs.
* Add an inline policy to allow `sns:Publish` specifically for your Topic ARN.

  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "YOUR-SNS-TOPIC-ARN"
        }
    ]
  }
  ```
<p align="center">
  <img width="750" alt="IAM Role and Permissions" src="TestCases/IAM Role and Permissions.png" />
</p>

### 3. Compute Layer (Lambda)

* Create a Python 3.x Lambda function.
* Paste the provided `lambda_function.py` code.


<p align="center">
  <img width="750" alt="Lambda Creation" src="TestCases/Lambda Creation.png" />
</p>

### 4. Storage Trigger (S3)
* In your S3 bucket properties, create a new **Event Notification**.
* Set the Event type to `All object create events`.
* Select your Lambda function as the destination.


<p align="center">
  <img width="750" alt="S3-Event-notification creation" src="TestCases/S3-Event notification creation.png" />
</p>

---

## 🧪 Testing
1. Upload a file to the configured S3 bucket.


<p align="center">
  <img width="750" alt="S3-Bucket-Image-Upload" src="TestCases/S3-bucket -Image-upload.png" />
</p>

2. The Lambda will trigger automatically.

3. Check your email for a message like:

<p align="center">
  <img width="750" alt="Email Message Notification" src="TestCases/Email message notification.png" />
</p>

---

## 📊 Observability & Monitoring
* **Structured Logging:** Centralized application logs in **CloudWatch Logs** with a 14-day retention policy for cost optimization.


<p align="center">
  <img width="750" alt="Cloudwatch Lambda logs" src="TestCases/Cloudwatch%20Lambda%20logs.png" />
</p>

* **Proactive Alerting:** Configured **CloudWatch Alarms** to trigger SNS notifications if Lambda execution errors exceed a 0% threshold.


<p align="center">
  <img width="750" alt="Proactive Alarm for Error handling" src="TestCases/Proactive Alarm for Error handling.png" />
</p>

---

## 🧠 Key Learnings
1. **Event-Driven Logic**: Learned how to make AWS services "talk" to each other automatically without manual intervention.

2. **Serverless Benefits**: Understood how to build tools that cost ₹0 when not in use and scale instantly when files are uploaded.

3. **Security (IAM)**: Learned to give a service the minimum power it needs to work (Least Privilege), keeping the cloud account safe.

4. **Monitoring**: Used CloudWatch to "see" inside the code and fix errors quickly using logs.

---

## 🚀 Future Enhancements
1. **IaC (Terraform)**: Automate the entire setup so it can be deployed in seconds with one command.

2. **Dead Letter Queue (DLQ)**: Add a "safety net" (SQS) to catch and save any failed notifications for later review.

3. **Database Integration**: Instead of just an email, save the file details into a DynamoDB table for a permanent record.

4. **Image Security**: Use AWS Rekognition to automatically check if an uploaded image is safe or contains specific objects.

---