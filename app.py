from fastapi import FastAPI
from fastapi import Header, Request
from fastapi.responses import JSONResponse
from utils.redis import get_redis_client
import stripe
import uvicorn

endpoint_secret = "whsec_pEtYE2JqYqMn5gohiIqTuTEKWwixavHl"
app = FastAPI()


@app.post("/webhook")
async def webhook_received(request: Request, stripe_signature: str = Header(None)):
    webhook_secret = endpoint_secret
    data = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload=data, sig_header=stripe_signature, secret=webhook_secret
        )
        event_data = event["data"]
    except Exception as e:
        return {"error": str(e)}

    event_type = event["type"]
    if event_type == "checkout.session.completed":
        print("checkout session completed")
        redis_client = get_redis_client()
        email = event_data["object"]["customer_details"]["email"]

        email = email[: email.index("@")].lower() + email[email.index("@") :]
        print("email", email)
        redis_client.lpush("check_out_completed", email)
    elif event_type == "invoice.paid":
        print("invoice paid")
    elif event_type == "invoice.payment_failed":
        print("invoice payment failed")
    else:
        print(f"unhandled event: {event_type}")

   
    return JSONResponse(content={"success": True})


uvicorn.run(app, host="0.0.0.0", port=8000)
