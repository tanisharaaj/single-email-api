from datetime import timedelta
from temporalio import workflow

@workflow.defn
class NotifyMemberWorkflow:
    @workflow.run
    async def run(self, member: dict) -> str:
        # Call by string name, do NOT import activities
        await workflow.execute_activity(
            "send_email_activity",
            member,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return f"sent:{member.get('member_id')}"
