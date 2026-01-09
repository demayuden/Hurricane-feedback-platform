def strip_metadata(request):
    return {
        "category": request.category,
        "message": request.message,
        "urgency": request.urgency
    }
