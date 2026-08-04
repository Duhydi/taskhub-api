import asyncio


async def send_assign_email(
    email: str,
    title: str,
):
    await asyncio.sleep(2)

    print(
        "\n=========================="
    )
    print("Email Notification")
    print(f"To: {email}")
    print(f"Task: {title}")
    print("==========================\n")