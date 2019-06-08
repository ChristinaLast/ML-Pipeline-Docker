# Deploying Python application using Docker and AWS

The use of Docker in conjunction with AWS can be highly effective when it comes to building a data pipeline.

Let me ask you if you have ever had this situation before. You are building a model in Python which you need to send over to a third-party, e.g. a client, colleague, etc. However, the person on the other end cannot run the code! Maybe they don't have the right libraries installed, or their system is not configured correctly.

Whatever the reason, Docker alleviates this situation by storing the necessary components in an image, which can then be used by a third-party to deploy an application effectively.

In this example, we will see how a simple Python script can be 
