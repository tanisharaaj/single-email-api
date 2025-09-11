from uuid import uuid4
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from temporalio.client import Client

from app.settings import settings
from app.models import NotifyRequest, NotifyResponse
from app.workflows import NotifyMemberWorkflow
from app.auth import require_auth

app = FastAPI(
    title="Member Email API",
    swagger_ui_parameters={"persistAuthorization": True},
)

security = HTTPBearer()


@app.on_event("startup")
async def startup_event():
    app.state.temporal = await Client.connect(
        "us-east-1.aws.api.temporal.io:7233",
        namespace=settings.TEMPORAL_NAMESPACE,
        api_key=settings.TEMPORAL_API_KEY,
        tls=True,
    )


@app.post("/notify", response_model=NotifyResponse)
async def notify(
    req: NotifyRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    require_auth(credentials)

    member = req.member.dict()
    workflow_id = f"notify-{member['member_id']}-{uuid4().hex}"

    handle = await app.state.temporal.start_workflow(
        NotifyMemberWorkflow.run,
        member,
        id=workflow_id,
        task_queue=settings.TEMPORAL_TASK_QUEUE,
    )

    return NotifyResponse(
        status="queued",
        run_id=handle.run_id,
        message="Workflow started",
    )
