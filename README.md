# Serverless S3 Event Distributor
---
## Project Overview
This project implements a reliable, serverless, event-driven architecture on AWS to process file uploads to an S3 bucket and distribute a clean notification to downstream subscribers via an SNS Topic.

The core of the architecture is the **Amazon EventBridge Pipe**, which connects an SQS queue (acting as a durable buffer) to an SNS Topic. This approach ensures **durability**, **decoupling**, and **scalability** for file processing notifications.

---
## Project Architecture
The pipeline consists of four primary AWS services linked together: 
**S3 $\rightarrow$ SQS $\rightarrow$ EventBridge Pipe $\rightarrow$ SNS.** 

![Serverless-S3-Event-Distributor](Architecture/Serverless%20S3%20Event%20Distributor%20Architecture.png)

### Architecture Flow

1. **Event Source: Amazon S3 Bucket**
- Component: S3 Bucket (image-moderation-project-bucket)
- Role: Initiation Point
- Action: Triggers an s3:ObjectCreated:Put event.
- Output: Sends the raw, verbose S3 event JSON payload.

2. **Durable Buffer: Amazon SQS Queue**
- Component: SQS Queue (s3-upload-events-queue)
- Role: Decoupling and Durability
- Action: Receives the raw S3 event and holds it.
- Input for Next Step: The SQS message is the source data polled by the Pipe.

3. **Core Processor: Amazon EventBridge Pipe**
This component handles the critical tasks of **polling, transformation, and routing.**

- Component: EventBridge Pipe (Your configured pipe name)
- Role: Polling, Transformation, and Routing
- Action 1 (Polling): Continuously reads (polls) the SQS queue.
- Action 2 (Transformation): Executes the Input Transformer to clean the data:
   1) Input: Full SQS message with the wrapped S3 event.
   2) Output: Clean JSON payload containing only imageName and uploadTimestamp.
- Action 3 (Routing): Successfully processed messages are deleted from SQS and delivered to the target.

4. **Final Target: Amazon SNS Topic**

- Component: SNS Topic (upload-notifications-topic)
- Role: Fan-out Delivery
- Action: Receives the clean JSON payload from the Pipe.
- Output: Instantly publishes and distributes the clean event to all subscribed endpoints (e.g., email, Lambda, HTTP).

---
## Deployment and Configuration 

### Prerequisites
- An existing S3 Bucket for image uploads.
- IAM roles configured for the EventBridge Pipe to read from SQS and publish to SNS.

### Implementation steps:

1) **Create SQS Queue**: Create a Standard SQS queue (e.g., s3-upload-events-queue).

2) **Create SNS Topic**: Create a Standard SNS Topic (e.g., upload-notifications-topic).Subscribe your desired endpoints (e.g., email) to this topic.

3) **Configure S3 Event Notifications**: 

- In the S3 Console for your bucket, go to Properties $\rightarrow$ Event Notifications.
- Set the Destination to the SQS queue created in Step 1.
- Set the Events to s3:ObjectCreated:*.
4) **Create EventBridge Pipe**: 
- **Source**: Select the SQS queue (s3-upload-events-queue).

- **Target**: Select the SNS Topic (upload-notifications-topic).

- **Input Transformer**: Configure the Input Transformer to clean the SQS message body.

---

## 🚦 Monitoring and Alarms (CloudWatch)

Critical alarms have been configured using **Amazon CloudWatch** to ensure the pipeline's health and prevent message loss or backlogs.

1. **SQS Queue** (Source Monitoring):
We monitor the (**ApproximateAgeOfOldestMessage**) metric. An alarm is set to trigger when the **Maximum** age exceeds **60 seconds** for three consecutive periods. This alert is critical for detecting a message backlog, indicating that the EventBridge Pipe is either failing or is unable to poll the queue fast enough to keep up with the incoming S3 events.

2. **EventBridge Pipe** (Core Monitoring):
We monitor the (**TargetFailures**) metric, which tracks any failure to deliver a message to the SNS target. An alarm is set to trigger immediately if the **Sum** of failures is **greater than 0** for even a single period. This ensures that any permissions issue or configuration problem preventing successful routing is caught immediately.

3. **SNS Topic** (Target Monitoring):
We monitor the (**NumberOfNotificationsFailed**) metric. This tracks the final stage of delivery—whether the SNS topic is successfully fanning out messages to its own subscribers (e.g., failed HTTP endpoints). An alert is triggered when the **Sum** of failures exceeds 5 over a five-minute period, allowing for a few transient errors while still ensuring reliable final delivery.

---

## 🚀 Future Enhancements
To make the pipeline more efficient, smarter, and resilient you can make some changes in future.

1. **Data Filtering and Efficiency**: Reduce costs and downstream processing load by filtering out non-essential S3 events.

- Mechanism: Implement a JSONPath filter on the Pipe's Source stage to check for specific file extensions (e.g., only .png or .jpg) or file size thresholds.

2. **Message Enrichment and Business Logic**: Look up external metadata (e.g., file owner, project ID) before sending the final notification.

- Mechanism: Insert an AWS Lambda function into the Enrichment stage of the EventBridge Pipe. The Lambda will perform the lookup and return an enhanced JSON object.

3. **Error Handling and Resilience (DLQ)**: Prevent message loss due to repeated target failures.

- Mechanism: Configure a Dead-Letter Queue (DLQ) on the Source SQS Queue. Messages that fail to be processed by the Pipe after a set number of retries (maxReceiveCount) will be shunted to the DLQ for manual inspection.

---