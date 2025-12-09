☁️ Serverless Event Pipeline: S3 to External Services
🌟 Overview
This project implements a reliable, serverless, event-driven architecture on Amazon Web Services (AWS) to process file uploads to an S3 bucket and distribute a clean notification to downstream subscribers via an SNS Topic.

The core of the architecture is the Amazon EventBridge Pipe, which connects an SQS queue (acting as a durable buffer) to an SNS Topic (acting as a fan-out mechanism). This approach ensures durability, decoupling, and scalability for file processing notifications.

🏗️ Architecture
The pipeline consists of four primary AWS services linked together: S3 $\rightarrow$ SQS $\rightarrow$ EventBridge Pipe $\rightarrow$ SNS.ServiceRole in Pipeline


🛠️ Deployment and Configuration 

Prerequisites
AWS CLI configured with necessary permissions. 
An existing S3 Bucket for image uploads.
IAM roles configured for the EventBridge Pipe to read from SQS and publish to SNS.

Step-by-Step SetupCreate SQS Queue: 
Create a Standard SQS queue (e.g., s3-upload-events-queue).

Create SNS Topic: Create a Standard SNS Topic (e.g., upload-notifications-topic). 

Subscribe your desired endpoints (e.g., email, Lambda) to this topic.

Configure S3 Event Notifications:

In the S3 Console for your bucket, go to Properties $\rightarrow$ Event Notifications.Set the Destination to the SQS queue created in Step 1.

Set the Events to s3:ObjectCreated:*.

Create EventBridge Pipe:Source: 

Select the SQS queue (s3-upload-events-queue).

Target: Select the SNS Topic (upload-notifications-topic).

Input Transformer: Configure the Input Transformer to clean the SQS message body (as detailed below).