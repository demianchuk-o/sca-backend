import httpx

class CatBreedServiceError(Exception):
    """Custom exception for cat breed service errors."""
    pass

_breed_cache: set[str] | None = None

async def get_valid_cat_breeds() -> set[str]:
    """
    Fetches and caches valid cat breeds from TheCatAPI.
    """
    global _breed_cache
    if _breed_cache is not None:
        return _breed_cache

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.thecatapi.com/v1/breeds")
            response.raise_for_status()
            breeds_data = response.json()
            _breed_cache = {breed["name"].lower() for breed in breeds_data if "name" in breed}
            return _breed_cache
        except httpx.HTTPStatusError as e:
            raise CatBreedServiceError(f"API returned an error: {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise CatBreedServiceError(f"Request to the cat breeds API failed: {e}") from e