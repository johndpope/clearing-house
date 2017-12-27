from flask import Blueprint

from views.event import (EditEventView, EventsByTagView, EventsView, EventView,
                         NewEventView)
from views.outcome import EditOutcomeView
from views.tag import DeleteTagView, EditTagView, NewTagView, TagsView

api_v1 = Blueprint('api_v1', __name__)


def configure_routes(app):
    api_v1.add_url_rule(
        '/event/',
        view_func=EventsView.as_view('events'),
        methods=['GET']
    )
    api_v1.add_url_rule(
        '/event/',
        view_func=NewEventView.as_view('new_event'),
        methods=['POST']
    )
    api_v1.add_url_rule(
        '/event/<int:event_id>/',
        view_func=EventView.as_view('event'),
        methods=['GET']
    )
    api_v1.add_url_rule(
        '/event/<int:event_id>/',
        view_func=EditEventView.as_view('edit_event'),
        methods=['POST']
    )
    api_v1.add_url_rule(
        '/tag/<string:tag_name>/',
        view_func=EventsByTagView.as_view('events_by_tag'),
        methods=['GET']
    )
    api_v1.add_url_rule(
        '/tag/<string:tag_name>/',
        view_func=EditTagView.as_view('edit_tag'),
        methods=['POST']
    )
    api_v1.add_url_rule(
        '/tag/<string:tag_name>/',
        view_func=DeleteTagView.as_view('delete_tag'),
        methods=['DELETE']
    )
    api_v1.add_url_rule(
        '/tag/',
        view_func=NewTagView.as_view('new_tag'),
        methods=['POST']
    )
    api_v1.add_url_rule(
        '/tag/',
        view_func=TagsView.as_view('tags'),
        methods=['GET']
    )
    api_v1.add_url_rule(
        '/outcome/<int:outcome_id>/',
        view_func=EditOutcomeView.as_view('edit_outcome_view'),
        methods=['POST']
    )
    app.register_blueprint(api_v1, url_prefix="/api/v1")
