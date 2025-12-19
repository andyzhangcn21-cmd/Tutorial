import asyncio

# Define an event handler function to handle timer events
async def handle_timer_event():
    print("Timer event triggered!")
    # Simulate some processing logic
    await asyncio.sleep(1)
    print("Timer event handled.")

# Define an event handler function to handle user input events
async def handle_user_input_event(user_input):
    print(f"User input event triggered with input: {user_input}")
    # Simulate some processing logic
    await asyncio.sleep(1)
    print("User input event handled.")

# Simulate an event loop
async def event_loop():
    # Create an event queue
    event_queue = asyncio.Queue()

    # Simulate event triggering
    async def trigger_events():
        await asyncio.sleep(2)  # Wait for 2 seconds before triggering the timer event
        await event_queue.put(("timer", None))  # Put the timer event into the queue

        await asyncio.sleep(1)  # Wait for another 1 second before triggering the user input event
        await event_queue.put(("user_input", "Hello, world!"))  # Put the user input event into the queue

    # Start the event trigger
    asyncio.create_task(trigger_events())

    # Process events in the event queue
    while True:
        event_type, event_data = await event_queue.get()
        if event_type == "timer":
            await handle_timer_event()
        elif event_type == "user_input":
            await handle_user_input_event(event_data)
        event_queue.task_done()

# Run the event loop
asyncio.run(event_loop())
