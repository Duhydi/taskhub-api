import time

from fastapi import Request


async def logging_middleware(
    request: Request,
    call_next,
):
    start = time.time()

    response = await call_next(request)

    process_time = time.time() - start

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{process_time:.4f}s"
    )

    return response