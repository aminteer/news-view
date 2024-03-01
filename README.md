# NewsView Technical Design Document

## 1. Background

### 1.1 Product Purpose

In today’s fast-paced world, staying updated with the latest business news can be a daunting task for many. The traditional means of consuming news are often seen as time-consuming and dull, creating a gap for individuals who wish to stay informed but are short on time and prefer engaging content. **NewsView** is developed with the aim to bridge this gap by offering a unique, efficient, and enjoyable news consumption experience. The application is designed specifically for those who seek a quick overview of the day’s top stories in a format that is both captivating and straightforward. Unlike traditional news apps, NewsView summarizes the essence of top business news into a single, AI-generated image that captures the day’s highlights in a visually appealing manner. This novel approach not only makes staying informed a fun and less tedious task but also provides an excellent opportunity for ad placements, thereby creating a sustainable revenue model. NewsView is tailored to attract users with its simplicity and the innovative presentation of news, ensuring they can catch up with the world in a glance and still feel connected in conversations about current events.

![NewsView application](./project_overview_assets/NewsViewScreenShot.png?raw=true "NewsView application")

### 1.2 Description of Product Features

- **Summarized Top Stories:** NewsView distills complex news stories into an easy-to-digest summary, allowing users to grasp the day’s most important events quickly.
- **AI-Generated Images:** Leveraging advanced AI, the app transforms text summaries into a single compelling, fun image that encapsulates the essence of the news, adding a layer of engagement through visual storytelling.
- **Interactive Comment Section:** Users are not just passive consumers of news; they can actively engage by sharing their thoughts and opinions through a built-in comment feature, enhancing the communal aspect of the application.
- **Analytics and Graphs:** Beyond news consumption, NewsView offers analytical insights through interactive graphs, allowing users to delve deeper into news trends and metrics, thereby enriching the user experience with educational content.

## 2. High Level Design

![NewsView high level architecture](./project_overview_assets/SoftArchClassFinalArchitecture.png?raw=true "NewsView high level architecture")

### 2.1 Loosely Coupled Design Philosophy

The architectural philosophy behind NewsView prioritizes a loosely coupled system, which ensures that its various components can be developed, updated, and scaled independently of each other. This design principle is key to achieving a robust and flexible application that can quickly adapt to new technologies and increased user demands without extensive rework.

### 2.2 Major Components Overview

1. **Web Frontend UI:** Designed to be intuitive and responsive, the frontend serves as the face of NewsView, offering a simple and seamless user experience across different devices and platforms.
2. **Data Collection Engine:** An automated system tasked with gathering the latest top news stories from a variety of reputable sources, ensuring the content is fresh and relevant.
3. **Data Analysis Module:** This component analyzes the collected news data to identify trends and insights, which are essential for the summarization process and for providing users with analytical content.
4. **Data Storage Solutions:** A combination of SQL databases and cloud storage (S3 buckets) is used to efficiently store and manage the text and image data generated and collected by the application.
5. **API Gateways:** Serve as the intermediary between the controllers and the AI service providers, facilitating smooth data flow and integration of services like LLM APIs for text summarization and image generation APIs for visual content creation.
6. **Image Generation APIs:** Leverages a generative AI service to convert text summaries into engaging visual representations of news stories.
7. **Logging and Monitoring/Metrics Systems:** Essential for maintaining the health of the application, these systems track operations, user activities, and system performance to identify and resolve issues promptly.
8. **Message Queue:** Acts as a backbone for asynchronous communication between services, enhancing the application’s efficiency and scalability by managing the flow of data and tasks.

## 3. Technical Considerations

### 3.1 Web Application

- **Development Frameworks:** Utilizing Flask for its simplicity and versatility, with Dash for adding interactive elements, such as analytics and graphs, to the web interface.  The application was developed in Python.
- **Key Features:**
  - **News Summaries and Images:** Automatically updated daily to reflect the latest news, ensuring content is always fresh and engaging. Top stories are collected on a scheduled basis.  The stories are sent as a message in the message queue.  The listening component kicks off the transformation and image generation steps when a new message is received.  The results are then stored and refreshed in the Web interface.
  - **User Comments:** A feature enabling users to interact with the news and each other, adding a social dimension to the app.
  - **Interactive Analytics:** Provides users with deeper insights into news trends, enhancing the informational value of NewsView.

### 3.2 Data Collection & Storage

- **Comprehensive Storage Strategy:** Incorporating both SQL databases for structured data and S3 buckets for unstructured data like images and AI-generated summaries, ensuring robust and scalable data management. All top news stories are stored and persisted in a SQL database for later analysis.  Generated images and the simplified news summary are also stored.

### 3.3 Data Analysis & Insights

- **Analytics:** Employing data analysis techniques to offer users valuable insights into news patterns and metrics.  These are displayed through an interactive Dash graph interface.

### 3.4 REST collaboration 

- **REST interfaces:** REST route points were created to facilitate handling of data ingestion and basic health checks.

### 3.5 Event collaboration messaging 

- **Message Queues:** Message queue was created to communicate a new batch of top stories from the data collection scheduled job to the transformation and summary generation process. RabittMQ was used for local testing and the hosted RabittMQ provided by CloudAMQP on Heroku is used for production messaging.  Connections are switched between local development environments and production environments through use of environment variables.

### 3.6 Testing & Quality Assurance

- **Unit and Integration Testing:** Both unit testing and integration testing methodologies are applied, focusing on key components like API gateways to ensure reliability and robust integration across the application. Unit tests were created for key functionality. Integration tests created to test the transformation and storage process.  Mock test objects were used to test gateway functions.

### 3.7 Product environment 

- **Environments:** Heroku used for deployment and production environment.  Local virtual environment used for testing and development. Environmental variables were set up to hold secrets and key variables that change between local dev and remote production environments.

### Key links
- **GitHub repository:** [NewsView code base](https://github.com/aminteer/usbsoftarch_final) https://github.com/aminteer/usbsoftarch_final
- **NewsView production app:** [NewsView](https://ucb-softarch-final-a2c796b0db0f.herokuapp.com/) https://ucb-softarch-final-a2c796b0db0f.herokuapp.com/
- Note: API keys are needed for the associated APIs - News API and OpenAI, also for AppSignal for the code to function correctly.  These keys are not stored in the public repo.

## 4 Deployment & Operations

- **Cloud-based Deployment:** Leveraging Heroku for its ease of use and scalability, ensuring NewsView is always available to its users.
- **Continuous Integration:** Utilizing GitHub Actions for a streamlined development lifecycle, enabling rapid updates and ensuring the application remains at the forefront of innovation. CI is supported through Git code versioning and GitHub actions to trigger the build on merge to main.
- **Continuous Delivery:** 
Continuous delivery is supported through Github actions triggers an automated build and deploy process on Heroku.  Builds are fully automated.  Continuous Deployment is also supported through automated deployment on Heroku.  Once code is merged into the main branch in the remote repository, all integration, builds, and deployments are automated.
- **Production monitoring:** Heroku dashboards are used for production. monitoring and alerting. 
- **Instrumenting:** AppSignal was setup to monitor operations. AppSignal is similar to a Prometheus and Grafana combination and supports OpenTelemetry.  Span telemetry and customer metrics created and collected. 

## Conclusion

NewsView redefines the experience of staying informed by combining advanced AI with user-centric design principles. Through its innovative use of technology, NewsView offers a refreshing alternative to traditional news consumption, making it not only informative but also enjoyable. As we continue to develop and refine NewsView, our focus remains on delivering an unparalleled user experience that meets the evolving needs of our audience.
