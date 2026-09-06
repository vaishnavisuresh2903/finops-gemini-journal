# FinOps Gemini Journal

## Cloud Waste Auditor and Smart Savings Planner

FinOps Gemini Journal is a secure, AI-powered cloud cost optimization application that combines conversational AI with personal FinOps tracking.

The application allows authenticated users to discuss their cloud spending with Google Gemini, identify potential cloud waste, generate prioritized optimization recommendations, and save AI-generated summaries to their personal FinOps journal.

The application is designed around secure application development principles, including Firebase Authentication, user-isolated Cloud Firestore storage, Google Cloud Secret Manager, and Cloud Run deployment.



## 1. Project Overview

Cloud environments can become expensive when resources are oversized, idle, underutilized, or no longer required.

FinOps Gemini Journal provides a conversational interface that helps users analyze their cloud spending without requiring them to manually interpret large amounts of cost information.

Users can provide information such as:

- Monthly cloud spending
- Service-level costs
- Compute resource usage
- Storage costs
- Database costs
- Unexpected billing increases
- Resource utilization information

Gemini analyzes the information and provides recommendations for reducing unnecessary cloud expenditure.



## 2. Core Features

### Firebase Authentication

Users sign in using Firebase Authentication before accessing the application.

Each authenticated user has an isolated application experience.

Authentication is used to establish the user's identity and control access to personal FinOps data.

### Gemini Multi-Turn Conversation

The application provides a conversational interface powered by Google Gemini.

Users can ask follow-up questions without restarting the analysis.

Example conversation:

**User:**

> My cloud spending increased from ₹18,000 to ₹25,000 this month. What should I investigate?

**Gemini:**

> The increase should first be investigated across compute, database, and storage services. Start by identifying resources with significant usage or cost changes.

**User:**

> Create a prioritized savings plan.

**Gemini:**

> Priority 1: Review idle compute resources.  
> Priority 2: Analyze database sizing.  
> Priority 3: Review unused storage.

### Cloud Waste Auditor

The Cloud Waste Auditor analyzes user-provided cloud cost and resource information.

It looks for potential optimization opportunities such as:

- Idle resources
- Underutilized compute resources
- Oversized resources
- Unexpected cost increases
- Unused storage
- High-cost services
- Recurring unnecessary expenditure

The auditor provides recommendations rather than making destructive changes to cloud resources.

### Smart Savings Planner

The Smart Savings Planner converts the audit into an actionable plan.

Each recommendation can contain:

- Problem
- Priority
- Recommended action
- Expected impact
- Next step

Example:

| Priority | Area | Recommendation | Expected Impact |
|---|---|---|---|
| High | Compute | Review idle VM resources | High |
| Medium | Database | Review database sizing | Medium |
| Medium | Storage | Remove unnecessary stored data | Medium |
| Low | Monitoring | Review recurring cost increases | Low |

### Personal FinOps Journal

The application automatically stores relevant conversations and AI-generated summaries in Cloud Firestore.

Users can return to previous analyses and review their recommendations.

### User-Isolated Data

Each user's journal records are associated with their authenticated Firebase user ID.

The application is designed so that one user cannot access another user's FinOps journal.

### Secure Secret Management

Sensitive credentials are not stored directly in the source code.

Google Cloud Secret Manager is used to securely manage application secrets and API credentials.

### Cloud Run Deployment

The application is containerized and deployed to Google Cloud Run.

Cloud Run provides the production hosting environment for the application.



## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web application interface |
| Google Gemini | Conversational AI and FinOps analysis |
| Firebase Authentication | User authentication |
| Cloud Firestore | Persistent user-specific journal storage |
| Google Cloud Secret Manager | Secure secret management |
| Docker | Application containerization |
| Google Cloud Run | Application deployment |
| Artifact Registry | Container image storage |



## 4. Application Architecture

```text
                         User
                           |
                           v
                  Firebase Authentication
                           |
                           v
                 FinOps Gemini Journal
                           |
              +------------+------------+
              |                         |
              v                         v
       FinOps Conversation       Personal Journal
              |                         |
              v                         v
         Google Gemini            Cloud Firestore
              |
              v
      Cloud Waste Auditor
              |
              v
      Smart Savings Planner


Sensitive Credentials
        |
        v
Google Cloud Secret Manager


Application Container
        |
        v
Google Cloud Run
```



## 5. Application Flow

```text
1. User opens the application
2. User authenticates using Firebase
3. Application establishes the authenticated user session
4. User enters cloud spending information
5. Gemini analyzes the information
6. Cloud Waste Auditor identifies optimization opportunities
7. Smart Savings Planner creates prioritized recommendations
8. Gemini conversation and summary are saved to Firestore
9. User can return to the personal FinOps journal
```



## 6. Example FinOps Analysis

### Example Input

```text
Monthly cloud spending: ₹24,500

Compute Engine: ₹12,000
Cloud Storage: ₹5,000
Cloud SQL: ₹5,500
Other services: ₹2,000
```

The application sends the information to Gemini for analysis.

A simplified prompt can be structured as:

```python
prompt = f"""
You are a FinOps cloud cost optimization assistant.

Analyze the following cloud spending information:

{cost_data}

Identify:
1. Potential cost waste
2. High-cost areas
3. Possible optimization opportunities
4. Priority of each recommendation
5. Suggested next actions

Do not recommend destructive actions.
Return practical and actionable recommendations.
"""
```

Gemini can then return structured recommendations such as:

### Cloud Waste Audit

**High Priority**

Review Compute Engine resources for idle or underutilized instances.

**Medium Priority**

Review Cloud SQL sizing and utilization.

**Medium Priority**

Analyze Cloud Storage for unused or unnecessary data.

**Recommended Next Step**

Begin with Compute Engine because it represents the largest portion of the reported cloud expenditure.



## 7. Gemini Integration

A simplified Gemini integration can be implemented using the Google Gen AI SDK.

Example:

```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

answer = response.text
```

The production application should obtain credentials through the configured Google Cloud security mechanism rather than placing sensitive credentials directly in the source code.



## 8. Firestore Data Model

A user-isolated Firestore structure can follow this pattern:

```text
users/
    {user_id}/
        journal/
            {entry_id}
                title
                summary
                conversation
                created_at
                recommendations
```

Example document:

```json
{
  "title": "September Cloud Cost Audit",
  "summary": "Compute resources represent the largest optimization opportunity.",
  "recommendations": [
    "Review idle compute resources",
    "Analyze database sizing",
    "Review unused storage"
  ],
  "created_at": "timestamp"
}
```

The authenticated Firebase user ID is used to associate journal records with the correct user.



## 9. Firestore Security

Firestore security rules should enforce user-level isolation.

Example:

```text
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {

    match /users/{userId}/journal/{entryId} {

      allow read, write:
        if request.auth != null
        && request.auth.uid == userId;
    }
  }
}
```

This ensures that an authenticated user can access only the journal records associated with their own Firebase UID.



## 10. Secret Management

Secrets must not be stored directly in source code.

Avoid:

```python
API_KEY = "my-secret-api-key"
```

Instead, the application should retrieve sensitive credentials through Google Cloud Secret Manager or the appropriate runtime authentication mechanism.

Example concept:

```python
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()

secret_name = (
    "projects/PROJECT_ID/secrets/GEMINI_API_KEY/versions/latest"
)

response = client.access_secret_version(
    request={"name": secret_name}
)

api_key = response.payload.data.decode("UTF-8")
```

The secret itself should never be committed to GitHub.



## 11. Firebase Authentication Example

A simplified authentication flow can be represented as:

```python
def authenticate_user(email, password):
    # Firebase authentication logic
    # Validate credentials
    # Return authenticated user information
    pass
```

After successful authentication, the application should use the authenticated user's UID when accessing Firestore.

```python
user_id = authenticated_user.uid
```

The UID is then used to access:

```text
users/{user_id}/journal/
```



## 12. Streamlit Application Structure

A typical Streamlit application can be structured as:

```python
import streamlit as st

st.set_page_config(
    page_title="FinOps Gemini Journal",
    layout="wide"
)

st.title("FinOps Gemini Journal")
st.subheader("Cloud Waste Auditor and Smart Savings Planner")

user_input = st.text_area(
    "Enter your cloud spending information"
)

if st.button("Analyze Cloud Costs"):

    if user_input:

        # Send user input to Gemini
        # Generate FinOps analysis
        # Display recommendations
        # Save summary to Firestore

        st.success("FinOps analysis generated.")
```

The actual application can extend this structure with authentication, conversation history, Firestore persistence, and secure secret retrieval.



## 13. Docker Configuration

Example Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8080"]
```

The container can then be deployed to Google Cloud Run.



## 14. Requirements

Example `requirements.txt`:

```text
streamlit
google-genai
google-cloud-firestore
google-cloud-secret-manager
firebase-admin
```

The exact dependency versions should match the working application.



## 15. Project Structure

```text
finops-gemini-journal/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── README.md
│
├── firebase/
│   └── firebase_config.py
│
├── services/
│   ├── gemini_service.py
│   ├── firestore_service.py
│   └── secret_manager.py
│
└── assets/
    └── screenshots/
```

The final structure should reflect the actual files used by the deployed application.



## 16. Security Considerations

Security is a fundamental part of this project.

The application follows these principles:

- Firebase Authentication is used for user identity.
- Firestore records are isolated by authenticated user ID.
- Firestore Security Rules enforce access boundaries.
- API credentials are not hardcoded.
- Google Cloud Secret Manager is used for sensitive credentials.
- Secrets are excluded from Git using `.gitignore`.
- The application does not expose credentials to the browser.
- The application runs on Google Cloud Run.
- The AI assistant provides recommendations and does not automatically perform destructive cloud operations.



## 17. .gitignore

Sensitive and temporary files should be excluded from source control.

Example:

```text
.env
.env.*
*.key
*.pem
service-account.json
*-service-account.json
__pycache__/
*.pyc
.venv/
venv/
.streamlit/secrets.toml
.DS_Store
```

Never commit:

- API keys
- Passwords
- Firebase private keys
- Service account JSON files
- Cloud credentials
- Environment secrets



## 18. Deployment

The application is designed to run as a containerized Streamlit application on Google Cloud Run.

High-level deployment flow:

```text
Source Code
    |
    v
Docker Build
    |
    v
Container Image
    |
    v
Artifact Registry
    |
    v
Cloud Run
    |
    v
Public Application
```

Cloud Run provides the production runtime for the application.



## 19. Original Innovation

The base challenge provides the Personal Gemini Journal concept.

This project extends that concept with two original FinOps capabilities.

### Cloud Waste Auditor

The Cloud Waste Auditor uses Gemini to analyze cloud spending information and identify potential areas of waste.

It converts raw cost information into understandable optimization insights.

### Smart Savings Planner

The Smart Savings Planner converts the audit into a prioritized action plan.

Instead of simply explaining cloud costs, the application answers:

```text
What is costing me money?
        |
        v
Where might waste exist?
        |
        v
What should I investigate first?
        |
        v
What action should I take?
```

This makes the journal actionable rather than simply storing conversations.



## 20. Example User Journey

```text
Login
  |
  v
FinOps Dashboard
  |
  v
Enter Cloud Cost Information
  |
  v
Ask Gemini
  |
  v
Cloud Waste Audit
  |
  v
Savings Recommendations
  |
  v
Generate Smart Savings Plan
  |
  v
Save Summary
  |
  v
Personal FinOps Journal
```



## 21. Future Enhancements

Potential future enhancements include:

- Direct Google Cloud Billing export integration
- Automated cost trend analysis
- Budget threshold alerts
- Historical spending dashboards
- Cost anomaly detection
- Service-level cost comparisons
- Monthly FinOps reports
- Estimated savings tracking
- CSV billing data upload
- Resource utilization analysis
- Automated recommendation prioritization


## 22. Project Goals

The project aims to demonstrate how generative AI and Google Cloud services can be combined to create a secure, personalized, and practical cloud operations application.

The main goals are:

- Provide secure authenticated AI interactions.
- Maintain isolated personal FinOps data.
- Use Gemini for conversational cloud cost analysis.
- Identify potential cloud waste.
- Generate actionable savings plans.
- Persist useful AI-generated summaries.
- Protect sensitive credentials.
- Deploy the application using Cloud Run.



## 23. Technologies and Google Cloud Services

The project demonstrates the use of:

- Google Gemini
- Firebase Authentication
- Cloud Firestore
- Google Cloud Secret Manager
- Google Cloud Run
- Artifact Registry
- Docker
- Python
- Streamlit



## 24. Conclusion

FinOps Gemini Journal combines conversational AI, personal journaling, and cloud cost optimization into a single application.

Instead of simply showing cloud costs, the application helps users understand where their spending may be inefficient and provides a prioritized plan for further investigation and optimization.

The project demonstrates secure authentication, user-isolated data storage, AI-powered multi-turn interaction, secure credential management, and production deployment on Google Cloud Run.
