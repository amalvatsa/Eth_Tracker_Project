import threading
from django.http import HttpResponse
from .utils import track_deposits 

def home(request):
    return HttpResponse("Welcome to the Ethereum Deposit Tracker!")

def run_tracker(request):
    try:
        thread = threading.Thread(target=track_deposits)
        thread.daemon = True  # Daemonize the thread so it exits when the main program does
        thread.start()
        return HttpResponse("Ethereum Deposit Tracker is running in the background.")
    except Exception as e:
        return HttpResponse(f"Error occurred while running the tracker: {e}", status=500)