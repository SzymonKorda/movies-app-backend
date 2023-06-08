from typing import List, Union, Mapping, Any

from django.db.models import QuerySet
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpRequest
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound, ErrorDetail
from rest_framework.parsers import JSONParser
from rest_framework.utils.serializer_helpers import ReturnDict

from movies.models.actor import Actor
from movies.models.movie import Movie
from movies.payload.actor_update_request import ActorUpdateRequest
from movies.payload.tmdb_actor_response import TmdbActorResponse
from movies.serializers.actor_serializer import FullActorSerializer, SimpleActorSerializer
from movies.serializers.movie_serializer import SimpleMovieSerializer
from movies.services.tmdb_service import TmdbService


class ActorService:
    def __init__(self) -> None:
        self.tmdb_service = TmdbService()
        super().__init__()

    def get_actor(self, actor_id: int) -> ReturnDict:
        actor: Actor = self.find_actor(actor_id)
        return FullActorSerializer(actor).data

    def get_all_actors(self) -> ReturnDict:
        actors: QuerySet[Actor] = Actor.objects.all()
        actor_serializer: SimpleActorSerializer = SimpleActorSerializer(
            actors, many=True
        )
        return actor_serializer.data

    def create_actor(self, request: HttpRequest) -> ReturnDict:
        actor_id: int = JSONParser().parse(request)["actor_id"]
        actor_details: TmdbActorResponse = self.tmdb_service.fetch_actor(actor_id)
        actor: Actor = Actor.from_response(actor_details)
        actor_serializer: FullActorSerializer = FullActorSerializer(
            data=model_to_dict(actor)
        )
        actor_serializer.is_valid(raise_exception=True)
        actor_serializer.save()
        return actor_serializer.data

    def update_actor(self, actor_id: int, request: HttpRequest) -> ReturnDict:
        actor: Actor = self.find_actor(actor_id)
        actor_data: Mapping[str, ActorUpdateRequest] = JSONParser().parse(request)
        actor_serializer: FullActorSerializer = FullActorSerializer(
            actor, data=actor_data, partial=True
        )
        actor_serializer.is_valid(raise_exception=True)
        actor_serializer.save()
        return actor_serializer.data

    def delete_actor(self, actor_id: int) -> None:
        actor: Actor = self.find_actor(actor_id)
        actor.delete()

    def get_movies_from_actor(self, actor_id: int) -> ReturnDict:
        # TODO: error "Actor" has no attribute "movie_set" [attr-defined] -> Dynamically created property
        actor: Any = self.find_actor(actor_id)
        return SimpleMovieSerializer(actor.movie_set.all(), many=True).data

    def add_movie_to_actor(self, actor_id: int, movie_id: int) -> None:
        try:
            movie: Movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            raise NotFound(
                detail={"detail": f"Movie with id {movie_id} does not exist"}
            )
        actor: Any = self.find_actor(actor_id)
        actor.movie_set.add(movie)

    def find_actor(self, actor_id: int) -> Actor:
        try:
            actor: Actor = Actor.objects.get(pk=actor_id)
        except Actor.DoesNotExist:
            raise NotFound(
                detail={"detail": f"Actor with id {actor_id} does not exist"}
            )
        return actor

    def get_or_create_actors(self, cast_members: List[int]) -> List[Actor]:
        actor_ids: List[int] = cast_members[:5]
        movie_actors: List[Actor] = []
        for actor_id in actor_ids:
            try:
                actor_details: TmdbActorResponse = self.tmdb_service.fetch_actor(
                    actor_id
                )
            except NotFound:
                continue
            actor: Actor = Actor.from_response(actor_details)
            actor_serializer: FullActorSerializer = FullActorSerializer(
                data=model_to_dict(actor)
            )
            try:
                actor_serializer.is_valid(raise_exception=True)
            except ValidationError as ex:
                non_field_errors_key: Union[ErrorDetail, None] = (
                    ex.args[0]["non_field_errors"][0]
                    if "non_field_errors" in ex.args[0]
                    else None
                )
                if non_field_errors_key and non_field_errors_key.code == "unique":
                    existing_actor: Actor = Actor.objects.get(
                        name=actor_details.name, date_of_birth=actor_details.birthday
                    )
                    movie_actors.append(existing_actor)
                    continue
                else:
                    continue
            actor = actor_serializer.save()
            movie_actors.append(actor)

        return movie_actors

    def find_movie_actors(self, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse(
                {"message": "Movie does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        actor_serializer = SimpleActorSerializer(movie.actors.all(), many=True)
        return JsonResponse(
            {"actors": actor_serializer.data}, status=status.HTTP_200_OK
        )

    def serialize_to_simple_actors(self, movie: Movie) -> ReturnDict:
        return SimpleActorSerializer(movie.actors.all(), many=True).data
