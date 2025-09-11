import asyncio
from temporalio.worker import Worker
from temporalio.client import Client

from app.settings import settings
from app.workflows import NotifyMemberWorkflow
from app.activities import send_email_activity



print("send_email_activity:", send_email_activity)
print("is decorated?:", hasattr(send_email_activity, "__temporal_activity__"))


async def main():
    client = await Client.connect(
        "us-east-1.aws.api.temporal.io:7233",
        namespace=settings.TEMPORAL_NAMESPACE,
        api_key=settings.TEMPORAL_API_KEY,
        tls=True,
    )

    worker = Worker(
        client,
        task_queue=settings.TEMPORAL_TASK_QUEUE,
        workflows=[NotifyMemberWorkflow],
        activities=[send_email_activity],  # map name → fn
    )

    print("Worker started. Listening for tasks...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
