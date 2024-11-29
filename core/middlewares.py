from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse


class CheckSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define paths to exclude
        exempt_paths = [
            reverse("soundscape:login"),
            reverse("soundscape:signup"),
            reverse("soundscape:logout"),
            reverse("soundscape:homepage"),
            reverse("soundscape:validate_session"),
            "/static/",
            "/media/",
            "/ws/",
        ]

        # Allow paths that start with any exempt path (e.g., static/media)
        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Return JSON response for AJAX/JSON requests
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "error": "Unauthenticated",
                        "redirect": reverse("soundscape:login"),
                    },
                    status=401,
                )
            # Redirect non-AJAX requests to login
            return redirect(reverse("soundscape:login"))

        # Continue processing for authenticated users
        return self.get_response(request)
